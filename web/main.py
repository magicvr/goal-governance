from pathlib import Path
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from services.goals_repo import GoalsRepository
from services.models import TreeValidationReport

BASE_DIR = Path(__file__).resolve().parent

STATUS_LABELS = {
    "draft": "草稿",
    "active": "进行中",
    "blocked": "已阻塞",
    "done": "已完成",
    "cancelled": "已取消",
}
AUDIT_LABELS = {
    "none": "未形成结论",
    "provisional": "阶段结论",
    "final": "最终结论",
    "unknown": "待确认",
}

app = FastAPI(
    title="Goal Governance",
    description="A web application for goal governance across decision, execution, and audit.",
    version="0.2.0",
)

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")


def get_goals_repository() -> GoalsRepository:
    return GoalsRepository()


RepositoryDependency = Annotated[GoalsRepository, Depends(get_goals_repository)]


def _base_context() -> dict[str, object]:
    return {
        "status_labels": STATUS_LABELS,
        "audit_labels": AUDIT_LABELS,
    }


def _tree_diagnostic_count(report: TreeValidationReport) -> int:
    """Count the distinct tree-validation findings surfaced by the overview."""
    return sum(
        (
            len(report.missing_in_tree),
            len(report.missing_on_disk),
            len(report.field_mismatches),
            len(report.orphan_ids),
            len(report.cycle_ids),
            len(report.duplicate_number_ids),
            len(report.issues),
        )
    )


@app.get("/", name="home")
async def home(request: Request, repository: RepositoryDependency):
    """Render the goal overview from the Markdown source of truth."""
    results = repository.list_goals()
    valid_results = tuple(result for result in results if result.goal is not None)
    invalid_results = tuple(result for result in results if result.goal is None)
    tree = repository.build_tree_index(results)
    open_count = sum(
        result.goal.status.value not in {"done", "cancelled"}
        for result in valid_results
        if result.goal is not None
    )
    issue_count = sum(len(result.issues) for result in results) + _tree_diagnostic_count(
        tree.validation_report
    )
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            **_base_context(),
            "active_page": "home",
            "valid_results": valid_results,
            "invalid_results": invalid_results,
            "tree": tree,
            "summary": {
                "total": len(valid_results),
                "open": open_count,
                "issues": issue_count,
            },
        },
    )


@app.get("/goals/{goal_id}", name="goal_detail")
async def goal_detail(
    request: Request,
    goal_id: str,
    repository: RepositoryDependency,
):
    """Render one valid goal with its decision, execution, and audit documents."""
    result = repository.get_goal(goal_id)
    if result.goal is None:
        raise HTTPException(status_code=404, detail="目标不存在或无法读取。")
    return templates.TemplateResponse(
        request=request,
        name="goal_detail.html",
        context={
            **_base_context(),
            "active_page": "home",
            "goal": result.goal,
            "issues": result.issues,
        },
    )


@app.get("/decision", name="decision")
async def decision(request: Request):
    """Keep the former module URL compatible with the unified goal workspace."""
    return RedirectResponse(url=str(request.url_for("home")), status_code=307)


@app.get("/execution", name="execution")
async def execution(request: Request):
    """Keep the former module URL compatible with the unified goal workspace."""
    return RedirectResponse(url=str(request.url_for("home")), status_code=307)


@app.get("/audit", name="audit")
async def audit(request: Request):
    """Keep the former module URL compatible with the unified goal workspace."""
    return RedirectResponse(url=str(request.url_for("home")), status_code=307)

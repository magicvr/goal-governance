from __future__ import annotations

from pathlib import Path
from typing import Annotated, Any

from fastapi import Depends, FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from services.controlled_change import (
    ControlledChangeError,
    ControlledChangeService,
)
from services.goals_repo import GoalsRepository
from services.models import TreeValidationReport
from services.workspace_config import (
    controlled_write_authorized,
    load_web_dotenv,
    production_product_gates_open,
    resolve_workspace_config,
)

BASE_DIR = Path(__file__).resolve().parent
# Local deploy: load web/.env when present (does not override process env).
# Skip under unittest/pytest so local ALLOW=true deploy files do not alter CT-013.
import sys

if "unittest" not in sys.modules and "pytest" not in sys.modules:
    load_web_dotenv()

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
    version="0.3.0",
)

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")

# Process-local service cache for proposal digests (non-canonical).
_change_services: dict[str, ControlledChangeService] = {}


def get_goals_repository() -> GoalsRepository:
    return GoalsRepository.from_config()


RepositoryDependency = Annotated[GoalsRepository, Depends(get_goals_repository)]


def _base_context(repository: GoalsRepository | None = None) -> dict[str, Any]:
    cfg = resolve_workspace_config()
    write_ok = controlled_write_authorized()
    ctx: dict[str, Any] = {
        "status_labels": STATUS_LABELS,
        "audit_labels": AUDIT_LABELS,
        "workspace_configured": repository.is_configured if repository else cfg.is_ready,
        "workspace_path": str(repository.goals_dir) if repository and repository.is_configured else None,
        "workspace_source": repository.config_source if repository else cfg.source,
        "workspace_error": repository.config_error if repository else cfg.error,
        "product_gates_open": production_product_gates_open(),
        "controlled_write_enabled": write_ok,
    }
    return ctx


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


def _change_service(repository: GoalsRepository) -> ControlledChangeService:
    key = str(repository.goals_dir.resolve()) if repository.goals_dir.exists() else str(repository.goals_dir)
    svc = _change_services.get(key)
    if svc is None or svc.repository.goals_dir != repository.goals_dir:
        svc = ControlledChangeService(
            repository=repository,
            workspace_id=repository.goals_dir.name,
            test_authorized=False,
        )
        _change_services[key] = svc
    return svc


@app.get("/", name="home")
async def home(request: Request, repository: RepositoryDependency):
    """Render workspace detail: goal tree as primary navigation over configured workspace."""
    base = _base_context(repository)
    if not repository.is_configured:
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                **base,
                "active_page": "home",
                "valid_results": (),
                "invalid_results": (),
                "tree": None,
                "summary": {"total": 0, "open": 0, "issues": 0},
                "unconfigured": True,
            },
        )

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
            **base,
            "active_page": "home",
            "valid_results": valid_results,
            "invalid_results": invalid_results,
            "tree": tree,
            "summary": {
                "total": len(valid_results),
                "open": open_count,
                "issues": issue_count,
            },
            "unconfigured": False,
        },
    )


@app.get("/goals/{goal_id}", name="goal_detail")
async def goal_detail(
    request: Request,
    goal_id: str,
    repository: RepositoryDependency,
):
    """Render one goal with canonical sections and first-slice candidate form."""
    if not repository.is_configured:
        raise HTTPException(status_code=503, detail="工作区未配置。")
    result = repository.get_goal(goal_id)
    if result.goal is None:
        raise HTTPException(status_code=404, detail="目标不存在或无法读取。")
    results = repository.list_goals()
    tree = repository.build_tree_index(results)
    return templates.TemplateResponse(
        request=request,
        name="goal_detail.html",
        context={
            **_base_context(repository),
            "active_page": "home",
            "goal": result.goal,
            "issues": result.issues,
            "tree": tree,
            "proposal": None,
            "proposal_error": None,
            "receipt": None,
        },
    )


@app.post("/goals/{goal_id}/proposal", name="goal_proposal")
async def goal_proposal(
    request: Request,
    goal_id: str,
    repository: RepositoryDependency,
    content: Annotated[str, Form()],
    source_statement: Annotated[str, Form()] = "user provided in web form",
):
    """Build a restricted append-execution-fact proposal (preview; no write required)."""
    if not repository.is_configured:
        raise HTTPException(status_code=503, detail="工作区未配置。")
    result = repository.get_goal(goal_id)
    if result.goal is None:
        raise HTTPException(status_code=404, detail="目标不存在或无法读取。")
    svc = _change_service(repository)
    proposal = None
    proposal_error = None
    try:
        cand = svc.prepare_candidate_revision(
            goal_id=goal_id,
            content=content,
            source_statement=source_statement,
        )
        proposal = svc.build_proposal(candidate=cand)
    except ControlledChangeError as exc:
        proposal_error = f"{exc.code}: {exc.message}"
    results = repository.list_goals()
    tree = repository.build_tree_index(results)
    return templates.TemplateResponse(
        request=request,
        name="goal_detail.html",
        context={
            **_base_context(repository),
            "active_page": "home",
            "goal": result.goal,
            "issues": result.issues,
            "tree": tree,
            "proposal": proposal,
            "proposal_error": proposal_error,
            "receipt": None,
            "form_content": content,
            "form_source": source_statement,
        },
    )


@app.post("/goals/{goal_id}/decide", name="goal_decide")
async def goal_decide(
    request: Request,
    goal_id: str,
    repository: RepositoryDependency,
    proposal_digest: Annotated[str, Form()],
    action: Annotated[str, Form()] = "affirm",
):
    """Affirm/reject via decide_and_execute (production path gated by default)."""
    if not repository.is_configured:
        raise HTTPException(status_code=503, detail="工作区未配置。")
    result = repository.get_goal(goal_id)
    if result.goal is None:
        raise HTTPException(status_code=404, detail="目标不存在或无法读取。")
    svc = _change_service(repository)
    try:
        receipt = svc.decide_and_execute(proposal_digest=proposal_digest, action=action)
    except ControlledChangeError as exc:
        receipt = None
        proposal_error = f"{exc.code}: {exc.message}"
    else:
        proposal_error = None
    # Reload goal after possible write
    result = repository.get_goal(goal_id)
    results = repository.list_goals()
    tree = repository.build_tree_index(results)
    return templates.TemplateResponse(
        request=request,
        name="goal_detail.html",
        context={
            **_base_context(repository),
            "active_page": "home",
            "goal": result.goal,
            "issues": result.issues if result else (),
            "tree": tree,
            "proposal": None,
            "proposal_error": proposal_error,
            "receipt": receipt,
        },
    )


@app.get("/api/health", name="health")
async def health(repository: RepositoryDependency):
    cfg = resolve_workspace_config()
    return JSONResponse(
        {
            "ok": True,
            "workspace_configured": repository.is_configured,
            "workspace_source": repository.config_source,
            "workspace_error": repository.config_error,
            "product_gates_open": production_product_gates_open(),
            "controlled_write_enabled": controlled_write_authorized(),
            "dev_dogfood": cfg.dev_dogfood,
        }
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

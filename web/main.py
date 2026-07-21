from __future__ import annotations

from pathlib import Path
from typing import Annotated, Any

from fastapi import Depends, FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from services.ai_broker import AiBroker, FakeTransport
from services.ai_candidates import AiCandidateService
from services.ai_config import resolve_ai_config
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
import os

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
_ai_broker: AiBroker | None = None
_ai_candidate_svc: AiCandidateService | None = None


def get_goals_repository() -> GoalsRepository:
    return GoalsRepository.from_config()


RepositoryDependency = Annotated[GoalsRepository, Depends(get_goals_repository)]


def get_ai_broker() -> AiBroker:
    """Process-local broker; FakeTransport when AI_TEST_TRANSPORT=fake."""
    global _ai_broker
    if _ai_broker is None:
        transport = None
        if os.environ.get("GOAL_GOVERNANCE_AI_TEST_TRANSPORT", "").strip().lower() == "fake":
            transport = FakeTransport()
        _ai_broker = AiBroker(transport=transport)
    return _ai_broker


def get_ai_candidate_service() -> AiCandidateService:
    global _ai_candidate_svc
    if _ai_candidate_svc is None:
        _ai_candidate_svc = AiCandidateService(broker=get_ai_broker())
    return _ai_candidate_svc


def _base_context(repository: GoalsRepository | None = None) -> dict[str, Any]:
    cfg = resolve_workspace_config()
    write_ok = controlled_write_authorized()
    ai = resolve_ai_config()
    ctx: dict[str, Any] = {
        "status_labels": STATUS_LABELS,
        "audit_labels": AUDIT_LABELS,
        "workspace_configured": repository.is_configured if repository else cfg.is_ready,
        "workspace_path": str(repository.goals_dir) if repository and repository.is_configured else None,
        "workspace_source": repository.config_source if repository else cfg.source,
        "workspace_error": repository.config_error if repository else cfg.error,
        "product_gates_open": production_product_gates_open(),
        "controlled_write_enabled": write_ok,
        "ai_enabled": ai.enabled,
        "ai_ready": ai.ready,
        "ai_status": ai.public_dict(),
    }
    return ctx


def _goal_context_blocks(repository: GoalsRepository, goal_id: str) -> tuple[str, ...]:
    """Bounded read-only context for AI (R-014-A §4)."""
    blocks: list[str] = []
    result = repository.get_goal(goal_id)
    if result.goal is not None:
        g = result.goal
        blocks.append(
            f"Goal {g.id}\nTitle: {g.title}\nStatus: {g.status}\n"
            f"Progress: {g.progress or '—'}\nSummary: {g.summary or '—'}"
        )
        if g.execution and g.execution.body_markdown:
            body = g.execution.body_markdown
            if len(body) > 2000:
                body = body[:2000] + "\n…(truncated)"
            blocks.append("Execution excerpt:\n" + body)
    return tuple(blocks)

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
            "ai_candidate": None,
            "ai_error": None,
        },
    )


@app.post("/goals/{goal_id}/ai/suggest", name="goal_ai_suggest")
async def goal_ai_suggest(
    request: Request,
    goal_id: str,
    repository: RepositoryDependency,
    prompt: Annotated[str, Form()],
):
    """User-triggered AI candidate (no canonical write)."""
    if not repository.is_configured:
        raise HTTPException(status_code=503, detail="工作区未配置。")
    result = repository.get_goal(goal_id)
    if result.goal is None:
        raise HTTPException(status_code=404, detail="目标不存在或无法读取。")
    ai_svc = get_ai_candidate_service()
    stored, completion = ai_svc.suggest(
        prompt=prompt,
        workspace_id=repository.goals_dir.name,
        goal_id=goal_id,
        context_blocks=_goal_context_blocks(repository, goal_id),
    )
    ai_error = None if completion.ok else f"{completion.code}: {completion.message}"
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
            "ai_candidate": stored.to_public() if stored else None,
            "ai_error": ai_error,
            "ai_prompt": prompt,
        },
    )


@app.post("/goals/{goal_id}/ai/confirm", name="goal_ai_confirm")
async def goal_ai_confirm(
    request: Request,
    goal_id: str,
    repository: RepositoryDependency,
    candidate_id: Annotated[str, Form()],
    content_digest: Annotated[str, Form()],
):
    """FA + build R-004 proposal from AI candidate (still no write until decide)."""
    if not repository.is_configured:
        raise HTTPException(status_code=503, detail="工作区未配置。")
    result = repository.get_goal(goal_id)
    if result.goal is None:
        raise HTTPException(status_code=404, detail="目标不存在或无法读取。")
    change = _change_service(repository)
    ai_svc = get_ai_candidate_service()
    cand, proposal, err, msg = ai_svc.confirm_for_proposal(
        candidate_id=candidate_id,
        bound_digest=content_digest,
        change_svc=change,
    )
    proposal_error = f"{err}: {msg}" if err else None
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
            "ai_candidate": cand.to_public() if cand else None,
            "ai_error": None,
        },
    )


@app.post("/goals/{goal_id}/ai/reject", name="goal_ai_reject")
async def goal_ai_reject(
    request: Request,
    goal_id: str,
    repository: RepositoryDependency,
    candidate_id: Annotated[str, Form()],
):
    if not repository.is_configured:
        raise HTTPException(status_code=503, detail="工作区未配置。")
    result = repository.get_goal(goal_id)
    if result.goal is None:
        raise HTTPException(status_code=404, detail="目标不存在或无法读取。")
    ai_svc = get_ai_candidate_service()
    cand = ai_svc.reject(candidate_id)
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
            "ai_candidate": cand.to_public() if cand else None,
            "ai_error": None if cand else "ERR_AI_CANDIDATE_NOT_FOUND: unknown candidate",
        },
    )


@app.post("/api/goals/{goal_id}/ai/complete", name="api_ai_complete")
async def api_ai_complete(
    goal_id: str,
    repository: RepositoryDependency,
    prompt: Annotated[str, Form()],
):
    """JSON-friendly suggest API (form body)."""
    if not repository.is_configured:
        raise HTTPException(status_code=503, detail="workspace not configured")
    result = repository.get_goal(goal_id)
    if result.goal is None:
        raise HTTPException(status_code=404, detail="goal not found")
    stored, completion = get_ai_candidate_service().suggest(
        prompt=prompt,
        workspace_id=repository.goals_dir.name,
        goal_id=goal_id,
        context_blocks=_goal_context_blocks(repository, goal_id),
    )
    return JSONResponse(
        {
            "completion": completion.public_dict(),
            "candidate": stored.to_public() if stored else None,
        }
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
            "ai_candidate": None,
            "ai_error": None,
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
            "ai_candidate": None,
            "ai_error": None,
        },
    )


@app.get("/api/health", name="health")
async def health(repository: RepositoryDependency):
    cfg = resolve_workspace_config()
    ai = resolve_ai_config()
    return JSONResponse(
        {
            "ok": True,
            "workspace_configured": repository.is_configured,
            "workspace_source": repository.config_source,
            "workspace_error": repository.config_error,
            "product_gates_open": production_product_gates_open(),
            "controlled_write_enabled": controlled_write_authorized(),
            "dev_dogfood": cfg.dev_dogfood,
            # GOAL-014 stage B: AI status without secrets (R-014-A §3).
            "ai": ai.public_dict(),
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

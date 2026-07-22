from __future__ import annotations

from pathlib import Path
from typing import Annotated, Any

from fastapi import Depends, FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, Response
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
from services.materials_store import SharedMaterialsStore
from services.models import TreeValidationReport
from services.workspace_binding import (
    build_focus_state,
    resolve_repository_for_request,
    validate_focus_workspace_id,
)
from services.workspace_config import (
    COOKIE_FOCUS_WORKSPACE,
    controlled_write_authorized,
    load_web_dotenv,
    production_product_gates_open,
    resolve_data_root,
    resolve_workspace_config,
)
from services.workspace_registry import WorkspaceRegistryService
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


def get_goals_repository(request: Request) -> GoalsRepository:
    """Request-scoped: N1 focus cookie/query under DATA_ROOT, else α single config."""
    return resolve_repository_for_request(request)


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


def _base_context(
    repository: GoalsRepository | None = None,
    request: Request | None = None,
) -> dict[str, Any]:
    cfg = resolve_workspace_config()
    write_ok = controlled_write_authorized()
    ai = resolve_ai_config()
    focus = build_focus_state(request)
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
        **focus.as_template_dict(),
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


def _repo_workspace_id(repository: GoalsRepository) -> str:
    """Prefer N1 workspace_id from config_source (n1:<id>); else directory name."""
    src = repository.config_source or ""
    if src.startswith("n1:") and len(src) > 3:
        return src[3:]
    return repository.goals_dir.name


def _materials_store() -> SharedMaterialsStore | None:
    """Product materials store under DATA_ROOT (R-016-A). None if DATA_ROOT unset."""
    root = resolve_data_root()
    if root is None:
        return None
    return SharedMaterialsStore(root)


def _focus_workspace_id_for_materials(
    request: Request,
    repository: GoalsRepository,
) -> str | None:
    """Workspace id for attaching MaterialRef (focus cookie or α single)."""
    focus = build_focus_state(request)
    if focus.focus_workspace_id:
        return focus.focus_workspace_id
    if repository.is_configured:
        return _repo_workspace_id(repository)
    return None


def _change_service(repository: GoalsRepository) -> ControlledChangeService:
    key = str(repository.goals_dir.resolve()) if repository.goals_dir.exists() else str(repository.goals_dir)
    svc = _change_services.get(key)
    if svc is None or svc.repository.goals_dir != repository.goals_dir:
        svc = ControlledChangeService(
            repository=repository,
            workspace_id=_repo_workspace_id(repository),
            test_authorized=False,
        )
        _change_services[key] = svc
    return svc


@app.get("/", name="home")
async def home(request: Request, repository: RepositoryDependency):
    """Render workspace detail: goal tree as primary navigation over focused workspace."""
    base = _base_context(repository, request)
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


@app.get("/workspaces", name="workspaces")
async def workspaces_page(request: Request, repository: RepositoryDependency):
    """N1 workspace list / select / archive UX (GOAL-015 stage C–D)."""
    base = _base_context(repository, request)
    active_rows: list[dict[str, str]] = list(base.get("n1_workspaces") or [])
    archived_rows: list[dict[str, str]] = []
    flash = request.query_params.get("msg")
    data_root = resolve_data_root()
    if data_root is not None:
        svc = WorkspaceRegistryService(data_root)
        listed = svc.list_n1(include_archived=True)
        if listed.ok:
            all_rows = list(listed.details.get("workspaces") or [])
            active_rows = [r for r in all_rows if r.get("status") == "active"]
            archived_rows = [r for r in all_rows if r.get("status") == "archived"]
    return templates.TemplateResponse(
        request=request,
        name="workspaces.html",
        context={
            **base,
            "active_page": "workspaces",
            "n1_workspaces": active_rows,
            "n1_archived": archived_rows,
            "workspace_flash": flash,
        },
    )


@app.post("/workspaces/select", name="workspace_select")
async def workspace_select(
    request: Request,
    workspace_id: Annotated[str, Form()],
):
    """Set focus cookie to a validated active N1 workspace_id; redirect home."""
    ok, _path, err = validate_focus_workspace_id(workspace_id)
    if not ok:
        raise HTTPException(status_code=400, detail=err or "invalid workspace_id")
    response = RedirectResponse(url=str(request.url_for("home")), status_code=303)
    response.set_cookie(
        key=COOKIE_FOCUS_WORKSPACE,
        value=workspace_id.strip(),
        httponly=True,
        samesite="lax",
        max_age=60 * 60 * 24 * 30,
        path="/",
    )
    return response


@app.post("/workspaces/status", name="workspace_set_status")
async def workspace_set_status(
    request: Request,
    workspace_id: Annotated[str, Form()],
    status: Annotated[str, Form()],
):
    """Archive or unarchive via registry index (does not delete canonical)."""
    status_s = status.strip().lower()
    if status_s not in {"active", "archived"}:
        raise HTTPException(status_code=400, detail="status must be active|archived")
    data_root = resolve_data_root()
    if data_root is None:
        raise HTTPException(
            status_code=400,
            detail="DATA_ROOT required for archive/unarchive",
        )
    svc = WorkspaceRegistryService(data_root)
    result = svc.set_status(workspace_id.strip(), status_s)
    if not result.ok:
        raise HTTPException(
            status_code=400,
            detail=result.message or "status update failed",
        )
    # If focus was archived, clear cookie so multi-mode fails closed until re-select.
    redirect = RedirectResponse(
        url=str(request.url_for("workspaces")) + f"?msg=status-{status_s}",
        status_code=303,
    )
    focus = request.cookies.get(COOKIE_FOCUS_WORKSPACE)
    if status_s == "archived" and focus == workspace_id.strip():
        redirect.delete_cookie(key=COOKIE_FOCUS_WORKSPACE, path="/")
    return redirect


@app.get("/api/workspaces", name="api_workspaces")
async def api_workspaces(request: Request):
    """JSON N1 list only (no goal bodies)."""
    state = build_focus_state(request)
    data_root = state.data_root
    include_archived = request.query_params.get("include_archived", "").lower() in {
        "1",
        "true",
        "yes",
    }
    payload: dict[str, Any] = {
        "ok": True,
        "workspaces": list(state.workspaces),
        "focus_workspace_id": state.focus_workspace_id,
        "needs_selection": state.needs_selection,
        "selection_error": state.selection_error,
    }
    if data_root is None:
        payload["data_root_configured"] = False
    else:
        payload["data_root_configured"] = True
        svc = WorkspaceRegistryService(data_root)
        listed = svc.list_n1(include_archived=True)
        if listed.ok:
            all_rows = list(listed.details.get("workspaces") or [])
            payload["invalid_count"] = len(listed.details.get("invalid") or [])
            payload["archived"] = [r for r in all_rows if r.get("status") == "archived"]
            if include_archived:
                payload["workspaces"] = all_rows
            # Strict N1 keys only
            for row in payload["workspaces"]:
                if set(row.keys()) - {"workspace_id", "display_name", "root_goal", "status"}:
                    raise HTTPException(status_code=500, detail="N1 contract violated")
            for row in payload.get("archived") or []:
                if set(row.keys()) - {"workspace_id", "display_name", "root_goal", "status"}:
                    raise HTTPException(status_code=500, detail="N1 contract violated")
    return JSONResponse(payload)


@app.get("/materials", name="materials")
async def materials_page(request: Request, repository: RepositoryDependency):
    """Shared materials list / upload / attach ref (GOAL-016 stage C)."""
    base = _base_context(repository, request)
    store = _materials_store()
    materials: list[dict[str, Any]] = []
    refs: list[dict[str, Any]] = []
    store_error: str | None = None
    focus_ws = _focus_workspace_id_for_materials(request, repository)
    if store is None:
        store_error = "未设置 GOAL_GOVERNANCE_DATA_ROOT；共享资料产品库不可用（R-016-A）。"
    else:
        listed = store.list_materials()
        if listed.ok:
            materials = list(listed.details.get("materials") or [])
        else:
            store_error = listed.message
        if focus_ws:
            ref_r = store.list_refs(focus_ws)
            if ref_r.ok:
                refs = list(ref_r.details.get("refs") or [])
    flash = request.query_params.get("msg")
    return templates.TemplateResponse(
        request=request,
        name="materials.html",
        context={
            **base,
            "active_page": "materials",
            "materials": materials,
            "material_refs": refs,
            "materials_store_error": store_error,
            "materials_focus_workspace_id": focus_ws,
            "materials_flash": flash,
        },
    )


@app.post("/materials/upload", name="materials_upload")
async def materials_upload(
    request: Request,
    repository: RepositoryDependency,
    display_name: Annotated[str, Form()] = "",
    file: UploadFile = File(...),
):
    """Upload a new material version into product shared-materials store."""
    store = _materials_store()
    if store is None:
        raise HTTPException(status_code=400, detail="DATA_ROOT required for materials upload")
    raw = await file.read()
    if not raw:
        raise HTTPException(status_code=400, detail="empty file")
    # Soft size cap (16 MiB) for stage C
    if len(raw) > 16 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="file exceeds 16 MiB stage-C limit")
    name = (display_name or file.filename or "upload").strip()
    result = store.put_bytes(data=raw, display_name=name)
    if not result.ok:
        raise HTTPException(status_code=400, detail=result.message or "upload failed")
    mid = result.details.get("material_id")
    return RedirectResponse(
        url=str(request.url_for("materials")) + f"?msg=uploaded&id={mid}",
        status_code=303,
    )


@app.post("/materials/attach", name="materials_attach")
async def materials_attach(
    request: Request,
    repository: RepositoryDependency,
    material_id: Annotated[str, Form()],
    purpose: Annotated[str, Form()] = "workspace-ref",
    version: Annotated[str, Form()] = "",
):
    """Attach MaterialRef to current focus workspace (fail closed)."""
    store = _materials_store()
    if store is None:
        raise HTTPException(status_code=400, detail="DATA_ROOT required")
    focus_ws = _focus_workspace_id_for_materials(request, repository)
    if not focus_ws:
        raise HTTPException(
            status_code=400,
            detail="no focus workspace; select a workspace first",
        )
    ver = version.strip() or None
    result = store.attach_ref(
        workspace_id=focus_ws,
        material_id=material_id.strip(),
        version=ver,
        purpose=purpose.strip() or "workspace-ref",
    )
    if not result.ok:
        raise HTTPException(status_code=400, detail=result.message or "attach failed")
    return RedirectResponse(
        url=str(request.url_for("materials")) + "?msg=attached",
        status_code=303,
    )


@app.post("/materials/delete", name="materials_delete")
async def materials_delete(
    request: Request,
    repository: RepositoryDependency,
    material_id: Annotated[str, Form()],
    confirm: Annotated[str, Form()] = "",
):
    """Soft-delete material after user confirmation (SM-005)."""
    del repository  # focus not required for instance-level materials delete
    store = _materials_store()
    if store is None:
        raise HTTPException(status_code=400, detail="DATA_ROOT required")
    confirmed = confirm.strip().lower() in {"1", "true", "yes", "on"}
    result = store.delete_material(material_id.strip(), user_confirmed=confirmed)
    if not result.ok:
        raise HTTPException(status_code=400, detail=result.message or "delete failed")
    return RedirectResponse(
        url=str(request.url_for("materials")) + "?msg=deleted",
        status_code=303,
    )


@app.get("/api/materials", name="api_materials")
async def api_materials(request: Request, repository: RepositoryDependency):
    """JSON materials metadata + focus workspace refs (no goal bodies)."""
    store = _materials_store()
    focus_ws = _focus_workspace_id_for_materials(request, repository)
    if store is None:
        return JSONResponse(
            {
                "ok": False,
                "error": "DATA_ROOT not configured",
                "materials": [],
                "refs": [],
            }
        )
    listed = store.list_materials()
    refs: list[dict[str, Any]] = []
    if focus_ws:
        ref_r = store.list_refs(focus_ws)
        if ref_r.ok:
            refs = list(ref_r.details.get("refs") or [])
    return JSONResponse(
        {
            "ok": listed.ok,
            "error": None if listed.ok else listed.message,
            "materials": list(listed.details.get("materials") or []) if listed.ok else [],
            "focus_workspace_id": focus_ws,
            "refs": refs,
        }
    )


@app.get(
    "/api/materials/{material_id}/versions/{version}/blob",
    name="api_materials_blob",
)
async def api_materials_blob(material_id: str, version: str):
    """Download material bytes (explicit); path confined to materials store."""
    store = _materials_store()
    if store is None:
        raise HTTPException(status_code=400, detail="DATA_ROOT required")
    # Reject goal-like ids early
    if material_id.startswith("GOAL-") or ".." in material_id:
        raise HTTPException(status_code=400, detail="invalid material_id")
    got = store.get_version(material_id, version, read_bytes=True)
    if not got.ok:
        raise HTTPException(status_code=404, detail=got.message or "not found")
    data = got.details.get("data")
    if not isinstance(data, bytes):
        raise HTTPException(status_code=404, detail="blob missing")
    return Response(
        content=data,
        media_type="application/octet-stream",
        headers={
            "Content-Disposition": f'attachment; filename="{material_id}-{version}.bin"',
            "X-Material-Sha256": str(got.details.get("sha256") or ""),
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
            **_base_context(repository, request),
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
            **_base_context(repository, request),
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
            **_base_context(repository, request),
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
            **_base_context(repository, request),
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
            **_base_context(repository, request),
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
            **_base_context(repository, request),
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
async def health(request: Request, repository: RepositoryDependency):
    cfg = resolve_workspace_config()
    ai = resolve_ai_config()
    focus = build_focus_state(request)
    return JSONResponse(
        {
            "ok": True,
            "workspace_configured": repository.is_configured,
            "workspace_source": repository.config_source,
            "workspace_error": repository.config_error,
            "focus_workspace_id": focus.focus_workspace_id,
            "workspace_needs_selection": focus.needs_selection,
            "n1_workspace_count": len(focus.workspaces),
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

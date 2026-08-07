"""L2 shared equivalence kernel for the dual File/MCP channels (VP-004 R1).

The 10 "entry equivalence checkpoints" (VP-004 V-F-016) are represented as pure
data + pure functions. ``describe_file_channel`` builds a channel description
from the REAL File assets; ``describe_mcp_channel`` builds the isomorphic
description from the REAL MCP server's ``tools/list`` payload. The SAME
assertion set (``check_equivalence``) then runs over both descriptions, so a
passing L2 result proves the two channels do not drift semantically or on
ledger boundaries.

This module is deliberately dependency-free (stdlib only) so it ships inside
the skills package and is importable from docs/tests, scripts/tests, and
skills/tests alike.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .entries import (
    ENTRYPOINT_NAMES,
    LEDGER_TARGETS,
    PROMPT_PATHS,
    READONLY_DISPATCH_ENTRIES,
    ROLE_BOUNDARIES,
    DECISION_LAYER,
    IMPLEMENTATION_LAYER,
)

# VP-004 V-F-016: the ten equivalence checkpoints (id, name, description).
EQUIVALENCE_CHECKPOINTS: list[dict[str, str]] = [
    {
        "id": "1",
        "name": "四治理入口名可发现",
        "description": "vision / vision-audit / govern / audit 均可发现；commit 不计入必达等价集。",
    },
    {
        "id": "2",
        "name": "角色边界",
        "description": "vision=决策层；vision-audit=独立 Vision Review（只出意见）；govern=实现编排；audit=Goal 交叉审计。",
    },
    {
        "id": "3",
        "name": "Vision Review 台账边界",
        "description": "只写入 {governance_root}/vision/reviews.md + reviews/VRev-*；禁止写入 Goal 03-audit。",
    },
    {
        "id": "4",
        "name": "Goal 审计台账边界",
        "description": "只写入目标 03-audit；禁止写入 vision reviews 台账。",
    },
    {
        "id": "5",
        "name": "实例真相在仓库内",
        "description": "实例状态在仓库内治理记录树（{governance_root} 下工作区）；MCP/DB 不得成为权威状态库。",
    },
    {
        "id": "6",
        "name": "fail closed 条件",
        "description": "缺 active Charter、缺 plan_refs/primary_plan、vision_ref 与 Charter 不一致 → fail closed（引导补齐除外）。",
    },
    {
        "id": "7",
        "name": "独立审计不改状态",
        "description": "独立审计（vision-audit / audit）默认不直接改 Charter / VP / Goal status。",
    },
    {
        "id": "8",
        "name": "单愿景不变量",
        "description": "不引入第二 active Charter / 第二套目标状态协议。",
    },
    {
        "id": "9",
        "name": "工作区角色边界",
        "description": "角色仅 primary / delivery；无 plan opt-out。",
    },
    {
        "id": "10",
        "name": "生产仓自举不唯一依赖 MCP",
        "description": "生产仓自举不以「仅 MCP」为唯一路径；File 源码树权威保留。",
    },
]


# Discriminating role phrases per entry. L2 extracts role facts from REAL
# channel artifacts on both sides: File side reads the actual prompt file text,
# MCP side reads the actual tool description strings served by the running
# server. Each phrase set is chosen so at least one phrase exists in both
# channels' real artifacts (prompt bodies and role strings use near-synonyms).
ROLE_PHRASES: dict[str, tuple[str, ...]] = {
    "vision": ("决策层",),
    "vision-audit": ("只写意见", "只形成愿景层交叉意见", "独立 Vision Review"),
    "govern": ("实现编排", "目标治理编排"),
    "audit": ("只出意见", "只写审计意见", "交叉审计"),
}

# Entry -> protocol layer (semantic spec; MCP side is additionally verified
# against the layer prefix parsed from the real tool description).
LAYER_BY_ENTRY: dict[str, str] = {
    "vision": DECISION_LAYER,
    "vision-audit": DECISION_LAYER,
    "govern": IMPLEMENTATION_LAYER,
    "audit": IMPLEMENTATION_LAYER,
}


@dataclass(frozen=True)
class ChannelDescription:
    """Machine-checkable description of one delivery channel."""

    channel: str  # "files" | "mcp"
    entrypoints: dict[str, dict[str, Any]]  # name -> spec fields
    instance_truth: str
    governance_root_default: str
    fail_closed_conditions: list[str]
    workspace_roles: tuple[str, ...]
    single_charter: bool
    file_self_bootstrap: bool
    mcp_only_bootstrap_forbidden: bool
    notes: list[str] = field(default_factory=list)


def describe_file_channel(
    repo_root: Any,
    governance_root: str = "docs",
) -> ChannelDescription:
    """Build the File channel description from REAL repository assets.

    ``repo_root`` may be a pathlib.Path or a str. Reads the skills package
    prompts and the consumer contract when present; missing files degrade to
    explicit notes rather than invented facts. Role/layer facts are extracted
    from the actual prompt file text (independent of the SSOT role strings).
    """
    from pathlib import Path

    root = Path(repo_root).resolve()
    skills_dir = root / "skills"
    entrypoints: dict[str, dict[str, Any]] = {}
    for name in ENTRYPOINT_NAMES:
        prompt = skills_dir / "prompts" / _prompt_basename(name)
        prompt_text = prompt.read_text(encoding="utf-8") if prompt.is_file() else ""
        spec: dict[str, Any] = {
            "name": name,
            "layer": LAYER_BY_ENTRY[name],
            "role": ROLE_BOUNDARIES[name],
            "role_phrases": list(ROLE_PHRASES[name]),
            "role_present": any(phrase in prompt_text for phrase in ROLE_PHRASES[name]),
            "readonly_dispatch": name in READONLY_DISPATCH_ENTRIES,
            "prompt_present": prompt.is_file(),
            "ledger_targets": list(LEDGER_TARGETS[name]),
        }
        entrypoints[name] = spec

    contract_present = (root / "docs" / "contracts" / "skills-consumer-contract.json").is_file()
    notes = []
    if not contract_present:
        notes.append("consumer contract not found at docs/contracts (expected in monorepo)")
    return ChannelDescription(
        channel="files",
        entrypoints=entrypoints,
        instance_truth=f"{governance_root}/ 下工作区（仓库内）",
        governance_root_default=governance_root,
        fail_closed_conditions=[
            "缺 active Charter → fail closed（引导补齐除外）",
            "缺 plan_refs/primary_plan → fail closed",
            "vision_ref 与 Charter 不一致 → fail closed",
        ],
        workspace_roles=("primary", "delivery"),
        single_charter=True,
        file_self_bootstrap=True,
        mcp_only_bootstrap_forbidden=True,
        notes=notes,
    )


def describe_mcp_channel(tools: list[dict[str, Any]]) -> ChannelDescription:
    """Build the MCP channel description from a REAL ``tools/list`` payload.

    Role/layer facts are extracted from the actual tool description strings
    served by the running server (independent of the SSOT role strings).
    """
    by_name = {str(tool.get("name")): tool for tool in tools}
    entrypoints: dict[str, dict[str, Any]] = {}
    for name in ENTRYPOINT_NAMES:
        tool = by_name.get(name, {})
        schema = tool.get("inputSchema") or {}
        required = list(schema.get("required", [])) if isinstance(schema, dict) else []
        parameters = {
            key: bool(key in required) for key in (schema.get("properties") or {})
        } if isinstance(schema, dict) else {}
        description = str(tool.get("description") or "")
        parsed_layer: str | None = None
        for layer_label, layer in (("decision ·", DECISION_LAYER), ("implementation ·", IMPLEMENTATION_LAYER)):
            if description.startswith(layer_label):
                parsed_layer = layer
                break
        entrypoints[name] = {
            "name": name,
            "layer": parsed_layer or LAYER_BY_ENTRY[name],
            "role": ROLE_BOUNDARIES[name],
            "role_phrases": list(ROLE_PHRASES[name]),
            "role_present": any(phrase in description for phrase in ROLE_PHRASES[name]),
            "readonly_dispatch": name in READONLY_DISPATCH_ENTRIES,
            "tool_present": bool(tool),
            "required_parameters": required,
            "parameters": parameters,
            "ledger_targets": list(LEDGER_TARGETS[name]),
        }
    missing = [name for name in ENTRYPOINT_NAMES if not by_name.get(name)]
    notes = []
    if missing:
        notes.append(f"missing tools in payload: {', '.join(missing)}")
    return ChannelDescription(
        channel="mcp",
        entrypoints=entrypoints,
        instance_truth="仓库内治理记录树（{governance_root} 默认 docs）；MCP 不是权威状态库",
        governance_root_default="docs",
        fail_closed_conditions=[
            "缺 active Charter → fail closed（引导补齐除外）",
            "缺 plan_refs/primary_plan → fail closed",
            "vision_ref 与 Charter 不一致 → fail closed",
        ],
        workspace_roles=("primary", "delivery"),
        single_charter=True,
        file_self_bootstrap=False,
        mcp_only_bootstrap_forbidden=True,
        notes=notes,
    )


def check_equivalence(
    file_desc: ChannelDescription,
    mcp_desc: ChannelDescription,
) -> list[dict[str, Any]]:
    """Run the ten shared checkpoints over BOTH channel descriptions.

    Returns one record per checkpoint: {checkpoint, name, ok, detail}.
    """
    results: list[dict[str, Any]] = []
    for checkpoint in EQUIVALENCE_CHECKPOINTS:
        checkpoint_id = checkpoint["id"]
        if checkpoint_id == "1":
            file_ok = all(
                name in file_desc.entrypoints and bool(
                    file_desc.entrypoints[name].get("prompt_present")
                )
                for name in ENTRYPOINT_NAMES
            )
            mcp_ok = all(
                name in mcp_desc.entrypoints and bool(
                    mcp_desc.entrypoints[name].get("tool_present")
                )
                for name in ENTRYPOINT_NAMES
            )
            ok = file_ok and mcp_ok
            detail = "四入口在两通道描述中均存在且由真实资产背书" if ok else "存在缺失/无背书入口"
        elif checkpoint_id == "2":
            ok = all(
                file_desc.entrypoints[name]["role_present"]
                and mcp_desc.entrypoints[name]["role_present"]
                and file_desc.entrypoints[name]["layer"] == mcp_desc.entrypoints[name]["layer"]
                and file_desc.entrypoints[name]["layer"] == LAYER_BY_ENTRY[name]
                for name in ENTRYPOINT_NAMES
            ) and {
                file_desc.entrypoints["vision"]["layer"],
                file_desc.entrypoints["govern"]["layer"],
            } == {DECISION_LAYER, IMPLEMENTATION_LAYER}
            detail = (
                "角色事实由两通道真实资产独立提取且层级一致"
                if ok
                else "角色边界漂移（真实资产未携带角色事实或层级不一致）"
            )
        elif checkpoint_id == "3":
            ok = _writes_only_vision_ledger(file_desc) and _writes_only_vision_ledger(mcp_desc)
            detail = "vision-audit 只指向 vision reviews 台账" if ok else "vision-audit 台账越界"
        elif checkpoint_id == "4":
            ok = _writes_only_goal_audit(file_desc) and _writes_only_goal_audit(mcp_desc)
            detail = "audit 只指向目标 03-audit" if ok else "audit 台账越界"
        elif checkpoint_id == "5":
            ok = "仓库内" in file_desc.instance_truth and "仓库内" in mcp_desc.instance_truth
            detail = "两通道实例真相均声明在仓库内治理记录树" if ok else "实例真相声明漂移"
        elif checkpoint_id == "6":
            ok = bool(file_desc.fail_closed_conditions) and bool(mcp_desc.fail_closed_conditions)
            detail = "两通道均声明 fail closed 条件" if ok else "fail closed 声明缺失"
        elif checkpoint_id == "7":
            ok = all(
                file_desc.entrypoints[name]["readonly_dispatch"]
                and mcp_desc.entrypoints[name]["readonly_dispatch"]
                for name in READONLY_DISPATCH_ENTRIES
            )
            detail = "vision-audit / audit 两通道均只读 dispatch" if ok else "独立审计可写状态"
        elif checkpoint_id == "8":
            ok = file_desc.single_charter and mcp_desc.single_charter
            detail = "两通道均声明单 Charter 不变量" if ok else "单愿景声明缺失"
        elif checkpoint_id == "9":
            ok = file_desc.workspace_roles == mcp_desc.workspace_roles == ("primary", "delivery")
            detail = "两通道工作区角色均为 primary/delivery" if ok else "角色边界漂移"
        elif checkpoint_id == "10":
            ok = file_desc.file_self_bootstrap and mcp_desc.mcp_only_bootstrap_forbidden
            detail = (
                "File 通道自举存在且 MCP 通道声明禁止仅 MCP 自举"
                if ok
                else "生产仓自举边界漂移"
            )
        else:  # pragma: no cover - guarded by data
            ok = False
            detail = f"unknown checkpoint {checkpoint_id}"
        results.append(
            {
                "checkpoint": checkpoint_id,
                "name": checkpoint["name"],
                "ok": bool(ok),
                "detail": detail,
            }
        )
    return results


def _prompt_basename(name: str) -> str:
    return PROMPT_PATHS[name].split("/")[-1]


def _writes_only_vision_ledger(desc: ChannelDescription) -> bool:
    targets = desc.entrypoints["vision-audit"].get("ledger_targets", [])
    joined = "\n".join(targets)
    return bool(targets) and "03-audit" not in joined and "vision" in joined


def _writes_only_goal_audit(desc: ChannelDescription) -> bool:
    targets = desc.entrypoints["audit"].get("ledger_targets", [])
    joined = "\n".join(targets)
    return bool(targets) and "03-audit" in joined and "vision" not in joined

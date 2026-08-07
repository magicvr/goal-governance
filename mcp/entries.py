"""Four governance entrypoints mapping for the dual File/MCP channels.

Pure data + pure functions. This module is the single source of truth for
entrypoint names, key parameter boundaries, layer, and role boundaries shared
by the MCP server, the L1 tests, and the L2 equivalence kernel.

VP-004 entry surface: ``vision`` / ``vision-audit`` / ``govern`` / ``audit``
are governance-mandatory; ``commit`` is a convenience, orthogonal to goal
governance and deliberately NOT part of the MCP tool set.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

# Layer names used by the L2 equivalence kernel.
DECISION_LAYER = "decision"
IMPLEMENTATION_LAYER = "implementation"

# Human-readable role boundary per entry (kept in sync with VP-004 entry table).
ROLE_BOUNDARIES: dict[str, str] = {
    "vision": (
        "决策层：建修 Charter、组合编排（VP）、Vision Review、re-align；冷启动优先。"
    ),
    "vision-audit": (
        "独立 Vision Review：只写意见到 {governance_root}/vision/reviews* 台账，"
        "不改 Charter / VP / Goal 状态。"
    ),
    "govern": (
        "实现编排：扫描工作区与审计台账、分类、P-004 用户裁决、提议下一步、"
        "确认后调用原语写入目标五件套。"
    ),
    "audit": (
        "Goal 交叉审计：只出意见到被审目标 03-audit 台账，不直接改 status/progress。"
    ),
}

# Writable ledger targets per entry (relative to governance_root, with globs).
LEDGER_TARGETS: dict[str, list[str]] = {
    "vision": ["vision/"],
    "vision-audit": ["vision/reviews.md", "vision/reviews/VRev-*"],
    "govern": ["goal-tree.md", "workspace-*/", "workspace-*/GOAL-*/"],
    "audit": ["workspace-*/GOAL-*/03-audit/"],
}

# Independent-review entries: their dispatch must never change goal/plan status.
READONLY_DISPATCH_ENTRIES = frozenset({"vision-audit", "audit"})

# Prompts that back each entry inside the skills package (File channel truth).
PROMPT_PATHS: dict[str, str] = {
    "vision": "prompts/06-vision-orchestrator.md",
    "vision-audit": "prompts/07-independent-vision-review.md",
    "govern": "prompts/00-govern-orchestrator.md",
    "audit": "prompts/05-independent-audit.md",
}

# Key parameter boundary per tool: name -> (type, required, description).
TOOL_PARAMETERS: dict[str, dict[str, tuple[str, bool, str]]] = {
    "vision": {
        "task": ("string", True, "决策层请求：建修 Charter / VP / Vision Review / re-align 意图。"),
        "workspace": ("string", False, "工作区 id 路径（如 docs/workspace-003-...），缺省由上下文定位。"),
    },
    "vision-audit": {
        "task": ("string", True, "独立 Vision Review 请求：被审对象与关注点。"),
        "scope": ("string", False, "审视范围（charter / plan / portfolio / existing-vrev）。"),
    },
    "govern": {
        "task": ("string", True, "实现编排请求：推进目标 / 响应审计 / 下一步建议。"),
        "workspace": ("string", False, "工作区 id 路径；缺省当前工作区。"),
        "goal_id": ("string", False, "焦点目标 id（如 GOAL-002-r1-mcp-equivalence-kernel）。"),
    },
    "audit": {
        "task": ("string", True, "交叉审计请求：被审对象与关注点。"),
        "goal_id": ("string", True, "被审目标 id（完整 id，如 GOAL-002-r1-mcp-equivalence-kernel）。"),
        "scope": ("string", False, "审计范围（整体 / 阶段 / 门禁）。"),
    },
}

# Ordered governance entrypoint names (contract hostEntrypoints order).
ENTRYPOINT_NAMES: tuple[str, ...] = ("vision", "vision-audit", "govern", "audit")


@dataclass(frozen=True)
class EntrypointSpec:
    """Stable, machine-checkable spec for one governance entrypoint."""

    name: str
    layer: str
    role: str
    readonly_dispatch: bool
    prompt_path: str
    parameters: dict[str, tuple[str, bool, str]]


def entrypoint_specs() -> dict[str, EntrypointSpec]:
    """Return the four governance entrypoint specs (deterministic)."""
    return {
        name: EntrypointSpec(
            name=name,
            layer=DISPATCH_LAYERS[name],
            role=ROLE_BOUNDARIES[name],
            readonly_dispatch=name in READONLY_DISPATCH_ENTRIES,
            prompt_path=PROMPT_PATHS[name],
            parameters=TOOL_PARAMETERS[name],
        )
        for name in ENTRYPOINT_NAMES
    }


# Layer per entry (must exist before entrypoint_specs; declared after use above).
DISPATCH_LAYERS: dict[str, str] = {
    "vision": DECISION_LAYER,
    "vision-audit": DECISION_LAYER,
    "govern": IMPLEMENTATION_LAYER,
    "audit": IMPLEMENTATION_LAYER,
}


def tool_definitions() -> list[dict[str, Any]]:
    """MCP ``tools/list`` definitions derived from the entrypoint specs."""
    definitions: list[dict[str, Any]] = []
    for spec in entrypoint_specs().values():
        properties: dict[str, Any] = {}
        required: list[str] = []
        for name, (kind, is_required, description) in spec.parameters.items():
            properties[name] = {"type": kind, "description": description}
            if is_required:
                required.append(name)
        definitions.append(
            {
                "name": spec.name,
                "description": f"{spec.layer} · {spec.role}",
                "inputSchema": {
                    "type": "object",
                    "properties": properties,
                    "required": required,
                    "additionalProperties": False,
                },
            }
        )
    return definitions


def validate_tool_names(tools: list[dict[str, Any]]) -> list[str]:
    """Return the missing governance names in a ``tools/list`` payload."""
    present = {str(tool.get("name")) for tool in tools}
    return [name for name in ENTRYPOINT_NAMES if name not in present]

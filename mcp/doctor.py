"""Doctor: read-only thin-shell / installation status report (VP-004 R2)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

try:  # package context
    from .config import GovernanceRootError, resolve_governance_root
    from .lifecycle import (
        INSTALL_JSON,
        MANAGED_BEGIN,
        MANAGED_END,
        THIN_SHELL_DIR,
        parse_managed_version,
        read_install_state,
    )
except ImportError:  # plain script / top-level module context
    from config import (  # type: ignore[no-redef]
        GovernanceRootError,
        resolve_governance_root,
    )
    from lifecycle import (  # type: ignore[no-redef]
        INSTALL_JSON,
        MANAGED_BEGIN,
        MANAGED_END,
        THIN_SHELL_DIR,
        parse_managed_version,
        read_install_state,
    )


def doctor(root: Path, *, governance_root: str | None = None) -> dict[str, Any]:
    """Return a structured installation status for a consumer repository.

    Never writes. Reports: governance root (resolved from project config,
    fail-closed), managed section presence/version, thin-shell state
    consistency, gitignore coverage of the thin shell, and contract presence.
    ``ok`` is True only when the managed section and thin shell agree on the
    installed version.
    """
    root = root.resolve()
    root_error: str | None = None
    if governance_root is None:
        try:
            governance_root = resolve_governance_root(root)
        except GovernanceRootError as error:
            root_error = str(error)
            governance_root = "docs"
    agents_path = root / "AGENTS.md"
    agents_text = agents_path.read_text(encoding="utf-8") if agents_path.is_file() else ""
    has_begin = MANAGED_BEGIN in agents_text
    has_end = MANAGED_END in agents_text
    managed_version = parse_managed_version(agents_text)

    state = read_install_state(root)
    state_version = None
    state_channel = None
    state_error = None
    if isinstance(state, dict):
        if "error" in state:
            state_error = state["error"]
        else:
            state_version = state.get("version")
            state_channel = state.get("channel")

    thin_dir_ignored = _is_gitignored(root, THIN_SHELL_DIR)

    contract_path = root / governance_root / "contracts" / "skills-consumer-contract.json"
    thin_contract_path = root / "skills" / "contracts" / "skills-consumer-contract.json"
    contract_present = contract_path.is_file() or thin_contract_path.is_file()
    contract_locations = [str(contract_path)]
    if thin_contract_path.is_file():
        contract_locations.append(str(thin_contract_path))
    contract_note = None
    if not contract_present:
        contract_note = (
            f"consumer contract not found at {governance_root}/contracts "
            "or skills/contracts (thin MCP channel 可选)"
        )

    issues: list[str] = []
    if root_error:
        issues.append(f"governance_root resolution failed: {root_error}")
    if not has_begin or not has_end:
        issues.append("AGENTS.md managed section missing or malformed")
    if state_error:
        issues.append(f"thin-shell state error: {state_error}")
    if managed_version and state_version and managed_version != state_version:
        issues.append(
            f"version mismatch: AGENTS managed={managed_version} install.json={state_version}"
        )
    if managed_version is None and state_version is None:
        issues.append("not installed (no managed section and no thin-shell state)")

    return {
        "ok": not issues,
        "governanceRoot": governance_root,
        "governanceRootError": root_error,
        "managedSection": {
            "present": has_begin and has_end,
            "version": managed_version,
        },
        "thinShell": {
            "stateFile": f"{THIN_SHELL_DIR}/{INSTALL_JSON}",
            "present": (root / THIN_SHELL_DIR / INSTALL_JSON).is_file(),
            "version": state_version,
            "channel": state_channel,
            "error": state_error,
        },
        "gitignore": {
            "thinShellIgnored": thin_dir_ignored,
            "fragment": "mcp/gitignore-fragment.txt",
        },
        "contract": {
            "present": contract_present,
            "path": contract_locations,
            "note": contract_note,
        },
        "issues": issues,
    }


def _is_gitignored(root: Path, relative: str) -> bool:
    """Best-effort gitignore check without requiring git on PATH."""
    gitignore = root / ".gitignore"
    if not gitignore.is_file():
        return False
    text = gitignore.read_text(encoding="utf-8", errors="replace")
    pattern = f"/{relative}/"
    return pattern in text or f"\n{relative}/" in text or f"{relative}/\n" in text or f"{relative}/" in text

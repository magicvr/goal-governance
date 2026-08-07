"""goal-governance MCP channel package (workspace-003 / VP-004 R1).

Contains the MCP stdio server (``server.py``), the four-entry mapping
(``entries.py``), the L2 shared equivalence kernel (``kernel.py``), and the
R2/R3 productization modules (``lifecycle.py``, ``doctor.py``, ``config.py``).
"""

import os

# Internal layout version of the MCP channel package. Stable across releases:
# it identifies the channel protocol/layout generation, NOT the product
# release version (A-012 F-002). Effective server version below.
MCP_LAYOUT_VERSION = "0.1.0"

# Release pin env var: the publish workflow (skills-pack-release.yml) passes
# the pack/tag version to the Docker build as GOAL_GOVERNANCE_MCP_VERSION, so
# the image's effective version always matches its GHCR tag / GitHub Release.
# Local source checkouts (stdio process) fall back to MCP_LAYOUT_VERSION.
# initialize.serverInfo.version, lifecycle install/upgrade and the version
# command all read __version__, so they cannot drift from the image tag.
RELEASE_VERSION_ENV = "GOAL_GOVERNANCE_MCP_VERSION"


def effective_version() -> str:
    return os.environ.get(RELEASE_VERSION_ENV) or MCP_LAYOUT_VERSION


__version__ = effective_version()

#!/usr/bin/env bash
# Goal Governance Skills installer (Claude Code + GitHub Copilot)
# Run from the target project root. No network access required.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_ROOT="$SCRIPT_DIR"
INSTALL_DIR="$SOURCE_ROOT/install"
CLAUDE_SRC="$INSTALL_DIR/claude/AGENTS.md"
COPILOT_SRC="$INSTALL_DIR/copilot/copilot-instructions.md"
PROMPTS_SRC="$SOURCE_ROOT/prompts"
TEMPLATES_SRC="$SOURCE_ROOT/templates"

TARGET_DIR="${PWD}"
INSTALL_CLAUDE=0
INSTALL_COPILOT=0
INSTALL_EXTRAS=0

usage() {
  cat <<'EOF'
Goal Governance Skills installer

Usage (run from target project root):
  ./install.sh --claude      Install Claude Code rules (AGENTS.md)
  ./install.sh --copilot     Install GitHub Copilot rules (.github/copilot-instructions.md)
  ./install.sh --all         Install both + optional prompts/ and templates/
  ./install.sh --help        Show this help

Behavior:
  - Copies into the current working directory
  - Prompts before overwriting existing files
  - Offline only; no network calls
EOF
}

die() {
  echo "Error: $*" >&2
  exit 1
}

confirm_overwrite() {
  local path="$1"
  if [[ ! -e "$path" ]]; then
    return 0
  fi
  printf "File already exists: %s\nOverwrite? [y/N] " "$path"
  read -r answer
  case "$answer" in
    y|Y|yes|YES) return 0 ;;
    *) echo "Skipped: $path"; return 1 ;;
  esac
}

copy_file() {
  local src="$1"
  local dest="$2"
  [[ -f "$src" ]] || die "Source file not found: $src"
  mkdir -p "$(dirname "$dest")"
  if confirm_overwrite "$dest"; then
    cp "$src" "$dest"
    echo "Installed: $dest"
  fi
}

copy_dir_merge() {
  local src="$1"
  local dest="$2"
  local label="$3"
  [[ -d "$src" ]] || die "Source directory not found: $src"

  if [[ -e "$dest" ]]; then
    printf "Directory already exists: %s\nOverwrite contents from %s? [y/N] " "$dest" "$label"
    read -r answer
    case "$answer" in
      y|Y|yes|YES) ;;
      *) echo "Skipped: $dest"; return 0 ;;
    esac
  fi

  mkdir -p "$dest"
  # shellcheck disable=SC2086
  cp -R "$src"/. "$dest"/
  echo "Installed: $dest/  (from $label)"
}

print_next_steps() {
  cat <<EOF

Done.

Next steps:
  1. Review installed rule file(s) and adjust paths for your project.
  2. Ensure docs/goals/goal-tree.md exists (create if needed).
  3. Create or update Root Goal GOAL-001 under docs/goals/.
  4. Optional: use prompts/ for common goal workflows.

Target directory: $TARGET_DIR
EOF
}

# --- parse args ---
if [[ $# -eq 0 ]]; then
  usage
  exit 1
fi

while [[ $# -gt 0 ]]; do
  case "$1" in
    --claude)
      INSTALL_CLAUDE=1
      shift
      ;;
    --copilot)
      INSTALL_COPILOT=1
      shift
      ;;
    --all)
      INSTALL_CLAUDE=1
      INSTALL_COPILOT=1
      INSTALL_EXTRAS=1
      shift
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      die "Unknown option: $1 (use --help)"
      ;;
  esac
done

echo "Installing into: $TARGET_DIR"
echo "Source package:  $SOURCE_ROOT"
echo

if [[ "$INSTALL_CLAUDE" -eq 1 ]]; then
  copy_file "$CLAUDE_SRC" "$TARGET_DIR/AGENTS.md"
fi

if [[ "$INSTALL_COPILOT" -eq 1 ]]; then
  copy_file "$COPILOT_SRC" "$TARGET_DIR/.github/copilot-instructions.md"
fi

if [[ "$INSTALL_EXTRAS" -eq 1 ]]; then
  copy_dir_merge "$PROMPTS_SRC" "$TARGET_DIR/skills/prompts" "prompts"
  copy_dir_merge "$TEMPLATES_SRC" "$TARGET_DIR/skills/templates" "templates"
fi

print_next_steps

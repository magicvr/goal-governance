#!/usr/bin/env bash
# Goal Governance Skills installer (Claude Code + GitHub Copilot)
# Run from the target project root. No network access required.
#
# Typical flow:
#   1. Copy this whole skills package into the project root
#      (may rename, e.g. my-governance-skills)
#   2. cd to project root
#   3. bash ./skills/install.sh --copilot --skills-dir ./skills
#      or: bash ./my-governance-skills/install.sh --all --skills-dir ./my-governance-skills

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PACKAGE_ROOT="$SCRIPT_DIR"

TARGET_DIR="${PWD}"
SKILLS_DIR_ARG="./skills"
INSTALL_CLAUDE=0
INSTALL_COPILOT=0
INSTALL_EXTRAS=0

usage() {
  cat <<'EOF'
Goal Governance Skills installer

Prerequisites:
  Copy the entire skills package into the target project root first
  (you may rename it, e.g. my-governance-skills). Then run this script
  from the project root.

Usage (run from target project root):
  ./install.sh --claude [--skills-dir DIR]
  ./install.sh --copilot [--skills-dir DIR]
  ./install.sh --all [--skills-dir DIR]
  ./install.sh --help

Options:
  --claude              Install Claude Code rules → ./AGENTS.md
  --copilot             Install GitHub Copilot rules → ./.github/copilot-instructions.md
  --all                 Install both tools + ensure prompts/ and templates/
                        under --skills-dir
  --skills-dir DIR      Skills package / destination directory (default: ./skills)
                        Relative paths are resolved from the current working directory.
  --help, -h            Show this help

Behavior:
  - Rule files always install into the current working directory (project root)
  - .github/ is created under the project root when installing Copilot
  - prompts/ and templates/ are placed under --skills-dir
  - Source files are read from the package next to this script
  - Prompts before overwriting existing files
  - Offline only; no network calls

Examples:
  cd /path/to/your-project
  bash ./skills/install.sh --copilot --skills-dir ./skills
  bash ./my-governance-skills/install.sh --all --skills-dir ./my-governance-skills
  bash /path/to/goal-governance/skills/install.sh --all --skills-dir ./skills
EOF
}

die() {
  echo "Error: $*" >&2
  exit 1
}

same_path() {
  local a b
  a="$(cd "$(dirname "$1")" 2>/dev/null && pwd)/$(basename "$1")"
  b="$(cd "$(dirname "$2")" 2>/dev/null && pwd)/$(basename "$2")"
  [[ "$a" == "$b" ]]
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

  # Same path → already in place (common after copying whole package)
  if [[ -d "$dest" ]] && same_path "$src" "$dest"; then
    echo "Already present: $dest/  (from $label)"
    return 0
  fi

  if [[ -e "$dest" ]]; then
    printf "Directory already exists: %s\nOverwrite contents from %s? [y/N] " "$dest" "$label"
    read -r answer
    case "$answer" in
      y|Y|yes|YES) ;;
      *) echo "Skipped: $dest"; return 0 ;;
    esac
  fi

  mkdir -p "$dest"
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
  4. Use prompts under $SKILLS_DIR/prompts/ for common goal workflows
     (e.g. 01-create-new-goal.md … 04-write-audit.md).

Project root:  $TARGET_DIR
Skills dir:    $SKILLS_DIR
Package root:  $PACKAGE_ROOT
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
    --skills-dir)
      [[ $# -ge 2 ]] || die "--skills-dir requires a path argument"
      SKILLS_DIR_ARG="$2"
      shift 2
      ;;
    --skills-dir=*)
      SKILLS_DIR_ARG="${1#--skills-dir=}"
      [[ -n "$SKILLS_DIR_ARG" ]] || die "--skills-dir requires a path argument"
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

if [[ "$INSTALL_CLAUDE" -eq 0 && "$INSTALL_COPILOT" -eq 0 ]]; then
  usage
  exit 1
fi

# Resolve skills-dir (relative to CWD / project root)
if [[ "$SKILLS_DIR_ARG" = /* ]]; then
  SKILLS_DIR="$SKILLS_DIR_ARG"
else
  SKILLS_DIR="$TARGET_DIR/$SKILLS_DIR_ARG"
fi
# Normalize if directory already exists
if [[ -d "$SKILLS_DIR" ]]; then
  SKILLS_DIR="$(cd "$SKILLS_DIR" && pwd)"
fi

CLAUDE_SRC="$PACKAGE_ROOT/install/claude/AGENTS.md"
COPILOT_SRC="$PACKAGE_ROOT/install/copilot/copilot-instructions.md"
PROMPTS_SRC="$PACKAGE_ROOT/prompts"
TEMPLATES_SRC="$PACKAGE_ROOT/templates"

# Safety checks
[[ -f "$CLAUDE_SRC" ]] || die "Missing package file: $CLAUDE_SRC"
[[ -f "$COPILOT_SRC" ]] || die "Missing package file: $COPILOT_SRC"
[[ -d "$PROMPTS_SRC" ]] || die "Missing package directory: $PROMPTS_SRC"
[[ -d "$TEMPLATES_SRC" ]] || die "Missing package directory: $TEMPLATES_SRC"

if [[ ! -d "$TARGET_DIR" ]]; then
  die "Current working directory is not a directory: $TARGET_DIR"
fi

echo "Project root:  $TARGET_DIR"
echo "Skills dir:    $SKILLS_DIR"
echo "Package root:  $PACKAGE_ROOT"
echo

if [[ "$INSTALL_CLAUDE" -eq 1 ]]; then
  copy_file "$CLAUDE_SRC" "$TARGET_DIR/AGENTS.md"
fi

if [[ "$INSTALL_COPILOT" -eq 1 ]]; then
  # .github always under project root (CWD)
  mkdir -p "$TARGET_DIR/.github"
  copy_file "$COPILOT_SRC" "$TARGET_DIR/.github/copilot-instructions.md"
fi

if [[ "$INSTALL_EXTRAS" -eq 1 ]]; then
  mkdir -p "$SKILLS_DIR"
  copy_dir_merge "$PROMPTS_SRC" "$SKILLS_DIR/prompts" "prompts"
  copy_dir_merge "$TEMPLATES_SRC" "$SKILLS_DIR/templates" "templates"
fi

print_next_steps
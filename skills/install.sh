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
INSTALL_PRIMITIVE_WRAPPERS=0

usage() {
  cat <<'EOF'
Goal Governance Skills installer

Prerequisites:
  Copy the entire skills package into the target project root first
  (you may rename it, e.g. my-governance-skills). Then run this script
  from the project root.

Usage (run from target project root):
  ./install.sh --claude [--skills-dir DIR]
  ./install.sh --copilot [--skills-dir DIR] [--with-primitives]
  ./install.sh --all [--skills-dir DIR] [--with-primitives]
  ./install.sh --help

Options:
  --claude              Install Claude Code rules → ./AGENTS.md
  --copilot             Install GitHub Copilot rules → ./.github/copilot-instructions.md
                        and PRIMARY slash only → ./.github/prompts/govern.prompt.md
  --with-primitives     Also install advanced slash wrappers (new-goal, log-decision,
                        update-execution, write-audit). Opt-in only — avoids form-menu UX.
  --all                 Install both tools + ensure prompts/ and templates/
                        under --skills-dir; Copilot still gets /govern only unless
                        --with-primitives is set
  --skills-dir DIR      Skills package / destination directory (default: ./skills)
                        Relative paths are resolved from the current working directory.
  --help, -h            Show this help

Behavior:
  - Rule files always install into the current working directory (project root)
  - .github/ is created under the project root when installing Copilot
  - Default Copilot slash surface is /govern only (orchestrator)
  - Advanced form-filling slashes are NOT installed unless --with-primitives
  - Primitive prompt files (01–04) always ship under prompts/ (with --all or package copy)
  - prompts/ and templates/ are placed under --skills-dir (with --all)
  - Source files are read from the package next to this script
  - Prompts before overwriting existing files
  - Offline only; no network calls

Examples:
  cd /path/to/your-project
  bash ./skills/install.sh --copilot --skills-dir ./skills
  bash ./skills/install.sh --copilot --with-primitives --skills-dir ./skills
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
  3. DEFAULT (only) user path: goal-governance orchestrator
     - Core: $SKILLS_DIR/prompts/00-govern-orchestrator.md
     - Copilot: /govern  (installed by default with --copilot)
     Scans project, classifies purposes, guides set-goal → advance →
     stage/close-audit (confirm before writes). Invokes 01–04 as needed.
  4. Do not look for four form-filling slash commands — they are not installed
     unless you re-run with --with-primitives (advanced / optional).

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
    --with-primitives)
      INSTALL_PRIMITIVE_WRAPPERS=1
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
COPILOT_WRAPPERS_SRC="$PACKAGE_ROOT/install/copilot/prompts"
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

  # Slash wrappers → always .github/prompts/ (not under --skills-dir)
  # Default: primary /govern only (avoid four form-filling slash entries)
  [[ -d "$COPILOT_WRAPPERS_SRC" ]] || die "Missing package directory: $COPILOT_WRAPPERS_SRC"
  mkdir -p "$TARGET_DIR/.github/prompts"
  WRAPPER_NAMES=(govern)
  if [[ "$INSTALL_PRIMITIVE_WRAPPERS" -eq 1 ]]; then
    WRAPPER_NAMES+=(new-goal log-decision update-execution write-audit)
    echo "Including advanced primitive slash wrappers (--with-primitives)"
  else
    echo "Copilot slash surface: /govern only (pass --with-primitives for advanced form ops)"
  fi
  for name in "${WRAPPER_NAMES[@]}"; do
    copy_file \
      "$COPILOT_WRAPPERS_SRC/${name}.md" \
      "$TARGET_DIR/.github/prompts/${name}.prompt.md"
  done
fi

if [[ "$INSTALL_EXTRAS" -eq 1 ]]; then
  mkdir -p "$SKILLS_DIR"
  copy_dir_merge "$PROMPTS_SRC" "$SKILLS_DIR/prompts" "prompts"
  copy_dir_merge "$TEMPLATES_SRC" "$SKILLS_DIR/templates" "templates"
fi

print_next_steps
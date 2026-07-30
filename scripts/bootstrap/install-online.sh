#!/usr/bin/env bash
# Goal Governance · online / offline bootstrap installer (GOAL-023)
#
# Entry point 1 (bootstrap): obtain skills zip (embedded core) → verify SHA-256
# → materialize ./skills → invoke package-local install.sh (default --all).
# Does NOT download core separately; skills zip already embeds core.
#
# Offline:
#   bash install-online.sh --version 0.9.2 --zip-path ./goal-governance-skills-v0.9.2.zip
# Online:
#   bash install-online.sh --version 0.9.2

set -euo pipefail

VERSION=""
TARGET_DIR=""
SKILLS_DIR_NAME="skills"
ZIP_PATH=""
SHA256_PATH=""
REPO="magicvr/goal-governance"
RELEASE_TAG=""
SKIP_INSTALL=0
FORCE=0

usage() {
  cat <<'EOF'
Goal Governance bootstrap installer (GOAL-023)

Usage:
  install-online.sh --version X.Y.Z [--target-dir DIR] [--zip-path PATH] [--sha256-path PATH]
  install-online.sh --version X.Y.Z --zip-path ./goal-governance-skills-vX.Y.Z.zip   # offline
  install-online.sh --version X.Y.Z                                                 # online Release

Options:
  --version V         SemVer (optional leading v)
  --target-dir DIR    Project root (default: cwd)
  --skills-dir-name N Directory under target (default: skills)
  --zip-path PATH     Local skills zip (skip download)
  --sha256-path PATH  Local .sha256 sidecar
  --repo OWNER/NAME   GitHub repo (default: magicvr/goal-governance)
  --release-tag TAG   Download tag (default: v + normalized version)
  --skip-install      Only verify + extract
  --force             Replace existing skills dir; pass --force to package install
  --help, -h          Show help

Default package install: --all --non-interactive [--force].
EOF
}

die() {
  echo "Error: $*" >&2
  exit 1
}

normalize_version() {
  local v="${1#"${1%%[![:space:]]*}"}"
  v="${v%"${v##*[![:space:]]}"}"
  [[ -n "$v" ]] || die "Version must be non-empty"
  if [[ "$v" == [vV]* ]]; then
    v="${v:1}"
  fi
  if [[ ! "$v" =~ ^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(-[0-9A-Za-z.-]+)?(\+[0-9A-Za-z.-]+)?$ ]]; then
    die "Version must be SemVer-like (got $1)"
  fi
  printf '%s' "$v"
}

file_sha256_hex() {
  local path="$1"
  if command -v sha256sum >/dev/null 2>&1; then
    sha256sum -b "$path" | awk '{print tolower($1)}'
  elif command -v shasum >/dev/null 2>&1; then
    shasum -a 256 "$path" | awk '{print tolower($1)}'
  else
    die "Need sha256sum or shasum on PATH"
  fi
}

assert_digest_match() {
  local zip_file="$1"
  local sidecar="$2"
  [[ -f "$sidecar" ]] || die "SHA-256 sidecar not found: $sidecar"
  local zip_base expected name actual
  zip_base="$(basename "$zip_file")"
  # shellcheck disable=SC2034
  read -r expected name < <(awk 'NF>=2 {print tolower($1), $2; exit}' "$sidecar")
  [[ -n "$expected" && "$expected" =~ ^[0-9a-f]{64}$ ]] || die "Invalid SHA-256 sidecar: $sidecar"
  local base_name
  base_name="$(basename "$name")"
  [[ "$base_name" == "$zip_base" ]] || die "Sidecar filename '$name' does not match zip basename '$zip_base'"
  actual="$(file_sha256_hex "$zip_file")"
  if [[ "$actual" != "$expected" ]]; then
    die "SHA-256 mismatch for $zip_base
  expected: $expected
  actual:   $actual"
  fi
  echo "SHA-256 OK: $zip_base"
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --version) VERSION="${2:-}"; shift 2 ;;
    --target-dir) TARGET_DIR="${2:-}"; shift 2 ;;
    --skills-dir-name) SKILLS_DIR_NAME="${2:-}"; shift 2 ;;
    --zip-path) ZIP_PATH="${2:-}"; shift 2 ;;
    --sha256-path) SHA256_PATH="${2:-}"; shift 2 ;;
    --repo) REPO="${2:-}"; shift 2 ;;
    --release-tag) RELEASE_TAG="${2:-}"; shift 2 ;;
    --skip-install) SKIP_INSTALL=1; shift ;;
    --force) FORCE=1; shift ;;
    --help|-h) usage; exit 0 ;;
    *) die "Unknown argument: $1" ;;
  esac
done

[[ -n "$VERSION" ]] || die "Missing --version"
NORM="$(normalize_version "$VERSION")"
ARCHIVE_ROOT="goal-governance-skills-v${NORM}"
ZIP_NAME="${ARCHIVE_ROOT}.zip"
SHA_NAME="${ZIP_NAME}.sha256"

if [[ -z "$TARGET_DIR" ]]; then
  TARGET_DIR="$(pwd)"
fi
mkdir -p "$TARGET_DIR"
TARGET_DIR="$(cd "$TARGET_DIR" && pwd)"

WORK_DIR="${TARGET_DIR}/.goal-governance-bootstrap-tmp"
rm -rf "$WORK_DIR"
mkdir -p "$WORK_DIR"

cleanup() {
  rm -rf "$WORK_DIR"
}
trap cleanup EXIT

LOCAL_ZIP=""
LOCAL_SHA=""

if [[ -n "$ZIP_PATH" ]]; then
  # Relative zip/sha paths resolve against process CWD (pwd), not --target-dir.
  if [[ "$ZIP_PATH" = /* ]]; then
    LOCAL_ZIP="$ZIP_PATH"
  else
    LOCAL_ZIP="$(pwd)/${ZIP_PATH}"
  fi
  LOCAL_ZIP="$(cd "$(dirname "$LOCAL_ZIP")" && pwd)/$(basename "$LOCAL_ZIP")"
  [[ -f "$LOCAL_ZIP" ]] || die "Zip path not found: $LOCAL_ZIP"
  if [[ -n "$SHA256_PATH" ]]; then
    if [[ "$SHA256_PATH" = /* ]]; then
      LOCAL_SHA="$SHA256_PATH"
    else
      LOCAL_SHA="$(pwd)/${SHA256_PATH}"
    fi
    LOCAL_SHA="$(cd "$(dirname "$LOCAL_SHA")" && pwd)/$(basename "$LOCAL_SHA")"
  elif [[ -f "${LOCAL_ZIP}.sha256" ]]; then
    LOCAL_SHA="${LOCAL_ZIP}.sha256"
  elif [[ -f "$(dirname "$LOCAL_ZIP")/${SHA_NAME}" ]]; then
    LOCAL_SHA="$(dirname "$LOCAL_ZIP")/${SHA_NAME}"
  else
    die "SHA-256 sidecar not found next to zip (pass --sha256-path)"
  fi
  echo "Offline mode: using local zip $LOCAL_ZIP"
else
  TAG="${RELEASE_TAG:-v${NORM}}"
  BASE_URL="https://github.com/${REPO}/releases/download/${TAG}"
  LOCAL_ZIP="${WORK_DIR}/${ZIP_NAME}"
  LOCAL_SHA="${WORK_DIR}/${SHA_NAME}"
  echo "Online mode: downloading ${BASE_URL}/${ZIP_NAME}"
  if command -v curl >/dev/null 2>&1; then
    curl -fsSL -o "$LOCAL_ZIP" "${BASE_URL}/${ZIP_NAME}"
    curl -fsSL -o "$LOCAL_SHA" "${BASE_URL}/${SHA_NAME}"
  elif command -v wget >/dev/null 2>&1; then
    wget -q -O "$LOCAL_ZIP" "${BASE_URL}/${ZIP_NAME}"
    wget -q -O "$LOCAL_SHA" "${BASE_URL}/${SHA_NAME}"
  else
    die "Need curl or wget for online mode"
  fi
fi

assert_digest_match "$LOCAL_ZIP" "$LOCAL_SHA"

EXTRACT_DIR="${WORK_DIR}/extract"
mkdir -p "$EXTRACT_DIR"
if command -v unzip >/dev/null 2>&1; then
  unzip -q -o "$LOCAL_ZIP" -d "$EXTRACT_DIR"
else
  die "Need unzip on PATH"
fi

PACKAGE_SRC="${EXTRACT_DIR}/${ARCHIVE_ROOT}"
if [[ ! -d "$PACKAGE_SRC" ]]; then
  # single top-level directory fallback
  mapfile -t tops < <(find "$EXTRACT_DIR" -mindepth 1 -maxdepth 1 -type d | head -n 2)
  if [[ ${#tops[@]} -eq 1 ]]; then
    PACKAGE_SRC="${tops[0]}"
  else
    die "Expected archive root folder '${ARCHIVE_ROOT}' under extract dir"
  fi
fi

DEST_SKILLS="${TARGET_DIR}/${SKILLS_DIR_NAME}"
if [[ -e "$DEST_SKILLS" ]]; then
  if [[ "$FORCE" -ne 1 ]]; then
    die "Destination already exists (use --force to replace): $DEST_SKILLS"
  fi
  rm -rf "$DEST_SKILLS"
fi
cp -a "$PACKAGE_SRC" "$DEST_SKILLS"
echo "Materialized skills package: $DEST_SKILLS"

INSTALL_SH="${DEST_SKILLS}/install.sh"
[[ -f "$INSTALL_SH" ]] || die "Package install.sh missing after extract: $INSTALL_SH"
chmod +x "$INSTALL_SH" || true

if [[ "$SKIP_INSTALL" -eq 1 ]]; then
  echo "SkipInstall: package extracted; package install not run."
  exit 0
fi

INSTALL_ARGS=(--all --non-interactive --skills-dir "$DEST_SKILLS")
if [[ "$FORCE" -eq 1 ]]; then
  INSTALL_ARGS+=(--force)
fi

echo "Running package install: install.sh ${INSTALL_ARGS[*]}"
(
  cd "$TARGET_DIR"
  bash "$INSTALL_SH" "${INSTALL_ARGS[@]}"
)

echo "Bootstrap complete."

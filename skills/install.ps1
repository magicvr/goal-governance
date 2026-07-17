# Goal Governance Skills installer (Claude Code + GitHub Copilot)
# Run from the target project root. No network access required.
# Usage:
#   .\install.ps1 -Claude
#   .\install.ps1 -Copilot
#   .\install.ps1 -All
#   .\install.ps1 -Help

param(
    [switch]$Claude,
    [switch]$Copilot,
    [switch]$All,
    [switch]$Help,
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$RemainingArgs
)

$ErrorActionPreference = 'Stop'

function Show-Usage {
    @"
Goal Governance Skills installer

Usage (run from target project root):
  .\install.ps1 -Claude       Install Claude Code rules (AGENTS.md)
  .\install.ps1 -Copilot      Install GitHub Copilot rules (.github\copilot-instructions.md)
  .\install.ps1 -All          Install both + optional prompts\ and templates\
  .\install.ps1 -Help         Show this help

Also accepted:
  .\install.ps1 --claude | --copilot | --all | --help

Behavior:
  - Copies into the current working directory
  - Prompts before overwriting existing files
  - Offline only; no network calls
"@
}

function Write-Err([string]$Message) {
    Write-Host "Error: $Message" -ForegroundColor Red
    exit 1
}

function Confirm-Overwrite([string]$Path) {
    if (-not (Test-Path -LiteralPath $Path)) {
        return $true
    }
    $answer = Read-Host "File already exists: $Path`nOverwrite? [y/N]"
    if ($answer -match '^(y|yes)$') {
        return $true
    }
    Write-Host "Skipped: $Path"
    return $false
}

function Copy-RuleFile {
    param(
        [string]$Source,
        [string]$Destination
    )
    if (-not (Test-Path -LiteralPath $Source -PathType Leaf)) {
        Write-Err "Source file not found: $Source"
    }
    $destDir = Split-Path -Parent $Destination
    if ($destDir -and -not (Test-Path -LiteralPath $destDir)) {
        New-Item -ItemType Directory -Path $destDir -Force | Out-Null
    }
    if (Confirm-Overwrite -Path $Destination) {
        Copy-Item -LiteralPath $Source -Destination $Destination -Force
        Write-Host "Installed: $Destination"
    }
}

function Copy-DirMerge {
    param(
        [string]$Source,
        [string]$Destination,
        [string]$Label
    )
    if (-not (Test-Path -LiteralPath $Source -PathType Container)) {
        Write-Err "Source directory not found: $Source"
    }
    if (Test-Path -LiteralPath $Destination) {
        $answer = Read-Host "Directory already exists: $Destination`nOverwrite contents from $Label? [y/N]"
        if ($answer -notmatch '^(y|yes)$') {
            Write-Host "Skipped: $Destination"
            return
        }
    }
    if (-not (Test-Path -LiteralPath $Destination)) {
        New-Item -ItemType Directory -Path $Destination -Force | Out-Null
    }
    Copy-Item -Path (Join-Path $Source '*') -Destination $Destination -Recurse -Force
    Write-Host "Installed: $Destination\  (from $Label)"
}

function Show-NextSteps([string]$TargetDir) {
    @"

Done.

Next steps:
  1. Review installed rule file(s) and adjust paths for your project.
  2. Ensure docs\goals\goal-tree.md exists (create if needed).
  3. Create or update Root Goal GOAL-001 under docs\goals\.
  4. Optional: use prompts\ for common goal workflows.

Target directory: $TargetDir
"@
}

# Accept GNU-style flags for docs consistency (e.g. --claude)
foreach ($arg in @($RemainingArgs)) {
    switch -Regex ($arg) {
        '^--claude$' { $Claude = $true }
        '^--copilot$' { $Copilot = $true }
        '^--all$' { $All = $true }
        '^(--help|-h)$' { $Help = $true }
        default { Write-Err "Unknown option: $arg (use -Help)" }
    }
}

if ($Help -or (-not $Claude -and -not $Copilot -and -not $All)) {
    Show-Usage
    if ($Help) { exit 0 } else { exit 1 }
}

if ($All) {
    $Claude = $true
    $Copilot = $true
    $installExtras = $true
} else {
    $installExtras = $false
}

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$SourceRoot = $ScriptDir
$InstallDir = Join-Path $SourceRoot 'install'
$ClaudeSrc = Join-Path $InstallDir 'claude\AGENTS.md'
$CopilotSrc = Join-Path $InstallDir 'copilot\copilot-instructions.md'
$PromptsSrc = Join-Path $SourceRoot 'prompts'
$TemplatesSrc = Join-Path $SourceRoot 'templates'
$TargetDir = (Get-Location).Path

Write-Host "Installing into: $TargetDir"
Write-Host "Source package:  $SourceRoot"
Write-Host ''

if ($Claude) {
    Copy-RuleFile -Source $ClaudeSrc -Destination (Join-Path $TargetDir 'AGENTS.md')
}

if ($Copilot) {
    Copy-RuleFile -Source $CopilotSrc -Destination (Join-Path $TargetDir '.github\copilot-instructions.md')
}

if ($installExtras) {
    Copy-DirMerge -Source $PromptsSrc -Destination (Join-Path $TargetDir 'skills\prompts') -Label 'prompts'
    Copy-DirMerge -Source $TemplatesSrc -Destination (Join-Path $TargetDir 'skills\templates') -Label 'templates'
}

Show-NextSteps -TargetDir $TargetDir

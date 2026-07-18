# Goal Governance Skills installer (Claude Code + GitHub Copilot)
# Run from the target project root. No network access required.
#
# Typical flow:
#   1. Copy this whole skills package into the project root
#      (may rename, e.g. my-governance-skills)
#   2. cd to project root
#   3. .\skills\install.ps1 -Copilot -SkillsDir .\skills
#      or: .\my-governance-skills\install.ps1 -All -SkillsDir .\my-governance-skills

param(
    [switch]$Claude,
    [switch]$Copilot,
    [switch]$All,
    [switch]$Help,
    [switch]$WithPrimitives,
    [string]$SkillsDir = './skills',
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$RemainingArgs
)

$ErrorActionPreference = 'Stop'

function Show-Usage {
    @"
Goal Governance Skills installer

Prerequisites:
  Copy the entire skills package into the target project root first
  (you may rename it, e.g. my-governance-skills). Then run this script
  from the project root.

Usage (run from target project root):
  .\install.ps1 -Claude [-SkillsDir DIR]
  .\install.ps1 -Copilot [-SkillsDir DIR] [-WithPrimitives]
  .\install.ps1 -All [-SkillsDir DIR] [-WithPrimitives]
  .\install.ps1 -Help

Options:
  -Claude / --claude       Install Claude Code rules -> .\AGENTS.md
  -Copilot / --copilot     Install GitHub Copilot rules -> .\.github\copilot-instructions.md
                           and PRIMARY slash only -> .\.github\prompts\govern.prompt.md
  -WithPrimitives / --with-primitives
                           Also install advanced slash wrappers (new-goal, log-decision,
                           update-execution, write-audit). Opt-in only.
  -All / --all             Install both tools + ensure prompts\ and templates\
                           under -SkillsDir; Copilot still gets /govern only unless
                           -WithPrimitives is set
  -SkillsDir / --skills-dir DIR
                           Skills package / destination directory (default: .\skills)
                           Relative paths are resolved from the current working directory.
  -Help / --help           Show this help

Behavior:
  - Rule files always install into the current working directory (project root)
  - .github\ is created under the project root when installing Copilot
  - Default Copilot slash surface is /govern only (orchestrator)
  - Advanced form-filling slashes are NOT installed unless -WithPrimitives
  - Primitive prompt files (01-04) always ship under prompts\ (with -All or package copy)
  - prompts\ and templates\ are placed under -SkillsDir (with -All)
  - Source files are read from the package next to this script
  - Prompts before overwriting existing files
  - Offline only; no network calls

Examples:
  cd C:\path\to\your-project
  .\skills\install.ps1 -Copilot -SkillsDir .\skills
  .\skills\install.ps1 -Copilot -WithPrimitives -SkillsDir .\skills
  .\my-governance-skills\install.ps1 -All -SkillsDir .\my-governance-skills
  & C:\path\to\goal-governance\skills\install.ps1 -All -SkillsDir .\skills
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

function Get-ResolvedPath([string]$Path, [string]$BaseDir) {
    if ([System.IO.Path]::IsPathRooted($Path)) {
        return [System.IO.Path]::GetFullPath($Path)
    }
    return [System.IO.Path]::GetFullPath((Join-Path $BaseDir $Path))
}

function Test-SamePath([string]$PathA, [string]$PathB) {
    try {
        $a = [System.IO.Path]::GetFullPath($PathA).TrimEnd('\', '/')
        $b = [System.IO.Path]::GetFullPath($PathB).TrimEnd('\', '/')
        return $a.Equals($b, [System.StringComparison]::OrdinalIgnoreCase)
    } catch {
        return $false
    }
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

    # Same path -> already in place (common after copying whole package)
    if ((Test-Path -LiteralPath $Destination -PathType Container) -and (Test-SamePath $Source $Destination)) {
        Write-Host "Already present: $Destination\  (from $Label)"
        return
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

function Show-NextSteps {
    param(
        [string]$TargetDir,
        [string]$SkillsDir,
        [string]$PackageRoot
    )
    @"

Done.

Next steps:
  1. Review installed rule file(s) and adjust paths for your project.
  2. Ensure docs\goals\goal-tree.md exists (create if needed).
  3. DEFAULT (only) user path: goal-governance orchestrator
     - Core: $SkillsDir\prompts\00-govern-orchestrator.md
     - Copilot: /govern  (installed by default with -Copilot)
     Scans project, classifies purposes, guides set-goal -> advance ->
     stage/close-audit (confirm before writes). Invokes 01-04 as needed.
  4. Do not look for four form-filling slash commands - they are not installed
     unless you re-run with -WithPrimitives (advanced / optional).

Project root:  $TargetDir
Skills dir:    $SkillsDir
Package root:  $PackageRoot
"@
}

# Accept GNU-style flags for docs consistency (e.g. --claude, --skills-dir DIR)
$i = 0
while ($i -lt @($RemainingArgs).Count) {
    $arg = $RemainingArgs[$i]
    switch -Regex ($arg) {
        '^--claude$' { $Claude = $true; $i++ }
        '^--copilot$' { $Copilot = $true; $i++ }
        '^--all$' { $All = $true; $i++ }
        '^--with-primitives$' { $WithPrimitives = $true; $i++ }
        '^(--help|-h)$' { $Help = $true; $i++ }
        '^--skills-dir$' {
            if ($i + 1 -ge $RemainingArgs.Count) {
                Write-Err "--skills-dir requires a path argument"
            }
            $SkillsDir = $RemainingArgs[$i + 1]
            $i += 2
        }
        '^--skills-dir=(.+)$' {
            $SkillsDir = $Matches[1]
            if ([string]::IsNullOrWhiteSpace($SkillsDir)) {
                Write-Err "--skills-dir requires a path argument"
            }
            $i++
        }
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

$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$TargetDir = (Get-Location).Path
$SkillsDirResolved = Get-ResolvedPath -Path $SkillsDir -BaseDir $TargetDir

$ClaudeSrc = Join-Path $PackageRoot 'install\claude\AGENTS.md'
$CopilotSrc = Join-Path $PackageRoot 'install\copilot\copilot-instructions.md'
$CopilotWrappersSrc = Join-Path $PackageRoot 'install\copilot\prompts'
$PromptsSrc = Join-Path $PackageRoot 'prompts'
$TemplatesSrc = Join-Path $PackageRoot 'templates'

# Safety checks
if (-not (Test-Path -LiteralPath $ClaudeSrc -PathType Leaf)) {
    Write-Err "Missing package file: $ClaudeSrc"
}
if (-not (Test-Path -LiteralPath $CopilotSrc -PathType Leaf)) {
    Write-Err "Missing package file: $CopilotSrc"
}
if (-not (Test-Path -LiteralPath $PromptsSrc -PathType Container)) {
    Write-Err "Missing package directory: $PromptsSrc"
}
if (-not (Test-Path -LiteralPath $TemplatesSrc -PathType Container)) {
    Write-Err "Missing package directory: $TemplatesSrc"
}
if (-not (Test-Path -LiteralPath $TargetDir -PathType Container)) {
    Write-Err "Current working directory is not a directory: $TargetDir"
}

Write-Host "Project root:  $TargetDir"
Write-Host "Skills dir:    $SkillsDirResolved"
Write-Host "Package root:  $PackageRoot"
Write-Host ''

if ($Claude) {
    Copy-RuleFile -Source $ClaudeSrc -Destination (Join-Path $TargetDir 'AGENTS.md')
}

if ($Copilot) {
    # .github always under project root (CWD)
    $githubDir = Join-Path $TargetDir '.github'
    if (-not (Test-Path -LiteralPath $githubDir)) {
        New-Item -ItemType Directory -Path $githubDir -Force | Out-Null
    }
    Copy-RuleFile -Source $CopilotSrc -Destination (Join-Path $githubDir 'copilot-instructions.md')

    # Slash wrappers → always .github/prompts/ (not under -SkillsDir)
    # Default: primary /govern only (avoid four form-filling slash entries)
    if (-not (Test-Path -LiteralPath $CopilotWrappersSrc -PathType Container)) {
        Write-Err "Missing package directory: $CopilotWrappersSrc"
    }
    $promptsDir = Join-Path $githubDir 'prompts'
    if (-not (Test-Path -LiteralPath $promptsDir)) {
        New-Item -ItemType Directory -Path $promptsDir -Force | Out-Null
    }
    $wrapperNames = @('govern')
    if ($WithPrimitives) {
        $wrapperNames += @('new-goal', 'log-decision', 'update-execution', 'write-audit')
        Write-Host 'Including advanced primitive slash wrappers (-WithPrimitives)'
    } else {
        Write-Host 'Copilot slash surface: /govern only (pass -WithPrimitives for advanced form ops)'
    }
    foreach ($name in $wrapperNames) {
        Copy-RuleFile `
            -Source (Join-Path $CopilotWrappersSrc "$name.md") `
            -Destination (Join-Path $promptsDir "$name.prompt.md")
    }
}

if ($installExtras) {
    if (-not (Test-Path -LiteralPath $SkillsDirResolved)) {
        New-Item -ItemType Directory -Path $SkillsDirResolved -Force | Out-Null
    }
    Copy-DirMerge -Source $PromptsSrc -Destination (Join-Path $SkillsDirResolved 'prompts') -Label 'prompts'
    Copy-DirMerge -Source $TemplatesSrc -Destination (Join-Path $SkillsDirResolved 'templates') -Label 'templates'
}

Show-NextSteps -TargetDir $TargetDir -SkillsDir $SkillsDirResolved -PackageRoot $PackageRoot

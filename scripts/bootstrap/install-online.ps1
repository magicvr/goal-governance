# Goal Governance · online / offline bootstrap installer (GOAL-023)
#
# Entry point 1 (bootstrap): obtain skills zip (embedded core) → verify SHA-256
# → materialize ./skills → invoke package-local install.ps1 (default -All).
# Does NOT download core separately; skills zip already embeds core.
#
# Offline / air-gap:
#   .\install-online.ps1 -Version 0.9.2 -ZipPath .\goal-governance-skills-v0.9.2.zip
# Online (network):
#   .\install-online.ps1 -Version 0.9.2
#
# Package-local install (entry point 2) remains: skills\install.ps1 after extract.

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$Version,

    [string]$TargetDir = '',

    [string]$SkillsDirName = 'skills',

    [string]$ZipPath = '',

    [string]$Sha256Path = '',

    [string]$Repo = 'magicvr/goal-governance',

    [string]$ReleaseTag = '',

    [switch]$SkipInstall,

    [switch]$Force,

    [switch]$Help
)

$ErrorActionPreference = 'Stop'

function Show-Usage {
    @"
Goal Governance bootstrap installer (GOAL-023)

Downloads or uses a local skills zip (core embedded), verifies SHA-256,
extracts to <TargetDir>\<SkillsDirName>, then runs package install -All.

Usage:
  .\install-online.ps1 -Version X.Y.Z [-TargetDir DIR] [-ZipPath PATH] [-Sha256Path PATH]
  .\install-online.ps1 -Version X.Y.Z -ZipPath .\goal-governance-skills-vX.Y.Z.zip   # offline
  .\install-online.ps1 -Version X.Y.Z                                               # online Release

Options:
  -Version        SemVer (optional leading v); archive name uses stripped form
  -TargetDir      Project root (default: current directory)
  -SkillsDirName  Directory name under TargetDir (default: skills)
  -ZipPath        Local skills zip (skip download when set)
  -Sha256Path     Local .sha256 sidecar (default: <ZipPath>.sha256 or beside zip)
  -Repo           GitHub owner/repo for online mode (default: magicvr/goal-governance)
  -ReleaseTag     Tag for download URL (default: v + normalized version)
  -SkipInstall    Only verify + extract; do not run package install
  -Force          Pass -Force to package install (overwrite)
  -Help           Show this help

Default install flags: -All -NonInteractive (-Force when -Force set).
"@
}

if ($Help) {
    Show-Usage
    exit 0
}

function Write-Err([string]$Message) {
    Write-Host "Error: $Message" -ForegroundColor Red
    exit 1
}

function Normalize-Version([string]$Raw) {
    $v = $Raw.Trim()
    if ($v.Length -eq 0) { Write-Err 'Version must be non-empty' }
    if ($v.StartsWith('v') -or $v.StartsWith('V')) { $v = $v.Substring(1) }
    if ($v -notmatch '^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(-[0-9A-Za-z.-]+)?(\+[0-9A-Za-z.-]+)?$') {
        Write-Err "Version must be SemVer-like (got $Raw)"
    }
    return $v
}

function Get-FileSha256Hex([string]$Path) {
    return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
}

function Read-ExpectedDigest {
    param(
        [string]$SidecarPath,
        [string]$ZipBaseName
    )
    if (-not (Test-Path -LiteralPath $SidecarPath -PathType Leaf)) {
        Write-Err "SHA-256 sidecar not found: $SidecarPath"
    }
    $raw = (Get-Content -LiteralPath $SidecarPath -Raw -Encoding utf8).Trim()
    if ($raw -notmatch '^([0-9a-fA-F]{64})[ \t]+(\S+)\s*$') {
        Write-Err "Invalid SHA-256 sidecar format (want '<hex>  <filename>'): $SidecarPath"
    }
    $hex = $Matches[1].ToLowerInvariant()
    $name = $Matches[2]
    $base = [System.IO.Path]::GetFileName($name)
    if ($base -ne $ZipBaseName) {
        Write-Err "Sidecar filename '$name' does not match zip basename '$ZipBaseName'"
    }
    return $hex
}

function Assert-DigestMatch {
    param(
        [string]$ZipFile,
        [string]$SidecarPath
    )
    $zipBase = [System.IO.Path]::GetFileName($ZipFile)
    $expected = Read-ExpectedDigest -SidecarPath $SidecarPath -ZipBaseName $zipBase
    $actual = Get-FileSha256Hex -Path $ZipFile
    if ($actual -ne $expected) {
        Write-Err "SHA-256 mismatch for $zipBase`n  expected: $expected`n  actual:   $actual"
    }
    Write-Host "SHA-256 OK: $zipBase"
}

function Resolve-FullPath([string]$Path, [string]$Base) {
    if ([System.IO.Path]::IsPathRooted($Path)) {
        return [System.IO.Path]::GetFullPath($Path)
    }
    return [System.IO.Path]::GetFullPath((Join-Path $Base $Path))
}

$norm = Normalize-Version $Version
$archiveRoot = "goal-governance-skills-v$norm"
$zipName = "$archiveRoot.zip"
$shaName = "$zipName.sha256"

if (-not $TargetDir) {
    $TargetDir = (Get-Location).Path
}
$TargetDir = [System.IO.Path]::GetFullPath($TargetDir)
if (-not (Test-Path -LiteralPath $TargetDir -PathType Container)) {
    New-Item -ItemType Directory -Path $TargetDir -Force | Out-Null
}

$workDir = Join-Path $TargetDir '.goal-governance-bootstrap-tmp'
if (Test-Path -LiteralPath $workDir) {
    Remove-Item -LiteralPath $workDir -Recurse -Force
}
New-Item -ItemType Directory -Path $workDir -Force | Out-Null

try {
    $localZip = $null
    $localSha = $null

    if ($ZipPath) {
        $localZip = Resolve-FullPath $ZipPath $TargetDir
        if (-not (Test-Path -LiteralPath $localZip -PathType Leaf)) {
            Write-Err "ZipPath not found: $localZip"
        }
        if ($Sha256Path) {
            $localSha = Resolve-FullPath $Sha256Path $TargetDir
        } else {
            $sibling = "$localZip.sha256"
            if (Test-Path -LiteralPath $sibling -PathType Leaf) {
                $localSha = $sibling
            } else {
                $beside = Join-Path (Split-Path -Parent $localZip) $shaName
                if (Test-Path -LiteralPath $beside -PathType Leaf) {
                    $localSha = $beside
                } else {
                    Write-Err "SHA-256 sidecar not found next to zip (pass -Sha256Path)"
                }
            }
        }
        Write-Host "Offline mode: using local zip $localZip"
    } else {
        $tag = if ($ReleaseTag) { $ReleaseTag } else { "v$norm" }
        $baseUrl = "https://github.com/$Repo/releases/download/$tag"
        $localZip = Join-Path $workDir $zipName
        $localSha = Join-Path $workDir $shaName
        Write-Host "Online mode: downloading $baseUrl/$zipName"
        try {
            Invoke-WebRequest -Uri "$baseUrl/$zipName" -OutFile $localZip -UseBasicParsing
            Invoke-WebRequest -Uri "$baseUrl/$shaName" -OutFile $localSha -UseBasicParsing
        } catch {
            Write-Err "Download failed: $_"
        }
    }

    Assert-DigestMatch -ZipFile $localZip -SidecarPath $localSha

    $extractDir = Join-Path $workDir 'extract'
    New-Item -ItemType Directory -Path $extractDir -Force | Out-Null
    Expand-Archive -LiteralPath $localZip -DestinationPath $extractDir -Force

    $packageSrc = Join-Path $extractDir $archiveRoot
    if (-not (Test-Path -LiteralPath $packageSrc -PathType Container)) {
        # Some extractors flatten or nest differently; accept single top-level dir.
        $children = @(Get-ChildItem -LiteralPath $extractDir -Directory)
        if ($children.Count -eq 1) {
            $packageSrc = $children[0].FullName
        } else {
            Write-Err "Expected archive root folder '$archiveRoot' under extract dir"
        }
    }

    $destSkills = Join-Path $TargetDir $SkillsDirName
    if (Test-Path -LiteralPath $destSkills) {
        if (-not $Force) {
            Write-Err "Destination already exists (use -Force to replace): $destSkills"
        }
        Remove-Item -LiteralPath $destSkills -Recurse -Force
    }
    # Copy package into place (preserve install scripts at package root)
    Copy-Item -LiteralPath $packageSrc -Destination $destSkills -Recurse -Force
    Write-Host "Materialized skills package: $destSkills"

    $installPs1 = Join-Path $destSkills 'install.ps1'
    if (-not (Test-Path -LiteralPath $installPs1 -PathType Leaf)) {
        Write-Err "Package install.ps1 missing after extract: $installPs1"
    }

    if ($SkipInstall) {
        Write-Host 'SkipInstall: package extracted; package install not run.'
        exit 0
    }

    $installArgs = @(
        '-NoProfile',
        '-ExecutionPolicy', 'Bypass',
        '-File', $installPs1,
        '-All',
        '-NonInteractive',
        '-SkillsDir', $destSkills
    )
    if ($Force) {
        $installArgs += '-Force'
    }

    Write-Host "Running package install: install.ps1 -All -NonInteractive$(if ($Force) { ' -Force' } else { '' })"
    Push-Location $TargetDir
    try {
        & powershell @installArgs
        if ($LASTEXITCODE -ne 0 -and $null -ne $LASTEXITCODE) {
            Write-Err "Package install failed with exit code $LASTEXITCODE"
        }
    } finally {
        Pop-Location
    }

    Write-Host 'Bootstrap complete.'
    exit 0
} finally {
    if (Test-Path -LiteralPath $workDir) {
        Remove-Item -LiteralPath $workDir -Recurse -Force -ErrorAction SilentlyContinue
    }
}

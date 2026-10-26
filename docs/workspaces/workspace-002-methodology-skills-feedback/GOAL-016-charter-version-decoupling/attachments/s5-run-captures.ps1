# GOAL-016 S5 runtime-evidence recapture for the v0.13.8 candidate.
# Invokes the derived s5-host-probes.py driver per host and writes producer
# envelopes into docs/releases/runtime/v0.13.8/. Not a production runner.
param(
    [Parameter(Mandatory = $true)]
    [ValidateSet('claude', 'grok', 'copilot', 'codex')]
    [string]$HostName,
    [string]$Attempt = '01',
    [string]$NameSuffix = ''
)

# The DSH harness process did not inherit COPILOT_PROVIDER_API_KEY from the user
# scope (it was written to HKCU:\Environment after this process started) while
# BASE_URL/TYPE/MODEL were inherited, so the Copilot CLI saw a provider URL with
# no key and answered HTTP 401 "Invalid API key". Hydrate the provider variables
# the host reads, so each probe runs under the user's actual provider
# configuration instead of a key-less environment. No value is written to disk.
foreach ($name in 'COPILOT_PROVIDER_API_KEY', 'COPILOT_PROVIDER_BASE_URL', 'COPILOT_PROVIDER_TYPE', 'COPILOT_MODEL') {
    if (-not [Environment]::GetEnvironmentVariable($name, 'Process')) {
        $userValue = [Environment]::GetEnvironmentVariable($name, 'User')
        if ($userValue) { [Environment]::SetEnvironmentVariable($name, $userValue, 'Process') }
    }
}

$root = $PSScriptRoot
while (-not (Test-Path (Join-Path $root 'scripts/capture_runtime_evidence.py'))) {
    $root = Split-Path $root -Parent
}
$driver = Join-Path $PSScriptRoot 's5-host-probes.py'
$evidenceDir = Join-Path $root 'docs/releases/runtime/v0.13.8'
New-Item -ItemType Directory -Force -Path $evidenceDir | Out-Null

$cases = if ($HostName -eq 'codex') { @('catalog') } else { @('govern', 'audit', 'vision', 'vision-audit', 'catalog') }
$consumer = @{
    claude  = 'claude-code-cli'
    grok    = 'grok-build-cli'
    copilot = 'github-copilot-cli'
    codex   = 'codex-cli'
}[$HostName]

$results = @()
foreach ($case in $cases) {
    $name = if ($case -eq 'catalog') { "$HostName-mcp-four-entry$NameSuffix" } else { "$consumer-$case-2026-10-26$NameSuffix" }
    $out = Join-Path $evidenceDir "$name.json"
    $argv = @($driver, '--host', $HostName, '--case', $case, '--timeout', '600', '--attempt', $Attempt, '--runtime-evidence', $out)
    if ($HostName -eq 'codex') { $argv += @('--codex-model', 'gpt-6.1-sol') }
    Write-Output "=== $HostName/$case -> $name.json"
    & python @argv 2>&1 | ForEach-Object { Write-Output $_ }
    $results += [pscustomobject]@{ host = $HostName; case = $case; exit = $LASTEXITCODE; evidence = "$name.json" }
}
$results | Format-Table -AutoSize

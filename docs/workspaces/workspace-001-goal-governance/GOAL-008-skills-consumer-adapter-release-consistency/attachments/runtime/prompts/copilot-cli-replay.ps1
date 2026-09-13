$ErrorActionPreference = 'Stop'

$prompt = [Console]::In.ReadToEnd()
$token = gh auth token
if ([string]::IsNullOrWhiteSpace($token)) {
    throw 'gh auth token unavailable'
}
$env:COPILOT_GITHUB_TOKEN = $token

$byokSettings = @(
    'COPILOT_PROVIDER_BASE_URL',
    'COPILOT_PROVIDER_API_KEY',
    'COPILOT_PROVIDER_BEARER_TOKEN',
    'COPILOT_MODEL'
)
foreach ($setting in $byokSettings) {
    if ([string]::IsNullOrWhiteSpace([Environment]::GetEnvironmentVariable($setting, 'Process'))) {
        $userValue = [Environment]::GetEnvironmentVariable($setting, 'User')
        if (-not [string]::IsNullOrWhiteSpace($userValue)) {
            [Environment]::SetEnvironmentVariable($setting, $userValue, 'Process')
        }
    }
}

$copilotArguments = @(
    '-C', '.', '--mode', 'interactive', '--allow-all-tools', '--deny-tool=write',
    '--deny-tool=edit', '--allow-all-paths', '--no-ask-user', '--no-auto-update',
    '--secret-env-vars', 'COPILOT_PROVIDER_API_KEY,COPILOT_PROVIDER_BEARER_TOKEN,COPILOT_GITHUB_TOKEN',
    '--output-format', 'text', '--stream', 'off'
)
# GOAL-008 S6 (2026-09-13): the host's persisted settings.json model and any
# stale session cache can override COPILOT_MODEL, so pass the model explicitly.
# The first positional argument wins; otherwise fall back to COPILOT_MODEL.
$modelOverride = if ($args.Count -ge 1 -and -not [string]::IsNullOrWhiteSpace($args[0])) {
    $args[0]
} elseif (-not [string]::IsNullOrWhiteSpace($env:COPILOT_MODEL)) {
    $env:COPILOT_MODEL
} else {
    $null
}
if ($modelOverride) {
    $copilotArguments += @('--model', $modelOverride)
    Write-Host "copilot replay model: $modelOverride"
}
$copilotArguments += @('-p', $prompt)

& copilot @copilotArguments
exit $LASTEXITCODE

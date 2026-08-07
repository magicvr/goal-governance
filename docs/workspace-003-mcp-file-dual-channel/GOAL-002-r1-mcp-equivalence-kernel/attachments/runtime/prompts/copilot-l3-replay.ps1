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
    '--output-format', 'text', '--stream', 'off', '-p', $prompt
)
if (-not [string]::IsNullOrWhiteSpace($env:COPILOT_MODEL)) {
    $copilotArguments += @('--model', $env:COPILOT_MODEL)
}

& copilot @copilotArguments
exit $LASTEXITCODE

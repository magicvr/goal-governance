$ErrorActionPreference = 'Stop'

$prompt = [Console]::In.ReadToEnd()
$token = gh auth token
if ([string]::IsNullOrWhiteSpace($token)) {
    throw 'gh auth token unavailable'
}
$env:COPILOT_GITHUB_TOKEN = $token

& copilot -C . --mode interactive --allow-all-tools --deny-tool=write --deny-tool=edit --allow-all-paths --no-ask-user --no-auto-update --output-format text --stream off -p $prompt
exit $LASTEXITCODE

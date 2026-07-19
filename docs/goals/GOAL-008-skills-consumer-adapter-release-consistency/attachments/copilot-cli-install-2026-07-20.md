---
title: GitHub Copilot CLI installation evidence
status: active
created: 2026-07-20
updated: 2026-07-20
parent: GOAL-008-skills-consumer-adapter-release-consistency
version: 1.0.0
---

# GitHub Copilot CLI installation evidence

## Commands and results

```text
node --version
v22.17.0

npm --version
10.9.2

npm install -g @github/copilot
added 3 packages

Get-Command copilot
C:\Users\magicvr\AppData\Roaming\npm\copilot.ps1

copilot version
GitHub Copilot CLI 1.0.71
```

`copilot --help` confirmed the non-interactive `-p/--prompt` surface, `--mode`, `--output-format`, and explicit permission controls. The two replay commands use `gh auth token` only within the child process; no token value is recorded here or in runtime evidence.

The current evidence source is the standalone GitHub Copilot CLI. VS Code or an IDE plugin was not used for the GOAL-008 replay.

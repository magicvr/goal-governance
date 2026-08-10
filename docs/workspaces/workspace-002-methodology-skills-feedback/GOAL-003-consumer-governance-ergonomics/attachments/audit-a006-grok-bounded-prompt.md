---
title: A-006 Grok Build bounded finding-closure prompt
status: recorded
created: 2026-08-04
updated: 2026-08-04
parent: GOAL-003-consumer-governance-ergonomics
version: 0.1.0
---

# A-006 bounded independent prompt

## Invocation boundary

- session: `019fc9d5-02ac-7ff2-b8ed-d611cf4f36df`
- CLI: Grok Build `0.2.118` / model `grok-4.5`
- mode: headless single turn, `--always-approve --sandbox read-only`
- cwd: isolated release-verification directory, outside the repository
- disabled: subagents, memory, web search
- system override: read only; do not load Skills, `AGENTS.md`, or unrelated context; use narrow commands; always return a conclusion

The Grok session summary records `sandbox_profile: read-only`, `reasoning_effort: medium`, and `stopReason: end_turn`.

## User prompt

```text
Independently audit only GOAL-003 A-004 F-001 fixed closure. Repository:
C:\Users\magicvr\Documents\Code\goal-governance
Official assets:
C:\Users\magicvr\AppData\Local\Temp\goal-governance-v0.12.0-release-verification-30859281729
Consumer:
C:\Users\magicvr\AppData\Local\Temp\goal-governance-v0.12.0-release-verification-30859281729\consumer-project

Use narrow read-only commands. Do not read AGENTS.md, load /audit skills, dump whole JSON files,
or trust A-005 conclusions. Check A-004, D-010, the annotated remote v0.12.0 tag and peeled
commit 0748c8d8480e7f87f23578b60ec24dc809d6d8d7, Actions run 30859281729, published
Release assets, both zip sidecar hashes, selected release-evidence fields, compatibility
candidate/readiness/uncovered, 12 committed runtime JSON units, updater/README entries and
producer-only exclusions in the official skills zip, then consumer manifest/rollback/updaters/
four host surfaces/contracts/producer-only absence.

The consumer was bootstrapped from the official v0.12.0 zip, then its installed updater ran an
online fixed-version dry-run and real transaction to the formal v0.12.0 Release. The resulting
manifest and rollback directory are on disk. Explicitly judge whether this same-version real
transaction is sufficient for A-004's first-updater-version requirement, without pretending it
is a cross-version upgrade.

Return ONLY one JSON object with keys:
verdict (pass|conditional|fail), f001_status (fixed|open), open_required_count (integer),
same_version_update_sufficient (boolean), same_version_reason (string),
evidence (array of at least 6 objects with gate/status/detail),
findings (array of id/level/status/summary), limitations (array), recommendation (string).
F-002/F-003 are recommended unless new evidence independently justifies otherwise.
Do not decide lifecycle state.
```

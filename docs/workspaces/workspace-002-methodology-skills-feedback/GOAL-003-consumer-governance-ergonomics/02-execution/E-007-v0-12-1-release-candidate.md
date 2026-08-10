---
id: GOAL-003-consumer-governance-ergonomics
doc: execution-entry
record_id: E-007
status: recorded
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-08-04
updated: 2026-08-04
version: 0.1.0
---

# E-007 - v0.12.1 release candidate checkpoint

## Facts

- Started from clean local `dev` commit `e3bcec19a67a0ac7ace2b109f7f814a465368fcb`, 13 commits ahead of `origin/dev`; `origin/dev` and `origin/main` both pointed to `d1e5ae57d133a89bc3b54032cf5e5887d3ad6f94` and no PR was open.
- D-012 selected the A-009/F-001 `fixed` path and patch identity `v0.12.1` without changing GOAL-003 `done / 100%` or any existing finding severity.
- Added the `0.12.1` CHANGELOG section, updated the three pinned installation surfaces, set compatibility `candidateRevision` to `v0.12.1`, and staged the canonical matrix mirror.
- Copied 36 runtime-capture files into `docs/releases/runtime/v0.12.1/`. Their capture time and host facts remain unchanged; the matrix states that they are reused only because the compatibility verifier rechecked unchanged behavior-source and output hashes.
- `python scripts/stage_skills_mirrors.py --check`: 34 pairs matched.
- `python scripts/compatibility_report.py --require-ready`: `ready-for-release-evidence`, uncovered required cells `0`.
- The first rehearsal correctly failed because three tests still pinned `candidateRevision` to `v0.12.0`. Only those release-identity assertions were updated to `v0.12.1`; no coverage or release gate was weakened.
- Final `python scripts/release_evidence.py --mode rehearsal --run-checks --include-web`: `releaseStatus: rehearsal`, `checksPassed: true`, source commit `70ed3559ff53807d59b84925acce8aee4e6a5d81`, candidate `v0.12.1`, coverage ready.
- Full docs suite: 26 tests passed. `git diff --check` passed.

## Checkpoint

`70ed3559ff53807d59b84925acce8aee4e6a5d81` (`release: prepare v0.12.1 candidate`) contains the release identity and candidate evidence. The working tree was clean after the commit.

## Remaining gate

F-001 remains open. Remote `dev` push, PR CI, ordinary merge, post-merge `main` CI, annotated tag, strict evidence, Environment approval, Release creation, and asset digest verification have not yet happened at this record.

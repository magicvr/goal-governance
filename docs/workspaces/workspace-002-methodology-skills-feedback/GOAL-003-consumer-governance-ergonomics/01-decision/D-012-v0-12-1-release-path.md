---
id: GOAL-003-consumer-governance-ergonomics
doc: decision-entry
record_id: D-012
status: accepted
parent: GOAL-001-methodology-skills-feedback-evolution
created: 2026-08-04
updated: 2026-08-04
version: 0.1.0
---

# D-012 - v0.12.1 release path for A-009/F-001

## Trigger

A-009 independently passed GOAL-003 close-out but left F-001 required and open for the next tag/Release only. The user explicitly requested progression through PR, tag, and published Release assets.

## Decision

1. Choose the `fixed` path for F-001 with patch release `v0.12.1`. A patch is appropriate because the post-`v0.12.0` delta is governance, documentation, and release identity work; no minor or major behavior change is claimed.
2. Keep GOAL-003 `done / 100%`, I-001 through I-007 `verified`, and A-004 F-002/F-003 plus the historical Web writer finding `recommended/open`.
3. Integrate the current local `dev` through a normal `dev -> main` PR, PR CI, ordinary merge, and post-merge `main` CI before creating the tag.
4. Freeze `CHANGELOG`, compatibility `candidateRevision`, evidence scope, canonical-to-mirror parity, and the three pinned installation surfaces for `v0.12.1`.
5. Reuse the 2026-08-04 runtime captures only as unchanged-source evidence: the candidate must first pass the compatibility verifier, and any behavior-source hash drift requires fresh runtime capture. The matrix scope must state this boundary explicitly.
6. Create an annotated `v0.12.1` tag on the exact merged `main` commit only after rehearsal passes. Run strict release evidence locally, push the tag only after it passes, approve the `release` Environment, and verify every uploaded asset and digest.

## Gate closure

F-001 remains open until the actual merged commit, tag object, Actions run, Environment approval, GitHub Release, asset inventory, and SHA-256 sidecars are recorded. The eventual response must be appended as a governed A-010 entry; it must not rewrite A-009 or claim that a plan is release evidence.

## Rejected alternative

`merge-only` would be valid for the existing v0.12.0 artifact, but it does not satisfy the user's explicit request for a new tag and Release assets. A new minor or major version is not justified by the current change scope.

"""R-002 FA-001..FA-006 executable negative cases (pure; no workspace I/O)."""

from __future__ import annotations

import unittest

from services.fact_admission import (
    ERR_FA_DIGEST_STALE,
    ERR_FA_MISSING_SOURCE_KIND,
    ERR_FA_MISSING_SOURCE_STATEMENT,
    ERR_FA_RENDER_CANONICAL_UNCONFIRMED,
    ERR_FA_SOURCE_KIND_DISGUISE,
    ERR_FA_SOURCE_KIND_MUTATION,
    CandidateSnapshot,
    RenderItem,
    can_confirm,
    can_request_proposal,
    compute_content_digest,
    validate_confirm_or_proposal,
    validate_content_digest_binding,
    validate_no_source_disguise,
    validate_render_contract,
    validate_source_kind_immutability,
    validate_source_kind_present,
    validate_source_statement_present,
)


def _base_candidate(**kwargs: object) -> CandidateSnapshot:
    content = str(kwargs.pop("content", "User typed an execution fact body."))
    digest = compute_content_digest(content)
    defaults: dict[str, object] = {
        "candidate_id": "cand-001",
        "revision": 1,
        "workspace_id": "workspace-ok-fixture",
        "goal_id": "GOAL-001-fixture-target",
        "source_kind": "user-provided",
        "source_statement": "typed by operator in session",
        "content": content,
        "content_digest": digest,
        "status": "submitted",
    }
    defaults.update(kwargs)
    return CandidateSnapshot(**defaults)  # type: ignore[arg-type]


class FactAdmissionFATests(unittest.TestCase):
    """Evidence: pure-function assertions; no canonical file writes."""

    def test_fa001_missing_source_kind_blocks_confirm_and_proposal(self) -> None:
        cand = _base_candidate(source_kind=None)
        r = validate_source_kind_present(cand)
        self.assertFalse(r.ok)
        self.assertEqual(r.code, ERR_FA_MISSING_SOURCE_KIND)

        digest = cand.content_digest
        gate = validate_confirm_or_proposal(cand, digest)
        self.assertFalse(gate.ok)
        self.assertEqual(gate.code, ERR_FA_MISSING_SOURCE_KIND)
        self.assertFalse(can_confirm(cand, digest))
        self.assertFalse(can_request_proposal(cand, digest))

        empty = _base_candidate(source_kind="  ")
        self.assertEqual(validate_source_kind_present(empty).code, ERR_FA_MISSING_SOURCE_KIND)

    def test_fa002_missing_source_statement_blocks_confirm_and_proposal(self) -> None:
        cand = _base_candidate(source_statement=None)
        r = validate_source_statement_present(cand)
        self.assertFalse(r.ok)
        self.assertEqual(r.code, ERR_FA_MISSING_SOURCE_STATEMENT)

        digest = cand.content_digest
        gate = validate_confirm_or_proposal(cand, digest)
        self.assertFalse(gate.ok)
        self.assertEqual(gate.code, ERR_FA_MISSING_SOURCE_STATEMENT)
        self.assertFalse(can_confirm(cand, digest))
        self.assertFalse(can_request_proposal(cand, digest))

        blank = _base_candidate(source_statement="")
        self.assertEqual(
            validate_source_statement_present(blank).code,
            ERR_FA_MISSING_SOURCE_STATEMENT,
        )

    def test_fa003_ai_origin_disguised_as_user_provided_rejected(self) -> None:
        disguised = _base_candidate(
            source_kind="user-provided",
            produced_by_ai=True,
            tool_call_ids=("tool-search-1",),
            retrieval_refs=("https://example.invalid/doc",),
        )
        r = validate_no_source_disguise(disguised)
        self.assertFalse(r.ok)
        self.assertEqual(r.code, ERR_FA_SOURCE_KIND_DISGUISE)
        self.assertFalse(can_confirm(disguised, disguised.content_digest))
        self.assertFalse(can_request_proposal(disguised, disguised.content_digest))

        honest_user = _base_candidate(source_kind="user-provided", produced_by_ai=False)
        self.assertTrue(validate_no_source_disguise(honest_user).ok)
        self.assertTrue(can_confirm(honest_user, honest_user.content_digest))

        honest_ai = _base_candidate(
            source_kind="ai-retrieval",
            source_statement="retrieved under user consent",
            produced_by_ai=True,
            retrieval_refs=("https://example.invalid/doc",),
        )
        # Not a disguise (kind matches origin); confirm gate still ok at admission layer
        self.assertTrue(validate_no_source_disguise(honest_ai).ok)

    def test_fa004_unconfirmed_candidate_in_canonical_zone_unlabeled(self) -> None:
        bad = (
            RenderItem(
                zone="canonical_fact",
                object_kind="Candidate",
                status="submitted",
                labeled_as_candidate=False,
                content_preview="looks like a fact",
            ),
        )
        r = validate_render_contract(bad)
        self.assertFalse(r.ok)
        self.assertEqual(r.code, ERR_FA_RENDER_CANONICAL_UNCONFIRMED)

        ok_labeled = (
            RenderItem(
                zone="canonical_fact",
                object_kind="Candidate",
                status="submitted",
                labeled_as_candidate=True,
                content_preview="still candidate",
            ),
            RenderItem(
                zone="candidate_panel",
                object_kind="Candidate",
                status="draft",
                labeled_as_candidate=False,
                content_preview="panel ok without label requirement",
            ),
            RenderItem(
                zone="canonical_fact",
                object_kind="CanonicalFact",
                status="confirmed",
                labeled_as_candidate=False,
                content_preview="real fact",
            ),
        )
        self.assertTrue(validate_render_contract(ok_labeled).ok)

        computed_bad = (
            RenderItem(
                zone="canonical_fact",
                object_kind="ComputedView",
                status=None,
                labeled_as_computed=False,
                content_preview="aggregate",
            ),
        )
        self.assertEqual(
            validate_render_contract(computed_bad).code,
            ERR_FA_RENDER_CANONICAL_UNCONFIRMED,
        )

    def test_fa005_stale_digest_after_source_change_rejected(self) -> None:
        original = _base_candidate(content="original statement")
        old_digest = original.content_digest
        changed_content = "statement after source/content change"
        # Confirm still presenting old digest
        r = validate_content_digest_binding(
            original,
            bound_digest=old_digest,
            content_after_source_change=changed_content,
        )
        self.assertFalse(r.ok)
        self.assertEqual(r.code, ERR_FA_DIGEST_STALE)

        new_digest = compute_content_digest(changed_content)
        gate = validate_confirm_or_proposal(
            original.with_mutations(content=changed_content, content_digest=old_digest),
            bound_digest=old_digest,
        )
        self.assertFalse(gate.ok)
        self.assertEqual(gate.code, ERR_FA_DIGEST_STALE)

        # Fresh revision binding passes
        refreshed = original.with_mutations(
            content=changed_content,
            content_digest=new_digest,
            revision=2,
        )
        ok = validate_confirm_or_proposal(refreshed, new_digest)
        self.assertTrue(ok.ok)
        self.assertTrue(can_confirm(refreshed, new_digest))

    def test_fa006_source_kind_mutation_same_revision_after_submit_rejected(self) -> None:
        stored = _base_candidate(source_kind="user-provided", status="submitted", revision=1)
        attempted = stored.with_mutations(source_kind="ai-knowledge")
        r = validate_source_kind_immutability(stored, attempted)
        self.assertFalse(r.ok)
        self.assertEqual(r.code, ERR_FA_SOURCE_KIND_MUTATION)

        # New revision may change kind
        new_rev = attempted.with_mutations(revision=2)
        self.assertTrue(validate_source_kind_immutability(stored, new_rev).ok)

        # Draft still mutable at same revision
        draft = _base_candidate(status="draft", revision=1, source_kind="user-provided")
        draft_edit = draft.with_mutations(source_kind="ai-retrieval")
        self.assertTrue(validate_source_kind_immutability(draft, draft_edit).ok)

    def test_happy_path_user_provided_confirm_allowed(self) -> None:
        cand = _base_candidate()
        r = validate_confirm_or_proposal(cand, cand.content_digest)
        self.assertTrue(r.ok)
        self.assertTrue(can_confirm(cand, cand.content_digest))
        self.assertTrue(can_request_proposal(cand, cand.content_digest))


if __name__ == "__main__":
    unittest.main()

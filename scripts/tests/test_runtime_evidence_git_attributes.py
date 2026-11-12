"""Keep archived JSONL digests stable with Git core.autocrlf enabled."""
from __future__ import annotations
import hashlib
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

REPO_ROOT = Path(os.environ.get("GOAL_GOVERNANCE_SOURCE_ROOT", Path(__file__).resolve().parents[2]))

class RuntimeEvidenceGitAttributesTests(unittest.TestCase):
    @unittest.skipUnless(shutil.which("git"), "git is required for checkout round-trip")
    def test_archived_jsonl_keeps_digest_after_autocrlf_checkout(self):
        with tempfile.TemporaryDirectory(prefix="gg-jsonl-checkout-") as tmp:
            root = Path(tmp).resolve()
            self.assertTrue(root.is_relative_to(Path(tempfile.gettempdir()).resolve()))
            def git(*args):
                return subprocess.check_output(["git", "-c", "core.longpaths=true", "-C", str(root), *args], stderr=subprocess.PIPE)
            git("init")
            for key, value in (("user.name", "Goal Governance Tests"), ("user.email", "tests@example.invalid"), ("core.autocrlf", "true"), ("core.safecrlf", "false"), ("gc.auto", "0")):
                git("config", key, value)
            (root / ".gitattributes").write_bytes((REPO_ROOT / ".gitattributes").read_bytes())
            rels = [
                f"docs/workspaces/workspace-002-methodology-skills-feedback/{goal}/attachments/s3-runtime/checkout-probe/stdout.jsonl"
                for goal in ("GOAL-013-audit-dispatch-and-user-input-gates", "GOAL-018-host-wait-and-audit-config")
            ]
            original = b'{"kind":"synthetic-runtime-evidence","answer":null}\n'
            for rel in rels:
                target = root / rel
                target.parent.mkdir(parents=True)
                target.write_bytes(original)
            git("add", "--", ".gitattributes", *rels)
            git("commit", "-m", "fixture runtime evidence")
            for rel in rels:
                target = root / rel
                self.assertTrue(target.resolve().is_relative_to(root))
                target.unlink()
                git("checkout", "--", rel)
                self.assertEqual(hashlib.sha256(target.read_bytes()).hexdigest(), hashlib.sha256(original).hexdigest())
                self.assertEqual(target.read_bytes(), original)

if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "scripts" / "rebuild_shared_materials_index.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("shared_materials_index", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


indexer = _load_module()


class SharedMaterialsIndexTests(unittest.TestCase):
    def test_repository_skeleton_is_an_empty_candidate_inventory(self) -> None:
        index = json.loads(
            (REPO_ROOT / "docs" / "shared-materials" / "index.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(index["format"], "goal-governance.shared-materials-inventory")
        self.assertTrue(index["inventoryOnly"])
        self.assertEqual(index["files"], [])

    def _materials_dir(self, root: Path) -> Path:
        directory = root / "docs" / "shared-materials"
        directory.mkdir(parents=True)
        return directory

    def test_rebuilds_sorted_candidate_inventory_with_hashes(self) -> None:
        with tempfile.TemporaryDirectory(prefix="gg-material-index-") as tmp:
            materials = self._materials_dir(Path(tmp))
            (materials / "zeta.txt").write_text("zeta", encoding="utf-8")
            nested = materials / "nested"
            nested.mkdir()
            (nested / "alpha.bin").write_bytes(b"\x00\x01")

            payload = indexer.rebuild_index(materials)
            index = json.loads((materials / "index.json").read_text(encoding="utf-8"))

        expected_hash = hashlib.sha256(b"\x00\x01").hexdigest()
        self.assertEqual(payload, index)
        self.assertTrue(index["inventoryOnly"])
        self.assertEqual(
            index["files"],
            [
                {"path": "nested/alpha.bin", "sizeBytes": 2, "sha256": expected_hash},
                {
                    "path": "zeta.txt",
                    "sizeBytes": 4,
                    "sha256": hashlib.sha256(b"zeta").hexdigest(),
                },
            ],
        )

    def test_rebuild_is_stable_and_ignores_root_control_files(self) -> None:
        with tempfile.TemporaryDirectory(prefix="gg-material-index-") as tmp:
            materials = self._materials_dir(Path(tmp))
            (materials / "README.md").write_text("control", encoding="utf-8")
            (materials / ".gitkeep").write_text("", encoding="utf-8")
            cache = materials / "__pycache__"
            cache.mkdir()
            (cache / "cache.pyc").write_bytes(b"cache")
            (materials / "material.txt").write_text("material", encoding="utf-8")

            indexer.rebuild_index(materials)
            first = (materials / "index.json").read_bytes()
            indexer.rebuild_index(materials)
            second = (materials / "index.json").read_bytes()

        self.assertEqual(first, second)
        self.assertEqual(["material.txt"], [item["path"] for item in json.loads(first)["files"]])

    def test_rejects_output_outside_the_materials_root(self) -> None:
        with tempfile.TemporaryDirectory(prefix="gg-material-index-") as tmp:
            root = Path(tmp)
            materials = self._materials_dir(root)
            with self.assertRaisesRegex(indexer.IndexBuildError, "must stay inside"):
                indexer.build_inventory(materials, root / "outside.json")

    def test_cli_rebuilds_a_repository_relative_directory(self) -> None:
        with tempfile.TemporaryDirectory(prefix="gg-material-index-") as tmp:
            root = Path(tmp)
            materials = self._materials_dir(root)
            (materials / "manual.txt").write_text("copied", encoding="utf-8")
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--repo-root",
                    str(root),
                ],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )

            index = json.loads((materials / "index.json").read_text(encoding="utf-8"))

        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertIn("1 candidate file", result.stdout)
        self.assertEqual(index["files"][0]["path"], "manual.txt")

    def test_rejects_symbolic_links_when_supported(self) -> None:
        with tempfile.TemporaryDirectory(prefix="gg-material-index-") as tmp:
            materials = self._materials_dir(Path(tmp))
            target = materials / "target.txt"
            target.write_text("target", encoding="utf-8")
            link = materials / "link.txt"
            try:
                link.symlink_to(target)
            except OSError:
                self.skipTest("symbolic links require unavailable Windows privileges")

            with self.assertRaisesRegex(indexer.IndexBuildError, "symbolic links"):
                indexer.rebuild_index(materials)


if __name__ == "__main__":
    unittest.main()

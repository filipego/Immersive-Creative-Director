#!/usr/bin/env python3

import json
import subprocess
import sys
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("validate_visual_corpus.py")
SKILL_ROOT = SCRIPT.parent.parent
EXPECTED_REFERENCES = {
    "site-sondaven",
    "site-lando-norris",
    "site-indigo-laboratory",
    "site-noth",
    "site-mr-black",
    "site-santioni-spirits",
    "site-become-a-yogi",
    "site-mesh3d",
    "site-haoqi",
    "site-ride-radian",
    "site-pear",
}


class VisualCorpusValidationTests(unittest.TestCase):
    def test_installed_corpus_is_complete_and_decodable(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), str(SKILL_ROOT)],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

        manifest_path = SKILL_ROOT / "assets" / "visual-taste-corpus" / "manifest.json"
        manifest = json.loads(manifest_path.read_text())
        self.assertEqual(
            {reference["id"] for reference in manifest["references"]},
            EXPECTED_REFERENCES,
        )
        self.assertEqual(manifest["frameCount"], 321)
        strip_root = SKILL_ROOT / "assets" / "visual-taste-corpus" / "motion-strips"
        self.assertEqual(
            {path.stem for path in strip_root.glob("*.jpg")},
            EXPECTED_REFERENCES,
        )

    def test_entrypoint_makes_visual_grounding_blocking(self):
        entrypoint = (SKILL_ROOT / "SKILL.md").read_text()
        self.assertIn("visual-reference-manifest.md", entrypoint)
        self.assertIn("motion-reference-manifest.md", entrypoint)
        self.assertIn("validate_visual_corpus.py", entrypoint)
        self.assertIn("view_image", entrypoint)
        self.assertIn("Visual Grounding Ledger", entrypoint)

    def test_discovery_persists_each_evidence_class(self):
        discovery = (SKILL_ROOT / "references" / "evolving-the-library.md").read_text()
        self.assertIn("assets/visual-taste-corpus/", discovery)
        self.assertIn("assets/process-corpus/transcripts/", discovery)
        self.assertIn("validate_process_corpus.py", discovery)
        self.assertNotIn(
            "The evidence record belongs outside this runtime reference",
            discovery,
        )


if __name__ == "__main__":
    unittest.main()

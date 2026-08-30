#!/usr/bin/env python3

import hashlib
import json
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).parent.parent
WEBSITE_IDS = {
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
VIDEO_IDS = {
    "video-QUI6Ug4cHnE",
    "video-39IlNR-P3-Q",
    "video-GJxchJkk4Lk",
    "video-ubH1ulaK-t4",
}


class CorpusSeparationTests(unittest.TestCase):
    def test_visual_taste_manifest_contains_only_websites(self):
        manifest = json.loads(
            (SKILL_ROOT / "assets" / "visual-taste-corpus" / "manifest.json").read_text()
        )
        self.assertEqual(
            {reference["id"] for reference in manifest["references"]},
            WEBSITE_IDS,
        )
        self.assertEqual(manifest["frameCount"], 321)

    def test_process_manifest_contains_four_transcripts(self):
        manifest = json.loads(
            (SKILL_ROOT / "assets" / "process-corpus" / "manifest.json").read_text()
        )
        self.assertEqual(
            {reference["id"] for reference in manifest["references"]},
            VIDEO_IDS,
        )
        for reference in manifest["references"]:
            transcript = SKILL_ROOT / "assets" / "process-corpus" / reference["transcript"]
            self.assertTrue(transcript.is_file(), transcript)
            self.assertGreater(transcript.stat().st_size, 1_000)
            data = transcript.read_bytes()
            self.assertEqual(reference["transcriptBytes"], len(data))
            self.assertEqual(reference["transcriptSha256"], hashlib.sha256(data).hexdigest())

    def test_entrypoint_assigns_distinct_authority(self):
        entrypoint = (SKILL_ROOT / "SKILL.md").read_text()
        self.assertIn("11 mandatory website overview sheets", entrypoint)
        self.assertIn("Process Evidence Ledger", entrypoint)
        self.assertIn("process-reference-manifest.md", entrypoint)
        self.assertNotIn("all 15 mandatory overview sheets", entrypoint)

    def test_video_frames_cannot_supply_visual_taste(self):
        process_manifest = (
            SKILL_ROOT / "references" / "process-reference-manifest.md"
        ).read_text()
        self.assertIn("zero visual-taste authority", process_manifest)
        self.assertIn("transcripts are the source evidence", process_manifest)

    def test_live_animation_requests_reopen_stored_website_urls(self):
        manifest = json.loads(
            (SKILL_ROOT / "assets" / "visual-taste-corpus" / "manifest.json").read_text()
        )
        self.assertTrue(all(item["source"].startswith("https://") for item in manifest["references"]))
        orchestration = (SKILL_ROOT / "references" / "orchestration.md").read_text()
        self.assertIn("double-check the live animation", orchestration)
        self.assertIn("stored frames support composition but never claim live timing", orchestration)

    def test_every_website_has_written_motion_analysis(self):
        corpus = (SKILL_ROOT / "references" / "reference-corpus.md").read_text()
        self.assertGreaterEqual(corpus.count("Motion grammar and input mapping:"), 11)
        for reference_id in WEBSITE_IDS:
            self.assertIn(reference_id, corpus)


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3

import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).parent.parent


class ScrollcraftRoutingTests(unittest.TestCase):
    def test_scrollcraft_is_primary_scroll_motion_specialist(self):
        orchestration = (SKILL_ROOT / "references" / "orchestration.md").read_text()
        self.assertIn("primary scroll-motion specialist", orchestration)
        self.assertIn("Direction and Transformation", orchestration)
        self.assertIn("feeling curve", orchestration)
        self.assertIn("grammar", orchestration)
        self.assertIn("signature move", orchestration)
        self.assertIn("scroll score", orchestration)

    def test_direction_uses_planning_without_crossing_production_gate(self):
        orchestration = (SKILL_ROOT / "references" / "orchestration.md").read_text()
        self.assertIn("deferred at Scrollcraft Step 3", orchestration)
        self.assertIn("Production resumes Scrollcraft at Step 3", orchestration)
        self.assertNotIn("defer Scrollcraft’s build workflow", orchestration)


if __name__ == "__main__":
    unittest.main()

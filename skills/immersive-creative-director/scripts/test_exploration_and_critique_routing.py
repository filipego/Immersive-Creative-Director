import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ExplorationAndCritiqueRoutingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.orchestration = (ROOT / "references" / "orchestration.md").read_text(encoding="utf-8")
        cls.dependencies = (ROOT / "references" / "dependencies.md").read_text(encoding="utf-8")
        cls.visual_development = (ROOT / "references" / "visual-development.md").read_text(encoding="utf-8")
        cls.motion = (ROOT / "references" / "motion-vocabulary.md").read_text(encoding="utf-8")
        cls.quality = (ROOT / "references" / "quality-gates.md").read_text(encoding="utf-8")

    def test_prototype_is_conditional_and_question_led(self):
        combined = self.orchestration + self.dependencies + self.visual_development
        self.assertIn("Prototype", combined)
        self.assertIn("unresolved design question", combined)
        self.assertIn("named divergence axis", combined)
        self.assertIn("throwaway", combined)

    def test_motion_records_operational_behavior(self):
        for field in ("trigger frequency", "interruptibility", "reversal", "exit behavior"):
            self.assertIn(field, self.motion.lower())

    def test_quality_gates_include_subtraction_and_dual_lens_critique(self):
        self.assertIn("QUALITY-intensity-subtraction", self.quality)
        self.assertIn("creative-direction lens", self.quality)
        self.assertIn("visitor-experience lens", self.quality)
        self.assertIn("highest-leverage correction", self.quality)


if __name__ == "__main__":
    unittest.main()

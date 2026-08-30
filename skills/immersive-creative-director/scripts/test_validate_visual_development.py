import json
import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("validate_visual_development.py")


def valid_manifest():
    roles = ["opening", "quiet-editorial", "peak", "decision-utility", "resolution"]
    return {
        "visualDevelopmentId": "VISDEV-test",
        "version": 1,
        "contractId": "CONTRACT-test",
        "contractVersion": 1,
        "territoryId": "TERRITORY-1",
        "status": "approved",
        "system": {
            "grid": "12-column stage with route-specific editorial variants",
            "spacingRhythm": "subject-derived sparse/dense cadence",
            "typographyRoles": ["display", "reading", "utility"],
            "colorMaterialLaw": "one project material changes function across modes",
            "imageryTreatment": "truthful source imagery with explicit crop relationships",
            "motionLaw": "state change prepares the next responsibility",
            "soundPolicy": "silent parity; sound only if later approved",
            "verdict": "strong",
        },
        "styleFrames": [
            {"id": f"STYLE-{i}", "role": role, "stateIds": [f"STATE-{i}"], "desktopEvidence": f"/tmp/{i}-desktop.png", "mobileEvidence": f"/tmp/{i}-mobile.png", "compositionJob": f"{role} composition", "verdict": "strong"}
            for i, role in enumerate(roles, 1)
        ],
        "motionStudy": {
            "id": "MOTION-STUDY-1",
            "fromStateId": "STATE-3", "toStateId": "STATE-4",
            "whyRepresentative": "highest-risk transition and signature move",
            "evidence": "/tmp/motion-study.mp4",
            "desktopInspected": True, "mobileInspected": True,
            "reducedMotionInspected": True, "reversalInspected": True,
            "verdict": "strong",
        },
        "approval": {"completeBoardApproved": True, "approvalEvidence": "User approved VISDEV-test v1"},
        "reconciliation": {"missingRoles": [], "blockers": [], "verdict": "strong"},
    }


class VisualDevelopmentValidatorTests(unittest.TestCase):
    def run_validator(self, payload):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "visual.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            return subprocess.run(["python3", str(SCRIPT), str(path)], capture_output=True, text=True)

    def test_complete_visual_development_passes(self):
        result = self.run_validator(valid_manifest())
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_missing_quiet_state_fails(self):
        payload = valid_manifest()
        payload["styleFrames"] = [x for x in payload["styleFrames"] if x["role"] != "quiet-editorial"]
        result = self.run_validator(payload)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("quiet-editorial", result.stdout)

    def test_motion_study_is_mandatory(self):
        payload = valid_manifest()
        payload["motionStudy"] = {}
        result = self.run_validator(payload)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("motionStudy", result.stdout)


if __name__ == "__main__":
    unittest.main()

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("validate_performance_budget.py")


def valid_budget():
    return {
        "performanceBudgetId": "PERF-test", "version": 1,
        "targetSurfaces": [
            {"id": "desktop", "viewport": "1440x900", "input": "wheel/trackpad", "deviceClass": "current laptop"},
            {"id": "mobile", "viewport": "390x844", "input": "touch", "deviceClass": "mid-range phone"},
        ],
        "budgets": {
            "initialTransferBytes": 3000000, "initialHeavyMediaBytes": 1500000,
            "largestSingleAssetBytes": 500000, "maximumConcurrentVideoDecoders": 1,
            "minimumAnimationFps": 45, "maximumLongTaskMs": 100,
            "maximumLayoutShift": 0.1, "memoryRiskCeiling": "one active chapter plus prefetch neighbor",
        },
        "loadingStrategy": "poster-first, explicit readiness, adjacent-only prefetch",
        "responsiveAssetStrategy": "separate mobile crops and media variants",
        "lowPowerFallback": "approved key-state sequence with semantic controls",
        "noWebglFallback": "DOM/SVG or approved still-state route",
        "reducedMotionRoute": "opening-to-resolution state parity",
        "failureRecovery": "show truthful approved state and keep navigation/conversion working",
        "measurementPlan": ["cold load", "warm load", "scroll chronology", "memory", "fallback"],
        "approvalEvidence": "Project-specific budget approved",
        "verdict": "strong",
    }


class PerformanceBudgetValidatorTests(unittest.TestCase):
    def run_validator(self, payload):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "performance.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            return subprocess.run(["python3", str(SCRIPT), str(path)], capture_output=True, text=True)

    def test_complete_budget_passes(self):
        result = self.run_validator(valid_budget())
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_missing_mobile_target_fails(self):
        payload = valid_budget()
        payload["targetSurfaces"] = payload["targetSurfaces"][:1]
        result = self.run_validator(payload)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("mobile", result.stdout)

    def test_zero_budget_fails(self):
        payload = valid_budget()
        payload["budgets"]["initialTransferBytes"] = 0
        result = self.run_validator(payload)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("initialTransferBytes", result.stdout)


if __name__ == "__main__":
    unittest.main()

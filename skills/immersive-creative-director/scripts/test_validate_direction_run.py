import json
import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("validate_direction_run.py")


def valid_run():
    return {
        "runId": "IMMERSIVE-RUN-test",
        "version": 1,
        "mode": "direction",
        "status": "concept-ready",
        "corpusGrounding": {
            "coreFilesAtEof": [
                "orchestration.md", "preferences.md", "experience-contract.md",
                "evidence-library.md", "visual-reference-manifest.md", "motion-reference-manifest.md",
                "process-reference-manifest.md", "reference-corpus.md", "doctrine.md",
                "motion-vocabulary.md", "production.md", "previsualization.md",
                "quality-gates.md", "evolving-the-library.md",
                "execution-contract.md", "scrollcraft-adapter.md",
                "visual-development.md", "performance-budget.md", "dependencies.md",
            ],
            "visualOverviewIds": [
                "site-sondaven", "site-lando-norris", "site-indigo-laboratory",
                "site-noth", "site-mr-black", "site-santioni-spirits",
                "site-become-a-yogi", "site-mesh3d", "site-haoqi",
                "site-ride-radian", "site-pear",
            ],
            "processIds": [
                "video-QUI6Ug4cHnE", "video-39IlNR-P3-Q",
                "video-GJxchJkk4Lk", "video-ubH1ulaK-t4",
            ],
            "visualValidatorEvidence": "PASS at 2026-08-30T12:00:00Z",
            "processValidatorEvidence": "PASS at 2026-08-30T12:00:00Z",
            "verdict": "strong",
        },
        "intake": {
            "grillingComplete": True,
            "domainModelingComplete": True,
            "frontierEmpty": True,
            "rounds": [
                {
                    "round": 1,
                    "questions": [
                        {
                            "id": "Q1",
                            "decision": "subject and audience",
                            "prerequisites": [],
                            "allPrerequisitesSettledBeforeRound": True,
                            "answered": True,
                        }
                    ],
                    "agentEndedTurnAndWaited": True,
                    "domainModelingEvidence": "Terms and edge cases challenged",
                },
                {
                    "round": 2,
                    "questions": [
                        {
                            "id": "Q2",
                            "decision": "belief and action",
                            "prerequisites": ["Q1"],
                            "allPrerequisitesSettledBeforeRound": True,
                            "answered": True,
                        }
                    ],
                    "agentEndedTurnAndWaited": True,
                    "domainModelingEvidence": "Resolved subject language applied",
                },
            ],
            "userConfirmationEvidence": "User confirmed shared understanding",
            "verdict": "strong",
        },
        "experienceContract": {
            "id": "CONTRACT-test", "version": 1,
            "path": "/tmp/IMMERSIVE-EXPERIENCE-CONTRACT.json",
            "validatorEvidence": "PASS", "verdict": "strong",
        },
        "evidenceLineage": [
            {
                "territoryId": f"TERRITORY-{i}",
                "websiteEvidenceIds": ["EVID-site-pear", "EVID-site-son-daven"],
                "mechanismFamilies": ["causal-object-state", "material-law"],
                "processEvidenceIds": ["EVID-video-reference-transfer"],
                "surfaceExclusion": "No copied palette, imagery, type, or exact choreography",
                "subjectOwnership": "The project-specific subject verbs determine the synthesis",
                "verdict": "strong",
            }
            for i in range(1, 4)
        ],
        "territories": [
            {"id": "TERRITORY-1", "disposition": "survivor", "coherenceSource": "material-law", "journey": ["opening", "proof", "resolution"], "verdict": "strong"},
            {"id": "TERRITORY-2", "disposition": "survivor", "coherenceSource": "subject-relationship", "journey": ["opening", "proof", "resolution"], "verdict": "strong"},
            {"id": "TERRITORY-3", "disposition": "rejected", "coherenceSource": "route-process", "journey": ["opening", "proof", "resolution"], "rejectionReason": "Least subject-specific", "verdict": "reject"},
        ],
        "recommendedTerritoryId": "TERRITORY-1",
        "scrollcraft": {
            "applicable": True,
            "adapterApplied": True,
            "journeyBeats": ["opening", "proof", "resolution"],
            "feelingCurve": ["curiosity", "confidence", "resolve"],
            "peak": "Proof becomes environment",
            "grammar": "subject-derived causal passage",
            "signatureMove": "The real process object changes role across proof states",
            "scrollScore": ["orient", "transform", "release"],
            "inputContract": "reversible bounded authored scroll with normal-flow relief",
            "responsivePlan": "mobile is re-composed, not cropped",
            "reducedMotionParity": "same state order and content meaning",
            "verdict": "strong",
        },
        "visualDevelopment": {"required": True, "manifestPath": "pending", "validatorEvidence": "pending", "verdict": "pending"},
        "performanceBudget": {"requiredBeforeBuild": True, "manifestPath": "pending", "validatorEvidence": "pending", "verdict": "pending"},
        "dependencies": {"manifestPath": "references/dependencies.md", "compatibilityChecked": True, "validatorEvidence": "PASS", "verdict": "strong"},
        "qualityGates": [{"id": gate, "evidence": "direct project evidence", "verdict": "strong"} for gate in [
            "QUALITY-corpus-authority", "QUALITY-protocol-compliance", "QUALITY-source-lock",
            "QUALITY-route-integrity", "QUALITY-content-coverage", "QUALITY-state-storyboard",
            "QUALITY-contract-validation", "QUALITY-protected-kernel", "QUALITY-subject-specificity",
            "QUALITY-transplantation", "QUALITY-coherence-source", "QUALITY-story-causality",
            "QUALITY-motion-necessity", "QUALITY-composition", "QUALITY-agency-orientation",
            "QUALITY-whole-site", "QUALITY-peak-resolution",
        ]],
        "reconciliation": {"blockers": [], "missingArtifacts": [], "verdict": "strong"},
    }


class DirectionRunValidatorTests(unittest.TestCase):
    def run_validator(self, payload, phase="concept"):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "run.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            return subprocess.run(["python3", str(SCRIPT), str(path), "--phase", phase], capture_output=True, text=True)

    def test_valid_concept_run_passes(self):
        result = self.run_validator(valid_run())
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("PASS", result.stdout)

    def test_missing_intake_confirmation_fails(self):
        payload = valid_run()
        payload["intake"]["userConfirmationEvidence"] = ""
        result = self.run_validator(payload)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("userConfirmationEvidence", result.stdout)

    def test_dependent_question_in_same_round_fails(self):
        payload = valid_run()
        payload["intake"]["rounds"][0]["questions"].append({
            "id": "Q2",
            "decision": "belief and action",
            "prerequisites": ["Q1"],
            "allPrerequisitesSettledBeforeRound": False,
            "answered": True,
        })
        result = self.run_validator(payload)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("allPrerequisitesSettledBeforeRound", result.stdout)

    def test_weak_reference_lineage_fails(self):
        payload = valid_run()
        payload["evidenceLineage"][0]["mechanismFamilies"] = ["causal-object-state"]
        result = self.run_validator(payload)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("mechanismFamilies", result.stdout)

    def test_experience_contract_requires_validator_evidence(self):
        payload = valid_run()
        payload["experienceContract"]["validatorEvidence"] = ""
        result = self.run_validator(payload)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("experienceContract.validatorEvidence", result.stdout)

    def test_scrollcraft_requires_adapter(self):
        payload = valid_run()
        payload["scrollcraft"]["adapterApplied"] = False
        result = self.run_validator(payload)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("adapterApplied", result.stdout)

    def test_visual_phase_requires_manifest(self):
        result = self.run_validator(valid_run(), "visual-development")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("visualDevelopment.manifestPath", result.stdout)

    def test_build_phase_requires_linked_validator_evidence(self):
        payload = valid_run()
        payload["visualDevelopment"] = {"required": True, "manifestPath": "/tmp/visual.json", "validatorEvidence": "PASS", "verdict": "strong"}
        payload["performanceBudget"] = {"requiredBeforeBuild": True, "manifestPath": "/tmp/perf.json", "validatorEvidence": "", "verdict": "strong"}
        result = self.run_validator(payload, "build")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("performanceBudget.validatorEvidence", result.stdout)


if __name__ == "__main__":
    unittest.main()

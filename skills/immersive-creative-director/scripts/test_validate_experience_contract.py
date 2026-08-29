#!/usr/bin/env python3

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("validate_experience_contract.py")


def valid_contract():
    parity = {
        "desktop": "Full composition",
        "mobile": "Re-art-directed composition",
        "reducedMotion": "Ordered static states",
        "fallback": "Semantic content remains reachable",
    }
    return {
        "contractId": "CONTRACT-test-surface",
        "version": 1,
        "status": "approval-candidate",
        "previsualization": {
            "required": False,
            "reason": "This fixture uses no continuity-dependent generated motion",
            "motionDependencies": [
                {
                    "id": "MOTION-DEPENDENCY-opening-proof",
                    "method": "none",
                    "generated": False,
                    "fromStateId": "STATE-opening",
                    "toStateId": "STATE-proof",
                    "shotIds": [],
                    "authority": "Approved survivor causal handoff",
                },
                {
                    "id": "MOTION-DEPENDENCY-proof-resolution",
                    "method": "semantic-dom-svg",
                    "generated": False,
                    "fromStateId": "STATE-proof",
                    "toStateId": "STATE-resolution",
                    "shotIds": [],
                    "authority": "Approved survivor causal handoff",
                },
            ],
            "contractStateIds": [],
            "manifestId": "not-applicable",
            "verdict": "strong",
        },
        "canonicalScope": {
            "target": "Complete target experience",
            "sourceEvidence": ["source.md#required-surface"],
            "focusLens": "whole-experience",
            "approvalTarget": "Complete target experience direction",
            "sourceSnapshot": ["source.md@v1", "current-surface@2026-08-29"],
            "amendments": [],
        },
        "routes": [
            {
                "id": "ROUTE-primary",
                "kind": "route",
                "destination": "/example",
                "navigationCopyId": "COPY-primary-navigation",
                "visitorJob": "Reach the required experience",
                "authority": "source.md#routes",
                "status": "required",
                "entryHandoff": "Primary navigation",
                "states": ["default", "active"],
                "verdict": "strong",
            }
        ],
        "copy": [
            {
                "id": "COPY-primary-navigation",
                "text": "Primary",
                "provenance": "live copy",
                "authority": "https://example.com/ navigation inspected 2026-08-29",
                "authorityType": "live-source",
                "transformation": "verbatim",
                "uses": [
                    "ROUTE-primary",
                    "RESP-required-content-a",
                    "STATE-opening",
                    "STATE-proof",
                    "STATE-resolution",
                ],
                "verdict": "strong",
            }
        ],
        "responsibilities": [
            {
                "id": "RESP-required-content-a",
                "obligation": "Present required content item A",
                "authority": "source.md#required-content",
                "truthState": "Verified current required content item A",
                "routeIds": ["ROUTE-primary"],
                "stateIds": ["STATE-opening", "STATE-proof", "STATE-resolution"],
                "reachability": "Visible at load",
                "parity": parity,
                "copyIds": ["COPY-primary-navigation"],
                "assetIds": ["ASSET-primary"],
                "required": True,
                "verdict": "strong",
            }
        ],
        "storyboards": [
            {
                "territoryId": "TERRITORY-one",
                "survivor": True,
                "coverage": "opening-to-resolution",
                "states": [
                    {
                        "id": "STATE-opening",
                        "order": 1,
                        "routeId": "ROUTE-primary",
                        "mode": "opening",
                        "responsibilityIds": ["RESP-required-content-a"],
                        "copyIds": ["COPY-primary-navigation"],
                        "assetIds": ["ASSET-primary"],
                        "startComposition": "Required content item A in immediate focus",
                        "inputCause": "load",
                        "transformation": "The opening establishes the required content and visitor purpose",
                        "endComposition": "Required content and premise remain legible",
                        "causalHandoff": "STATE-proof",
                        "agency": "Native scroll and chapter access",
                        "parity": parity,
                        "verdict": "strong",
                    },
                    {
                        "id": "STATE-proof",
                        "order": 2,
                        "routeId": "ROUTE-primary",
                        "mode": "proof",
                        "responsibilityIds": ["RESP-required-content-a"],
                        "copyIds": ["COPY-primary-navigation"],
                        "assetIds": ["ASSET-primary"],
                        "startComposition": "Opening premise remains as invariant",
                        "inputCause": "scroll",
                        "transformation": "Verified evidence changes the meaning of the premise",
                        "endComposition": "Evidence becomes primary focus",
                        "causalHandoff": "STATE-resolution",
                        "agency": "Reversible native scroll",
                        "parity": parity,
                        "verdict": "strong",
                    },
                    {
                        "id": "STATE-resolution",
                        "order": 3,
                        "routeId": "ROUTE-primary",
                        "mode": "resolution",
                        "responsibilityIds": ["RESP-required-content-a"],
                        "copyIds": ["COPY-primary-navigation"],
                        "assetIds": ["ASSET-primary"],
                        "startComposition": "Proof releases into decision",
                        "inputCause": "scroll",
                        "transformation": "The opening promise resolves into a clear next action",
                        "endComposition": "Resolution and route handoff are stable",
                        "causalHandoff": "terminal",
                        "agency": "Direct navigation remains available",
                        "parity": parity,
                        "verdict": "strong",
                    },
                ],
            }
        ],
        "reconciliation": {
            "obligationCount": 1,
            "mappedCount": 1,
            "unmappedIds": [],
            "inventedIds": [],
            "unresolvedIds": [],
            "routeCount": 1,
            "storyboardStateCount": 3,
            "placeholderCount": 0,
            "blockers": [],
            "exclusions": [],
        },
    }


def run_validator(contract, phase="approval"):
    with tempfile.TemporaryDirectory() as temp_dir:
        contract_path = Path(temp_dir) / "contract.json"
        contract_path.write_text(json.dumps(contract), encoding="utf-8")
        return subprocess.run(
            [sys.executable, str(SCRIPT), str(contract_path), "--phase", phase],
            capture_output=True,
            text=True,
            check=False,
        )


class ExperienceContractValidatorTests(unittest.TestCase):
    def test_accepts_complete_approval_candidate(self):
        result = run_validator(valid_contract())
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("PASS", result.stdout)

    def test_rejects_unmapped_atomic_responsibility(self):
        contract = valid_contract()
        contract["responsibilities"][0]["stateIds"] = []
        contract["reconciliation"]["mappedCount"] = 0
        contract["reconciliation"]["unmappedIds"] = ["RESP-required-content-a"]
        result = run_validator(contract)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("RESP-required-content-a", result.stdout)

    def test_rejects_internal_strategy_as_public_copy(self):
        contract = valid_contract()
        contract["copy"][0]["provenance"] = "approved new copy"
        contract["copy"][0]["authorityType"] = "internal-strategy"
        contract["copy"][0]["authority"] = "internal-notes.md#draft-language"
        result = run_validator(contract)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("explicit-user-approval", result.stdout)

    def test_accepts_asset_only_states_and_responsibilities_without_copy(self):
        contract = valid_contract()
        contract["responsibilities"][0]["copyIds"] = []
        for state in contract["storyboards"][0]["states"]:
            state["copyIds"] = []
        contract["copy"][0]["uses"] = ["ROUTE-primary"]
        result = run_validator(contract)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_rejects_partial_storyboard_that_omits_required_content(self):
        contract = valid_contract()
        contract["responsibilities"].append(
            {
                "id": "RESP-required-content-b",
                "obligation": "Keep required content item B directly reachable",
                "authority": "source.md#required-content",
                "truthState": "Verified current required content item B",
                "routeIds": ["ROUTE-primary"],
                "stateIds": [],
                "reachability": "Unassigned",
                "parity": contract["responsibilities"][0]["parity"],
                "copyIds": [],
                "assetIds": [],
                "required": True,
                "verdict": "needs work",
            }
        )
        contract["reconciliation"].update(
            obligationCount=2,
            mappedCount=1,
            unmappedIds=["RESP-required-content-b"],
        )
        result = run_validator(contract)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("RESP-required-content-b", result.stdout)

    def test_build_phase_rejects_placeholders(self):
        contract = valid_contract()
        contract["status"] = "approved"
        contract["copy"][0].update(
            text="[PLACEHOLDER] Navigation label",
            provenance="placeholder",
            authorityType="placeholder",
            authority="Awaiting content approval",
        )
        contract["reconciliation"]["placeholderCount"] = 1
        result = run_validator(contract, phase="build")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("placeholder", result.stdout.lower())

    def test_build_rejects_required_previsualization_without_manifest(self):
        contract = valid_contract()
        contract["status"] = "approved"
        contract["previsualization"] = {
            "required": True,
            "reason": "Approved concept requires connected generated motion",
            "motionDependencies": [
                {
                    "id": "MOTION-DEPENDENCY-opening-proof",
                    "method": "short-clip",
                    "generated": True,
                    "fromStateId": "STATE-opening",
                    "toStateId": "STATE-proof",
                    "shotIds": ["SHOT-opening-proof"],
                    "authority": "Approved survivor storyboard and motion plan",
                },
                {
                    "id": "MOTION-DEPENDENCY-proof-resolution",
                    "method": "short-clip",
                    "generated": True,
                    "fromStateId": "STATE-proof",
                    "toStateId": "STATE-resolution",
                    "shotIds": ["SHOT-proof-resolution"],
                    "authority": "Approved survivor storyboard and motion plan",
                },
            ],
            "contractStateIds": ["STATE-opening", "STATE-proof", "STATE-resolution"],
            "manifestId": "pending",
            "verdict": "needs work",
        }
        result = run_validator(contract, phase="build")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("previsualization", result.stdout.lower())

    def test_rejects_false_not_applicable_claim_for_connected_generated_motion(self):
        contract = valid_contract()
        contract["previsualization"]["motionDependencies"] = [
            {
                "id": "MOTION-DEPENDENCY-opening-proof",
                "method": "long-video",
                "generated": True,
                "fromStateId": "STATE-opening",
                "toStateId": "STATE-proof",
                "shotIds": ["SHOT-opening-proof"],
                "authority": "Survivor storyboard requires connected generated video",
            },
            {
                "id": "MOTION-DEPENDENCY-proof-resolution",
                "method": "none",
                "generated": False,
                "fromStateId": "STATE-proof",
                "toStateId": "STATE-resolution",
                "shotIds": [],
                "authority": "Approved survivor causal handoff",
            },
        ]
        result = run_validator(contract)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("computed connected generated-motion", result.stdout)

    def test_rejects_previsualization_state_from_rejected_territory(self):
        contract = valid_contract()
        contract["storyboards"].append(
            {
                "territoryId": "TERRITORY-rejected",
                "survivor": False,
                "coverage": "opening-to-resolution",
                "states": [{"id": "STATE-rejected", "order": 1}],
            }
        )
        contract["previsualization"] = {
            "required": True,
            "reason": "Invalidly points at a rejected territory",
            "motionDependencies": [
                {
                    "id": "MOTION-DEPENDENCY-opening-rejected",
                    "method": "short-clip",
                    "generated": True,
                    "fromStateId": "STATE-opening",
                    "toStateId": "STATE-rejected",
                    "shotIds": ["SHOT-opening-rejected"],
                    "authority": "Rejected territory",
                },
                {
                    "id": "MOTION-DEPENDENCY-proof-resolution",
                    "method": "none",
                    "generated": False,
                    "fromStateId": "STATE-proof",
                    "toStateId": "STATE-resolution",
                    "shotIds": [],
                    "authority": "Approved survivor causal handoff",
                },
            ],
            "contractStateIds": ["STATE-opening", "STATE-rejected"],
            "manifestId": "pending",
            "verdict": "needs work",
        }
        result = run_validator(contract)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unknown survivor STATE-ID STATE-rejected", result.stdout)


if __name__ == "__main__":
    unittest.main()

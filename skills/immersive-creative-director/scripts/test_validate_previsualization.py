#!/usr/bin/env python3

import copy
import binascii
import hashlib
import json
import struct
import subprocess
import sys
import tempfile
import unittest
import zlib
from pathlib import Path

from test_validate_experience_contract import valid_contract as valid_experience_contract


SCRIPT = Path(__file__).with_name("validate_previsualization.py")
EXPERIENCE_SCRIPT = Path(__file__).with_name("validate_experience_contract.py")
CONTRACT_STATE_IDS = ["STATE-opening", "STATE-proof", "STATE-resolution"]


def png_bytes(rgb):
    def chunk(kind, payload):
        return (
            struct.pack(">I", len(payload))
            + kind
            + payload
            + struct.pack(">I", binascii.crc32(kind + payload) & 0xFFFFFFFF)
        )

    header = struct.pack(">IIBBBBB", 1, 1, 8, 2, 0, 0, 0)
    pixels = zlib.compress(b"\x00" + bytes(rgb))
    return b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", header) + chunk(b"IDAT", pixels) + chunk(b"IEND", b"")


def responsive(asset_id):
    return {
        "desktop": {
            "method": "same-asset-verified",
            "assetId": asset_id,
            "visualEvidence": {
                "type": "local-file",
                "locator": f"__TEMP__/responsive/{asset_id}-desktop.png",
                "mediaType": "image/png",
                "inspectedAt": "2026-08-29T12:10:00-04:00",
            },
            "inspectionEvidence": "Desktop framing inspected at target viewport",
            "meaningPreserved": True,
        },
        "mobile": {
            "method": "separate-asset",
            "assetId": f"{asset_id}-mobile",
            "visualEvidence": {
                "type": "local-file",
                "locator": f"__TEMP__/responsive/{asset_id}-mobile.png",
                "mediaType": "image/png",
                "inspectedAt": "2026-08-29T12:15:00-04:00",
            },
            "inspectionEvidence": "Mobile framing inspected; subject, action, and copy-safe area preserved",
            "meaningPreserved": True,
        },
    }


def state(state_id, order):
    asset_id = f"ASSET-previs-{order}"
    return {
        "id": state_id,
        "order": order,
        "contractStateIds": [CONTRACT_STATE_IDS[order]],
        "imageAssetId": asset_id,
        "imageEvidence": {
            "type": "local-file",
            "locator": f"__TEMP__/state-{order}.png",
            "mediaType": "image/png",
            "inspectedAt": "2026-08-29T12:00:00-04:00",
        },
        "sourceAssetIds": ["ASSET-authentic-source"],
        "semanticJob": f"Prove meaningful state {order}",
        "composition": "One authored focal relationship",
        "subjectIdentity": "Canonical subject traits remain unchanged",
        "environmentTopology": "Named spatial relationship remains coherent",
        "camera": "Explicit framing, angle, and distance",
        "lighting": "Locked light direction and grade",
        "copySafe": "Named copy-safe region",
        "responsive": responsive(asset_id),
        "parity": {
            "reducedMotion": "State remains in the ordered static narrative",
            "fallback": "State remains available without heavy media",
        },
        "approvalEvidence": "Explicit state-board approval",
        "verdict": "strong",
    }


def edge(edge_id, from_id, to_id, method="short-clip"):
    external = method in {"short-clip", "long-video"}
    return {
        "id": edge_id,
        "fromStateId": from_id,
        "toStateId": to_id,
        "contractShotIds": [f"SHOT-{edge_id}"],
        "job": "Carry one meaningful state change",
        "action": "Specific subject action between the approved endpoints",
        "camera": "Explicit camera behavior",
        "duration": "4 seconds",
        "exitHold": "Hold the approved end state before release",
        "identityLocks": ["subject geometry", "materials", "light direction"],
        "negativeConstraints": ["no unapproved objects or identity drift"],
        "method": method,
        "externalService": external,
        "provider": "approved-video-provider" if external else "none",
        "responsive": responsive(f"ASSET-edge-{edge_id}"),
        "regenerationBoundary": "Regenerate this edge only; reopen endpoints if either drifts",
        "fallback": "Approved endpoints with a layered transition",
        "outputAssetIds": [],
        "outputEvidence": [],
        "approvalEvidence": "Explicit motion-edge approval",
        "reviewEvidence": {},
        "verdict": "strong",
    }


def valid_contract():
    contract = valid_experience_contract()
    contract.update(
        contractId="CONTRACT-test",
        status="approved",
        previsualization={
            "required": True,
            "reason": "Connected generated motion depends on approved visual endpoints",
            "motionDependencies": [
                {
                    "id": "MOTION-DEPENDENCY-opening-proof",
                    "method": "short-clip",
                    "generated": True,
                    "fromStateId": "STATE-opening",
                    "toStateId": "STATE-proof",
                    "shotIds": ["SHOT-PREVIS-EDGE-00-01"],
                    "authority": "Approved survivor storyboard and motion plan",
                },
                {
                    "id": "MOTION-DEPENDENCY-proof-resolution",
                    "method": "short-clip",
                    "generated": True,
                    "fromStateId": "STATE-proof",
                    "toStateId": "STATE-resolution",
                    "shotIds": ["SHOT-PREVIS-EDGE-01-02"],
                    "authority": "Approved survivor storyboard and motion plan",
                },
            ],
            "contractStateIds": CONTRACT_STATE_IDS,
            "manifestId": "PREVIS-test",
            "verdict": "strong",
        },
    )
    return contract


def valid_manifest(status="motion-approved"):
    states = [
        state("PREVIS-STATE-00", 0),
        state("PREVIS-STATE-01", 1),
        state("PREVIS-STATE-02", 2),
    ]
    edges = [
        edge("PREVIS-EDGE-00-01", "PREVIS-STATE-00", "PREVIS-STATE-01"),
        edge("PREVIS-EDGE-01-02", "PREVIS-STATE-01", "PREVIS-STATE-02"),
    ]
    return {
        "previsualizationId": "PREVIS-test",
        "version": 1,
        "contractId": "CONTRACT-test",
        "contractVersion": 1,
        "status": status,
        "continuityScope": {
            "required": True,
            "reason": "Generated motion depends on a recurring subject and connected scene states",
            "topology": "linear",
            "sourceSnapshot": ["approved-contract@v1", "authentic-assets@v1"],
            "contractStateIds": CONTRACT_STATE_IDS,
            "contactSheetEvidence": {
                "type": "local-file",
                "locator": "__TEMP__/contact-sheet.png",
                "mediaType": "image/png",
                "inspectedAt": "2026-08-29T12:00:00-04:00",
            },
            "requiredEdgePairs": [
                "PREVIS-STATE-00->PREVIS-STATE-01",
                "PREVIS-STATE-01->PREVIS-STATE-02",
            ],
        },
        "sourceLock": {
            "sourceMode": "authentic-reference",
            "authenticSourceIds": ["ASSET-authentic-source"],
            "anchorStateId": "PREVIS-STATE-00",
            "fixedTraits": ["subject identity", "geometry", "material language"],
            "variableTraits": ["approved pose and camera distance"],
            "invalidTraits": ["identity drift", "invented features"],
            "approvalEvidence": "Explicit canonical-source approval",
            "verdict": "strong",
        },
        "states": states,
        "edges": edges,
        "approval": {
            "conceptApproved": True,
            "stillGenerationAuthorized": True,
            "stateBoardApproved": True,
            "providerDecision": "approved",
            "approvedProviders": ["approved-video-provider"],
            "mediaApproved": True,
            "mediaApprovalEvidence": "Explicit named-provider and media approval",
            "approvalEvidence": ["Explicit state-board approval"],
            "costCeiling": {
                "unit": "credits",
                "limit": 20,
                "description": "Maximum total provider credits for approved edges",
            },
            "regenerationLimit": 2,
        },
        "reconciliation": {
            "stateCount": 3,
            "edgeCount": 2,
            "expectedEdgeCount": 2,
            "unmappedContractStateIds": [],
            "missingEdgePairs": [],
            "unapprovedStateIds": [],
            "unapprovedEdgeIds": [],
            "blockers": [],
        },
    }


def prepare_build(manifest):
    manifest["status"] = "assembled"
    for motion_edge in manifest["edges"]:
        motion_edge["outputAssetIds"] = [f"ASSET-output-{motion_edge['id']}"]
        motion_edge["outputEvidence"] = [
            {
                "type": "local-file",
                "locator": f"__TEMP__/outputs/{motion_edge['id']}.mp4",
                "mediaType": "video/mp4",
                "inspectedAt": "2026-08-29T13:00:00-04:00",
            }
        ]
        motion_edge["reviewEvidence"] = {
            moment: {
                "type": "local-file",
                "locator": f"__TEMP__/review/{motion_edge['id']}-{moment}.png",
                "mediaType": "image/png",
                "inspectedAt": "2026-08-29T13:05:00-04:00",
            }
            for moment in ("firstFrame", "intermediate", "lastFrame", "handoff")
        }


def run_validator(manifest, phase="motion", contract=None, *, entrypoint="previsualization"):
    manifest = copy.deepcopy(manifest)
    contract = copy.deepcopy(contract or valid_contract())
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        fixtures = {
            "contact-sheet.png": (255, 255, 255),
            "state-0.png": (255, 0, 0),
            "state-1.png": (0, 255, 0),
            "state-2.png": (0, 0, 255),
        }
        for name, rgb in fixtures.items():
            (temp_path / name).write_bytes(png_bytes(rgb))
        (temp_path / "not-media.png").write_bytes(b"this is plain text")

        def resolve(value):
            if isinstance(value, dict):
                return {key: resolve(item) for key, item in value.items()}
            if isinstance(value, list):
                return [resolve(item) for item in value]
            if isinstance(value, str):
                return value.replace("__TEMP__", str(temp_path))
            return value

        manifest = resolve(manifest)

        def evidence_records(value):
            if isinstance(value, dict):
                if {"type", "locator", "mediaType", "inspectedAt"}.issubset(value):
                    yield value
                for item in value.values():
                    yield from evidence_records(item)
            elif isinstance(value, list):
                for item in value:
                    yield from evidence_records(item)

        for evidence in evidence_records(manifest):
            evidence_path = Path(evidence["locator"])
            if evidence_path.exists() or not any(
                part in evidence_path.parts for part in ("responsive", "outputs", "review")
            ):
                continue
            evidence_path.parent.mkdir(parents=True, exist_ok=True)
            if evidence["mediaType"] == "image/png":
                digest = hashlib.sha256(str(evidence_path).encode()).digest()
                evidence_path.write_bytes(png_bytes(digest[:3]))
            elif evidence["mediaType"] == "video/mp4":
                subprocess.run(
                    [
                        "ffmpeg",
                        "-loglevel",
                        "error",
                        "-f",
                        "lavfi",
                        "-i",
                        "color=c=black:s=16x16:d=0.08",
                        "-pix_fmt",
                        "yuv420p",
                        "-y",
                        str(evidence_path),
                    ],
                    check=True,
                )

        manifest_path = temp_path / "previsualization.json"
        contract_path = temp_path / "experience-contract.json"
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        contract_path.write_text(json.dumps(contract), encoding="utf-8")
        if entrypoint == "experience":
            command = [
                sys.executable,
                str(EXPERIENCE_SCRIPT),
                str(contract_path),
                "--previsualization",
                str(manifest_path),
                "--phase",
                phase,
            ]
        else:
            command = [
                sys.executable,
                str(SCRIPT),
                str(manifest_path),
                "--contract",
                str(contract_path),
                "--phase",
                phase,
            ]
        return subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
        )


class PrevisualizationValidatorTests(unittest.TestCase):
    def test_accepts_approved_state_board_before_motion_planning(self):
        manifest = valid_manifest(status="state-board-approved")
        manifest["edges"] = []
        manifest["approval"].update(
            providerDecision="pending",
            approvedProviders=[],
            mediaApproved=False,
            mediaApprovalEvidence="",
            costCeiling={
                "unit": "pending",
                "limit": 0,
                "description": "Set only after edge methods are approved",
            },
            regenerationLimit=0,
        )
        manifest["reconciliation"].update(edgeCount=0)
        result = run_validator(manifest, phase="state-board")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("PASS", result.stdout)

    def test_rejects_missing_visual_evidence_file(self):
        manifest = valid_manifest(status="state-board-approved")
        manifest["states"][1]["imageEvidence"]["locator"] = "__TEMP__/missing.png"
        result = run_validator(manifest, phase="state-board")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("does not exist", result.stdout)

    def test_rejects_non_media_bytes_disguised_as_image(self):
        manifest = valid_manifest(status="state-board-approved")
        manifest["states"][1]["imageEvidence"]["locator"] = "__TEMP__/not-media.png"
        result = run_validator(manifest, phase="state-board")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("not a recognized media file", result.stdout)

    def test_rejects_reused_visual_file_or_collapsed_contract_states(self):
        manifest = valid_manifest(status="state-board-approved")
        manifest["states"][1]["imageEvidence"]["locator"] = manifest["states"][0][
            "imageEvidence"
        ]["locator"]
        manifest["states"][0]["contractStateIds"] = ["STATE-opening", "STATE-proof"]
        manifest["states"][1]["contractStateIds"] = ["STATE-proof"]
        result = run_validator(manifest, phase="state-board")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("map exactly one", result.stdout)
        self.assertIn("distinct visual file", result.stdout)

    def test_rejects_one_state_zero_edge_bypass(self):
        manifest = valid_manifest(status="state-board-approved")
        manifest["states"] = manifest["states"][:1]
        manifest["edges"] = []
        manifest["continuityScope"]["requiredEdgePairs"] = []
        manifest["reconciliation"].update(
            stateCount=1,
            edgeCount=0,
            expectedEdgeCount=0,
            unmappedContractStateIds=["STATE-1", "STATE-2"],
        )
        result = run_validator(manifest, phase="state-board")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("at least two visual endpoints", result.stdout)

    def test_rejects_motion_plan_that_skips_adjacent_pair(self):
        manifest = valid_manifest()
        manifest["edges"] = [manifest["edges"][1]]
        manifest["reconciliation"].update(
            edgeCount=1,
            missingEdgePairs=["PREVIS-STATE-00->PREVIS-STATE-01"],
        )
        result = run_validator(manifest, phase="motion")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("PREVIS-STATE-00->PREVIS-STATE-01", result.stdout)

    def test_rejects_contract_version_or_state_mismatch(self):
        manifest = valid_manifest()
        contract = valid_contract()
        contract["version"] = 2
        contract["previsualization"]["contractStateIds"] = ["STATE-0", "STATE-1"]
        result = run_validator(manifest, contract=contract)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("contractVersion", result.stdout)
        self.assertIn("must exactly match", result.stdout)

    def test_rejects_swapped_contract_state_chronology(self):
        manifest = valid_manifest()
        manifest["states"][0]["contractStateIds"] = ["STATE-proof"]
        manifest["states"][1]["contractStateIds"] = ["STATE-opening"]
        result = run_validator(manifest, phase="motion")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("maps to unapproved contract handoff", result.stdout)

    def test_rejects_edge_method_or_shot_drift_from_contract(self):
        manifest = valid_manifest()
        manifest["edges"][0]["method"] = "layered-stills"
        manifest["edges"][0]["externalService"] = False
        manifest["edges"][0]["provider"] = "none"
        manifest["edges"][1]["contractShotIds"] = ["SHOT-invented"]
        result = run_validator(manifest, phase="motion")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("expected approved contract method short-clip", result.stdout)
        self.assertIn("must exactly match governing contract SHOT-IDs", result.stdout)

    def test_rejects_video_without_named_approved_provider_and_media_evidence(self):
        manifest = valid_manifest()
        manifest["edges"][0]["provider"] = "whatever"
        manifest["approval"].update(
            providerDecision="pending",
            approvedProviders=[],
            mediaApproved=False,
            mediaApprovalEvidence="",
            regenerationLimit=0,
        )
        result = run_validator(manifest, phase="motion")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("provider", result.stdout.lower())
        self.assertIn("mediaApprovalEvidence", result.stdout)
        self.assertIn("regenerationLimit", result.stdout)

    def test_rejects_untyped_cost_or_regeneration_approval(self):
        manifest = valid_manifest()
        manifest["approval"]["costCeiling"]["limit"] = "about twenty"
        manifest["approval"]["regenerationLimit"] = "as many as needed"
        result = run_validator(manifest, phase="motion")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("costCeiling.limit", result.stdout)
        self.assertIn("regenerationLimit", result.stdout)

    def test_rejects_placeholder_provider_and_approval_payload(self):
        manifest = valid_manifest()
        manifest["edges"][0]["provider"] = "."
        manifest["approval"]["approvedProviders"] = ["."]
        manifest["approval"]["mediaApprovalEvidence"] = "."
        manifest["approval"]["costCeiling"] = {
            "unit": "other",
            "limit": 0,
            "description": ".",
        }
        result = run_validator(manifest, phase="motion")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("invalid named provider", result.stdout)
        self.assertIn("mediaApprovalEvidence", result.stdout)
        self.assertIn("costCeiling.description", result.stdout)

    def test_accepts_provider_free_layered_still_edges(self):
        manifest = valid_manifest()
        contract = valid_contract()
        for motion_edge in manifest["edges"]:
            motion_edge.update(
                method="layered-stills",
                externalService=False,
                provider="none",
            )
        for dependency in contract["previsualization"]["motionDependencies"]:
            dependency["method"] = "layered-stills"
        manifest["approval"].update(
            providerDecision="not-required",
            approvedProviders=[],
            mediaApproved=False,
            mediaApprovalEvidence="",
            costCeiling={
                "unit": "included-plan",
                "limit": 0,
                "description": "No external paid media service",
            },
            regenerationLimit=0,
        )
        result = run_validator(manifest, phase="motion", contract=contract)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_accepts_original_generated_world_without_authentic_source_ids(self):
        manifest = valid_manifest()
        manifest["sourceLock"].update(
            sourceMode="original-generated-world",
            authenticSourceIds=[],
        )
        for visual_state in manifest["states"]:
            visual_state["sourceAssetIds"] = []
        result = run_validator(manifest, phase="motion")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_motion_phase_accepts_outputs_and_review_as_pending(self):
        manifest = valid_manifest()
        result = run_validator(manifest, phase="motion")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_build_rejects_unreviewed_or_missing_motion_output(self):
        manifest = valid_manifest()
        prepare_build(manifest)
        manifest["edges"][0]["outputAssetIds"] = []
        manifest["edges"][0]["outputEvidence"] = []
        manifest["edges"][0]["reviewEvidence"] = {}
        result = run_validator(manifest, phase="build")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("outputAssetIds", result.stdout)
        self.assertIn("reviewEvidence", result.stdout)

    def test_accepts_fully_evidenced_build_manifest(self):
        manifest = valid_manifest()
        prepare_build(manifest)
        result = run_validator(manifest, phase="build")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_experience_contract_build_loads_valid_linked_manifest(self):
        manifest = valid_manifest()
        prepare_build(manifest)
        result = run_validator(
            manifest,
            phase="build",
            entrypoint="experience",
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_rejects_unproved_mobile_meaning(self):
        manifest = valid_manifest()
        manifest["edges"][0]["responsive"]["mobile"].update(
            method="same-asset-verified",
            inspectionEvidence="CSS crop will be checked later",
            meaningPreserved=False,
        )
        result = run_validator(manifest, phase="motion")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("meaningPreserved", result.stdout)

    def test_rejects_duplicate_or_orphan_branch_pairs(self):
        manifest = valid_manifest()
        manifest["continuityScope"].update(
            topology="branching",
            requiredEdgePairs=[
                "PREVIS-STATE-00->PREVIS-STATE-01",
                "PREVIS-STATE-00->PREVIS-STATE-01",
            ],
        )
        manifest["edges"] = manifest["edges"][:1]
        manifest["reconciliation"].update(
            edgeCount=1,
            expectedEdgeCount=2,
            missingEdgePairs=[],
        )
        result = run_validator(manifest, phase="motion")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("duplicate transition pair", result.stdout)
        self.assertIn("orphan states", result.stdout)

    def test_rejects_branch_edges_that_only_flow_into_anchor_sink(self):
        manifest = valid_manifest()
        manifest["continuityScope"].update(
            topology="branching",
            requiredEdgePairs=[
                "PREVIS-STATE-01->PREVIS-STATE-00",
                "PREVIS-STATE-02->PREVIS-STATE-00",
            ],
        )
        manifest["edges"] = [
            edge("PREVIS-EDGE-01-00", "PREVIS-STATE-01", "PREVIS-STATE-00"),
            edge("PREVIS-EDGE-02-00", "PREVIS-STATE-02", "PREVIS-STATE-00"),
        ]
        result = run_validator(manifest, phase="motion")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("branching graph is disconnected", result.stdout)


if __name__ == "__main__":
    unittest.main()

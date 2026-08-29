#!/usr/bin/env python3

"""Validate a still-first previsualization manifest against its approved contract.

The validator proves contract linkage, visual-state evidence, transition coverage,
approval boundaries, responsive evidence, and build outputs. It cannot decide
whether the assets are beautiful; the skill's qualitative gates own that judgment.
"""

import argparse
import binascii
import hashlib
import json
import re
import shutil
import subprocess
import struct
import sys
import zlib
from datetime import datetime
from pathlib import Path
from xml.etree import ElementTree

from validate_experience_contract import validate_contract


STATUSES = {"exploration", "state-board-approved", "motion-approved", "assembled"}
TOPOLOGIES = {"linear", "branching"}
VERDICTS = {"strong", "needs work", "reject"}
SOURCE_MODES = {"authentic-reference", "original-generated-world", "canonical-model"}
METHODS = {
    "layered-stills",
    "image-sequence",
    "short-clip",
    "long-video",
    "3d",
    "procedural",
    "existing-authentic-video",
}
VIDEO_METHODS = {"short-clip", "long-video"}
EVIDENCE_TYPES = {"local-file"}
RESPONSIVE_METHODS = {
    "separate-asset",
    "same-asset-verified",
    "procedural-reflow",
}
RESERVED_PROVIDERS = {"", "none", "pending", "tbd", "whatever", "any", "unnamed"}
COST_UNITS = {"USD", "credits", "included-plan", "other", "pending"}
APPROVAL_DECISIONS = {"pending", "approved", "not-required"}
MEDIA_TYPES = {
    "image/png",
    "image/jpeg",
    "image/gif",
    "image/webp",
    "image/avif",
    "image/svg+xml",
    "video/mp4",
    "video/webm",
    "video/quicktime",
}
WEAK_TEXT = {".", "..", "...", "pending", "tbd", "todo", "later", "unknown", "none"}


def present(value):
    return isinstance(value, str) and bool(value.strip())


def substantive(value):
    return (
        present(value)
        and value.strip().casefold() not in WEAK_TEXT
        and len(value.strip()) >= 12
    )


def valid_timestamp(value):
    if not present(value):
        return False
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return parsed.tzinfo is not None


def detected_media_type(path):
    try:
        data = path.read_bytes()[:1024]
    except OSError:
        return None
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        return "image/png"
    if data.startswith(b"\xff\xd8\xff"):
        return "image/jpeg"
    if data.startswith((b"GIF87a", b"GIF89a")):
        return "image/gif"
    if data.startswith(b"RIFF") and data[8:12] == b"WEBP":
        return "image/webp"
    if data.startswith(b"\x1aE\xdf\xa3"):
        return "video/webm"
    if len(data) >= 12 and data[4:8] == b"ftyp":
        brand = data[8:12]
        if brand in {b"avif", b"avis"}:
            return "image/avif"
        if brand == b"qt  ":
            return "video/quicktime"
        return "video/mp4"
    stripped = data.lstrip()
    if stripped.startswith(b"<svg") or (
        stripped.startswith(b"<?xml") and b"<svg" in stripped[:512]
    ):
        return "image/svg+xml"
    return None


def decodable_png(data):
    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
        return False
    offset = 8
    saw_ihdr = False
    saw_idat = False
    saw_iend = False
    compressed = bytearray()
    while offset + 12 <= len(data):
        length = struct.unpack(">I", data[offset : offset + 4])[0]
        chunk_type = data[offset + 4 : offset + 8]
        chunk_start = offset + 8
        chunk_end = chunk_start + length
        if chunk_end + 4 > len(data):
            return False
        chunk_data = data[chunk_start:chunk_end]
        expected_crc = struct.unpack(">I", data[chunk_end : chunk_end + 4])[0]
        actual_crc = binascii.crc32(chunk_type + chunk_data) & 0xFFFFFFFF
        if expected_crc != actual_crc:
            return False
        if chunk_type == b"IHDR":
            if saw_ihdr or length != 13:
                return False
            width, height = struct.unpack(">II", chunk_data[:8])
            if width < 1 or height < 1:
                return False
            saw_ihdr = True
        elif chunk_type == b"IDAT":
            saw_idat = True
            compressed.extend(chunk_data)
        elif chunk_type == b"IEND":
            if length != 0:
                return False
            saw_iend = True
            offset = chunk_end + 4
            break
        offset = chunk_end + 4
    if not (saw_ihdr and saw_idat and saw_iend) or offset != len(data):
        return False
    try:
        return bool(zlib.decompress(bytes(compressed)))
    except zlib.error:
        return False


def structurally_decodable(path, media_type):
    try:
        data = path.read_bytes()
    except OSError:
        return False
    if media_type == "image/png":
        return decodable_png(data)
    if media_type == "image/jpeg":
        return data.startswith(b"\xff\xd8\xff") and data.endswith(b"\xff\xd9") and b"\xff\xda" in data
    if media_type == "image/gif":
        return (
            data.startswith((b"GIF87a", b"GIF89a"))
            and len(data) > 14
            and data.endswith(b";")
        )
    if media_type == "image/webp":
        return (
            len(data) >= 20
            and data.startswith(b"RIFF")
            and data[8:12] == b"WEBP"
            and data[12:16] in {b"VP8 ", b"VP8L", b"VP8X"}
        )
    if media_type == "image/avif":
        return len(data) >= 24 and data[4:8] == b"ftyp" and data[8:12] in {b"avif", b"avis"}
    if media_type == "image/svg+xml":
        try:
            root = ElementTree.fromstring(data)
        except ElementTree.ParseError:
            return False
        return root.tag.rsplit("}", 1)[-1] == "svg"
    if media_type.startswith("video/"):
        ffprobe = shutil.which("ffprobe")
        if ffprobe is None:
            return False
        result = subprocess.run(
            [
                ffprobe,
                "-v",
                "error",
                "-select_streams",
                "v:0",
                "-show_entries",
                "stream=codec_type,width,height",
                "-of",
                "json",
                str(path),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            return False
        try:
            streams = json.loads(result.stdout).get("streams", [])
        except json.JSONDecodeError:
            return False
        return any(
            stream.get("codec_type") == "video"
            and stream.get("width", 0) > 0
            and stream.get("height", 0) > 0
            for stream in streams
        )
    return False


def evidence_fingerprint(evidence, base_dir):
    if not isinstance(evidence, dict) or not present(evidence.get("locator")):
        return None
    asset_path = Path(evidence["locator"]).expanduser()
    if not asset_path.is_absolute():
        asset_path = base_dir / asset_path
    if not asset_path.is_file():
        return None
    return "sha256:" + hashlib.sha256(asset_path.read_bytes()).hexdigest()


def valid_provider_name(value):
    if not present(value) or value.strip().casefold() in RESERVED_PROVIDERS:
        return False
    return bool(re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9 ._/-]{1,}", value.strip()))


def require_fields(record, fields, path, errors, *, allow_empty=()):
    if not isinstance(record, dict):
        errors.append(f"{path}: expected an object")
        return
    for field in fields:
        if field not in record:
            errors.append(f"{path}.{field}: missing required field")
        elif (
            field not in allow_empty
            and isinstance(record[field], str)
            and not record[field].strip()
        ):
            errors.append(f"{path}.{field}: must not be empty")


def require_list(record, field, path, errors, *, nonempty=False):
    value = record.get(field) if isinstance(record, dict) else None
    if not isinstance(value, list):
        errors.append(f"{path}.{field}: must be a list")
    elif nonempty and not value:
        errors.append(f"{path}.{field}: must be a non-empty list")


def unique_ids(records, path, errors):
    seen = set()
    for index, record in enumerate(records):
        record_id = record.get("id") if isinstance(record, dict) else None
        if not present(record_id):
            errors.append(f"{path}[{index}].id: missing stable ID")
        elif record_id in seen:
            errors.append(f"{path}[{index}].id: duplicate ID {record_id}")
        else:
            seen.add(record_id)
    return seen


def edge_pair(edge):
    return f"{edge.get('fromStateId')}->{edge.get('toStateId')}"


def parse_pair(pair):
    if not present(pair) or pair.count("->") != 1:
        return None
    start, end = (part.strip() for part in pair.split("->", 1))
    if not start or not end or start == end:
        return None
    return start, end


def validate_evidence(evidence, path, errors, base_dir, *, expected_prefix=None):
    require_fields(evidence, ("type", "locator", "mediaType", "inspectedAt"), path, errors)
    if not isinstance(evidence, dict):
        return
    evidence_type = evidence.get("type")
    locator = evidence.get("locator")
    media_type = evidence.get("mediaType")
    if evidence_type not in EVIDENCE_TYPES:
        errors.append(f"{path}.type: expected one of {sorted(EVIDENCE_TYPES)}")
        return
    if media_type not in MEDIA_TYPES:
        errors.append(f"{path}.mediaType: expected one of {sorted(MEDIA_TYPES)}")
    elif expected_prefix and not media_type.startswith(expected_prefix):
        errors.append(f"{path}.mediaType: expected {expected_prefix} evidence")
    if not valid_timestamp(evidence.get("inspectedAt")):
        errors.append(f"{path}.inspectedAt: must be an ISO-8601 timestamp with timezone")
    if not present(locator):
        return
    if evidence_type == "local-file":
        asset_path = Path(locator).expanduser()
        if not asset_path.is_absolute():
            asset_path = base_dir / asset_path
        if not asset_path.is_file():
            errors.append(f"{path}.locator: local visual evidence file does not exist: {locator}")
        else:
            detected = detected_media_type(asset_path)
            if detected is None:
                errors.append(f"{path}.locator: local evidence is not a recognized media file")
            elif media_type in MEDIA_TYPES and detected != media_type:
                errors.append(
                    f"{path}.mediaType: declared {media_type}, detected {detected}"
                )
            elif media_type in MEDIA_TYPES and not structurally_decodable(asset_path, media_type):
                errors.append(f"{path}.locator: media file is not structurally decodable")


def validate_review_evidence(review, path, errors, base_dir):
    require_fields(
        review,
        ("firstFrame", "intermediate", "lastFrame", "handoff"),
        path,
        errors,
    )
    if not isinstance(review, dict):
        return
    locators = []
    fingerprints = []
    for field in ("firstFrame", "intermediate", "lastFrame", "handoff"):
        evidence = review.get(field)
        validate_evidence(
            evidence,
            f"{path}.{field}",
            errors,
            base_dir,
            expected_prefix="image/",
        )
        if isinstance(evidence, dict) and present(evidence.get("locator")):
            locators.append(evidence["locator"])
        fingerprint = evidence_fingerprint(evidence, base_dir)
        if fingerprint:
            fingerprints.append(fingerprint)
    if len(locators) != len(set(locators)):
        errors.append(f"{path}: first/intermediate/last/handoff need distinct visual evidence")
    if len(fingerprints) != len(set(fingerprints)):
        errors.append(f"{path}: first/intermediate/last/handoff need distinct visual content")


def validate_responsive(responsive, path, errors, base_dir, *, primary_asset_id=None):
    if not isinstance(responsive, dict):
        errors.append(f"{path}: expected responsive object")
        return
    for viewport in ("desktop", "mobile"):
        treatment = responsive.get(viewport)
        treatment_path = f"{path}.{viewport}"
        require_fields(
            treatment,
            (
                "method",
                "assetId",
                "visualEvidence",
                "inspectionEvidence",
                "meaningPreserved",
            ),
            treatment_path,
            errors,
        )
        if not isinstance(treatment, dict):
            continue
        if treatment.get("method") not in RESPONSIVE_METHODS:
            errors.append(
                f"{treatment_path}.method: expected one of {sorted(RESPONSIVE_METHODS)}"
            )
        if not present(treatment.get("assetId")) or not treatment.get("assetId").startswith(
            "ASSET-"
        ):
            errors.append(f"{treatment_path}.assetId: must name an ASSET-* record")
        if not substantive(treatment.get("inspectionEvidence")):
            errors.append(
                f"{treatment_path}.inspectionEvidence: needs substantive direct inspection evidence"
            )
        validate_evidence(
            treatment.get("visualEvidence"),
            f"{treatment_path}.visualEvidence",
            errors,
            base_dir,
            expected_prefix="image/",
        )
        if treatment.get("meaningPreserved") is not True:
            errors.append(
                f"{treatment_path}.meaningPreserved: must be true after direct inspection"
            )
    desktop = responsive.get("desktop") if isinstance(responsive, dict) else None
    mobile = responsive.get("mobile") if isinstance(responsive, dict) else None
    if isinstance(desktop, dict) and primary_asset_id and desktop.get("assetId") != primary_asset_id:
        errors.append(f"{path}.desktop.assetId: must match primary asset {primary_asset_id}")
    if isinstance(desktop, dict) and isinstance(mobile, dict):
        same_asset = mobile.get("method") == "same-asset-verified"
        if same_asset and mobile.get("assetId") != desktop.get("assetId"):
            errors.append(f"{path}.mobile.assetId: same-asset-verified must reuse desktop asset")
        if mobile.get("method") == "separate-asset" and mobile.get("assetId") == desktop.get(
            "assetId"
        ):
            errors.append(f"{path}.mobile.assetId: separate-asset needs a distinct ASSET-ID")
        desktop_fingerprint = evidence_fingerprint(desktop.get("visualEvidence"), base_dir)
        mobile_fingerprint = evidence_fingerprint(mobile.get("visualEvidence"), base_dir)
        if (
            mobile.get("method") == "separate-asset"
            and desktop_fingerprint
            and desktop_fingerprint == mobile_fingerprint
        ):
            errors.append(
                f"{path}.mobile.visualEvidence: separate-asset needs distinct visual content"
            )


def contract_storyboard_state_ids(contract):
    return {
        state.get("id")
        for board in contract.get("storyboards", [])
        if isinstance(board, dict) and board.get("survivor") is True
        for state in board.get("states", [])
        if isinstance(state, dict) and present(state.get("id"))
    }


def validate_contract_link(manifest, contract, errors):
    if not isinstance(contract, dict):
        errors.append("contract: expected an object")
        return set()
    if contract.get("status") != "approved":
        errors.append("contract.status: previsualization requires the approved contract version")
    if manifest.get("contractId") != contract.get("contractId"):
        errors.append("manifest.contractId: does not match linked experience contract")
    if str(manifest.get("contractVersion")) != str(contract.get("version")):
        errors.append("manifest.contractVersion: does not match linked experience contract")

    contract_previs = contract.get("previsualization")
    require_fields(
        contract_previs,
        (
            "required",
            "reason",
            "motionDependencies",
            "contractStateIds",
            "manifestId",
            "verdict",
        ),
        "contract.previsualization",
        errors,
    )
    if not isinstance(contract_previs, dict):
        return set()
    if contract_previs.get("required") is not True:
        errors.append("contract.previsualization.required: must be true for this manifest")
    if contract_previs.get("manifestId") != manifest.get("previsualizationId"):
        errors.append("contract.previsualization.manifestId: does not match manifest ID")
    expected_ids = contract_previs.get("contractStateIds")
    if not isinstance(expected_ids, list) or not expected_ids:
        errors.append("contract.previsualization.contractStateIds: must be a non-empty list")
        return set()
    if len(expected_ids) != len(set(expected_ids)):
        errors.append("contract.previsualization.contractStateIds: duplicate STATE-ID")
    known_ids = contract_storyboard_state_ids(contract)
    for state_id in expected_ids:
        if state_id not in known_ids:
            errors.append(
                f"contract.previsualization.contractStateIds: unknown survivor STATE-ID {state_id}"
            )
    return set(expected_ids)


def validate_manifest(manifest, contract, phase, base_dir):
    errors = []
    require_fields(
        manifest,
        (
            "previsualizationId",
            "version",
            "contractId",
            "contractVersion",
            "status",
            "continuityScope",
            "sourceLock",
            "states",
            "edges",
            "approval",
            "reconciliation",
        ),
        "manifest",
        errors,
    )
    if errors:
        return errors

    if not manifest.get("previsualizationId", "").startswith("PREVIS-"):
        errors.append("manifest.previsualizationId: must use PREVIS-* format")
    if not manifest.get("contractId", "").startswith("CONTRACT-"):
        errors.append("manifest.contractId: must use CONTRACT-* format")

    contract_errors = validate_contract(contract, "build" if phase == "build" else "approval")
    errors.extend(f"linked contract: {error}" for error in contract_errors)
    expected_contract_state_ids = validate_contract_link(manifest, contract, errors)
    status = manifest.get("status")
    if status not in STATUSES:
        errors.append(f"manifest.status: expected one of {sorted(STATUSES)}")
    allowed_statuses = {
        "state-board": {"state-board-approved", "motion-approved", "assembled"},
        "motion": {"motion-approved", "assembled"},
        "build": {"assembled"},
    }
    if status not in allowed_statuses[phase]:
        errors.append(
            f"manifest.status: phase {phase} requires one of {sorted(allowed_statuses[phase])}"
        )

    scope = manifest.get("continuityScope")
    require_fields(
        scope,
        (
            "required",
            "reason",
            "topology",
            "sourceSnapshot",
            "contractStateIds",
            "contactSheetEvidence",
            "requiredEdgePairs",
        ),
        "continuityScope",
        errors,
    )
    if isinstance(scope, dict):
        if scope.get("required") is not True:
            errors.append("continuityScope.required: must be true for this manifest")
        if not substantive(scope.get("reason")):
            errors.append("continuityScope.reason: needs a substantive continuity rationale")
        if scope.get("topology") not in TOPOLOGIES:
            errors.append("continuityScope.topology: expected linear or branching")
        require_list(scope, "sourceSnapshot", "continuityScope", errors, nonempty=True)
        require_list(scope, "contractStateIds", "continuityScope", errors, nonempty=True)
        require_list(scope, "requiredEdgePairs", "continuityScope", errors)
        if set(scope.get("contractStateIds", [])) != expected_contract_state_ids:
            errors.append(
                "continuityScope.contractStateIds: must exactly match the linked contract's "
                "required previsualization STATE-IDs"
            )
        validate_evidence(
            scope.get("contactSheetEvidence"),
            "continuityScope.contactSheetEvidence",
            errors,
            base_dir,
            expected_prefix="image/",
        )

    states = manifest.get("states") if isinstance(manifest.get("states"), list) else []
    edges = manifest.get("edges") if isinstance(manifest.get("edges"), list) else []
    if len(states) < 2:
        errors.append("states: connected generated motion requires at least two visual endpoints")
    state_ids = unique_ids(states, "states", errors)
    unique_ids(edges, "edges", errors)

    orders = []
    mapped_contract_state_ids = set()
    previs_to_contract = {}
    state_evidence_locators = []
    state_evidence_fingerprints = []
    computed_unapproved_states = []
    for index, state in enumerate(states):
        path = f"states[{index}]"
        require_fields(
            state,
            (
                "id",
                "order",
                "contractStateIds",
                "imageAssetId",
                "imageEvidence",
                "sourceAssetIds",
                "semanticJob",
                "composition",
                "subjectIdentity",
                "environmentTopology",
                "camera",
                "lighting",
                "copySafe",
                "responsive",
                "parity",
                "approvalEvidence",
                "verdict",
            ),
            path,
            errors,
        )
        if not isinstance(state, dict):
            continue
        if not state.get("id", "").startswith("PREVIS-STATE-"):
            errors.append(f"{path}.id: must use PREVIS-STATE-* format")
        order = state.get("order")
        if not isinstance(order, int):
            errors.append(f"{path}.order: must be an integer")
        elif order in orders:
            errors.append(f"{path}.order: duplicate order {order}")
        else:
            orders.append(order)
        require_list(state, "contractStateIds", path, errors, nonempty=True)
        require_list(state, "sourceAssetIds", path, errors)
        for asset_id in state.get("sourceAssetIds", []):
            if not present(asset_id) or not asset_id.startswith("ASSET-"):
                errors.append(f"{path}.sourceAssetIds: invalid ASSET-ID {asset_id}")
        if not present(state.get("imageAssetId")) or not state.get("imageAssetId").startswith(
            "ASSET-"
        ):
            errors.append(f"{path}.imageAssetId: must name an ASSET-* record")
        contract_state_ids = state.get("contractStateIds", [])
        if len(contract_state_ids) != 1:
            errors.append(
                f"{path}.contractStateIds: each visual endpoint must map exactly one contract STATE-ID"
            )
        elif present(state.get("id")):
            previs_to_contract[state["id"]] = contract_state_ids[0]
        for state_id in contract_state_ids:
            if state_id in mapped_contract_state_ids:
                errors.append(
                    f"{path}.contractStateIds: duplicate visual mapping for {state_id}"
                )
            mapped_contract_state_ids.add(state_id)
            if state_id not in expected_contract_state_ids:
                errors.append(f"{path}.contractStateIds: unapproved contract STATE-ID {state_id}")
        validate_evidence(
            state.get("imageEvidence"),
            f"{path}.imageEvidence",
            errors,
            base_dir,
            expected_prefix="image/",
        )
        image_evidence = state.get("imageEvidence")
        if isinstance(image_evidence, dict) and present(image_evidence.get("locator")):
            state_evidence_locators.append(image_evidence["locator"])
        fingerprint = evidence_fingerprint(image_evidence, base_dir)
        if fingerprint:
            state_evidence_fingerprints.append(fingerprint)
        validate_responsive(
            state.get("responsive"),
            f"{path}.responsive",
            errors,
            base_dir,
            primary_asset_id=state.get("imageAssetId"),
        )
        parity = state.get("parity")
        require_fields(parity, ("reducedMotion", "fallback"), f"{path}.parity", errors)
        if state.get("verdict") not in VERDICTS:
            errors.append(f"{path}.verdict: invalid verdict")
        if state.get("verdict") != "strong" or not substantive(
            state.get("approvalEvidence")
        ):
            if present(state.get("id")):
                computed_unapproved_states.append(state["id"])

    if len(state_evidence_locators) != len(set(state_evidence_locators)):
        errors.append("states.imageEvidence.locator: every endpoint needs a distinct visual file")
    if len(state_evidence_fingerprints) != len(set(state_evidence_fingerprints)):
        errors.append("states.imageEvidence: every endpoint needs distinct visual content")
    contact_sheet = scope.get("contactSheetEvidence") if isinstance(scope, dict) else None
    if (
        isinstance(contact_sheet, dict)
        and contact_sheet.get("locator") in state_evidence_locators
    ):
        errors.append(
            "continuityScope.contactSheetEvidence.locator: contact sheet must be distinct "
            "from every full-size state asset"
        )
    contact_fingerprint = evidence_fingerprint(contact_sheet, base_dir)
    if contact_fingerprint and contact_fingerprint in state_evidence_fingerprints:
        errors.append(
            "continuityScope.contactSheetEvidence: contact sheet content must differ from "
            "every full-size state asset"
        )

    contract_dependencies = (
        contract.get("previsualization", {}).get("motionDependencies", [])
        if isinstance(contract.get("previsualization"), dict)
        else []
    )
    generated_dependency_by_pair = {
        (dependency.get("fromStateId"), dependency.get("toStateId")): dependency
        for dependency in contract_dependencies
        if isinstance(dependency, dict) and dependency.get("generated") is True
    }

    source_lock = manifest.get("sourceLock")
    require_fields(
        source_lock,
        (
            "sourceMode",
            "authenticSourceIds",
            "anchorStateId",
            "fixedTraits",
            "variableTraits",
            "invalidTraits",
            "approvalEvidence",
            "verdict",
        ),
        "sourceLock",
        errors,
    )
    if isinstance(source_lock, dict):
        source_mode = source_lock.get("sourceMode")
        if source_mode not in SOURCE_MODES:
            errors.append(f"sourceLock.sourceMode: expected one of {sorted(SOURCE_MODES)}")
        require_list(source_lock, "authenticSourceIds", "sourceLock", errors)
        for asset_id in source_lock.get("authenticSourceIds", []):
            if not present(asset_id) or not asset_id.startswith("ASSET-"):
                errors.append(f"sourceLock.authenticSourceIds: invalid ASSET-ID {asset_id}")
        if source_mode == "authentic-reference" and not source_lock.get("authenticSourceIds"):
            errors.append(
                "sourceLock.authenticSourceIds: authentic-reference mode needs inspected sources"
            )
        if source_mode == "authentic-reference":
            authentic_ids = set(source_lock.get("authenticSourceIds", []))
            for index, state in enumerate(states):
                source_ids = set(state.get("sourceAssetIds", [])) if isinstance(state, dict) else set()
                if not source_ids:
                    errors.append(
                        f"states[{index}].sourceAssetIds: authentic-reference state needs source assets"
                    )
                elif not source_ids.intersection(authentic_ids):
                    errors.append(
                        f"states[{index}].sourceAssetIds: must retain at least one authentic source ID"
                    )
        for field in ("fixedTraits", "variableTraits", "invalidTraits"):
            require_list(source_lock, field, "sourceLock", errors, nonempty=True)
        if source_lock.get("anchorStateId") not in state_ids:
            errors.append("sourceLock.anchorStateId: must reference a state-board visual")
        if not substantive(source_lock.get("approvalEvidence")):
            errors.append("sourceLock.approvalEvidence: needs direct substantive approval evidence")
        if source_lock.get("verdict") != "strong":
            errors.append("sourceLock.verdict: canonical source lock must be strong")

    approval = manifest.get("approval")
    require_fields(
        approval,
        (
            "conceptApproved",
            "stillGenerationAuthorized",
            "stateBoardApproved",
            "providerDecision",
            "approvedProviders",
            "mediaApproved",
            "mediaApprovalEvidence",
            "approvalEvidence",
            "costCeiling",
            "regenerationLimit",
        ),
        "approval",
        errors,
        allow_empty=("mediaApprovalEvidence",),
    )
    if isinstance(approval, dict):
        for field in ("conceptApproved", "stillGenerationAuthorized", "stateBoardApproved"):
            if approval.get(field) is not True:
                errors.append(f"approval.{field}: must be true")
        require_list(approval, "approvedProviders", "approval", errors)
        require_list(approval, "approvalEvidence", "approval", errors, nonempty=True)
        if approval.get("providerDecision") not in APPROVAL_DECISIONS:
            errors.append(
                f"approval.providerDecision: expected one of {sorted(APPROVAL_DECISIONS)}"
            )
        if not isinstance(approval.get("mediaApproved"), bool):
            errors.append("approval.mediaApproved: must be true or false")
        approved_providers = approval.get("approvedProviders", [])
        if len(approved_providers) != len(set(approved_providers)):
            errors.append("approval.approvedProviders: duplicate provider")
        for provider in approved_providers:
            if not valid_provider_name(provider):
                errors.append(
                    f"approval.approvedProviders: invalid named provider {provider!r}"
                )
        for index, evidence in enumerate(approval.get("approvalEvidence", [])):
            if not substantive(evidence):
                errors.append(
                    f"approval.approvalEvidence[{index}]: needs substantive direct approval evidence"
                )
        cost = approval.get("costCeiling")
        require_fields(cost, ("unit", "limit", "description"), "approval.costCeiling", errors)
        if isinstance(cost, dict):
            if cost.get("unit") not in COST_UNITS:
                errors.append(f"approval.costCeiling.unit: expected one of {sorted(COST_UNITS)}")
            if not substantive(cost.get("description")):
                errors.append("approval.costCeiling.description: needs a substantive boundary")
            if (
                isinstance(cost.get("limit"), bool)
                or not isinstance(cost.get("limit"), (int, float))
                or cost.get("limit", -1) < 0
            ):
                errors.append("approval.costCeiling.limit: must be a non-negative number")
        if isinstance(approval.get("regenerationLimit"), bool) or not isinstance(
            approval.get("regenerationLimit"), int
        ):
            errors.append("approval.regenerationLimit: must be an integer")
        elif approval.get("regenerationLimit") < 0:
            errors.append("approval.regenerationLimit: must be zero or greater")

    required_pairs = scope.get("requiredEdgePairs", []) if isinstance(scope, dict) else []
    parsed_required_pairs = []
    translated_required_pairs = []
    if len(required_pairs) != len(set(required_pairs)):
        errors.append("continuityScope.requiredEdgePairs: duplicate transition pair")
    for pair in required_pairs:
        parsed = parse_pair(pair)
        if parsed is None:
            errors.append(f"continuityScope.requiredEdgePairs: invalid pair {pair}")
            continue
        parsed_required_pairs.append(parsed)
        if parsed[0] not in state_ids or parsed[1] not in state_ids:
            errors.append(f"continuityScope.requiredEdgePairs: unknown endpoint in {pair}")
            continue
        contract_pair = (
            previs_to_contract.get(parsed[0]),
            previs_to_contract.get(parsed[1]),
        )
        translated_required_pairs.append(contract_pair)
        if contract_pair not in generated_dependency_by_pair:
            errors.append(
                "continuityScope.requiredEdgePairs: visual edge "
                f"{pair} maps to unapproved contract handoff "
                f"{contract_pair[0]}->{contract_pair[1]}"
            )

    translated_pair_set = set(translated_required_pairs)
    missing_contract_pairs = set(generated_dependency_by_pair) - translated_pair_set
    extra_contract_pairs = translated_pair_set - set(generated_dependency_by_pair)
    for start, end in sorted(missing_contract_pairs):
        errors.append(
            f"continuityScope.requiredEdgePairs: missing generated contract handoff {start}->{end}"
        )
    for start, end in sorted(extra_contract_pairs, key=lambda item: str(item)):
        errors.append(
            f"continuityScope.requiredEdgePairs: extra generated contract handoff {start}->{end}"
        )

    if isinstance(scope, dict) and scope.get("topology") == "linear" and states:
        ordered_states = sorted(
            (state for state in states if isinstance(state, dict)),
            key=lambda item: item.get("order", 0),
        )
        linear_pairs = [
            f"{ordered_states[index].get('id')}->{ordered_states[index + 1].get('id')}"
            for index in range(len(ordered_states) - 1)
        ]
        if required_pairs != linear_pairs:
            errors.append(
                "continuityScope.requiredEdgePairs: linear topology must list every adjacent "
                "state pair in order; expected " + ", ".join(linear_pairs)
            )
    elif isinstance(scope, dict) and scope.get("topology") == "branching" and state_ids:
        graph = {state_id: set() for state_id in state_ids}
        participating = set()
        for start, end in parsed_required_pairs:
            if start in graph and end in graph:
                graph[start].add(end)
                participating.update((start, end))
        if participating != state_ids:
            errors.append("continuityScope.requiredEdgePairs: branching graph has orphan states")
        anchor = source_lock.get("anchorStateId") if isinstance(source_lock, dict) else None
        if anchor in graph:
            reached = set()
            frontier = [anchor]
            while frontier:
                current = frontier.pop()
                if current in reached:
                    continue
                reached.add(current)
                frontier.extend(graph[current] - reached)
            if reached != state_ids:
                errors.append("continuityScope.requiredEdgePairs: branching graph is disconnected")

    computed_unapproved_edges = []
    provided_pairs = []
    external_edges = []
    for index, motion_edge in enumerate(edges):
        path = f"edges[{index}]"
        require_fields(
            motion_edge,
            (
                "id",
                "fromStateId",
                "toStateId",
                "contractShotIds",
                "job",
                "action",
                "camera",
                "duration",
                "exitHold",
                "identityLocks",
                "negativeConstraints",
                "method",
                "externalService",
                "provider",
                "responsive",
                "regenerationBoundary",
                "fallback",
                "outputAssetIds",
                "outputEvidence",
                "approvalEvidence",
                "reviewEvidence",
                "verdict",
            ),
            path,
            errors,
            allow_empty=("reviewEvidence",),
        )
        if not isinstance(motion_edge, dict):
            continue
        if not motion_edge.get("id", "").startswith("PREVIS-EDGE-"):
            errors.append(f"{path}.id: must use PREVIS-EDGE-* format")
        if motion_edge.get("fromStateId") not in state_ids:
            errors.append(f"{path}.fromStateId: unknown visual state")
        if motion_edge.get("toStateId") not in state_ids:
            errors.append(f"{path}.toStateId: unknown visual state")
        if motion_edge.get("fromStateId") == motion_edge.get("toStateId"):
            errors.append(f"{path}: transition endpoints must differ")
        for field in ("contractShotIds", "identityLocks", "negativeConstraints"):
            require_list(motion_edge, field, path, errors, nonempty=True)
        require_list(motion_edge, "outputAssetIds", path, errors)
        require_list(motion_edge, "outputEvidence", path, errors)
        validate_responsive(
            motion_edge.get("responsive"),
            f"{path}.responsive",
            errors,
            base_dir,
        )
        method = motion_edge.get("method")
        if method not in METHODS:
            errors.append(f"{path}.method: invalid method")
        contract_pair = (
            previs_to_contract.get(motion_edge.get("fromStateId")),
            previs_to_contract.get(motion_edge.get("toStateId")),
        )
        governing_dependency = generated_dependency_by_pair.get(contract_pair)
        if governing_dependency is None:
            errors.append(
                f"{path}: no generated contract motion dependency governs "
                f"{contract_pair[0]}->{contract_pair[1]}"
            )
        else:
            if method != governing_dependency.get("method"):
                errors.append(
                    f"{path}.method: expected approved contract method "
                    f"{governing_dependency.get('method')}, got {method}"
                )
            if sorted(motion_edge.get("contractShotIds", [])) != sorted(
                governing_dependency.get("shotIds", [])
            ):
                errors.append(
                    f"{path}.contractShotIds: must exactly match governing contract SHOT-IDs"
                )
        if not isinstance(motion_edge.get("externalService"), bool):
            errors.append(f"{path}.externalService: must be true or false")
        needs_provider = method in VIDEO_METHODS or motion_edge.get("externalService") is True
        if needs_provider:
            external_edges.append(motion_edge)
            provider = str(motion_edge.get("provider", "")).strip()
            if not valid_provider_name(provider):
                errors.append(f"{path}.provider: requires a named approved provider")
            elif isinstance(approval, dict) and provider not in approval.get("approvedProviders", []):
                errors.append(f"{path}.provider: {provider} is not in approval.approvedProviders")
        elif motion_edge.get("provider") != "none":
            errors.append(f"{path}.provider: provider-free edge must use none")
        pair = edge_pair(motion_edge)
        provided_pairs.append(pair)
        if motion_edge.get("verdict") not in VERDICTS:
            errors.append(f"{path}.verdict: invalid verdict")
        if motion_edge.get("verdict") != "strong" or not substantive(
            motion_edge.get("approvalEvidence")
        ):
            if present(motion_edge.get("id")):
                computed_unapproved_edges.append(motion_edge["id"])
        if phase == "build":
            if not motion_edge.get("outputAssetIds"):
                errors.append(f"{path}.outputAssetIds: build requires approved motion output")
            for asset_id in motion_edge.get("outputAssetIds", []):
                if not present(asset_id) or not asset_id.startswith("ASSET-"):
                    errors.append(f"{path}.outputAssetIds: invalid ASSET-ID {asset_id}")
            output_evidence = motion_edge.get("outputEvidence", [])
            if not output_evidence:
                errors.append(f"{path}.outputEvidence: build requires resolvable motion output")
            elif len(output_evidence) != len(motion_edge.get("outputAssetIds", [])):
                errors.append(
                    f"{path}.outputEvidence: must contain one evidence record per outputAssetId"
                )
            for evidence_index, evidence in enumerate(output_evidence):
                expected_output_prefix = None
                if method in {"short-clip", "long-video", "existing-authentic-video"}:
                    expected_output_prefix = "video/"
                elif method in {"image-sequence", "layered-stills"}:
                    expected_output_prefix = "image/"
                validate_evidence(
                    evidence,
                    f"{path}.outputEvidence[{evidence_index}]",
                    errors,
                    base_dir,
                    expected_prefix=expected_output_prefix,
                )
            output_locators = [
                evidence.get("locator")
                for evidence in output_evidence
                if isinstance(evidence, dict) and present(evidence.get("locator"))
            ]
            if len(output_locators) != len(set(output_locators)):
                errors.append(f"{path}.outputEvidence: every output needs distinct evidence")
            validate_review_evidence(
                motion_edge.get("reviewEvidence"),
                f"{path}.reviewEvidence",
                errors,
                base_dir,
            )

    if len(provided_pairs) != len(set(provided_pairs)):
        errors.append("edges: duplicate transition pair")
    if phase in {"motion", "build"}:
        missing_pairs = [pair for pair in required_pairs if pair not in provided_pairs]
        extra_pairs = [pair for pair in provided_pairs if pair not in required_pairs]
        for pair in missing_pairs:
            errors.append(f"edges: missing required transition pair {pair}")
        for pair in extra_pairs:
            errors.append(f"edges: unapproved transition pair {pair}")
        if external_edges and isinstance(approval, dict):
            if approval.get("providerDecision") != "approved":
                errors.append("approval.providerDecision: external media requires approval")
            if approval.get("mediaApproved") is not True:
                errors.append("approval.mediaApproved: external media requires explicit approval")
            if not substantive(approval.get("mediaApprovalEvidence")):
                errors.append(
                    "approval.mediaApprovalEvidence: external media needs direct approval evidence"
                )
            cost = approval.get("costCeiling")
            if isinstance(cost, dict) and cost.get("unit") == "pending":
                errors.append("approval.costCeiling.unit: cannot be pending for external media")
            if (
                isinstance(approval.get("regenerationLimit"), bool)
                or not isinstance(approval.get("regenerationLimit"), int)
                or approval.get("regenerationLimit", 0) < 1
            ):
                errors.append(
                    "approval.regenerationLimit: external media requires at least one bounded attempt"
                )
        elif isinstance(approval, dict):
            if approval.get("providerDecision") != "not-required":
                errors.append(
                    "approval.providerDecision: provider-free motion must be not-required"
                )
            if approval.get("approvedProviders"):
                errors.append(
                    "approval.approvedProviders: provider-free motion must list no providers"
                )
            if approval.get("mediaApproved") is not False:
                errors.append("approval.mediaApproved: provider-free motion must be false")
            if present(approval.get("mediaApprovalEvidence")):
                errors.append(
                    "approval.mediaApprovalEvidence: provider-free motion must remain empty"
                )

    computed_unmapped = sorted(expected_contract_state_ids - mapped_contract_state_ids)
    reconciliation = manifest.get("reconciliation")
    require_fields(
        reconciliation,
        (
            "stateCount",
            "edgeCount",
            "expectedEdgeCount",
            "unmappedContractStateIds",
            "missingEdgePairs",
            "unapprovedStateIds",
            "unapprovedEdgeIds",
            "blockers",
        ),
        "reconciliation",
        errors,
    )
    if isinstance(reconciliation, dict):
        expected_values = {
            "stateCount": len(states),
            "edgeCount": len(edges),
            "expectedEdgeCount": len(required_pairs),
        }
        for field, expected in expected_values.items():
            if reconciliation.get(field) != expected:
                errors.append(
                    f"reconciliation.{field}: expected {expected}, got {reconciliation.get(field)}"
                )
        for field in (
            "unmappedContractStateIds",
            "missingEdgePairs",
            "unapprovedStateIds",
            "unapprovedEdgeIds",
            "blockers",
        ):
            require_list(reconciliation, field, "reconciliation", errors)
        computed = {
            "unmappedContractStateIds": computed_unmapped,
            "unapprovedStateIds": sorted(computed_unapproved_states),
        }
        if phase in {"motion", "build"}:
            computed.update(
                missingEdgePairs=sorted(
                    pair for pair in required_pairs if pair not in provided_pairs
                ),
                unapprovedEdgeIds=sorted(computed_unapproved_edges),
            )
        for field, expected in computed.items():
            if sorted(reconciliation.get(field, [])) != expected:
                errors.append(
                    f"reconciliation.{field}: must exactly match " + ", ".join(expected)
                )
        for field in ("unmappedContractStateIds", "unapprovedStateIds", "blockers"):
            if reconciliation.get(field):
                errors.append(
                    f"reconciliation.{field}: must be empty for {phase}; "
                    + ", ".join(map(str, reconciliation.get(field, [])))
                )
        if phase in {"motion", "build"} and reconciliation.get("unapprovedEdgeIds"):
            errors.append(
                f"reconciliation.unapprovedEdgeIds: must be empty for {phase}; "
                + ", ".join(map(str, reconciliation.get("unapprovedEdgeIds", [])))
            )

    return errors


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path, help="Path to previsualization JSON")
    parser.add_argument(
        "--contract",
        required=True,
        type=Path,
        help="Path to the exact approved experience-contract JSON",
    )
    parser.add_argument(
        "--phase",
        choices=("state-board", "motion", "build"),
        default="motion",
        help="Validation strictness (default: motion)",
    )
    return parser.parse_args()


def read_json(path, label):
    try:
        return json.loads(path.read_text(encoding="utf-8")), None
    except FileNotFoundError:
        return None, f"{label} file not found: {path}"
    except (OSError, json.JSONDecodeError) as error:
        return None, f"cannot read {label} JSON: {error}"


def main():
    args = parse_args()
    manifest, manifest_error = read_json(args.manifest, "previsualization")
    contract, contract_error = read_json(args.contract, "contract")
    read_errors = [error for error in (manifest_error, contract_error) if error]
    if read_errors:
        print("FAIL")
        for error in read_errors:
            print(f"- {error}")
        return 1

    errors = validate_manifest(manifest, contract, args.phase, args.manifest.parent)
    if errors:
        print("FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    reconciliation = manifest["reconciliation"]
    print(
        "PASS "
        f"{manifest['previsualizationId']} v{manifest['version']} "
        f"phase={args.phase} states={reconciliation['stateCount']} "
        f"edges={reconciliation['edgeCount']}/{reconciliation['expectedEdgeCount']}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
import json
import sys
from pathlib import Path


ROLES = {"opening", "quiet-editorial", "peak", "decision-utility", "resolution"}


def nonempty(value):
    return isinstance(value, str) and bool(value.strip()) and value.strip() not in {"pending", "unknown"}


def validate(data):
    errors = []
    for key in ["visualDevelopmentId", "version", "contractId", "contractVersion", "territoryId", "status", "system", "styleFrames", "motionStudy", "approval", "reconciliation"]:
        if key not in data:
            errors.append(f"missing top-level {key}")
    system = data.get("system", {})
    for key in ["grid", "spacingRhythm", "typographyRoles", "colorMaterialLaw", "imageryTreatment", "motionLaw", "soundPolicy"]:
        if not system.get(key):
            errors.append(f"system.{key} is required")
    if system.get("verdict") != "strong":
        errors.append("system.verdict must be strong")
    frames = data.get("styleFrames", [])
    frame_roles = {x.get("role") for x in frames}
    for role in sorted(ROLES - frame_roles):
        errors.append(f"styleFrames missing required role {role}")
    for frame in frames:
        for key in ["id", "role", "stateIds", "desktopEvidence", "mobileEvidence", "compositionJob"]:
            if not frame.get(key):
                errors.append(f"styleFrame {frame.get('id', '?')}.{key} is required")
        if frame.get("verdict") != "strong":
            errors.append(f"styleFrame {frame.get('id', '?')}.verdict must be strong")
    motion = data.get("motionStudy", {})
    for key in ["id", "fromStateId", "toStateId", "whyRepresentative", "evidence"]:
        if not motion.get(key):
            errors.append(f"motionStudy.{key} is required")
    for key in ["desktopInspected", "mobileInspected", "reducedMotionInspected", "reversalInspected"]:
        if motion.get(key) is not True:
            errors.append(f"motionStudy.{key} must be true")
    if motion.get("verdict") != "strong":
        errors.append("motionStudy.verdict must be strong")
    approval = data.get("approval", {})
    if approval.get("completeBoardApproved") is not True or not nonempty(approval.get("approvalEvidence")):
        errors.append("approval requires completeBoardApproved and direct approvalEvidence")
    rec = data.get("reconciliation", {})
    if rec.get("missingRoles") or rec.get("blockers") or rec.get("verdict") != "strong":
        errors.append("reconciliation must have no missing roles/blockers and a strong verdict")
    return errors


def main():
    try:
        data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"FAIL: cannot read manifest: {exc}")
        return 1
    errors = validate(data)
    if errors:
        print("FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("PASS: visual development manifest is valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

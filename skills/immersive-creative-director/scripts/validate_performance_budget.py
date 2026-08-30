#!/usr/bin/env python3
import json
import sys
from pathlib import Path


NUMERIC_BUDGETS = [
    "initialTransferBytes", "initialHeavyMediaBytes", "largestSingleAssetBytes",
    "maximumConcurrentVideoDecoders", "minimumAnimationFps", "maximumLongTaskMs",
    "maximumLayoutShift",
]


def nonempty(value):
    return isinstance(value, str) and bool(value.strip()) and value.strip() not in {"pending", "unknown"}


def validate(data):
    errors = []
    targets = data.get("targetSurfaces", [])
    ids = {x.get("id") for x in targets}
    for required in ["desktop", "mobile"]:
        if required not in ids:
            errors.append(f"targetSurfaces requires {required}")
    for target in targets:
        for key in ["id", "viewport", "input", "deviceClass"]:
            if not nonempty(target.get(key)):
                errors.append(f"targetSurface {target.get('id', '?')}.{key} is required")
    budgets = data.get("budgets", {})
    for key in NUMERIC_BUDGETS:
        value = budgets.get(key)
        if not isinstance(value, (int, float)) or value <= 0:
            errors.append(f"budgets.{key} must be a positive number")
    if not nonempty(budgets.get("memoryRiskCeiling")):
        errors.append("budgets.memoryRiskCeiling is required")
    for key in ["loadingStrategy", "responsiveAssetStrategy", "lowPowerFallback", "noWebglFallback", "reducedMotionRoute", "failureRecovery", "approvalEvidence"]:
        if not nonempty(data.get(key)):
            errors.append(f"{key} is required")
    if not data.get("measurementPlan"):
        errors.append("measurementPlan is required")
    if data.get("verdict") != "strong":
        errors.append("verdict must be strong")
    return errors


def main():
    try:
        data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"FAIL: cannot read budget: {exc}")
        return 1
    errors = validate(data)
    if errors:
        print("FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("PASS: performance budget is valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

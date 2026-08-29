#!/usr/bin/env python3

"""Validate an Immersive Creative Director experience contract.

The validator proves structural coverage and reference integrity. It cannot judge
visual quality; the skill's qualitative gates still own that decision.
"""

import argparse
import json
import sys
from pathlib import Path


PROVENANCE_AUTHORITY = {
    "live copy": "live-source",
    "approved new copy": "explicit-user-approval",
    "placeholder": "placeholder",
}
VERDICTS = {"strong", "needs work", "reject"}
STATUSES = {"exploration", "approval-candidate", "approved"}
ROUTE_STATUSES = {"required", "existing", "optional", "forbidden", "blocked"}
PARITY_FIELDS = ("desktop", "mobile", "reducedMotion", "fallback")


def present(value):
    return isinstance(value, str) and bool(value.strip())


def require_fields(record, fields, path, errors):
    if not isinstance(record, dict):
        errors.append(f"{path}: expected an object")
        return
    for field in fields:
        if field not in record:
            errors.append(f"{path}.{field}: missing required field")
        elif isinstance(record[field], str) and not record[field].strip():
            errors.append(f"{path}.{field}: must not be empty")


def require_nonempty_list(record, field, path, errors):
    value = record.get(field)
    if not isinstance(value, list) or not value:
        errors.append(f"{path}.{field}: must be a non-empty list")


def require_list(record, field, path, errors):
    if not isinstance(record.get(field), list):
        errors.append(f"{path}.{field}: must be a list")


def validate_parity(parity, path, errors):
    if not isinstance(parity, dict):
        errors.append(f"{path}: expected parity object")
        return
    for field in PARITY_FIELDS:
        if not present(parity.get(field)):
            errors.append(f"{path}.{field}: missing parity treatment")


def unique_ids(records, path, errors):
    seen = set()
    for index, record in enumerate(records):
        record_id = record.get("id") if isinstance(record, dict) else None
        if not present(record_id):
            errors.append(f"{path}[{index}].id: missing stable ID")
            continue
        if record_id in seen:
            errors.append(f"{path}[{index}].id: duplicate ID {record_id}")
        seen.add(record_id)
    return seen


def validate_contract(contract, phase):
    errors = []
    require_fields(
        contract,
        (
            "contractId",
            "version",
            "status",
            "canonicalScope",
            "routes",
            "copy",
            "responsibilities",
            "storyboards",
            "reconciliation",
        ),
        "contract",
        errors,
    )
    if errors:
        return errors

    if contract["status"] not in STATUSES:
        errors.append(f"contract.status: expected one of {sorted(STATUSES)}")
    if not isinstance(contract["version"], (int, str)) or str(contract["version"]).strip() == "":
        errors.append("contract.version: must identify the exact contract version")

    scope = contract["canonicalScope"]
    require_fields(
        scope,
        ("target", "sourceEvidence", "focusLens", "approvalTarget", "sourceSnapshot", "amendments"),
        "canonicalScope",
        errors,
    )
    if isinstance(scope, dict):
        require_nonempty_list(scope, "sourceEvidence", "canonicalScope", errors)
        require_nonempty_list(scope, "sourceSnapshot", "canonicalScope", errors)
        if not isinstance(scope.get("amendments"), list):
            errors.append("canonicalScope.amendments: expected a list")
        else:
            for index, amendment in enumerate(scope["amendments"]):
                require_fields(
                    amendment,
                    ("id", "before", "after", "affectedResponsibilityIds", "explicitUserApproval"),
                    f"canonicalScope.amendments[{index}]",
                    errors,
                )
                if isinstance(amendment, dict) and amendment.get("explicitUserApproval") is not True:
                    errors.append(
                        f"canonicalScope.amendments[{index}].explicitUserApproval: must be true"
                    )

    routes = contract["routes"] if isinstance(contract["routes"], list) else []
    copies = contract["copy"] if isinstance(contract["copy"], list) else []
    responsibilities = (
        contract["responsibilities"] if isinstance(contract["responsibilities"], list) else []
    )
    storyboards = contract["storyboards"] if isinstance(contract["storyboards"], list) else []
    if not routes:
        errors.append("routes: route inventory is empty")
    if not copies:
        errors.append("copy: copy-provenance ledger is empty")
    if not responsibilities:
        errors.append("responsibilities: atomic responsibility map is empty")
    if not storyboards:
        errors.append("storyboards: whole-experience state storyboard is empty")

    route_ids = unique_ids(routes, "routes", errors)
    copy_ids = unique_ids(copies, "copy", errors)
    responsibility_ids = unique_ids(responsibilities, "responsibilities", errors)

    for index, route in enumerate(routes):
        path = f"routes[{index}]"
        require_fields(
            route,
            (
                "id",
                "kind",
                "destination",
                "navigationCopyId",
                "visitorJob",
                "authority",
                "status",
                "entryHandoff",
                "states",
                "verdict",
            ),
            path,
            errors,
        )
        if not isinstance(route, dict):
            continue
        if route.get("status") not in ROUTE_STATUSES:
            errors.append(f"{path}.status: invalid route status")
        if route.get("verdict") not in VERDICTS:
            errors.append(f"{path}.verdict: invalid verdict")
        if route.get("navigationCopyId") not in copy_ids:
            errors.append(
                f"{path}.navigationCopyId: unknown COPY-ID {route.get('navigationCopyId')}"
            )
        require_nonempty_list(route, "states", path, errors)
        if phase in {"approval", "build"} and route.get("status") in {"required", "existing"}:
            if route.get("verdict") != "strong":
                errors.append(f"{path}: required route {route.get('id')} is not strong")

    placeholder_count = 0
    for index, copy_record in enumerate(copies):
        path = f"copy[{index}]"
        require_fields(
            copy_record,
            (
                "id",
                "text",
                "provenance",
                "authority",
                "authorityType",
                "transformation",
                "uses",
                "verdict",
            ),
            path,
            errors,
        )
        if not isinstance(copy_record, dict):
            continue
        provenance = copy_record.get("provenance")
        authority_type = copy_record.get("authorityType")
        expected_authority = PROVENANCE_AUTHORITY.get(provenance)
        if expected_authority is None:
            errors.append(
                f"{path}.provenance: expected live copy, approved new copy, or placeholder"
            )
        elif authority_type != expected_authority:
            errors.append(
                f"{path}.authorityType: {provenance} requires {expected_authority}; "
                f"internal strategy is not public-copy authority"
            )
        if provenance == "placeholder":
            placeholder_count += 1
            if "[PLACEHOLDER]" not in str(copy_record.get("text", "")):
                errors.append(f"{path}.text: placeholder must visibly include [PLACEHOLDER]")
        if copy_record.get("verdict") not in VERDICTS:
            errors.append(f"{path}.verdict: invalid verdict")
        require_nonempty_list(copy_record, "uses", path, errors)

    all_states = []
    survivor_states = []
    state_ids = set()
    for board_index, storyboard in enumerate(storyboards):
        board_path = f"storyboards[{board_index}]"
        require_fields(
            storyboard,
            ("territoryId", "survivor", "coverage", "states"),
            board_path,
            errors,
        )
        if not isinstance(storyboard, dict):
            continue
        states = storyboard.get("states") if isinstance(storyboard.get("states"), list) else []
        all_states.extend(states)
        for state_index, state in enumerate(states):
            state_id = state.get("id") if isinstance(state, dict) else None
            if present(state_id):
                if state_id in state_ids:
                    errors.append(f"{board_path}.states[{state_index}].id: duplicate {state_id}")
                state_ids.add(state_id)
        if storyboard.get("survivor") is not True:
            continue
        survivor_states.append(states)
        if storyboard.get("coverage") != "opening-to-resolution":
            errors.append(f"{board_path}.coverage: survivor must cover opening-to-resolution")
        if len(states) < 3:
            errors.append(f"{board_path}.states: survivor needs at least three causal states")
        ordered_states = sorted(
            states,
            key=lambda item: item.get("order", 0) if isinstance(item, dict) else 0,
        )
        modes = {state.get("mode") for state in ordered_states if isinstance(state, dict)}
        if "opening" not in modes:
            errors.append(f"{board_path}.states: missing opening state")
        if "resolution" not in modes:
            errors.append(f"{board_path}.states: missing resolution state")
        board_responsibilities = set()
        for state_index, state in enumerate(ordered_states):
            state_path = f"{board_path}.states[{state_index}]"
            require_fields(
                state,
                (
                    "id",
                    "order",
                    "routeId",
                    "mode",
                    "responsibilityIds",
                    "copyIds",
                    "assetIds",
                    "startComposition",
                    "inputCause",
                    "transformation",
                    "endComposition",
                    "causalHandoff",
                    "agency",
                    "parity",
                    "verdict",
                ),
                state_path,
                errors,
            )
            if not isinstance(state, dict):
                continue
            require_nonempty_list(state, "responsibilityIds", state_path, errors)
            require_list(state, "copyIds", state_path, errors)
            validate_parity(state.get("parity"), f"{state_path}.parity", errors)
            for responsibility_id in state.get("responsibilityIds", []):
                board_responsibilities.add(responsibility_id)
                if responsibility_id not in responsibility_ids:
                    errors.append(
                        f"{state_path}.responsibilityIds: unknown RESP-ID {responsibility_id}"
                    )
            for copy_id in state.get("copyIds", []):
                if copy_id not in copy_ids:
                    errors.append(f"{state_path}.copyIds: unknown COPY-ID {copy_id}")
            if state.get("routeId") not in route_ids:
                errors.append(f"{state_path}.routeId: unknown ROUTE-ID {state.get('routeId')}")
            if state.get("verdict") not in VERDICTS:
                errors.append(f"{state_path}.verdict: invalid verdict")
            expected_handoff = (
                ordered_states[state_index + 1].get("id")
                if state_index + 1 < len(ordered_states)
                else "terminal"
            )
            if state.get("causalHandoff") != expected_handoff:
                errors.append(
                    f"{state_path}.causalHandoff: expected {expected_handoff}, "
                    f"got {state.get('causalHandoff')}"
                )
        missing_from_board = sorted(
            responsibility.get("id")
            for responsibility in responsibilities
            if responsibility.get("required") is True
            and responsibility.get("id") not in board_responsibilities
        )
        if missing_from_board:
            errors.append(
                f"{board_path}: required responsibilities missing from scoped-experience storyboard: "
                + ", ".join(missing_from_board)
            )

    if phase in {"approval", "build"} and not survivor_states:
        errors.append("storyboards: no surviving whole-experience territory")

    mapped_required = []
    unmapped_required = []
    for index, responsibility in enumerate(responsibilities):
        path = f"responsibilities[{index}]"
        require_fields(
            responsibility,
            (
                "id",
                "obligation",
                "authority",
                "truthState",
                "routeIds",
                "stateIds",
                "reachability",
                "parity",
                "copyIds",
                "assetIds",
                "required",
                "verdict",
            ),
            path,
            errors,
        )
        if not isinstance(responsibility, dict):
            continue
        validate_parity(responsibility.get("parity"), f"{path}.parity", errors)
        require_nonempty_list(responsibility, "routeIds", path, errors)
        require_list(responsibility, "copyIds", path, errors)
        for route_id in responsibility.get("routeIds", []):
            if route_id not in route_ids:
                errors.append(f"{path}.routeIds: unknown ROUTE-ID {route_id}")
        for copy_id in responsibility.get("copyIds", []):
            if copy_id not in copy_ids:
                errors.append(f"{path}.copyIds: unknown COPY-ID {copy_id}")
        for state_id in responsibility.get("stateIds", []):
            if state_id not in state_ids:
                errors.append(f"{path}.stateIds: unknown STATE-ID {state_id}")
        if responsibility.get("verdict") not in VERDICTS:
            errors.append(f"{path}.verdict: invalid verdict")
        if responsibility.get("required") is True:
            if responsibility.get("stateIds") and responsibility.get("verdict") == "strong":
                mapped_required.append(responsibility.get("id"))
            else:
                unmapped_required.append(responsibility.get("id"))
                errors.append(
                    f"{path}: required responsibility {responsibility.get('id')} is unmapped or not strong"
                )

    reconciliation = contract["reconciliation"]
    require_fields(
        reconciliation,
        (
            "obligationCount",
            "mappedCount",
            "unmappedIds",
            "inventedIds",
            "unresolvedIds",
            "routeCount",
            "storyboardStateCount",
            "placeholderCount",
            "blockers",
            "exclusions",
        ),
        "reconciliation",
        errors,
    )
    if isinstance(reconciliation, dict):
        expected_values = {
            "obligationCount": len([r for r in responsibilities if r.get("required") is True]),
            "mappedCount": len(mapped_required),
            "routeCount": len(routes),
            "storyboardStateCount": sum(len(states) for states in survivor_states),
            "placeholderCount": placeholder_count,
        }
        for field, expected in expected_values.items():
            if reconciliation.get(field) != expected:
                errors.append(
                    f"reconciliation.{field}: expected {expected}, got {reconciliation.get(field)}"
                )
        if sorted(reconciliation.get("unmappedIds", [])) != sorted(unmapped_required):
            errors.append(
                "reconciliation.unmappedIds: must exactly match " + ", ".join(unmapped_required)
            )
        for field in ("inventedIds", "unresolvedIds", "blockers", "exclusions"):
            if not isinstance(reconciliation.get(field), list):
                errors.append(f"reconciliation.{field}: expected a list")
        if phase in {"approval", "build"}:
            for field in ("unmappedIds", "inventedIds", "unresolvedIds", "blockers"):
                if reconciliation.get(field):
                    errors.append(
                        f"reconciliation.{field}: must be empty for {phase}; "
                        + ", ".join(map(str, reconciliation.get(field, [])))
                    )

    if phase == "approval" and contract["status"] not in {"approval-candidate", "approved"}:
        errors.append("contract.status: approval phase requires approval-candidate or approved")
    if phase == "build":
        if contract["status"] != "approved":
            errors.append("contract.status: build phase requires approved")
        if placeholder_count:
            errors.append("copy: build phase permits no placeholder copy")

    return errors


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("contract", type=Path, help="Path to experience-contract JSON")
    parser.add_argument(
        "--phase",
        choices=("structure", "approval", "build"),
        default="approval",
        help="Validation strictness (default: approval)",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    try:
        contract = json.loads(args.contract.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"FAIL\n- contract file not found: {args.contract}")
        return 1
    except (OSError, json.JSONDecodeError) as error:
        print(f"FAIL\n- cannot read contract JSON: {error}")
        return 1

    errors = validate_contract(contract, args.phase)
    if errors:
        print("FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    reconciliation = contract["reconciliation"]
    print(
        "PASS "
        f"{contract['contractId']} v{contract['version']} "
        f"phase={args.phase} routes={reconciliation['routeCount']} "
        f"responsibilities={reconciliation['mappedCount']}/{reconciliation['obligationCount']} "
        f"states={reconciliation['storyboardStateCount']} "
        f"placeholders={reconciliation['placeholderCount']}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path


CORE_FILES = {
    "orchestration.md", "preferences.md", "experience-contract.md",
    "evidence-library.md", "visual-reference-manifest.md", "motion-reference-manifest.md",
    "process-reference-manifest.md", "reference-corpus.md", "doctrine.md",
    "motion-vocabulary.md", "production.md", "previsualization.md",
    "quality-gates.md", "evolving-the-library.md", "execution-contract.md",
    "scrollcraft-adapter.md", "visual-development.md", "performance-budget.md",
    "dependencies.md",
}
VISUAL_IDS = {
    "site-sondaven", "site-lando-norris", "site-indigo-laboratory", "site-noth",
    "site-mr-black", "site-santioni-spirits", "site-become-a-yogi", "site-mesh3d",
    "site-haoqi", "site-ride-radian", "site-pear",
}
PROCESS_IDS = {
    "video-QUI6Ug4cHnE", "video-39IlNR-P3-Q", "video-GJxchJkk4Lk",
    "video-ubH1ulaK-t4",
}
CONCEPT_GATES = {
    "QUALITY-corpus-authority", "QUALITY-protocol-compliance", "QUALITY-source-lock",
    "QUALITY-route-integrity", "QUALITY-content-coverage", "QUALITY-state-storyboard",
    "QUALITY-contract-validation", "QUALITY-protected-kernel", "QUALITY-subject-specificity",
    "QUALITY-transplantation", "QUALITY-coherence-source", "QUALITY-story-causality",
    "QUALITY-motion-necessity", "QUALITY-composition", "QUALITY-agency-orientation",
    "QUALITY-whole-site", "QUALITY-peak-resolution",
}


def nonempty(value):
    return isinstance(value, str) and bool(value.strip()) and value.strip() not in {"pending", "unknown"}


def validate(data, phase):
    errors = []
    for key in ["runId", "version", "mode", "status", "corpusGrounding", "intake",
                "experienceContract", "evidenceLineage", "territories", "qualityGates",
                "reconciliation"]:
        if key not in data:
            errors.append(f"missing top-level {key}")

    grounding = data.get("corpusGrounding", {})
    if set(grounding.get("coreFilesAtEof", [])) != CORE_FILES:
        errors.append("corpusGrounding.coreFilesAtEof must exactly cover every mandatory core file")
    if set(grounding.get("visualOverviewIds", [])) != VISUAL_IDS:
        errors.append("corpusGrounding.visualOverviewIds must exactly cover all 11 website overviews")
    if set(grounding.get("processIds", [])) != PROCESS_IDS:
        errors.append("corpusGrounding.processIds must exactly cover all four process records")
    for key in ["visualValidatorEvidence", "processValidatorEvidence"]:
        if not nonempty(grounding.get(key)):
            errors.append(f"corpusGrounding.{key} requires direct PASS evidence")
    if grounding.get("verdict") != "strong":
        errors.append("corpusGrounding.verdict must be strong")

    intake = data.get("intake", {})
    for key in ["grillingComplete", "domainModelingComplete", "frontierEmpty"]:
        if intake.get(key) is not True:
            errors.append(f"intake.{key} must be true")
    if not nonempty(intake.get("userConfirmationEvidence")):
        errors.append("intake.userConfirmationEvidence is required")
    if intake.get("verdict") != "strong":
        errors.append("intake.verdict must be strong")
    rounds = intake.get("rounds", [])
    if not rounds:
        errors.append("intake.rounds must preserve the complete Grilling frontier history")
    seen_question_ids = set()
    for index, round_record in enumerate(rounds, start=1):
        if round_record.get("round") != index:
            errors.append(f"intake.rounds[{index - 1}].round must be {index}")
        if round_record.get("agentEndedTurnAndWaited") is not True:
            errors.append(f"intake round {index} must end the turn and wait")
        if not nonempty(round_record.get("domainModelingEvidence")):
            errors.append(f"intake round {index} requires Domain Modeling evidence")
        questions = round_record.get("questions", [])
        if not questions:
            errors.append(f"intake round {index} requires its complete current frontier")
        current_ids = {question.get("id") for question in questions}
        for question in questions:
            question_id = question.get("id")
            if not nonempty(question_id) or not nonempty(question.get("decision")):
                errors.append(f"intake round {index} contains an unidentified decision")
            if question.get("allPrerequisitesSettledBeforeRound") is not True:
                errors.append(
                    f"intake round {index} question {question_id}: "
                    "allPrerequisitesSettledBeforeRound must be true"
                )
            prerequisites = set(question.get("prerequisites", []))
            if prerequisites & current_ids:
                errors.append(
                    f"intake round {index} question {question_id} depends on a question in the same round"
                )
            if not prerequisites <= seen_question_ids:
                errors.append(
                    f"intake round {index} question {question_id} has prerequisites not settled in earlier rounds"
                )
            if question.get("answered") is not True:
                errors.append(f"intake round {index} question {question_id} must be answered")
        seen_question_ids.update(current_ids)

    experience = data.get("experienceContract", {})
    for key in ["id", "path", "validatorEvidence"]:
        if not nonempty(experience.get(key)):
            errors.append(f"experienceContract.{key} is required")
    if not isinstance(experience.get("version"), int) or experience.get("version", 0) < 1:
        errors.append("experienceContract.version must be a positive integer")
    if experience.get("verdict") != "strong":
        errors.append("experienceContract.verdict must be strong")

    territories = data.get("territories", [])
    ids = [t.get("id") for t in territories]
    if len(territories) != 3 or len(set(ids)) != 3:
        errors.append("territories must contain exactly three unique records")
    survivors = [t for t in territories if t.get("disposition") == "survivor"]
    rejected = [t for t in territories if t.get("disposition") == "rejected"]
    if len(survivors) != 2 or len(rejected) != 1:
        errors.append("territories must contain exactly two survivors and one rejection")
    coherence = [t.get("coherenceSource") for t in territories]
    if len(set(coherence)) != len(coherence) or any(not nonempty(x) for x in coherence):
        errors.append("territories require three distinct non-empty coherenceSource values")
    for t in territories:
        if len(t.get("journey", [])) < 3:
            errors.append(f"{t.get('id', 'territory')}.journey requires opening-to-resolution evidence")
        if t.get("disposition") == "survivor" and t.get("verdict") != "strong":
            errors.append(f"{t.get('id', 'territory')}: survivor verdict must be strong")
        if t.get("disposition") == "rejected" and not nonempty(t.get("rejectionReason")):
            errors.append(f"{t.get('id', 'territory')}: rejected territory requires a reason")
    if data.get("recommendedTerritoryId") not in {t.get("id") for t in survivors}:
        errors.append("recommendedTerritoryId must name a survivor")

    lineage = data.get("evidenceLineage", [])
    if {x.get("territoryId") for x in lineage} != set(ids):
        errors.append("evidenceLineage must contain exactly one row for every territory")
    for row in lineage:
        if len(set(row.get("websiteEvidenceIds", []))) < 2:
            errors.append(f"{row.get('territoryId')}.websiteEvidenceIds requires two website records")
        if len(set(row.get("mechanismFamilies", []))) < 2:
            errors.append(f"{row.get('territoryId')}.mechanismFamilies requires two distinct families")
        if not row.get("processEvidenceIds"):
            errors.append(f"{row.get('territoryId')}.processEvidenceIds requires process evidence")
        for key in ["surfaceExclusion", "subjectOwnership"]:
            if not nonempty(row.get(key)):
                errors.append(f"{row.get('territoryId')}.{key} is required")
        if row.get("verdict") != "strong":
            errors.append(f"{row.get('territoryId')}.verdict must be strong")

    scrollcraft = data.get("scrollcraft", {})
    if scrollcraft.get("applicable"):
        if scrollcraft.get("adapterApplied") is not True:
            errors.append("scrollcraft.adapterApplied must be true")
        for key in ["journeyBeats", "feelingCurve", "peak", "grammar", "signatureMove",
                    "scrollScore", "inputContract", "responsivePlan", "reducedMotionParity"]:
            value = scrollcraft.get(key)
            if not value or value == "pending":
                errors.append(f"scrollcraft.{key} is required")
        if scrollcraft.get("verdict") != "strong":
            errors.append("scrollcraft.verdict must be strong")

    gate_rows = data.get("qualityGates", [])
    gate_map = {row.get("id"): row for row in gate_rows}
    missing = CONCEPT_GATES - set(gate_map)
    if missing:
        errors.append("qualityGates missing: " + ", ".join(sorted(missing)))
    for gate in CONCEPT_GATES & set(gate_map):
        row = gate_map[gate]
        if row.get("verdict") != "strong" or not nonempty(row.get("evidence")):
            errors.append(f"{gate} requires strong verdict and direct evidence")

    if data.get("reconciliation", {}).get("blockers"):
        errors.append("reconciliation.blockers must be empty at an advancement boundary")
    if data.get("reconciliation", {}).get("missingArtifacts"):
        errors.append("reconciliation.missingArtifacts must be empty at an advancement boundary")
    if data.get("reconciliation", {}).get("verdict") != "strong":
        errors.append("reconciliation.verdict must be strong")

    if phase in {"visual-development", "build"}:
        visual = data.get("visualDevelopment", {})
        if not nonempty(visual.get("manifestPath")):
            errors.append("visualDevelopment.manifestPath is required after concept approval")
        if visual.get("verdict") != "strong":
            errors.append("visualDevelopment.verdict must be strong")
        if not nonempty(visual.get("validatorEvidence")):
            errors.append("visualDevelopment.validatorEvidence is required")
    if phase == "build":
        perf = data.get("performanceBudget", {})
        if not nonempty(perf.get("manifestPath")) or perf.get("verdict") != "strong":
            errors.append("performanceBudget.manifestPath and strong verdict are required before build")
        if not nonempty(perf.get("validatorEvidence")):
            errors.append("performanceBudget.validatorEvidence is required before build")
        deps = data.get("dependencies", {})
        if deps.get("compatibilityChecked") is not True or deps.get("verdict") != "strong":
            errors.append("dependencies require a current compatibility check and strong verdict")
        if not nonempty(deps.get("validatorEvidence")):
            errors.append("dependencies.validatorEvidence is required before build")
    return errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest")
    parser.add_argument("--phase", choices=["concept", "visual-development", "build"], default="concept")
    args = parser.parse_args()
    try:
        data = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"FAIL: cannot read manifest: {exc}")
        return 1
    errors = validate(data, args.phase)
    if errors:
        print("FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"PASS: direction run is valid for phase {args.phase}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

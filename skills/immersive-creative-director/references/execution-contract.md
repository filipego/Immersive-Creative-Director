# Executable direction run

This is the persistent enforcement record for every Direction and Transformation engagement. Create `IMMERSIVE-DIRECTION-RUN.json` beside the canonical experience contract before the first intake question. It replaces private claims such as “I read the files,” “I considered the references,” or “Scrollcraft was applied” with one inspectable record that survives turns, compaction, handoffs, and model changes.

The record is required even in chat-only work. When filesystem mutation is unavailable, maintain the exact JSON in the response and label advancement blocked until it can be persisted and validated. Never treat a prose summary, protocol ledger held only in memory, or a prior run as current execution evidence.

## Phase boundaries

Run:

```bash
python3 scripts/validate_direction_run.py /absolute/path/IMMERSIVE-DIRECTION-RUN.json --phase concept
```

before presenting a recommended concept. This proves current corpus grounding, real intake completion, user-confirmed shared understanding, complete territory/evidence lineage, reconciled Scrollcraft planning, and conceptual quality gates.

After concept approval, create the universal visual-development package in [visual-development.md](visual-development.md), link it from the run record, and run:

```bash
python3 scripts/validate_direction_run.py /absolute/path/IMMERSIVE-DIRECTION-RUN.json --phase visual-development
```

Before build, add the approved project-specific performance budget from [performance-budget.md](performance-budget.md), rerun dependency compatibility, link every applicable previsualization artifact, and run the direction record with `--phase build` plus the experience-contract and previsualization validators.

Exit code zero and the exact current artifact version are mandatory. A validator proves structure and reconciliation; the quality gates still decide whether the evidence deserves `strong`.

## Required record

Use the exact top-level keys enforced by `validate_direction_run.py`:

- `runId`, `version`, `mode`, and `status`.
- `corpusGrounding`: all core files at EOF; all 11 visual overview IDs; all four process IDs; current validator evidence; strong verdict.
- `intake`: complete ordered `rounds` containing question IDs, decisions, prerequisites settled before each round, answers, wait evidence, and Domain Modeling evidence; then Grilling complete, Domain Modeling complete, frontier empty, direct user-confirmation evidence, strong verdict. A dependent question cannot share a round with its prerequisite.
- `experienceContract`: exact positive version, ID/path, direct validator evidence, strong verdict.
- `evidenceLineage`: one row per territory with at least two website records from different mechanism families, process evidence, surface exclusion, and subject ownership.
- `territories`: exactly three distinct coherence sources; two complete survivors; one explicit rejection; complete journeys.
- `recommendedTerritoryId`: one survivor only.
- `scrollcraft`: applicability plus every required planning output and `adapterApplied: true` when applicable.
- `visualDevelopment`: required, exact manifest path, direct validator evidence, and strong verdict.
- `performanceBudget`: required before build, exact manifest path, direct validator evidence, and strong verdict.
- `dependencies`: current compatibility check plus direct validator evidence from [dependencies.md](dependencies.md).
- `qualityGates`: every applicable gate with direct evidence and verdict.
- `reconciliation`: blockers, missing artifacts, and overall verdict.

Update the record at every consequential change. A new contract version, user decision, territory change, visual board, motion study, budget, dependency change, or gate result increments the run version. Specialists receive its exact version and may only return evidence or a scope-change request.

## Completion rule

The direction run is not a report about work. It is the control plane for the work. A phase is complete only when the artifact exists, its facts match the current project state, its linked artifacts are current, the phase validator exits zero, and every qualitative verdict is supported by direct evidence. If any row is false, preserve the false state and stop at its dependent boundary.

# Experience contract

The experience contract converts briefs, approved decisions, live content, assets, and route evidence into four checkable artifacts. It is the phase boundary between shared understanding and concept approval. Attractive prose, a mood board, an isolated keyframe, or a partial storyboard cannot substitute for it.

For a project-backed Direction or Transformation, create or update the canonical `IMMERSIVE-EXPERIENCE-CONTRACT.json` in the project's established context/docs location; use the project root only when no such location exists. A Markdown rendering may accompany it for humans, but cannot replace the JSON gate artifact. In a chat-only or explicitly non-mutating engagement, maintain the same records in the working response and label approval blocked because the executable artifact is unavailable. Read an existing contract before asking questions. Fill facts from available sources; ask only for unresolved decisions. Never make the user repeat a settled answer merely to populate a table.

## Contract authority

- Explicit current user decisions govern scope and approval.
- Canonical project files govern recorded requirements and prior decisions.
- Inspected live/current sources govern public content and route truth.
- Internal strategy, discovery language, model summaries, and factual notes may inform reasoning but are not public copy.
- Unknown means `blocked`, not omitted, invented, or deferred to implementation.
- A request to focus on one fragment changes work order, not canonical deliverable scope. A focused artifact may be approved only when the user explicitly defines it as the complete canonical deliverable; otherwise change scope only through an explicit amendment after the affected responsibilities are named.
- Direction artifacts are not production. Completing this contract does not authorize asset generation, implementation, spending, or release.

## Contract header and scope control

Every contract begins with:

| Field | Required content |
|---|---|
| `CONTRACT-ID` | Stable project/direction ID |
| Version | Increment whenever scope, responsibility, route, approved copy, or chronology changes |
| Status | `exploration`, `approval-candidate`, or `approved` |
| Canonical scope | Exact surface/route deliverable and source evidence |
| Focus lens | Current fragment being explored; never a scope amendment |
| Approval target | Exact canonical scope and contract version the user is being asked to approve |
| Source snapshot | Files, URLs/surfaces, CMS/content snapshot, prior decisions, and inspection time |
| Amendments | `SCOPE-CHANGE-*` rows with before, after, affected responsibilities, and explicit user approval |

Only a complete canonical-scope contract with all four artifacts `strong` may become `approval-candidate`. Only the user may move that exact version to `approved`. A specialist receives the current contract version and must report any drift; it cannot silently narrow, reinterpret, or supersede the scope.

## Canonical JSON and executable gate

Use these exact top-level keys and record keys; the tables below explain their meaning:

```json
{
  "contractId": "CONTRACT-*",
  "version": 1,
  "status": "exploration | approval-candidate | approved",
  "canonicalScope": {
    "target": "...",
    "sourceEvidence": ["source#location"],
    "focusLens": "...",
    "approvalTarget": "...",
    "sourceSnapshot": ["source@version-or-time"],
    "amendments": []
  },
  "routes": [{
    "id": "ROUTE-*", "kind": "...", "destination": "...",
    "navigationCopyId": "COPY-*", "visitorJob": "...", "authority": "...",
    "status": "required | existing | optional | forbidden | blocked",
    "entryHandoff": "...", "states": ["default"], "verdict": "strong"
  }],
  "copy": [{
    "id": "COPY-*", "text": "...", "provenance": "live copy",
    "authority": "source#location", "authorityType": "live-source",
    "transformation": "verbatim", "uses": ["ROUTE-*", "STATE-*"],
    "verdict": "strong"
  }],
  "responsibilities": [{
    "id": "RESP-*", "obligation": "...", "authority": "source#location",
    "truthState": "...", "routeIds": ["ROUTE-*"], "stateIds": ["STATE-*"],
    "reachability": "...", "parity": {
      "desktop": "...", "mobile": "...", "reducedMotion": "...", "fallback": "..."
    },
    "copyIds": ["COPY-*"], "assetIds": ["ASSET-*"],
    "required": true, "verdict": "strong"
  }],
  "storyboards": [{
    "territoryId": "TERRITORY-*", "survivor": true,
    "coverage": "opening-to-resolution", "states": [{
      "id": "STATE-*", "order": 1, "routeId": "ROUTE-*", "mode": "opening",
      "responsibilityIds": ["RESP-*"], "copyIds": ["COPY-*"],
      "assetIds": ["ASSET-*"], "startComposition": "...", "inputCause": "...",
      "transformation": "...", "endComposition": "...",
      "causalHandoff": "STATE-next | terminal", "agency": "...",
      "parity": {
        "desktop": "...", "mobile": "...", "reducedMotion": "...", "fallback": "..."
      },
      "verdict": "strong"
    }]
  }],
  "reconciliation": {
    "obligationCount": 0, "mappedCount": 0, "unmappedIds": [],
    "inventedIds": [], "unresolvedIds": [], "routeCount": 0,
    "storyboardStateCount": 0, "placeholderCount": 0,
    "blockers": [], "exclusions": []
  }
}
```

Copy provenance and `authorityType` must pair exactly:

| Provenance | Required `authorityType` |
|---|---|
| `live copy` | `live-source` |
| `approved new copy` | `explicit-user-approval` |
| `placeholder` | `placeholder` |

Run the bundled validator before requesting direction approval:

```bash
python3 scripts/validate_experience_contract.py /absolute/path/IMMERSIVE-EXPERIENCE-CONTRACT.json --phase approval
```

Run it again before build handoff:

```bash
python3 scripts/validate_experience_contract.py /absolute/path/IMMERSIVE-EXPERIENCE-CONTRACT.json --phase build
```

Resolve `scripts/` relative to the installed skill directory. Exit code zero and a `PASS` line are mandatory. On `FAIL`, preserve the exact errors in the protocol ledger, correct the contract or report the blocked evidence/decision, and rerun. Manual confidence, a quality-gate narrative, a compact response, or a specialist opinion cannot substitute for validator success. If the validator runtime is unavailable, advancement is blocked.

## `CONTRACT-route-inventory`

Enumerate every route, same-page chapter, navigation action, and required handoff named by canonical sources or observed on the current surface.

| Field | Required content |
|---|---|
| `ROUTE-ID` | Stable route or anchor ID |
| Kind | Route, chapter anchor, external destination, or action |
| Exact destination | Current/required path, anchor, URL, or unresolved destination |
| Navigation copy | `COPY-ID` for every visible label |
| Visitor job | Why this destination exists |
| Authority | Source file/URL and exact location or explicit user decision |
| Status | Required, existing, optional, forbidden, or blocked |
| Entry/handoff | Where it appears and how the visitor reaches/leaves it |
| States | Relevant default, active, loading, empty, error, or return states |
| Verdict | `strong`, `needs work`, or `reject` |

Completion requires every navigation item to resolve to a truthful destination, every required destination to have an access path, and every optional route to have a real visitor job. Never invent a route to make navigation look complete. If a source says a route is conditional, preserve that condition rather than silently creating it.

## `CONTRACT-copy-provenance`

Record every visitor-visible string proposed in a concept, storyboard, visual, prototype, or build—including navigation, headings, labels, calls to action, quotations, content titles, data/fixture text, empty/error states, and utility copy.

| Field | Required content |
|---|---|
| `COPY-ID` | Stable string ID |
| Exact string | Verbatim visible text |
| Provenance | `live copy`, `approved new copy`, or `placeholder` |
| Authority | Source file/URL plus exact location, or explicit approval decision |
| Transformation | Verbatim, reordered, shortened, rewritten, or new |
| Uses | Every `ROUTE-ID`, `RESP-ID`, and `STATE-ID` where it appears |
| Verdict | `strong`, `needs work`, or `reject` |

The three provenance values are exhaustive:

- `live copy` is verbatim from an inspected current public/canonical content source. Cite it exactly.
- `approved new copy` is the exact string the user or authorized content owner explicitly approved for public use. A model recommendation is not approval.
- `placeholder` is visibly marked `[PLACEHOLDER]` anywhere it appears in a visual or prototype and cannot be presented as final-looking public copy.

Facts are not automatically copy. Language found only in internal strategy, discovery material, a transcript, unapproved model-generated material, or rationale remains internal until it independently qualifies as live copy or receives explicit new-copy approval. Humanizer or another writing skill may improve a proposal; it cannot grant approval. No visitor-visible string is exempt because it is “only a concept label,” “obvious navigation,” or “temporary fixture text.”

## `CONTRACT-responsibility-map`

Map each independently required or experientially distinct obligation. Represent a collection through its source, selection rule, ordering, reachability, and fallback; enumerate individual records only when canonical scope names them individually.

| Field | Required content |
|---|---|
| `RESP-ID` | Stable responsibility/content ID |
| Atomic obligation | One requirement, item, state, or action |
| Authority | Source file/URL and exact location or explicit decision |
| Truth/current state | Verified content/state; never assumed |
| Required location | `ROUTE-ID` and surface/route/template responsibility |
| Story placement | One or more `STATE-ID`s |
| Reachability | Direct path, label, and interaction |
| Parity | Desktop, mobile, reduced-motion, and fallback treatment |
| Sources | Applicable `COPY-ID`s plus asset, content, interaction, or semantic-source IDs; `copyIds` may be empty when no visitor-visible text appears |
| Verdict | `strong`, `needs work`, or `reject` |

End the map with a reconciliation block: authoritative obligation count, mapped count, unmapped IDs, invented IDs, unresolved IDs, and coverage verdict. Coverage is `strong` only when unmapped and invented are both zero and every required item remains directly reachable in each promised experience variant. “Implementation will restore it” is a rejection, because implementation cannot repair a concept that never assigned the responsibility.

## `CONTRACT-state-storyboard`

Use real `RESP-ID`, applicable `COPY-ID`, route, and asset/content records to storyboard the complete scoped experience from opening through resolution and required route handoffs.

| Field | Required content |
|---|---|
| `STATE-ID` | Stable chronological state ID |
| Location | `ROUTE-ID`, chapter, and surface mode |
| Real evidence | Exact `RESP-ID`, applicable `COPY-ID`, and asset/content/interaction IDs active here; `copyIds` may be empty when the state has no visitor-visible text |
| Start composition | Focal hierarchy, scale, crop, density, and orientation before input |
| Input/cause | Scroll, time, click, pointer, media event, or normal document flow |
| Transformation | What meaningfully changes and why a still cannot do the same job |
| End composition | Resulting hierarchy and stable information state |
| Causal handoff | How this state prepares, causes, proves, transforms, or resolves the next |
| Agency | Progress, reversal/exit, hold/release, and direct-access behavior |
| Parity | Desktop, mobile, reduced-motion, and fallback expression |
| Verdict | `strong`, `needs work`, or `reject` |

Completion requires:

1. Opening, proof, reading, decision/utility, peak, release, and final resolution are represented wherever the source scope requires them.
2. Every required `RESP-ID` appears in at least one state and remains directly reachable.
3. Every claimed immersive passage contains at least three consecutive, causally linked state rows with different information or meaning—not three animation keyframes of one still idea.
4. Calm/native-scroll sections still receive intentional states and causal handoffs; they cannot become a generic remainder after one directed passage.
5. Each surviving territory receives a complete chronology using real evidence before presentation. A fragment-only study may be labeled `exploratory fragment`; it cannot represent a broader direction, approved concept, winning territory, or production basis.

## Advancement gate

Before generating territories, complete route inventory, copy provenance for known/current strings, and the responsibility map. For each territory, create the full state storyboard and reconcile it back to those three artifacts. Generate three structurally different territories, reject the weakest, and present only survivors whose four contract artifacts are `strong`.

Compact-output preference, deadline, exhaustion, sunk intake time, a request to approve only the current fragment, a promise that remaining work will follow, or reliance on implementation to restore omitted obligations never satisfy the advancement gate. These pressures may reduce narration, not evidence or scope.

Approval language is exact. Until the gate passes, use `exploratory fragment`, `incomplete territory`, or `blocked direction`. Reserve `recommended direction`, `approved concept`, and `ready for next phase` for a complete canonical-scope contract with no blocking row.

Every approval request, however compact, states the contract ID/version, canonical approval target, route count, atomic responsibility mapped/total count, storyboard state count, placeholder count, blocker count, and explicit exclusions. The detailed tables may remain in the contract artifact; the counts may not be hidden.

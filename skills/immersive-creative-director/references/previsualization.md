# Still-first previsualization

This is the blocking production protocol for continuity-dependent **generated** motion. It applies when clips, video, image sequences, generated camera travel, or connected animated scenes depend on a recurring product, person, character, object, environment, material system, or visual world. It also applies when an approved still layout has only one frame but the proposed motion requires several visually distinct endpoints.

It does not force generated stills when the work uses an already-produced authentic film, purely semantic DOM motion, a procedural system whose state can be proved directly, or a real 3D model that supplies canonical renders. Those routes still need equivalent approved visual states and transition evidence when continuity matters. Never label one source photo, a text storyboard, a prompt, or a model's confidence as a multi-state visual proof.

The mandatory order is:

**approved concept and still-generation authority → source-authority audit → canonical visual anchor → rendered still for every dependent state → numbered state-board approval → adjacent transition graph → medium approval → conditional external-provider/media approval → one-edge-at-a-time generation → visual continuity review → assembly and responsive verification → build**

No video generator, video-capable provider, interpolation service, or continuity-dependent build may be invoked before the applicable gate passes. “Use whatever tool,” urgency, provider claims of consistency, and a beautiful hero still do not waive this sequence.

## 1. Declare the continuity scope

Create `IMMERSIVE-PREVISUALIZATION.json` beside the approved experience contract whenever this protocol applies. The approved contract must first declare the protocol applicable, list every dependent `STATE-*`, and reserve the exact `PREVIS-*` manifest ID. Link the exact contract ID/version, state why continuity is required, identify whether the graph is linear or branching, attach the complete contact-sheet evidence, and list every required edge pair. The validator loads both files and computes coverage; typed IDs or self-reported counts alone are not evidence.

Use enough rendered states to prove every semantic, compositional, object, camera, environment, and handoff change. Do not copy a tutorial's scene count. Five or eight frames may suit one film; two may prove one bounded transformation; a branching experience may need more. State count follows the approved story and risk, never a recipe.

Before generating a still, record that the concept is approved and that still generation is authorized. Direction approval alone is not production authority. Continue reversible source audit and specification while authority is pending.

## 2. Lock truthful sources and one canonical anchor

Inspect authentic product, person, place, brand, geometry, copy-safe, and layout sources first. Authentic evidence outranks generated resemblance. For a real product or person, attach the real source assets to generation and prohibit invented geometry, logos, features, identity, or claims.

Build a proportional source lock and declare its mode: `authentic-reference` for a real product, person, place, or supplied identity; `original-generated-world` for a new authored world; or `canonical-model` for a controlled 3D/source model. Authentic IDs are mandatory only for the first mode. Every mode still needs an approved canonical anchor, fixed traits, invalid traits, and direct evidence.

Record:

- authentic source IDs and authority order;
- one canonical anchor state for the recurring subject/world, plus additional canonical angle or environment anchors only when one view cannot prove the required identity;
- fixed traits that cannot drift;
- variable traits that may change only because the approved story requires them;
- invalid traits and failure states;
- version and direct approval evidence.

Use Codex/OpenAI image generation for constrained still exploration when it is available and authorized. Another still-image tool may be chosen only for a named capability gap or an explicit user preference. Generate and review the anchor before dependent states. Do not produce an uncontrolled batch of unrelated “cinematic options” and choose a style after the fact.

## 3. Render the complete state board before motion

Every transition endpoint must exist as an inspectable still asset. Evidence locators must resolve to real, structurally decodable local media files so the gate cannot pass on invented URLs or asset IDs. Each full-size state must have distinct visual content, and the contact sheet must be a separate image. Map each `PREVIS-STATE-*` one-to-one to the applicable canonical `STATE-*` record and record:

- image asset ID and its authentic/generated source IDs;
- semantic job and why this state is distinct;
- composition, focus, hierarchy, scale, crop, and copy-safe region;
- subject identity and fixed continuity traits;
- environment topology or explicit `not applicable` rationale;
- camera angle, distance, lens/framing intent, and direction;
- lighting, material, palette, texture, and grade continuity;
- structured desktop and mobile treatments naming the asset, method, direct inspection evidence, and whether subject, action, hierarchy, and copy-safe meaning survived;
- reduced-motion and unavailable-heavy-media parity;
- direct approval evidence and verdict.

Generate one state at a time from the approved source lock and the nearest approved state. Preserve the state ID and asset version. If an image changes a fixed trait, introduces an unsupported object, breaks topology, loses the intended focal hierarchy, or cannot support its copy/viewport role, reject it before continuing.

Present a numbered contact sheet containing every state at a size that permits real inspection. Labels belong outside the artwork unless visible text or interface is genuinely part of the approved scene. Review the individual full-size assets as needed; a tiny montage cannot prove hands, faces, product geometry, type, or edge continuity. The user approves the state board as a specific version. A verbal “looks good” attached only to the anchor does not approve the remaining states.

Run:

```bash
python3 scripts/validate_previsualization.py /absolute/path/IMMERSIVE-PREVISUALIZATION.json --contract /absolute/path/IMMERSIVE-EXPERIENCE-CONTRACT.json --phase state-board
```

Exit code zero is mandatory before transition planning or motion-provider selection.

## 4. Convert approved states into an edge graph

After state-board approval, define one `PREVIS-EDGE-*` for every required adjacent pair. A linear chain of `N` states has `N - 1` required forward edges. A branching experience lists every approved edge explicitly. Do not skip an intermediate state inside a vague long clip; merge states first only when they perform no distinct job and update the approved contract/manifest.

Each edge records:

- approved from/to state IDs and governing `SHOT-*` IDs;
- the single semantic and transition job;
- subject action and environment change;
- camera action, direction, speed, duration, first hold, and exit hold;
- identity/material/topology locks;
- negative constraints derived from this subject's known failure risks;
- recommended method and why a simpler method loses;
- whether an external service is involved, plus the named provider or `none` when no provider is needed;
- separately inspected desktop and mobile treatment evidence;
- exact regeneration boundary;
- controlled fallback using the approved endpoints;
- edge approval, generated-output IDs, and later review evidence.

Negative constraints are project-derived. A tutorial's “no people, text, or UI” is not universal doctrine. Require those exclusions only when the approved scene and assets call for them.

Choose the medium separately for every edge. Many connected states are better served by layered stills, a compact image sequence, a mask/material transition, DOM/SVG, or controlled 3D than by video. “The whole site should feel cinematic” is not a reason to make every edge a clip.

## 5. Approve the provider and media only after the edge plan

Tool choice follows the approved edge requirements. The state board should normally be achievable with Codex/OpenAI image generation; motion may later use any approved provider that satisfies the edge's start/end control, identity fidelity, camera behavior, duration, aspect ratio, cost, privacy, and export needs. Midjourney, Gemini, Higgsfield, Runway, or another named service may be appropriate; none is mandatory, and provider branding never enters the creative doctrine.

Before a video or external-service edge, record the exact provider in the approved-provider list, expected cost/credits and numeric ceiling, source assets uploaded, approved edge scope, integer regeneration limit, continuity risk, fallback, and direct media-approval evidence. `whatever`, `any`, `pending`, and other unnamed providers fail validation. Blanket delegation such as “pick whatever provider” permits a recommendation, not an unnamed spend or generation call.

Run:

```bash
python3 scripts/validate_previsualization.py /absolute/path/IMMERSIVE-PREVISUALIZATION.json --contract /absolute/path/IMMERSIVE-EXPERIENCE-CONTRACT.json --phase motion
```

Exit code zero is mandatory before any planned edge generation. Named provider/media approval is required only for video or another external-service edge; provider-free edges explicitly record `provider: "none"` and `providerDecision: "not-required"`.

## 6. Generate and review one edge at a time

Generate only the approved pair. Preserve endpoint asset versions and output versions. Inspect the actual result, not the provider's description of it, for:

- first-frame fidelity to the source state;
- last-frame fidelity to the destination state;
- identity, geometry, material, topology, light, and grade through the middle;
- action/camera clarity and direction;
- no unapproved object, text, anatomy, interface, or environmental invention;
- a usable entry hold, exit hold, and clean connection to neighboring edges;
- behavior under reversal when the approved scroll contract requires it.

Reject an edge that is ambiguous, visually drifts, hides a transition error in motion blur, or lands on a merely similar endpoint. Regenerate only within the approved boundary. If targeted attempts fail, simplify the action, reopen a state, change medium/provider through approval, or use the specified layered/sequence fallback. Never accept a continuity defect because a model says it is fixed or because the rest of the clip is attractive.

Assemble only reviewed edges. Inspect every join chronologically and in reverse where relevant. Media should behave as an integrated scene system, not a visible embedded player. Do not turn the complete site into one pinned movie by default; use normal scroll and lower-intensity page modes wherever they better serve proof, reading, decision, and utility.

## 7. Re-art-direct responsive motion and verify build readiness

The desktop state board does not approve mobile. If CSS cropping hides the subject, changes the action, removes copy-safe space, or breaks the start/end relationship, create and approve alternate mobile states and edges or choose a different responsive method. A separately framed edit is required when the original asset cannot preserve meaning. Reduced-motion and fallback routes use the approved state order rather than an unrelated static page.

Before implementation handoff, every required edge must have output IDs plus resolvable output evidence, direct visual evidence for first/intermediate/last/handoff review states, responsive treatment, fallback, and no blocker. Output and review fields may remain honestly empty at the motion-approval phase; writing `pending` is not review evidence and build validation requires observed evidence. Local images must be structurally decodable and content-distinct; local video outputs must contain a playable video stream verified through `ffprobe`. If that verifier is unavailable, video build validation is blocked. Run:

```bash
python3 scripts/validate_previsualization.py /absolute/path/IMMERSIVE-PREVISUALIZATION.json --contract /absolute/path/IMMERSIVE-EXPERIENCE-CONTRACT.json --phase build
```

This pass joins—but does not replace—the experience-contract build validator and qualitative quality gates. Code or layout assembly begins only after both applicable artifacts pass.

## Canonical manifest shape

Use these exact top-level keys and preserve stable IDs:

```json
{
  "previsualizationId": "PREVIS-*",
  "version": 1,
  "contractId": "CONTRACT-*",
  "contractVersion": 1,
  "status": "exploration | state-board-approved | motion-approved | assembled",
  "continuityScope": {
    "required": true,
    "reason": "...",
    "topology": "linear | branching",
    "sourceSnapshot": ["source@version"],
    "contractStateIds": ["STATE-*"],
    "contactSheetEvidence": {
      "type": "local-file",
      "locator": "/absolute/path/contact-sheet.png",
      "mediaType": "image/png",
      "inspectedAt": "ISO-8601 timestamp"
    },
    "requiredEdgePairs": ["PREVIS-STATE-00->PREVIS-STATE-01"]
  },
  "sourceLock": {
    "sourceMode": "authentic-reference | original-generated-world | canonical-model",
    "authenticSourceIds": ["ASSET-*"],
    "anchorStateId": "PREVIS-STATE-00",
    "fixedTraits": ["..."],
    "variableTraits": ["..."],
    "invalidTraits": ["..."],
    "approvalEvidence": "...",
    "verdict": "strong"
  },
  "states": [{
    "id": "PREVIS-STATE-00",
    "order": 0,
    "contractStateIds": ["STATE-*"],
    "imageAssetId": "ASSET-*",
    "imageEvidence": {
      "type": "local-file",
      "locator": "/absolute/path/state.png",
      "mediaType": "image/png",
      "inspectedAt": "ISO-8601 timestamp"
    },
    "sourceAssetIds": ["ASSET-*"],
    "semanticJob": "...",
    "composition": "...",
    "subjectIdentity": "...",
    "environmentTopology": "...",
    "camera": "...",
    "lighting": "...",
    "copySafe": "...",
    "responsive": {
      "desktop": {
        "method": "separate-asset | same-asset-verified | procedural-reflow",
        "assetId": "ASSET-*",
        "visualEvidence": {
          "type": "local-file",
          "locator": "/absolute/path/desktop.png",
          "mediaType": "image/png",
          "inspectedAt": "ISO-8601 timestamp"
        },
        "inspectionEvidence": "...",
        "meaningPreserved": true
      },
      "mobile": {
        "method": "separate-asset | same-asset-verified | procedural-reflow",
        "assetId": "ASSET-*",
        "visualEvidence": {
          "type": "local-file",
          "locator": "/absolute/path/mobile.png",
          "mediaType": "image/png",
          "inspectedAt": "ISO-8601 timestamp"
        },
        "inspectionEvidence": "...",
        "meaningPreserved": true
      }
    },
    "parity": {"reducedMotion": "...", "fallback": "..."},
    "approvalEvidence": "...",
    "verdict": "strong"
  }],
  "edges": [{
    "id": "PREVIS-EDGE-00-01",
    "fromStateId": "PREVIS-STATE-00",
    "toStateId": "PREVIS-STATE-01",
    "contractShotIds": ["SHOT-*"],
    "job": "...",
    "action": "...",
    "camera": "...",
    "duration": "...",
    "exitHold": "...",
    "identityLocks": ["..."],
    "negativeConstraints": ["..."],
    "method": "layered-stills | image-sequence | short-clip | long-video | 3d | procedural | existing-authentic-video",
    "externalService": true,
    "provider": "none | named-provider",
    "responsive": {
      "desktop": {
        "method": "separate-asset | same-asset-verified | procedural-reflow",
        "assetId": "ASSET-*",
        "visualEvidence": {
          "type": "local-file",
          "locator": "/absolute/path/desktop-edge.png",
          "mediaType": "image/png",
          "inspectedAt": "ISO-8601 timestamp"
        },
        "inspectionEvidence": "...",
        "meaningPreserved": true
      },
      "mobile": {
        "method": "separate-asset | same-asset-verified | procedural-reflow",
        "assetId": "ASSET-*",
        "visualEvidence": {
          "type": "local-file",
          "locator": "/absolute/path/mobile-edge.png",
          "mediaType": "image/png",
          "inspectedAt": "ISO-8601 timestamp"
        },
        "inspectionEvidence": "...",
        "meaningPreserved": true
      }
    },
    "regenerationBoundary": "...",
    "fallback": "...",
    "outputAssetIds": [],
    "outputEvidence": [{
      "type": "local-file",
      "locator": "/absolute/path/output.mp4",
      "mediaType": "video/mp4",
      "inspectedAt": "ISO-8601 timestamp"
    }],
    "approvalEvidence": "...",
    "reviewEvidence": {
      "firstFrame": {
        "type": "local-file",
        "locator": "/absolute/path/first.png",
        "mediaType": "image/png",
        "inspectedAt": "ISO-8601 timestamp"
      },
      "intermediate": {
        "type": "local-file",
        "locator": "/absolute/path/middle.png",
        "mediaType": "image/png",
        "inspectedAt": "ISO-8601 timestamp"
      },
      "lastFrame": {
        "type": "local-file",
        "locator": "/absolute/path/last.png",
        "mediaType": "image/png",
        "inspectedAt": "ISO-8601 timestamp"
      },
      "handoff": {
        "type": "local-file",
        "locator": "/absolute/path/handoff.png",
        "mediaType": "image/png",
        "inspectedAt": "ISO-8601 timestamp"
      }
    },
    "verdict": "strong"
  }],
  "approval": {
    "conceptApproved": true,
    "stillGenerationAuthorized": true,
    "stateBoardApproved": true,
    "providerDecision": "pending | approved | not-required",
    "approvedProviders": ["named-provider"],
    "mediaApproved": false,
    "mediaApprovalEvidence": "",
    "approvalEvidence": ["..."],
    "costCeiling": {
      "unit": "USD | credits | included-plan | other | pending",
      "limit": 0,
      "description": "..."
    },
    "regenerationLimit": 0
  },
  "reconciliation": {
    "stateCount": 0,
    "edgeCount": 0,
    "expectedEdgeCount": 0,
    "unmappedContractStateIds": [],
    "missingEdgePairs": [],
    "unapprovedStateIds": [],
    "unapprovedEdgeIds": [],
    "blockers": []
  }
}
```

This block illustrates the exact record shape; it is not a ready-to-validate manifest. Repeat the complete state object for every state referenced by an edge, then set every reconciliation count/list to the computed truth before running the validator.

The validator supplies structural proof only. `QUALITY-previsualization` decides whether the actual stills, transitions, and responsive variants deserve approval.

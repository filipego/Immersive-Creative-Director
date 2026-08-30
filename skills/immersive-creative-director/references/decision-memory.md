# Approved decision memory

Conversation history is never the durable source of truth for an approved design. Maintain a human-readable project decision dossier from the first approval onward. Before beginning the next section, page, route, component, or production phase, write the approved unit into the dossier and reopen the latest affected records.

Use `IMMERSIVE-DECISION-MEMORY.md` at the project root. For a large site, keep it as the index and place page dossiers under `immersive-decisions/`; link every page dossier from the index. Store or reference approved visual evidence through stable project-relative paths so Markdown renders the image inside the dossier:

```markdown
![Approved homepage hero — desktop resting state](assets/approved/home-hero-v1.png)
```

## Required record for every approved unit

Create one versioned record for each approved site-wide system, page, section, component, transition, or responsive variant. Record:

- stable ID, version, status, route/page/parent, approval date, and direct approval evidence;
- embedded approved visuals for every consequential desktop, mobile, interaction, peak, utility, and reduced-motion state, with viewport/state labels, file path, provenance, and source asset;
- final copy and copy provenance;
- layout, grid, alignment anchors, dimensions, spacing, density, and breakpoint behavior;
- typography family and font file, weight/style, size, line height, tracking, casing, measure, and breakpoint values;
- color tokens and exact values, materials, borders, texture, lighting, and image treatment;
- imagery/video/3D sources, crops, focal points, aspect ratios, grades, layers, continuity locks, and asset paths;
- chronological motion states, triggers, scroll/input mapping, timing, easing, holds, handoffs, reversal, exit, and what remains still;
- responsive re-composition, touch/keyboard behavior, reduced-motion narrative parity, accessibility, loading, low-power, failure, and media fallbacks;
- implementation ownership: route, component, DOM/asset identifiers, dependencies, performance constraints, and acceptance evidence;
- entry from the previous unit, release into the next unit, unresolved items, linked contract/run/previsualization versions, and superseded record IDs.

Use exact values when approved. Label unresolved values explicitly; never silently convert an estimate or model proposal into an approved fact. If the user approves a visual but its reproducible specifications are incomplete, document the visual and mark the unit `approved-with-open-specification`; resolve those fields before dependent implementation.

## Approval boundary

Approval triggers documentation. Update the dossier immediately and show the user its path before advancing. Documentation records an approval; it does not manufacture one. A model-generated summary, chat transcript, screenshot without specifications, isolated JSON contract, or code implementation does not replace the dossier.

When a decision changes, create a new version, preserve the prior record as `superseded`, state what changed and why, update affected handoffs and assets, and reconcile linked contracts. Never overwrite history in a way that makes the former approved state unrecoverable.

## Continuity rule

Before touching a connected unit, read the current dossier records for the site-wide system, current page, adjacent sections, shared assets, and relevant transitions. Work from those records and actual files—not recalled conversation. A unit is not complete, and work may not advance past it, until its current approval is visually embedded, fully specified or explicitly open, linked, and saved.

# Immersive Creative Director

An evolving Codex skill for conceiving, transforming, critiquing, producing, and extending highly art-directed, animation-heavy, cinematic, spatial, narrative, and scroll-driven website experiences.

It replaces generic AI motion suggestions—automatic text reveals, arbitrary parallax, floating cards, decorative particles, and effect-heavy GSAP recipes—with subject-specific creative direction grounded in layout, imagery, motion, input, pacing, production reality, and story.

The bundled corpus is the skill's sole source of truth for design taste and creative judgment. Every invocation must read the complete corpus before asking design questions, generating concepts, critiquing work, or planning production. Generic pretrained taste, majority-web conventions, default AI patterns, and unstated outside references receive no aesthetic authority.

## What it does

- Generates three structurally different creative territories, rejects the weakest, develops two, and recommends one.
- Strengthens the protected idea instead of discarding it for a generic metaphor.
- Directs the complete experience across opening, proof, reading, decision, utility, and resolution.
- Builds and machine-validates a source-locked experience contract before approval: exact routes/navigation, copy provenance, atomic content responsibilities, and a real-content scoped-experience state storyboard.
- Treats motion as a narrative and compositional system rather than a quantity of effects.
- Preserves visually locked layouts and derives movement from observed crop, planes, reading order, handoffs, and negative space.
- Chooses among stills, layered images, image sequences, short clips, video, 3D, particles, DOM animation, and sound according to their irreplaceable job, cost, continuity risk, performance, and fallback.
- Runs a machine-validated still-first previsualization pipeline for connected generated motion: source-authority lock → canonical anchor → rendered state board → adjacent transition graph → conditional external-provider/media approval → reviewed outputs → build.
- Re-art-directs the experience for mobile and preserves narrative parity for reduced motion.
- Keeps concept, source assets, paid media, visual changes, implementation, and release approvals separate.
- Studies complete websites and videos through **Immersive Discovery**, admitting only evidence that changes a future decision.

## Operating modes

| Mode | Use it when |
| --- | --- |
| Direction | You have a brand, product, story, or rough idea and need original immersive concepts. |
| Transformation | You already have a still or visually locked layout and want to make the experience feel alive. |
| Critique | An existing animated site feels generic and you want an evidence-based diagnosis before redesigning it. |
| Production | The concept and relevant approvals are complete and Codex should build and verify the experience. |
| Immersive Discovery | You want to study a complete website or video and selectively evolve the skill. |

## Repository structure

```text
Immersive-Creative-Director/
├── README.md
├── .gitignore
└── skills/
    └── immersive-creative-director/
        ├── SKILL.md
        ├── agents/
        │   └── openai.yaml
        ├── scripts/
        │   ├── validate_experience_contract.py
        │   ├── validate_previsualization.py
        │   └── validate_visual_corpus.py
        ├── assets/
        │   └── reference-corpus/
        │       ├── manifest.json
        │       ├── corpus-overview.jpg
        │       ├── overviews/       # one overview sheet per source
        │       └── frames/          # 393 chronological captures
        └── references/
            ├── evidence-library.md
            ├── previsualization.md
            ├── reference-corpus.md
            ├── visual-reference-manifest.md
            └── ...
```

Only `skills/immersive-creative-director` is the installable skill. Repository documentation remains outside the runtime package.

## Install with Codex

Ask Codex to use its installed Skill Installer:

```text
Use $skill-installer to install the skill from
https://github.com/filipego/Immersive-Creative-Director/tree/main/skills/immersive-creative-director
```

The installer places it at:

```text
~/.codex/skills/immersive-creative-director
```

The skill becomes available on the next Codex turn.

## Manual installation

Clone the repository, then copy only the skill directory:

```bash
git clone https://github.com/filipego/Immersive-Creative-Director.git
mkdir -p ~/.codex/skills
cp -R Immersive-Creative-Director/skills/immersive-creative-director ~/.codex/skills/immersive-creative-director
```

If the destination already exists, review the changes before replacing it.

## Use it

### Create an original direction

```text
Use $immersive-creative-director.

I run a sustainable furniture company built around repairable pieces that become more personal over time. Give me an original immersive website direction.
```

### Transform a locked layout

```text
Use $immersive-creative-director.

This landing-page layout is visually locked. Make the complete experience feel immersive without changing typography, spacing, color, crops, imagery, content, or resting composition.
```

### Diagnose generic motion

```text
Use $immersive-creative-director.

This website has a video hero, pinned chapters, parallax, and text reveals, but it still feels generic. Diagnose why. Do not redesign it yet.
```

### Build after approval

```text
Use $immersive-creative-director.

The direction, layout changes, source assets, responsive behavior, and reduced-motion route are approved. Build and verify the complete experience in Codex.
```

### Evolve the skill

```text
Use $immersive-creative-director in Immersive Discovery mode.

Study this complete website or video and tell me whether it should change the skill. Do not update the installed package until the evidence pass is complete.
```

## How it works with other skills

Immersive Creative Director is the synthesis owner. Its complete internal corpus is mandatory on every invocation. After that grounding pass, it invokes complete installed execution skills according to the active mode and approved phase:

- **Impeccable** for substantive visual judgment and anti-generic critique.
- **Design DNA** for separating transferable mechanisms from recognizable reference identity.
- **Watch** for complete video chronology, including commercial exclusion and resumption.
- **Scrollcraft** for approved scroll-scene implementation.
- **Design Loop** for render-led iteration, with its Impeccable pass nested inside.
- **Filipe Flow** as the outer dispatcher for substantial multi-stage production.
- **Poteto Mode** only for a distinct general-code or skill-authoring phase not owned by Design Loop or Scrollcraft.
- **Browser Proof** for the final rendered browser surface.

Unavailable optional skills are reported rather than silently imitated or installed.

## Creative principles

- One central coherence source should govern the experience.
- Each motion family needs a story, composition, orientation, functional, tactile, or character job.
- Scroll authorship is allowed when its input contract remains legible and the transformation earns the hold.
- Proof, pricing, legal, forms, support, navigation, and other utility modes often need deliberate visual relief.
- Reference mechanisms may transfer; recognizable surface identity does not.
- A direction is not production-ready until its truthful assets, continuity, responsive route, fallbacks, and approvals are explicit.
- A focused artifact cannot become an approved direction for a broader canonical scope while any remaining required surface, content, route, or copy provenance is unresolved.
- A built site is not finished until the exact rendered surface is verified chronologically across relevant routes, inputs, viewports, loading, utility, and fallback states.

## Provenance

The skill was developed from a curated corpus of award-winning websites, educational videos, explicit creative preferences, production decisions, and matched RED/GREEN behavioral scenarios. The installed package contains the detailed written corpus, distilled operating judgment, and a machine-validated visual archive of 393 chronological captures across all 15 sources. Each source has an overview sheet; every frame is indexed by source, capture action, timestamp, checksum, and evidence record. References are evidence for transferable mechanisms and quality—not a catalog of surfaces to copy.

The visual archive is mandatory runtime evidence. On every invocation, the skill validates the archive, inspects all 15 overview sheets, and records a Visual Grounding Ledger before design questions or judgments. A selected or user-named reference also triggers chronological inspection of its detailed frames. If the images cannot be loaded, the design phase blocks rather than falling back to generic model taste.

## License

No open-source license has been selected yet. Add a license before encouraging unrestricted reuse or modification. MIT is a common choice for broad reuse with attribution and no warranty.

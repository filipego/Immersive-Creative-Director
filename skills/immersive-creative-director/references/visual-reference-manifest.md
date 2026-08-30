# Mandatory Visual Reference Manifest

This file binds the written doctrine to the recovered visual evidence. The image corpus is part of the skill, not supporting decoration. A design judgment is corpus-grounded only when both its written evidence record and its visual evidence have been inspected during the current invocation.

The machine manifest at `../assets/reference-corpus/manifest.json` is the source of truth for every frame path, capture title, timestamp, source URL, byte count, and SHA-256 checksum. The complete archive contains **15 references and 393 chronological frames**. `../assets/reference-corpus/corpus-overview.jpg` is a quick index; it does not replace the individual reference overviews.

## Mandatory visual-grounding protocol

Before questions, concepts, critique, or production planning:

1. Run `python3 scripts/validate_visual_corpus.py`. Exit code zero is required.
2. Use `view_image` to inspect every overview listed below during the current invocation. Reading filenames, Markdown descriptions, prior summaries, or the master sheet alone does not count as visual inspection.
3. Create an internal **Visual Grounding Ledger** with one row per reference: `reference ID`, `overview inspected`, `written evidence record read`, `transferable mechanism`, `surface identity excluded`, `detailed frames inspected`, and `verdict`.
4. Mark every row `complete` before substantive design work. A named reference, a selected mechanism, or a disputed judgment also requires chronological inspection of its individual frame directory and the matching entries in `manifest.json`.
5. Ground every territory, critique, or motion decision in at least one completed visual row and its written record. Cite the reference ID internally; transfer the mechanism and reject its recognizable subject, palette, artwork, typography identity, or exact sequence.

If `view_image` is unavailable, an overview is missing, the validator fails, or any ledger row remains incomplete, stop at the design boundary and report that the visual corpus could not be loaded. Do not substitute pretrained taste, live-link memory, prose-only grounding, or an approximate reference.

## Complete reference index

| Visual ID | Source | Frames | Mandatory overview | Detailed chronological frames | Written evidence |
|---|---|---:|---|---|---|
| `site-sondaven` | [Son Daven](https://sondaven.com/en) | 55 | `../assets/reference-corpus/overviews/site-sondaven.jpg` | `../assets/reference-corpus/frames/site-sondaven/` | `EVID-site-son-daven` |
| `site-lando-norris` | [Lando Norris](https://landonorris.com/) | 22 | `../assets/reference-corpus/overviews/site-lando-norris.jpg` | `../assets/reference-corpus/frames/site-lando-norris/` | `EVID-site-lando-norris` |
| `site-indigo-laboratory` | [Indigo Laboratory](https://indigo-laboratory.it/) | 11 | `../assets/reference-corpus/overviews/site-indigo-laboratory.jpg` | `../assets/reference-corpus/frames/site-indigo-laboratory/` | `EVID-site-indigo` |
| `site-noth` | [Noth.in](https://www.noth.in/) | 40 | `../assets/reference-corpus/overviews/site-noth.jpg` | `../assets/reference-corpus/frames/site-noth/` | `EVID-site-noth` |
| `site-mr-black` | [Mr Black case](https://mrblack-case.dolganev.com/) | 14 | `../assets/reference-corpus/overviews/site-mr-black.jpg` | `../assets/reference-corpus/frames/site-mr-black/` | `EVID-site-mr-black` |
| `site-santioni-spirits` | [Santioni Spirits](https://santionispirits.com/) | 30 | `../assets/reference-corpus/overviews/site-santioni-spirits.jpg` | `../assets/reference-corpus/frames/site-santioni-spirits/` | `EVID-site-santioni` |
| `site-become-a-yogi` | [Become a Yogi](https://www.become-a-yogi.com/) | 38 | `../assets/reference-corpus/overviews/site-become-a-yogi.jpg` | `../assets/reference-corpus/frames/site-become-a-yogi/` | `EVID-site-become-a-yogi` |
| `site-mesh3d` | [Mesh3D — The State of the Gallery](https://mesh3d.gallery/the-state-of-the-gallery) | 44 | `../assets/reference-corpus/overviews/site-mesh3d.jpg` | `../assets/reference-corpus/frames/site-mesh3d/` | `EVID-site-mesh3d` |
| `site-haoqi` | [Haoqi Design](https://haoqi.design/) | 17 | `../assets/reference-corpus/overviews/site-haoqi.jpg` | `../assets/reference-corpus/frames/site-haoqi/` | `EVID-site-haoqi` |
| `site-ride-radian` | [Ride Radian](https://www.rideradian.com/) | 15 | `../assets/reference-corpus/overviews/site-ride-radian.jpg` | `../assets/reference-corpus/frames/site-ride-radian/` | `EVID-site-ride-radian` |
| `site-pear` | [Pear](https://pear.no/) | 35 | `../assets/reference-corpus/overviews/site-pear.jpg` | `../assets/reference-corpus/frames/site-pear/` | `EVID-site-pear` |
| `video-QUI6Ug4cHnE` | [Creative skill process video](https://www.youtube.com/watch?v=QUI6Ug4cHnE) | 22 | `../assets/reference-corpus/overviews/video-QUI6Ug4cHnE.jpg` | `../assets/reference-corpus/frames/video-QUI6Ug4cHnE/` | `EVID-video-creative-skill-process` |
| `video-39IlNR-P3-Q` | [Reference-transfer and media-first video](https://www.youtube.com/watch?v=39IlNR-P3-Q) | 23 | `../assets/reference-corpus/overviews/video-39IlNR-P3-Q.jpg` | `../assets/reference-corpus/frames/video-39IlNR-P3-Q/` | `EVID-video-reference-transfer` |
| `video-GJxchJkk4Lk` | [Spatial production video](https://www.youtube.com/watch?v=GJxchJkk4Lk) | 9 | `../assets/reference-corpus/overviews/video-GJxchJkk4Lk.jpg` | `../assets/reference-corpus/frames/video-GJxchJkk4Lk/` | `EVID-video-spatial-production` |
| `video-ubH1ulaK-t4` | [Still-first previsualization video](https://www.youtube.com/watch?v=ubH1ulaK-t4) | 18 | `../assets/reference-corpus/overviews/video-ubH1ulaK-t4.jpg` | `../assets/reference-corpus/frames/video-ubH1ulaK-t4/` | `EVID-video-still-first-previsualization` |

## How to read the captures

The overview sheets contain evenly distributed frames from each complete recovered sequence so opening, middle, peak, utility, and resolution states remain visible in one inspection. The detailed directories preserve every recovered capture in chronological filename order. The machine manifest adds the capture action that produced each frame, making it possible to distinguish a menu state, internal page, scroll checkpoint, interaction state, video timestamp, or closing scene.

Still frames prove composition, hierarchy, density, continuity, state changes, and the visible consequences of interaction. The written chronology in `reference-corpus.md` and `evidence-library.md` explains timing, input mapping, scene causality, commercial exclusions, and limitations that a still cannot prove alone. Both evidence forms are mandatory and neither can replace the other.

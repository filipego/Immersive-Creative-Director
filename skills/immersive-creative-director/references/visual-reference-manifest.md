# Mandatory Website Visual-Taste Manifest

This file governs visual taste. Its eleven website captures are the only packaged images allowed to teach composition, spacing, scale, hierarchy, typography, color, imagery, camera language, scroll choreography, transition quality, and visual polish.

The machine manifest at `../assets/visual-taste-corpus/manifest.json` indexes **11 websites and 321 chronological frames** with paths, capture metadata, byte counts, and SHA-256 checksums.

## Mandatory visual-grounding protocol

Before questions, concepts, critique, or production planning:

1. Run `python3 scripts/validate_visual_corpus.py`. Exit code zero is required.
2. Use `view_image` to inspect every website overview below during the current invocation.
3. Complete an internal **Visual Grounding Ledger** with one row per website: `reference ID`, `overview inspected`, `written evidence read`, `transferable mechanism`, `surface identity excluded`, `detailed frames inspected`, and `verdict`.
4. Mark all eleven rows `complete`. A user-named website, selected mechanism, or disputed judgment also requires chronological inspection of its detailed frame directory and matching manifest entries.
5. Ground every territory, critique, and motion decision in completed website rows plus their written evidence. Transfer mechanisms; exclude recognizable subject matter, palette, artwork, type identity, and exact choreography.

If an overview cannot be inspected or validation fails, stop at the design boundary. The process-video corpus cannot fill a missing visual row.

## Website index

| Visual ID | Source | Frames | Mandatory overview | Detailed chronological frames | Written evidence |
|---|---|---:|---|---|---|
| `site-sondaven` | [Son Daven](https://sondaven.com/en) | 55 | `../assets/visual-taste-corpus/overviews/site-sondaven.jpg` | `../assets/visual-taste-corpus/frames/site-sondaven/` | `EVID-site-son-daven` |
| `site-lando-norris` | [Lando Norris](https://landonorris.com/) | 22 | `../assets/visual-taste-corpus/overviews/site-lando-norris.jpg` | `../assets/visual-taste-corpus/frames/site-lando-norris/` | `EVID-site-lando-norris` |
| `site-indigo-laboratory` | [Indigo Laboratory](https://indigo-laboratory.it/) | 11 | `../assets/visual-taste-corpus/overviews/site-indigo-laboratory.jpg` | `../assets/visual-taste-corpus/frames/site-indigo-laboratory/` | `EVID-site-indigo` |
| `site-noth` | [Noth.in](https://www.noth.in/) | 40 | `../assets/visual-taste-corpus/overviews/site-noth.jpg` | `../assets/visual-taste-corpus/frames/site-noth/` | `EVID-site-noth` |
| `site-mr-black` | [Mr Black case](https://mrblack-case.dolganev.com/) | 14 | `../assets/visual-taste-corpus/overviews/site-mr-black.jpg` | `../assets/visual-taste-corpus/frames/site-mr-black/` | `EVID-site-mr-black` |
| `site-santioni-spirits` | [Santioni Spirits](https://santionispirits.com/) | 30 | `../assets/visual-taste-corpus/overviews/site-santioni-spirits.jpg` | `../assets/visual-taste-corpus/frames/site-santioni-spirits/` | `EVID-site-santioni` |
| `site-become-a-yogi` | [Become a Yogi](https://www.become-a-yogi.com/) | 38 | `../assets/visual-taste-corpus/overviews/site-become-a-yogi.jpg` | `../assets/visual-taste-corpus/frames/site-become-a-yogi/` | `EVID-site-become-a-yogi` |
| `site-mesh3d` | [Mesh3D — The State of the Gallery](https://mesh3d.gallery/the-state-of-the-gallery) | 44 | `../assets/visual-taste-corpus/overviews/site-mesh3d.jpg` | `../assets/visual-taste-corpus/frames/site-mesh3d/` | `EVID-site-mesh3d` |
| `site-haoqi` | [Haoqi Design](https://haoqi.design/) | 17 | `../assets/visual-taste-corpus/overviews/site-haoqi.jpg` | `../assets/visual-taste-corpus/frames/site-haoqi/` | `EVID-site-haoqi` |
| `site-ride-radian` | [Ride Radian](https://www.rideradian.com/) | 15 | `../assets/visual-taste-corpus/overviews/site-ride-radian.jpg` | `../assets/visual-taste-corpus/frames/site-ride-radian/` | `EVID-site-ride-radian` |
| `site-pear` | [Pear](https://pear.no/) | 35 | `../assets/visual-taste-corpus/overviews/site-pear.jpg` | `../assets/visual-taste-corpus/frames/site-pear/` | `EVID-site-pear` |

Still frames establish composition, hierarchy, density, continuity, state changes, and visible interaction consequences. Written website chronology supplies timing, input mapping, scene causality, route coverage, and limitations. Both are required for website-grounded judgment.

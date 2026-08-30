# Mandatory Video Process-Evidence Manifest

This file governs how immersive work is conceived and produced. The four full timestamped transcripts are the source evidence; the distilled `EVID-video-*` records in `evidence-library.md` and detailed video sections in `reference-corpus.md` are the executable process knowledge.

The process corpus has **zero visual-taste authority**. Its archived video frames are secondary demonstration evidence only. They may clarify a named on-screen step, before/after demonstration, tool state, or production claim. They cannot determine layout, spacing, typography, palette, imagery, composition, animation taste, or aesthetic quality, and they never enter the Visual Grounding Ledger.

## Mandatory process-grounding protocol

1. Run `python3 scripts/validate_process_corpus.py`. Exit code zero is required.
2. Read every `EVID-video-*` record in `evidence-library.md` and every full video section in `reference-corpus.md` on every invocation. Complete a four-row **Process Evidence Ledger**: `video ID`, `distilled record read`, `full section read`, `active production principles`, `transcript consulted`, and `verdict`.
3. Read a packaged transcript completely to EOF when the user names that video, disputes its lesson, asks to inspect the source, or the current work enters a production branch materially governed by that video. Record `transcript consulted = complete`. Otherwise record `not activated`; the distilled records remain mandatory.
4. Consult archived frames only when a transcript/process record points to a visual demonstration whose visible state is necessary to resolve the current decision. Treat the frame as demonstration evidence, never design inspiration.
5. Translate vendor-specific tooling into available Codex/OpenAI, authentic-asset, image-generation, image-sequence, 3D, or separately approved video workflows while preserving the production principle.

## Process source index

| Process ID | Source | Full transcript | Distilled record | Archived demonstration frames |
|---|---|---|---|---|
| `video-QUI6Ug4cHnE` | [Creative skill process](https://www.youtube.com/watch?v=QUI6Ug4cHnE) | `../assets/process-corpus/transcripts/video-QUI6Ug4cHnE.vtt` | `EVID-video-creative-skill-process` | `../assets/process-corpus/frames/video-QUI6Ug4cHnE/` |
| `video-39IlNR-P3-Q` | [Reference transfer and media-first workflow](https://www.youtube.com/watch?v=39IlNR-P3-Q) | `../assets/process-corpus/transcripts/video-39IlNR-P3-Q.vtt` | `EVID-video-reference-transfer` | `../assets/process-corpus/frames/video-39IlNR-P3-Q/` |
| `video-GJxchJkk4Lk` | [Spatial production workflow](https://www.youtube.com/watch?v=GJxchJkk4Lk) | `../assets/process-corpus/transcripts/video-GJxchJkk4Lk.vtt` | `EVID-video-spatial-production` | `../assets/process-corpus/frames/video-GJxchJkk4Lk/` |
| `video-ubH1ulaK-t4` | [Still-first previsualization workflow](https://www.youtube.com/watch?v=ubH1ulaK-t4) | `../assets/process-corpus/transcripts/video-ubH1ulaK-t4.vtt` | `EVID-video-still-first-previsualization` | `../assets/process-corpus/frames/video-ubH1ulaK-t4/` |

The machine manifest at `../assets/process-corpus/manifest.json` preserves transcript locators and all 72 recovered demonstration frames. The frames remain archived so evidence is not lost; runtime taste grounding remains exclusively website-based.

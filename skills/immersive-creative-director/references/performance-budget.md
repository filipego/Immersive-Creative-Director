# Project-specific performance and device budget

Before build authorization, create `IMMERSIVE-PERFORMANCE-BUDGET.json`. The budget is a design constraint: it decides how much media, depth, state, and preloading the approved experience can honestly support. Do not borrow universal numbers from another project or wait until implementation to discover that the concept only works warm on a flagship device.

## Required decisions

- Named desktop and mobile viewport/input/device classes; add tablet, keyboard-only, low-power, or other surfaces when the project promises them.
- Positive numeric ceilings for initial transfer, initial heavy media, largest single asset, concurrent video decoders, minimum acceptable animation frame rate, maximum long task, and maximum layout shift.
- A memory-risk ceiling stated in project terms.
- Loading/readiness and adjacent prefetch strategy.
- Responsive asset strategy and when a separate mobile production is required.
- Low-power, no-WebGL, reduced-motion, and unavailable-heavy-media routes preserving the approved chronology and visitor task.
- Failure recovery that keeps truthful content, navigation, and conversion available.
- Cold/warm load, chronology, memory, responsive selection, input, and fallback measurement plan.
- Direct approval evidence and verdict.

Use the smallest credible budget that preserves the concept. If measurement later fails, reduce or segment the medium before weakening content, agency, or narrative parity. A better machine is not the fallback.

Run:

```bash
python3 scripts/validate_performance_budget.py /absolute/path/IMMERSIVE-PERFORMANCE-BUDGET.json
```

Build readiness additionally requires measured evidence against this exact version. Record observed values and the target surface in the direction run or final browser-proof artifact. Numeric presence is structural proof; direct browser/device measurement determines the rendered verdict.

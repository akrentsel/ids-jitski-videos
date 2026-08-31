# IDS Explainer — Inductive Deductive Synthesis (arXiv 2605.23109)

~2.5 min, 16:9, 1080p60. Audience: technical (undergrad+), light domain terms OK.
Arc: Problem-Solution. Voice: OpenAI tts-1-hd "nova".

Core analogy: **the proof grows with the code, and unfinished work is an
explicit IOU ("Admitted") that the type-checker still grades.**

Flagship scene (user request): incremental synthesis — full spec on the left,
implementation and proof columns start empty and fill in *together*, step by
step, with Rocq grading each partial state. Yellow = Admitted IOU, green =
proven/filled. Uses the counter example from Fig. 2 of the paper.

## Palette

- BG `#0D1117`
- Spec / blue `#58A6FF`
- Impl / orange `#E3B341`... no — impl = white/`#E6EDF3` code, panel accent `#BC8CFF` (purple)
- Proof / green `#3FB950`
- Admitted / yellow `#D29922`
- Error / red `#F85149`
- Dim text `#8B949E`
- Font: Menlo (macOS)

## Scenes

- **S1 Hook** — agents write code well; some software must be *provably*
  correct; distributed systems interleavings visual.
- **S2 Problem** — verification triangle (spec/impl/proof); months of expert
  effort; SOTA agents 2/7; "code first, whole proof after" = cliff with no
  feedback.
- **S3 Insight (FLAGSHIP)** — three panels: SPEC (full from start), IMPL
  (empty), PROOF (empty). Steps alternate impl/proof growth; Admitted IOUs in
  yellow; Rocq badge grades each step green; IOUs get paid off until both
  columns complete. Progress bars grow together.
- **S4 Backtrack** — a failing step = signal; red ✗ → revert to last good
  state → new strategy (per-key split) → greens cascade.
- **S5 Results** — 7/7 vs 2/7 bar comparison; 6.8h / $106 vs months; up to 3×
  throughput of hand-written verified systems.
- **S6 Outro** — human-labor bottleneck → compute problem; title card.

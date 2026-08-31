# Paper Animation Videos: IDS & Jitski

Manim CE animations for two papers, produced with the Ludwig explainer-video
pipeline.

## IDS — Inductive Deductive Synthesis

Paper: [Inductive Deductive Synthesis: Enabling AI to Generate Formally
Verified Systems](https://arxiv.org/abs/2605.23109) (arXiv 2605.23109)

- `incremental-synthesis/final.mp4` — full narrated explainer (~3 min,
  dark theme): the problem, the incremental spec/impl/proof insight,
  backtracking, results.
- `incremental-synthesis/ids_incremental_synthesis.mp4` — silent
  diagram-styled cut of the two core scenes (incremental synthesis and
  backtracking), light theme with Century Schoolbook styling.
- `script.py` — narrated dark-theme scenes, timed to the ElevenLabs
  voiceover (regenerate audio with `generate_audio.py`).
- `script_styled.py` — the silent light/diagram-styled scenes.
- `script_light.py` — thin palette override that renders the dark scenes
  on a light GitHub-style theme.

## Jitski — Just-in-Time Systems

Paper: [The Time is Here for Just-in-Time Systems: Challenges and
Opportunities](https://arxiv.org/abs/2605.24096) (arXiv 2605.24096)

- `jitski/jitski_architecture.mp4` — silent animation of the Jitski
  synthesis pipeline (Figure 1): spec cards → Planner → Coder →
  Evaluation, the Critic feedback loop, and the every-N-iterations
  Auditor catching a reward hack.
- `jitski/script.py` — the scene source.

## Rendering

Requires Manim CE v0.20.1, ffmpeg, LaTeX, and the TeX Gyre Schola
OpenType fonts installed (Century Schoolbook clone; ships with TeX Live
under `fonts/opentype/public/tex-gyre/`).

```bash
manim -qh script.py <SceneName>   # 1080p60
```

Styling conventions (both projects): white background, thin dark
outlines, Google Slides pastel fills, serif titles/captions via a
2x-render-then-scale text helper (works around collapsed word spacing
in small serif text), monospace Menlo for code.

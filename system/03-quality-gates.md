# Quality gates — evidence required
| Domain | Gate (all must pass) |
|---|---|
| Code | builds; lints; tests pass (new behavior has a test); no secrets (`git diff | grep -iE 'key|secret|token'`); runs end-to-end once |
| Web/UI | renders in a real browser (playwright-cli screenshot); responsive 375/1440; no console errors; WCAG AA contrast |
| Video | `ffprobe` duration/resolution/fps match spec; audio present & not clipping; watched 3 sample frames (start/middle/end); captions synced |
| Image | matches brief (subject, style, aspect, text spelled right); no artifacts on zoom; correct format/size |
| Animation | 60fps target, no layout thrash; reduced-motion fallback; loops cleanly if looping |
| Logo | works at 16px & 1024px, mono + reversed versions, original (no lookalike of a real brand) |
| SVG | valid XML (`xmllint`), has viewBox, no fixed width/height unless asked, optimized (svgo), renders in browser |
| Audio | LUFS ≈ -16 (voice) / -14 (music); no clicks; correct sample rate |
| Research | every claim has a source; conflicts noted; date-sensitive facts dated |
Failure → fix → re-verify (max 3 loops) → else report blocker with evidence.

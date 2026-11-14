---
name: "hyperframes-video"
description: "Use when building or rendering a motion video in code (conference films, explainers, product launches, title cards) with HyperFrames HTML-to-MP4; pairs with ai-media-director for story."
---

# HyperFrames Video (adapted from heygen-com/hyperframes, Apache-2.0)

HyperFrames renders HTML + GSAP to video by seeking a paused timeline frame by frame, so renders are deterministic. Free and open source; HeyGen avatars are optional and paid — never required.

## Setup
- Needs Node 20+, ffmpeg, and a Chromium the CLI can drive. If the workspace can't install or launch them, build the project files here and give the user the exact commands to run on their own machine.
- Commands: `npx hyperframes init <dir> --skip-skills`, `npx hyperframes check --json`, `npx hyperframes preview`, `npx hyperframes render`. Skip the CLI's usage/telemetry beacons unless the user wants them.

## Order of work
1. Story first (ai-media-director): brief → beats → storyboard, approved by the user.
2. Vector ledger: one row per scene cut — exit vector, entry vector, technique.
3. Build one sub-composition per scene; root `index.html` only hosts scenes, media, audio.
4. `check --json` until clean → render a 10–15 s style test → approve → full render.
5. Verify by extracting frames (`ffmpeg -vf fps=1/3,scale=640:-1,tile=4x3`) and viewing them, not by assuming.

## Render contract (violations break renders)
1. Every timed element: `class="clip"`, `data-start`, `data-duration` (seconds), stable `id`.
2. Root `data-duration` = video length. Default 1920×1080, 30 fps.
3. Each composition builds ONE paused GSAP timeline and registers it: `window.__timelines["<composition-id>"] = tl`.
4. No `Date.now()`, unseeded `Math.random()`, network fetches, timers, `repeat: -1`.
5. Never tween `display`/`visibility`/`autoAlpha` on a `.clip` — animate a child. Animate transforms, not left/top/width/height; no CSS transform on GSAP-transformed elements.
6. Never play/pause/seek media. Every `<audio>` has an `id`. Video keeps sound only with `data-has-audio="true"`, else `muted`.
7. Assets under `assets/` (no leading `/`); custom fonts need `@font-face` to `assets/fonts/`.
8. Scene files wrap styles/markup/scripts in `<template>`; root styled as `#root`.
9. Keep content in the 90% action-safe box, key text in 80% title-safe.
10. Copy, brand colours and swappable media as variables (`data-var-text`, `data-var-src`, CSS vars) so edits don't need code changes.

## Motion doctrine (makes it feel like one film, not slides)
- **Vector law:** how scene A exits decides how B enters — same axis, same direction, matched speed, cut mid-motion on both sides. Mirror eases: exit `power4.in` ↔ entry `power4.out`, same distance and duration.
- **Z sign:** growing = pushing forward, shrinking = pulling back. Don't answer a shrinking exit with a grow-from-small entry.
- **One current:** pick one default direction (e.g. left) for ordinary cuts. Reserve others for meaning: up = conclusion/reveal, zoom-through = deeper into the same idea, inverse zoom = arrival of something big. Never ping-pong directions.
- **Carriers:** carry an object (logo, card, line, cursor) across the cut so the eye has something to follow.
- **Causal motion:** things move because something caused them (click, impact, data arriving). No idle wobble or breathing — motion performs or stays still.
- **Stillness before climax:** hold ~0.5–1 s of calm before the big reveal.
- **Text cascades:** waterfall entry, 40–80 ms stagger, words not letters for body text.

## Sound
Films over ~15 s that tell a story get music plus light SFX on visible actions (whoosh on cuts, tick on data). Royalty-free sources only; duck music about −12 dB under voice; loudness-normalise to −16 LUFS.

## Delivery
MP4 (H.264, CRF 18–20), SRT captions, the editable project folder, and an optional 9:16 cut-down.
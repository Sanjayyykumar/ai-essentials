# Video playbook (creation + editing)
## Decide the engine
| Need | Engine |
|---|---|
| Edit existing footage (cut, trim, concat, captions, speed, audio) | ffmpeg (`libraries/offline/ffmpeg.md`) |
| Code-rendered motion/explainer/product film | HyperFrames / video-director (HTML+GSAP → MP4) or Python+Pillow frame renderer |
| Full short film from a prompt | take-one (12-role studio) |
| Product demo from a web app | argo (Playwright script + voiceover) |
| Explainer with local voice | explainroo |
| Launch/motion graphics | huashu-motion |
## Flow
1. **Brief:** goal, audience, length, aspect (16:9/9:16/1:1), fps, tone, CTA.
2. **Script:** timed LINES list `[(start_s, text)]` = single source of truth for VO + captions.
3. **Storyboard:** scene table (id, start, dur, visual, motion, text, sfx).
4. **Assets:** brand colors/fonts/logos; generate missing images (`image.md`).
5. **Render silent** in parallel chunks; preview 3 frames per scene.
6. **Voice:** offline Kokoro (`make_vo_kokoro.py`, voices hf_alpha/hf_beta/bf_emma/af_heart) or edge-tts online.
7. **Mix:** voice at each cut, music ducked −12 dB under voice, loudness −14 LUFS, burn or sidecar captions.
8. **Verify:** Video gate. Deliver MP4 (H.264, yuv420p, `-preset veryfast` unless best quality asked).

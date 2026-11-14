# AI.md — Universal Entry Point (read this first, read nothing else until routed)

Works with any agent: Claude, Gemini/Antigravity, Grok, Kimi, GPT, Codex, local LLMs.
Goal: finish the user's task end-to-end with the **fewest tokens, zero guesswork, live status, verified output**.

## 0. New machine
Run `scripts/setup.ps1 -Engines` (Windows) or `scripts/setup.sh --engines` (Linux/macOS/WSL), then `python scripts/doctor.py`. Skills for Claude live in `skills/` (setup copies them to ~/.claude/skills). Library repos: `vendor/library/` (env AI_LIBRARY_ROOT). Zip for another PC: `scripts/pack.ps1`.

## 1. Boot protocol (≤ 30 s, ≤ 2 k tokens)
1. Read this file only.
2. Classify the task with the **Router** (§3). Open ONLY the files it names.
3. Create/refresh `STATUS.md` in the user's working folder (template: `templates/STATUS.md`).
4. Run the **Lifecycle** (`system/00-lifecycle.md`). Do not skip VERIFY.

## 2. Hard rules
- **Inspect before acting.** Read existing files/configs before writing new ones.
- **Offline first.** Check `libraries/CATALOG.md` + `libraries/offline/` before any web search.
- **Smallest safe change.** No rewrites unless asked. No speculative features.
- **Evidence over claims.** "Done" requires a run, a render, a test, or an opened file.
- **Ask only when a wrong guess is expensive or irreversible.** Otherwise decide, state the assumption in STATUS.md, continue.
- **Never** commit secrets, delete user data without consent, or reproduce copyrighted works/brands.

## 3. Router — task → files to open
| Task signal | Open | Library hits (see CATALOG) |
|---|---|---|
| code, app, API, bug, deploy, DB | `playbooks/development.md` | e2eengine, skills-main, karpathy, playwright-cli, agent-skills |
| video, film, explainer, demo, edit, reel | `studio/SYSTEM.md` → `playbooks/video.md` | **Video studio (VIDEO_ROOT/studio/make.py)**, lemo-opuscar, remotion-skills, manim-skill, video-toolkit, take-one, video-director, huashu-motion, argo |
| image, illustration, photo, thumbnail | `studio/SYSTEM.md` → `playbooks/image.md` | code render (HTML/canvas), GPU kit image_flux.py, cloud (ElevenLabs/Canva) |
| animation, motion, Lottie, GSAP, shaders | `playbooks/animation.md` | rossark-motion, reanimate, shaders, e2e ui-motion / lottie-animation |
| UI, UX, landing page, brand, poster | `playbooks/design.md` | diagram-design, e2e ui-ux-designer / ux-laws |
| logo, logo animation | `playbooks/logo.md` | e2e vector-illustration |
| SVG create/edit/optimize | `playbooks/svg.md` + `libraries/offline/svg.md` | — |
| voice, TTS, music, sound, subtitles | `studio/SYSTEM.md` → `playbooks/audio.md` | Kokoro, Indic Parler-TTS, faster-whisper, chatterbox, XTTS, Pixabay (skills/pixabay-audio), earshot |
| SEO, copy, docs, humanize | `playbooks/content.md` | humanizer, open-seo, e2e seo-* |
| "figure out", unknown tech, clone, research, competitor, binary | `recon/RECON.md` | rea, reanimate, web-intelligence |
| Main system can't decide | `recon/RECON.md` (always the fallback) | — |

Multi-domain task → open each playbook, but only the sections you need.

## 4. Token economy (summary — full: `system/01-token-economy.md`)
Grep > read; read ranges, not whole files; one SKILL.md at a time; batch independent tool calls; summarize long outputs to STATUS.md and drop them from context; never paste >40 lines of code into chat — write files.

## 5. Live status (summary — full: `system/02-live-status.md`)
Update `STATUS.md` at each phase change: `phase | step x/y | done | next | blockers | assumptions`.
Optional: `python scripts/status.py set BUILD "rendering scene 3/7"`.

## 6. Definition of done
Output opens/runs; checks in `system/03-quality-gates.md` pass; STATUS.md = DELIVERED with paths; one-line summary + next step to the user.

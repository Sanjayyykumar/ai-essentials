# AI.md — Router & manual (opened on demand)
> The always-loaded rules are `KERNEL.md` (≈550 tokens), auto-registered with every AI by `scripts/link.py`. Open this file only to route a task or look something up.

Works with any agent: Claude, Gemini/Antigravity, Grok, Kimi, GPT, Codex, local LLMs.
Goal: finish the user's task end-to-end with the **fewest tokens, zero guesswork, live status, verified output**.

## 0. First run on a machine (do this before anything else)
If `.bootstrap.json` is missing next to this file, or says `"ok": false`: run `python scripts/bootstrap.py` (Windows without Python: `scripts\setup.ps1`). It is idempotent and installs only what is missing: tools (git, node, ffmpeg, yt-dlp), the video studio + voice model, own and external skills into `~/.claude/skills` and `~/.agents/skills`, and Claude Code plugins. Tell the user what it installed, then ask them to restart the agent so new skills load. Everything it installs is listed in `libraries/install.json` (edit that file to add more). Check anytime: `python scripts/bootstrap.py --check`.

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
- **Prove, then say it.** Run `python scripts/verify.py` (hub) or `python scripts/verify.py --project <path>` (your build) before delivering; report the proof level reached (P0–P5), never more. Failures → local self-heal loop, max 3, never weaken a test or gate (`system/04-proof-and-self-heal.md`).
- **Ask only when a wrong guess is expensive or irreversible.** Otherwise decide, state the assumption in STATUS.md, continue.
- **Never** commit secrets, delete user data without consent, or reproduce copyrighted works/brands.

## 3. Router — task → files to open
| Task signal | Open | Library hits (see CATALOG) |
|---|---|---|
| code, app, API, bug, deploy, DB | `playbooks/development.md` | e2eengine, skills-main, karpathy, playwright-cli, agent-skills |
| video, film, explainer, demo, edit, reel, "edit like these videos" | `studio/SYSTEM.md` → `playbooks/video.md`; references → `skills/reference-style` | **Video studio (VIDEO_ROOT/studio/make.py, reel.py, reference.py)**, HyperFrames, Remotion, lemo-opuscar, remotion-skills, manim-skill, video-toolkit, take-one, video-director, huashu-motion, argo |
| image, illustration, photo, thumbnail | `studio/SYSTEM.md` → `playbooks/image.md` | code render (HTML/canvas), GPU kit image_flux.py, cloud (ElevenLabs/Canva) |
| animation, motion, Lottie, GSAP, shaders | `playbooks/animation.md` | rossark-motion, reanimate, shaders, e2e ui-motion / lottie-animation |
| UI, UX, landing page, brand, poster | `playbooks/design.md` | skills ui-ux-pro-max · impeccable · taste-skill · emil-design-eng, diagram-design |
| logo, logo animation | `playbooks/logo.md` | e2e vector-illustration |
| SVG create/edit/optimize | `playbooks/svg.md` + `libraries/offline/svg.md` | — |
| voice, TTS, music, sound, subtitles | `studio/SYSTEM.md` → `playbooks/audio.md` | Kokoro, Indic Parler-TTS, faster-whisper, chatterbox, XTTS, Pixabay (skills/pixabay-audio), earshot |
| SEO, copy, docs, humanize | `playbooks/content.md` | humanizer, open-seo, e2e seo-* |
| "figure out", unknown tech, clone, research, competitor, binary | `recon/RECON.md` | rea, reanimate, web-intelligence |
| CI red, tests failing, "prove it", self-heal, release check | `system/04-proof-and-self-heal.md` | verify.py, .github/workflows (check, self-heal), e2eengine SD3 |
| new project, plan tasks, "what's next", resume | `scripts/project.py` (`.ai/` brain) · `templates/ai/README.md` | builder / reviewer agents |
| which model / effort | `scripts/models.py <L|M|H|X>` · `libraries/models.json` | — |
| input is an image, video, audio, PDF or URL; non-technical user; "build me X end to end" | `system/05-universal-flow.md` | Superpowers, reference-style, recon |
| review my code / PR / commit, audit a folder | `system/05-universal-flow.md` §4 | open-code-review-delegate (`ocr delegate`), reviewer agent, `templates/github/review.yml` |
| hard choice, "which is best", finishing a deliverable, exact output | `system/06-precision.md` | decision procedure, output contracts |
| "are we efficient?", lessons, retro | `scripts/evals.py` · `scripts/learn.py` · `evals/README.md` | — |
| Main system can't decide | `recon/RECON.md` (always the fallback) | — |

Multi-domain task → open each playbook, but only the sections you need.

## 4. Token economy (summary — full: `system/01-token-economy.md`)
Grep > read; read ranges, not whole files; one SKILL.md at a time; batch independent tool calls; summarize long outputs to STATUS.md and drop them from context; never paste >40 lines of code into chat — write files.

## 5. Live status (summary — full: `system/02-live-status.md`)
Update `STATUS.md` at each phase change: `phase | step x/y | done | next | blockers | assumptions`.
Optional: `python scripts/status.py set BUILD "rendering scene 3/7"`.

## 6. Definition of done
`verify.py` reaches P2 (evidence in `.proof/verify.json`); domain gate in `system/03-quality-gates.md` passes with evidence (P3); STATUS.md = DELIVERED with paths; one-line summary + next step to the user.

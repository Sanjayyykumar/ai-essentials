# Universal flow — any input → any finished product
For engineers and non-engineers alike. One path, scaled by tier (KERNEL.md §1).

## 1. Intake from any input (turn it into a spec before building)
| User gives | Do first (cheapest that works) | Becomes |
|---|---|---|
| Text / idea / chat | Restate goal in 1 line; list deliverables + "done when" | `.ai/PROJECT.md` |
| Image / screenshot / sketch / mockup | Look at it; extract layout, text (spell exactly), colours, components, states | UI spec or design brief |
| Video (reference, screen recording, reel) | `ffprobe` → frames every 2–5 s (`ffmpeg -vf fps=1/3`) → transcript (faster-whisper) → cut list / style notes | storyboard, bug repro steps or style.json (`skills/reference-style`) |
| Audio / voice note | transcribe (faster-whisper) → summarise asks | task list |
| PDF / doc / spreadsheet | extract text/tables; keep page refs | requirements with sources |
| URL / existing product / competitor | `recon/RECON.md` (fingerprint, screenshots, API map) | recon brief |
| Existing repo | `scout` agent: entry points, stack, tests, CI | `.ai/PROJECT.md` stack section |
| Vague ("make me an app") | ≤3 multiple-choice questions (who is it for · must-have · look/feel), then proceed | spec |
Never re-read the raw input after it has become a spec; work from the spec.

## 2. Method stack by tier
| Tier | Think | Plan | Build | Review | Finish |
|---|---|---|---|---|---|
| L | — | — | do it | self-check | reply |
| M | `brainstorming`* (short) | `project.py add` tasks | `builder` agent or inline, test-first | `open-code-review-delegate` on the diff | `verify.py` P2 + domain gate |
| H / X | `brainstorming`* full, design approved in chunks | `writing-plans`* → tasks in `.ai/TASKS.md` | `subagent-driven-development`* (fresh agent per task, 2-stage review); parallel only for independent tasks | OCR delegate + `reviewer` agent (independent) | `finishing-a-development-branch`* + `verify.py` + CI |
\* Superpowers skills (installed by bootstrap). Their trigger rule ("check skills before any response") applies to M+ work; for L-tier the kernel's skip rule wins (user instructions outrank skills).
Single sources of truth: tasks → `.ai/TASKS.md`; status → `.ai/STATUS.md`; done → `verify.py` + `system/03-quality-gates.md`.

## 3. Non-engineer mode (user says they're not technical, or never mentions code)
- Speak in outcomes, not tech: "your shop page works on phones" not "responsive grid".
- Pick the stack yourself (`libraries/offline/web-stack.md`); explain only what they must do (accounts, payments, domains).
- Decisions as 2–3 plain choices with a recommended one.
- Deliver something they can open: a link, a file, a video — plus 3 lines on how to use/change it.
- Hide the machinery; keep `.ai/` updated anyway so the next AI can continue.

## 4. Review (code)
`open-code-review-delegate` first: `ocr delegate preview --format json` picks reviewable files, `ocr delegate rule` gives repo rules (`.opencodereview/rule.json`); review only those files. High precision, low noise, no extra API key. `ocr scan <dir>` for audits with no diff. CI version: `templates/github/review.yml`.
Receiving review feedback: verify each point technically before changing code (`receiving-code-review`*); push back with evidence when it's wrong.

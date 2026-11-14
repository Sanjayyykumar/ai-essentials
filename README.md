<div align="center">

# 🧠 A.I-essentials

### One folder that turns any AI agent into a disciplined teammate — for code, video, design, audio and research.

[![check](https://github.com/Sanjayyykumar/ai-essentials/actions/workflows/check.yml/badge.svg)](https://github.com/Sanjayyykumar/ai-essentials/actions/workflows/check.yml)
![License: MIT](https://img.shields.io/badge/license-MIT-green)
![Agents](https://img.shields.io/badge/works%20with-Claude%20·%20Gemini%20·%20Codex%20·%20Cursor%20·%20local%20LLMs-blueviolet)
![Skills](https://img.shields.io/badge/skills-14-orange)
![Tools indexed](https://img.shields.io/badge/open--source%20tools%20indexed-34-blue)

**Drop it into a project, tell your agent _"Read AI.md and follow it"_, and get work that is planned, verified and cheap on tokens.**

</div>

---

## The problem

AI agents are brilliant and erratic. They re-read your whole repo, guess instead of asking, say "done" without running anything, and forget what they learned last session. Every new tool (Claude, Gemini, Codex, Cursor…) needs the same rules explained again.

## The fix

`ai-essentials` is a small, agent-neutral **operating system in Markdown**: one entry file, a router, playbooks per domain, quality gates, and a curated index of open-source tools. Any agent that can read files can use it.

```mermaid
flowchart LR
  T[Your task] --> A[AI.md<br/>router]
  A --> P[playbooks/<br/>video · dev · design · audio · svg · logo · content]
  A --> R[recon/<br/>unknown tech → research first]
  P --> L[libraries/<br/>34 indexed tools + offline cheat sheets]
  P --> S[system/<br/>lifecycle · token rules · quality gates]
  S --> D[✅ verified output<br/>+ STATUS.md]
```

## What you get

| | |
|---|---|
| 🧭 **One entry point** | `AI.md` routes any task to the 1–2 files it actually needs. `CLAUDE.md`, `AGENTS.md`, `GEMINI.md` and `.cursorrules` all point there. |
| 🔁 **A 7-phase lifecycle** | INTAKE → RECON → PLAN → BUILD → VERIFY → DELIVER → LEARN. VERIFY can't be skipped: "done" means it ran, rendered or passed. |
| 🪙 **Token economy** | Grep before read, read ranges, one skill at a time, batch tool calls, summarise long output to `STATUS.md`. |
| 📍 **Live status** | Agents keep `STATUS.md` current (`phase · step x/y · next · blockers · assumptions`), so you can step away and check in. |
| 🎬 **Media studio** | Routing tables for video, image and audio: code-rendered first, GPU kits when an NVIDIA card is present, cloud only when code can't do it. Pairs with [**video-generations**](https://github.com/Sanjayyykumar/video-generations). |
| 🕵️ **Recon mode** | A method for reverse-engineering and evidence-based research when the agent doesn't know the tech. |
| 📚 **Tool library** | `libraries/registry.json` indexes 34 open-source agent skills and tools (Remotion, Manim, Playwright, Chatterbox, humanizer…) with upstream and licence. `python scripts/find.py video` searches it offline. |

## Skills included

Ready-made [Claude Skills](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview) (`skills/`), also readable by any agent:

| Skill | Use it for |
|---|---|
| `engineering-system` | Default workflow for any coding task: inspect first, smallest safe change, evidence-based verification |
| `karpathy-guidelines` | Avoid the classic LLM coding mistakes: over-building, silent assumptions, sprawling diffs |
| `diagnosing-bugs` | A diagnosis loop for hard bugs and performance regressions |
| `grilling` | Stress-test a plan or design with relentless questions |
| `production-readiness` | Evidence-based go/no-go with P0–P3 gaps, staged rollout and rollback |
| `postgres-best-practices` | Schema, indexes, RLS, locking and pooling rules before you write SQL |
| `playwright-cli` | Drive a real browser from the shell to test and reproduce UI bugs |
| `premium-scroll-site` | Scroll-driven landing pages that don't look templated |
| `media-studio` | Route any image/audio/video job to the right engine; brief → build → mix → QC |
| `presenter-voiceover` | Narration that sounds like a presenter: script rules, pause markup, offline Kokoro voice, fit-to-video mix |
| `hyperframes-video` | Motion video from HTML + GSAP, rendered frame-perfect |
| `pixabay-audio` | Find, license-log and mix royalty-free SFX and music |
| `humanize-writing` | Strip AI writing patterns from docs, posts and emails |
| `tool-library` | Find and use the local library of open-source tools |

## Quick start

**Use it in a project (30 seconds):**
```bash
git clone https://github.com/Sanjayyykumar/ai-essentials
```
Then tell your agent: **"Read `ai-essentials/AI.md` and follow it."**

**Set up a whole machine** (skills into `~/.claude/skills`, env vars, the video studio, Kokoro voice model, optional tool library):
```bash
# Windows
powershell -ExecutionPolicy Bypass -File scripts\setup.ps1 -Engines -FetchMissing
# macOS / Linux / WSL
bash scripts/setup.sh --engines --fetch-missing

python scripts/doctor.py      # what's installed, what's missing
```

## Layout

```
ai-essentials/
├── AI.md              ← the only file an agent reads at boot
├── system/            lifecycle · token economy · live status · quality gates · lessons
├── playbooks/         development · video · image · animation · design · logo · svg · audio · content
├── recon/             reverse engineering & deep research method
├── studio/            media system: routing tables, GPU kits, Hugging Face notes, engines/
├── skills/            14 Claude skills
├── libraries/         registry.json + CATALOG.md (34 tools) + offline cheat sheets
├── templates/         STATUS · PLAN · TASK · HANDOFF
├── scripts/           setup · doctor · find · status · check · pack
└── vendor/            cloned tool repos (git-ignored, filled by setup --fetch-missing)
```

## Principles

**Inspect first · offline first · smallest safe change · evidence over claims · ask only when a wrong guess is costly.**

## Contributing

New tool? Add it to `libraries/registry.json` and `libraries/CATALOG.md`. New domain? Add `playbooks/<domain>.md`, a router row in `AI.md`, and a gate in `system/03-quality-gates.md`. Run `python scripts/check.py` before a PR. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Licence

MIT © [Sanjay Kumar](https://github.com/Sanjayyykumar). Adapted skills keep their original credit and licence — see [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md). Indexed tools are not redistributed; they're cloned from upstream under their own licences.

⭐ If this makes your agent less chaotic, star it so others can find it.

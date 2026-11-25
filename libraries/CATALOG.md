# Library catalog (offline-first map)
Set `AI_LIBRARY_ROOT` to your local library folder (default `vendor/library/`, filled by `scripts/setup.* --fetch-missing`). Entry paths are relative to it.
Search: `python scripts/find.py <keyword>`. Open ONE entry file, never a whole repo. Repos stay at their upstream — this project only indexes them.

## animation
| id | use for | entry | upstream | license |
|---|---|---|---|---|
| reanimate | Clone animations/sections from site, video, gif, Lottie | `04-design-diagrams-frontend/reanimate-main/skills/reanimate/SKILL.md` | (see LICENSE/README) | MIT |
| shaders | WebGPU effects for React/Vue/Svelte (npm shaders) | `04-design-diagrams-frontend/shaders-main/skills/shaders/SKILL.md` | npm: shaders | MIT |
| rossark-motion | Character/illustration motion | `05-video-motion/rossark-motion-skill-main/SKILL.md` | (see README) | MIT |

## audio
| id | use for | entry | upstream | license |
|---|---|---|---|---|
| earshot | Judge/choose sound; licensed soundtracks | `06-audio-voice/earshot-main/skills/earshot/; skills/real-sound/` | github.com/Leonxlnx/earshot | MIT |
| voicestudio | Local TTS, voice design, transcription, dubbing | `06-audio-voice/VoiceStudio-main/skills/voicestudio/SKILL.md` | github.com/debpalash/VoiceStudio | AGPL-3.0 (copyleft — do not vendor) |
| kimi-audio | Kimi-Audio-7B: ASR, audio understanding, generation (big NVIDIA GPU) | `06-audio-voice/Kimi-Audio-master/README.md; infer.py` | github.com/MoonshotAI/Kimi-Audio | see repo |
| kokoro-onnx | Offline TTS model used by the video pipeline | `(10 Video Generations/models)/kokoro-v1.0.int8.onnx, voices-v1.0.bin` | github.com/thewh1teagle/kokoro-onnx | MIT (model: Apache-2.0) |

## content
| id | use for | entry | upstream | license |
|---|---|---|---|---|
| humanizer | Remove AI writing tells (26 patterns) | `03-writing-content-seo/humanizer-main/SKILL.md` | github.com/blader/humanizer | MIT |
| open-seo | Keyword research, audits, local SEO, AI visibility (needs OpenSEO server) | `03-writing-content-seo/open-seo-main/plugins/openseo/skills/` | github.com/every-app/open-seo (verify) | MIT |

## database
| id | use for | entry | upstream | license |
|---|---|---|---|---|
| agent-skills | Supabase + Postgres best practices (33 rules) | `01-engineering-workflow/agent-skills-main/skills/supabase-postgres-best-practices/references/` | github.com/supabase/agent-skills | MIT |

## design
| id | use for | entry | upstream | license |
|---|---|---|---|---|
| diagram-design | Editorial HTML/SVG architecture, flow, sequence, ER diagrams | `04-design-diagrams-frontend/diagram-design-main/skills/diagram-design/SKILL.md` | github.com/cathrynlavery/diagram-design | MIT |
| ui-ux-pro-max | UI/UX intelligence: styles, palettes, font pairs, design systems | `04-design-diagrams-frontend/ui-ux-pro-max-skill/.claude/skills/ui-ux-pro-max/SKILL.md` | github.com/nextlevelbuilder/ui-ux-pro-max-skill | MIT |
| impeccable | Style guardian: one design language, anti-slop critique/polish | `04-design-diagrams-frontend/impeccable/.claude/skills/impeccable/SKILL.md` | github.com/pbakaus/impeccable | Apache-2.0 |
| taste-skill | Kills generic, samey AI UI output | `04-design-diagrams-frontend/taste-skill/skills/taste-skill/SKILL.md` | github.com/Leonxlnx/taste-skill | MIT |
| emil-design-eng | Animation, gestures, small UI details that feel finished | `04-design-diagrams-frontend/emil-design-eng/skills/emil-design-eng/SKILL.md` | github.com/emilkowalski/skill | MIT |

## engineering
| id | use for | entry | upstream | license |
|---|---|---|---|---|
| e2eengine | SD1/SD2/SD3 engineering system, 41 specialist skills (backend, api, db, devops, security, qa, ui-ux, seo, motion, lottie, vector) | `01-engineering-workflow/e2eengine-main/CLAUDE.md; skills/<name>/SKILL.md` | github.com/Creativestarjsp/e2eskill | MIT |
| skills-main | Matt Pocock skills: tdd, diagnosing-bugs, code-review, to-spec, to-tickets, grilling, handoff, prototype | `01-engineering-workflow/skills-main/skills/<group>/<name>/SKILL.md` | github.com/mattpocock/skills | MIT |
| karpathy-guidelines | Think first, simplicity, surgical changes, goal-driven coding | `01-engineering-workflow/andrej-karpathy-skills-main/CLAUDE.md` | github.com/forrestchang/andrej-karpathy-skills | MIT |
| claude-plugins-official | Anthropic official plugin directory (security etc.) | `01-engineering-workflow/claude-plugins-official-main/plugins/<name>/` | github.com/anthropics/claude-plugins-official | Apache-2.0 |

## integrations
| id | use for | entry | upstream | license |
|---|---|---|---|---|
| gws-cli | Google Workspace CLI + 40 recipes | `07-integrations/cli-main/skills/` | github.com/googleworkspace/cli | Apache-2.0 |

## recon
| id | use for | entry | upstream | license |
|---|---|---|---|---|
| rea | Reverse-engineer binaries, Electron, firmware | `02-testing-browser-security/rea-main/.agents/skills/reverse-engineer-anything/SKILL.md` | github.com/morluto/rea | MIT |

## research
| id | use for | entry | upstream | license |
|---|---|---|---|---|
| laya | Non-autoregressive decision models (research code) | `08-ai-ml-research/laya-main/README.md` | github.com/NandhaKishorM/laya | Apache-2.0 |
| transformers | Hugging Face Transformers v5 (reference; pip install transformers) | `08-ai-ml-research/transformers-main/docs/source/en/` | github.com/huggingface/transformers | Apache-2.0 |

## testing
| id | use for | entry | upstream | license |
|---|---|---|---|---|
| playwright-cli | Browser automation, UI tests, screenshots, traces | `02-testing-browser-security/playwright-cli-main/skills/playwright-cli/SKILL.md` | github.com/microsoft/playwright-cli | Apache-2.0 |

## video
| id | use for | entry | upstream | license |
|---|---|---|---|---|
| hyperframes | HTML+GSAP → MP4 for agents; `npx hyperframes measure` analyses any video | `npx hyperframes` (skill: skills/hyperframes-video) | github.com/heygen-com/hyperframes | Apache-2.0 |
| yt-dlp | Download reference videos (bootstrap installs it) | CLI `yt-dlp` | github.com/yt-dlp/yt-dlp | Unlicense |
| take-one | Full short film from a request (12-role studio) | `05-video-motion/take-one-main/SKILL.md` | github.com/talsiach/take-one | MIT |
| video-director | Code-rendered short videos (HTML/Canvas/GSAP/Three.js) | `05-video-motion/video-director-main/video-director/SKILL.md` | github.com/win4r/video-director | MIT |
| huashu-motion | Product launch / motion graphics videos | `05-video-motion/huashu-motion-main/skills/huashu-motion/SKILL.md` | github.com/alchaincyf/huashu-motion | MIT |
| explainroo | Explainer MP4 with local voice-over | `05-video-motion/explainroo-main/skills/explainroo/SKILL.md` | (see README) | MIT |
| argo | Product demo videos from Playwright scripts + voiceover | `05-video-motion/argo-main/skills/argo-guide/SKILL.md` | (see README) | MIT |

## Offline cheat sheets (`libraries/offline/`)
ffmpeg.md · svg.md · motion.md · image-prompts.md · git.md · web-stack.md

## methodology & review
| id | use for | entry | upstream | license |
|---|---|---|---|---|
| superpowers | brainstorm → plan → subagent build → review → finish; TDD; debugging; worktrees; writing-skills | plugin (bootstrap) | github.com/obra/superpowers | MIT |
| open-code-review | precise low-token code review (`ocr delegate`, `ocr review`, `ocr scan`, GitHub Action) | `01-engineering-workflow/open-code-review/skills/` | github.com/alibaba/open-code-review | Apache-2.0 |

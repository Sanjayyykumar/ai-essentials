# RECON — Reverse-engineering & Deep-Research Mini-System
Use when: the main system can't determine the approach, tech is unknown, you must clone/understand something, or a decision needs evidence.
Output is always a **Recon Brief** (`recon/brief-template.md`): answer, confidence, evidence, unknowns, recommended next action.

## The loop: Q → MAP → PROBE → TRIANGULATE → SYNTHESIZE
1. **Q — sharpen the question.** One sentence + "done when …". Split into ≤5 sub-questions.
2. **MAP — cheapest sources first (token ladder):**
   L0 what's already in context/STATUS → L1 local files & `libraries/` (grep) → L2 package docs offline (`--help`, `man`, `node_modules/*/README`, `pip show`, site-packages source) → L3 targeted web search → L4 fetch primary sources (official docs, repo source, changelogs, RFCs, papers) → L5 deep scrape / browser automation.
   Stop climbing as soon as the question is answered with evidence.
3. **PROBE — pick the method** (table below), run it, record raw facts in `notes.md` (facts + source, no prose).
4. **TRIANGULATE:** each key claim needs 2 independent sources OR 1 primary source + a reproduction. Note conflicts; prefer newest primary.
5. **SYNTHESIZE:** fill the Recon Brief. Confidence = High (reproduced) / Medium (2 sources) / Low (1 secondary source).

## Method selector
| Target | Method | Tools |
|---|---|---|
| Website / web app | Tech fingerprint (headers, `<meta generator>`, JS globals, bundle names), sitemap/robots, network tab (APIs, payloads), CSS tokens extraction | curl -I, playwright-cli (HAR, screenshots), `get_page_text`, Wappalyzer-style heuristics in `methods.md` |
| UI/animation to clone | Frame capture, computed styles, timing curves, asset list | reanimate, playwright trace, DevTools Animations |
| Codebase (unknown repo) | Entry points → call graph → data flow; `git log -S` for history of a symbol | rg, ctags, tree -L 2, e2eengine repo-intelligence |
| Library/API behaviour | Read source not blogs; minimal repro script; check version | site-packages / node_modules, REPL |
| Binary / Electron / firmware | strings, file, binwalk, asar extract, Ghidra/radare2 | rea (reverse-engineer-anything) |
| Media file | ffprobe, exiftool, frame dump, spectrogram | ffmpeg, sox |
| Market / competitor / product | Official pages, pricing, changelog, docs, GitHub activity, reviews (dated) | web search + fetch, `queries.md` |
| Research question (science/tech) | Papers (arXiv, Semantic Scholar), benchmarks, official reports | web search + fetch |

## Deep scrape rules (L5)
Respect robots.txt, ToS and rate limits (≤1 req/s); never bypass logins/paywalls/captchas; no personal data harvesting; cache pages to `recon/cache/` and re-use; extract to structured JSON/CSV, then discard HTML from context.

## Anti-hallucination
No source → write "UNKNOWN", never guess. Quote numbers with date + source. Version-specific facts must name the version.

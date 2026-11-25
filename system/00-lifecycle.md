# Lifecycle — 7 phases, every task
Scale it: trivial task = phases collapse to 1 line each. Never skip VERIFY.

| # | Phase | Do | Exit criteria |
|---|---|---|---|
| 1 | INTAKE | Restate goal in 1 line. List deliverables, format, constraints, deadline. Pick tier: S (≤15 min), M (≤2 h), L (multi-session). | Goal + deliverables written in STATUS.md |
| 2 | RECON | Inspect user files/repo. Check `libraries/CATALOG.md`. Unknown territory → `recon/RECON.md`. | Known: inputs, tools, unknowns (≤5 bullets) |
| 3 | PLAN | Numbered steps, each with a verification. L-tier: write `PLAN.md`. Ask user ONLY on expensive/irreversible ambiguity. | Steps x/y listed in STATUS.md |
| 4 | BUILD | Execute steps in order; smallest change; commit/save per step; update status per step. | All steps done or blocked |
| 5 | VERIFY | Run `python scripts/verify.py [--project PATH]` (P0–P2), then the domain gate in `system/03-quality-gates.md` (P3). Failure → self-heal loop in `system/04-proof-and-self-heal.md` (max 3, never weaken a check). L-tier: independent SD3 re-check (P4). | Proof level recorded in STATUS.md with evidence |
| 6 | DELIVER | Final paths, 1-line summary, proof level reached, how to run/open, known limits, 1 next step. | STATUS.md = DELIVERED |
| 7 | LEARN | `python scripts/learn.py add <domain> "lesson"` (dedupes; a lesson seen 3× → `learn.py promote` turns it into a rule). L-tier: only if something went wrong. `learn.py retro` for a quick session review. | Lesson filed or "none" |

## Tiers
- **S**: INTAKE+PLAN in your head, 1 status update, verify once.
- **M**: full STATUS.md, per-step updates.
- **L**: PLAN.md + HANDOFF.md (`templates/HANDOFF.md`) at end of every session so any other AI can resume.

## Resume protocol (any AI, any session)
Read `AI.md` → `STATUS.md` → `HANDOFF.md` (if present) → continue at "next". Do not redo done steps.

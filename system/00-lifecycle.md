# Lifecycle — 7 phases, every task
Scale it: trivial task = phases collapse to 1 line each. Never skip VERIFY.

| # | Phase | Do | Exit criteria |
|---|---|---|---|
| 1 | INTAKE | Restate goal in 1 line. List deliverables, format, constraints, deadline. Pick tier: S (≤15 min), M (≤2 h), L (multi-session). | Goal + deliverables written in STATUS.md |
| 2 | RECON | Inspect user files/repo. Check `libraries/CATALOG.md`. Unknown territory → `recon/RECON.md`. | Known: inputs, tools, unknowns (≤5 bullets) |
| 3 | PLAN | Numbered steps, each with a verification. L-tier: write `PLAN.md`. Ask user ONLY on expensive/irreversible ambiguity. | Steps x/y listed in STATUS.md |
| 4 | BUILD | Execute steps in order; smallest change; commit/save per step; update status per step. | All steps done or blocked |
| 5 | VERIFY | Run `system/03-quality-gates.md` for the domain. Fix → re-verify (max 3 loops, then report). | Gates pass with evidence |
| 6 | DELIVER | Final paths, 1-line summary, how to run/open, known limits, 1 next step. | STATUS.md = DELIVERED |
| 7 | LEARN | Append reusable lessons to `system/LESSONS.md` (1 line each, no secrets). | Lesson filed or "none" |

## Tiers
- **S**: INTAKE+PLAN in your head, 1 status update, verify once.
- **M**: full STATUS.md, per-step updates.
- **L**: PLAN.md + HANDOFF.md (`templates/HANDOFF.md`) at end of every session so any other AI can resume.

## Resume protocol (any AI, any session)
Read `AI.md` → `STATUS.md` → `HANDOFF.md` (if present) → continue at "next". Do not redo done steps.

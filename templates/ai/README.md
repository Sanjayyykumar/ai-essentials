# The `.ai/` project brain (created by `python <hub>/scripts/project.py init`)
| File | Holds | Who updates |
|---|---|---|
| `PROJECT.md` | goal, users, deliverables, scope in/out, stack, constraints, definition of done | user + AI at INTAKE |
| `TASKS.md` | Epic → Task table: ID, tier, status, deps, acceptance, verify | `project.py add/start/done/block` |
| `STATUS.md` | phase, step x/y, now, next, blockers, proof level | auto on start/done/block; `status.py` |
| `DECISIONS.md` | date · choice · alternatives · why | `project.py decide` |
| `HANDOFF.md` | state + next 3 actions for the next session/AI | AI at session end |
Resume cost: read STATUS.md + `project.py next` (~300–800 tokens) instead of re-exploring the repo.
Rules: tasks ≤2 h with one observable outcome; no task without acceptance + verify; start only when deps are done; `verify.py --project .` fails P2 if any task lacks them.

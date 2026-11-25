# Contributing
- Keep files short and scannable: tables > prose, ≤150 lines per file.
- New tool/repo → add to `libraries/registry.json` and `libraries/CATALOG.md` (id, domain, use, entry, upstream, license). Link upstream; do not vendor third-party code.
- New domain → `playbooks/<domain>.md` + a Router row in `AI.md` + a gate in `system/03-quality-gates.md`.
- Run `python scripts/verify.py` before a PR — it must reach P2 (CI enforces the same on 3 OSes).

## Skill quality (adapted from Superpowers `writing-skills`)
- Write the failing case first: a task where an agent without the skill goes wrong; the skill must fix it.
- Description = *when to use it* (trigger words), ≤60 words; `verify.py` enforces the limit.
- Body: steps an agent can follow cold; no essays; link heavy references instead of inlining them.
- Re-test after edits with a fresh agent session.

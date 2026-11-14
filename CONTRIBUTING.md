# Contributing
- Keep files short and scannable: tables > prose, ≤150 lines per file.
- New tool/repo → add to `libraries/registry.json` and `libraries/CATALOG.md` (id, domain, use, entry, upstream, license). Link upstream; do not vendor third-party code.
- New domain → `playbooks/<domain>.md` + a Router row in `AI.md` + a gate in `system/03-quality-gates.md`.
- Run `python scripts/check.py` before a PR.

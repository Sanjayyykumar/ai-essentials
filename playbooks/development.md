# Development playbook (any stack)
## Flow
1. **Recon repo:** README, manifest (package.json/pom.xml/pyproject), CI, `git log -10`, test command. Note stack in STATUS.md.
2. **Spec:** user story + acceptance criteria (3–7 bullets). L-tier → `PLAN.md` with ADR-style decisions.
3. **Design:** data model → API contract → UI states (empty/loading/error/success). Diagram only if >3 components.
4. **Build test-first** where tests exist: failing test → minimal code → green → refactor.
5. **Verify:** gates in `system/03-quality-gates.md` (Code + Web/UI).
6. **Prove:** `python <hub>/scripts/verify.py --project .` must reach P2; record the level in STATUS.md. Red → self-heal loop (`system/04-proof-and-self-heal.md`).
7. **CI:** copy `scripts/verify.py` into the project and `templates/github/proof.yml` (+ optional `templates/github/self-heal.yml`) into `.github/workflows/`.
8. **Ship:** deploy checklist — env vars documented, migrations reversible, rollback step written.
## Method (by tier, details in `system/05-universal-flow.md`)
H/X: Superpowers `brainstorming` → `writing-plans` → `subagent-driven-development` (TDD inside) → OCR review → `finishing-a-development-branch`. M: tasks via `project.py`, builder agent, OCR review. Review = `ocr delegate preview/rule` then review only those files.

## Roles (SD1/SD2/SD3 from e2eengine)
SD1 implements · SD2 orchestrates/plans · SD3 independently verifies. Solo agent: play SD3 last, re-reading the diff cold.
## Library
e2eengine skills: backend-developer, api-developer, database-engineer, frontend-developer, react-js-developer, expo-developer, devops-engineer, ci-cd-pipeline, security-engineer, qa-engineer, code-reviewer, software-architect, observability, app-deployment · skills-main: tdd, diagnosing-bugs, code-review, to-spec, to-tickets · karpathy guidelines · playwright-cli · agent-skills (Postgres/Supabase).
## Debug loop
Reproduce → minimise → hypothesise (≤3) → instrument → fix root cause → regression test.

---
name: "production-readiness"
description: "Use when asked whether a product or feature is ready for production, or when preparing a launch — gives an evidence-based go/no-go with P0–P3 gaps, staged rollout and rollback."
---

# Production Readiness (adapted from addyosmani/agent-skills shipping-and-launch)

Answer with a verdict first (Ready / Ready for pilot / Not ready), then the gaps. Every claim cites evidence (test run, file, doc, measurement) or is marked unverified.

## Gather evidence
Read the project's status, issues and plan docs first; run tests, build, lint, typecheck and dependency audit where possible. Separate "code done" from "decision/approval pending".

## Checklist
- **Code:** unit/integration/e2e pass; build clean; lint/types clean; reviewed; no debug logs; error handling.
- **Security:** real auth; authorisation on every endpoint; no secrets in code; audit shows no high/critical; CSP/HSTS; rate limits; CORS pinned; independent review/pentest for sensitive data.
- **Data & privacy:** backups + tested restore; migrations versioned; retention and deletion policy; DPIA / regulatory review for health, finance or children's data.
- **Performance:** Core Web Vitals good on a mid-range phone; bundle budget; indexed hot queries; caching.
- **Accessibility:** axe clean; keyboard; manual screen-reader pass.
- **Infrastructure:** prod env vars; DNS/TLS; CDN; logging, error reporting, alerts; health + readiness checks; CI actually run.
- **Domain sign-off:** clinical, legal or compliance approvals where the product needs them; named release owner.
- **Mobile apps:** device builds tested; store policies (privacy labels, account deletion, data safety) met.

## Output
1. Verdict + one-line reason.
2. Table: ID | gap | priority (P0 blocks real users/data, P1 before pilot, P2 before scale, P3 polish) | type (build / decision / external) | next step.
3. Shortest path to launch, with build work and approvals in parallel.
4. Rollout: feature flags, staged % (internal → 5% → 25% → 100%), metrics watched, explicit rollback triggers and steps.
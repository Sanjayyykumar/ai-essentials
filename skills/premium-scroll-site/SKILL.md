---
name: "premium-scroll-site"
description: "Use when building a premium, scroll-driven marketing or landing page (product sites, launches, brand experiences) that must feel bespoke rather than templated."
---

# Premium Scroll Site (adapted from scroll-craft)

Treat scroll as a timeline: the wheel scrubs, the page is a film with real, readable text on top. Paid asset generators are optional; default to the brand's real photos, product screenshots and code-drawn visuals.

## Plan before code
1. Brief: audience, the one action wanted, brand assets, tone.
2. Journey map: what the visitor doubts → what each section resolves.
3. Feeling curve with ONE engineered peak (the signature moment), placed around 60–70% down.
4. Scroll score: one row per section — device, motion, copy, asset.
5. One signature move unique to this brand.

## Rules
- **Variety:** at least 4 device families per page (pinned scrub, horizontal track, layered parallax hero, reveal/mask, counter/data, sticky split, comparison); never the same device twice in a row.
- **Layered hero:** separate background, subject, foreground and atmosphere planes moving at different rates; headline stays readable.
- **No single continuous camera flight** unless the brief literally is one journey.
- **No template tells:** no centred-copy-on-diorama, "01 / 06" counters or "scroll to explore" nudges by default; vary page structure, not just visuals.
- **Readability floor:** body contrast ≥ 4.5:1, headline ≤ 3 lines on a 375 px phone, body 16 px+.
- **Mobile is its own composition**, not the desktop shrunk.
- **Reduced motion:** `prefers-reduced-motion` gets a still, complete page.
- Prefer native CSS scroll-driven animations; fall back to GSAP ScrollTrigger. Animate transform/opacity only; lazy-load heavy media; keep LCP < 2.5 s and CLS < 0.1.
- Semantic HTML, design tokens for colour/type/spacing.

## Verify
Screenshot desktop and phone at 0/25/50/75/100% scroll plus reduced-motion, and view them. Fix contrast, overflow, wrapping and jank before delivering. Publish as an artifact page unless the user wants the files for their own site.
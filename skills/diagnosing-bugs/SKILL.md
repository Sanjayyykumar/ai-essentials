---
name: "diagnosing-bugs"
description: "Diagnosis loop for hard bugs and performance regressions. Use when the user says diagnose/debug this, or reports something broken, throwing, failing or slow."
---

# Diagnosing Bugs

A discipline for hard bugs. Skip phases only when explicitly justified. Read GLOSSARY.md and ADRs in the area if they exist.

**Redact every secret** in commands, outputs and artifacts (`<REDACTED>`); keep credentials in env vars.

## Phase 1: Build a feedback loop (this is the skill)
Get a tight pass/fail signal that goes red on *this* bug. Options, roughly in order: failing test at the seam that reaches the bug; curl/HTTP script against a dev server; CLI run with a fixture diffed against a known-good snapshot; headless browser script (Playwright) asserting DOM/console/network; replay a captured request/payload/event log; throwaway harness with mocked deps; property/fuzz loop; `git bisect run` harness; differential old-vs-new run; last resort, a scripted human-in-the-loop step.

Tighten it: faster (narrow scope, cache setup), sharper (assert the exact symptom), deterministic (pin time, seed RNG, freeze network). For flaky bugs, raise the reproduction rate (loop 100×, parallelise, stress) until debuggable.

If you cannot build a loop, say so, list what you tried, and ask for environment access, a redacted artifact (HAR, logs, dump), or permission for temporary instrumentation. Do not hypothesise without a loop.

Done when you can name one command you have already run that is red-capable (hits the real path, asserts the user's symptom), deterministic, fast, and runnable unattended.

## Phase 2: Reproduce + minimise
Confirm it shows the failure the user described, not a nearby one. Then cut inputs, callers, config and steps one at a time until every remaining element is load-bearing.

## Phase 3: Hypothesise
Write 3–5 ranked, falsifiable hypotheses: "If X is the cause, changing Y makes it disappear / changing Z makes it worse." Show the list to the user before testing (don't block if they're away).

## Phase 4: Instrument
Each probe maps to one prediction; change one variable at a time. Prefer debugger/REPL, then targeted logs at boundaries. Tag every debug log with a unique prefix like `[DEBUG-a4f2]`. For perf regressions: baseline measurement (timer, profiler, EXPLAIN), then bisect.

## Phase 5: Fix + regression test
Write the regression test before the fix, at a seam that exercises the real bug pattern. If no correct seam exists, record that as a finding. Watch it fail, fix, watch it pass, re-run the original Phase 1 loop.

## Phase 6: Cleanup
- Original repro no longer reproduces
- Regression test passes (or missing seam documented)
- All `[DEBUG-...]` logs removed (grep the prefix)
- Throwaway prototypes deleted
- The confirmed cause is stated in the commit/PR message

Adapted from mattpocock/skills (MIT).
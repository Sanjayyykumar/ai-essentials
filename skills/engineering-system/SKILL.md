---
name: "engineering-system"
description: "Default operating system for every software task in any project: inspect-first workflow, smallest safe change, evidence-based verification and token-efficient work. Use at the start of any coding, debugging, design or build task."
---

# Engineering system

Combines the E2E engineering system (e2eengine) with Karpathy's coding guidelines, plus rules for spending tokens wisely. Sources: [Creativestarjsp/e2eskill](https://github.com/Creativestarjsp/e2eskill) and [forrestchang/andrej-karpathy-skills](https://github.com/forrestchang/andrej-karpathy-skills) (MIT); local copies via the tool-library skill.

## Workflow
UNDERSTAND → INSPECT → DEFINE → DESIGN → IMPLEMENT → VALIDATE → REVIEW → VERIFY → DOCUMENT. Scale it: a one-line fix collapses these into seconds; a feature walks every step.

### Before changing anything
1. Inspect the repo: CLAUDE.md/AGENTS.md, README, conventions, the affected files and their callers.
2. Never invent repository facts that can be inspected.
3. Reuse existing conventions and libraries.
4. Define the smallest safe change and how it will be verified, before writing code.

### Think before coding
- State assumptions. If several readings exist, name them; don't pick silently.
- If a simpler approach exists, say so. If something is unclear, stop and ask.

### Simplicity and surgical changes
- Minimum code that solves the problem. No speculative features, abstractions or config.
- Touch only what the task needs. Match existing style. Don't refactor or reformat neighbours.
- Remove only what your change made unused; mention other dead code, don't delete it.
- Test: every changed line traces to the request.

### Goal-driven execution
Turn tasks into checks: "fix bug" → failing test that then passes; "refactor" → tests green before and after. For multi-step work, write a short plan: `step → verify: check`.

### Orchestration (big tasks)
- Decompose into stories; build one at a time; a story is done only with evidence for every acceptance criterion.
- Parallelise only independent work (max ~4 workers); never concurrent edits to the same files.
- Verify independently: a reviewer that didn't write the code checks requirements, security, tests, integration.
- Don't retry a failing approach endlessly; after 2 failures, change approach or escalate.

### Verification
Completion claims need evidence (command run + output). Report facts, inspected evidence, assumptions and unknowns separately. Never say "done" or "passing" without having run it.

### Security
No secrets in code, logs, memory or skills. Respect protected paths. Validate inputs at boundaries.

## Token discipline (always on)
- **Read narrowly**: search (grep/glob) before reading; read the relevant range, not whole large files; never re-read a file you just edited.
- **Batch**: send independent tool calls together; one ToolSearch for all needed tools.
- **Don't dump**: pipe long command output through `head`, `tail`, `grep`, `wc`; save large data to files and compute in code instead of pasting it into context.
- **Reuse**: check memory/project docs and the library INDEX before researching from scratch.
- **Subagents only when justified**: big independent fan-outs or independent review; each starts cold and costs context.
- **Right-size effort**: trivial asks get direct answers; no plans, task lists or ceremony for one-step work.
- **Short replies**: lead with the result; no recaps of steps, no repeated content, no restating the user's request.
- **Stop early**: once the success check passes, stop exploring.

## Done means
Validation run, evidence shown, docs/contracts that the change affects updated, and nothing left silently assumed.

Sources: Creativestarjsp/e2eskill (E2E), forrestchang/andrej-karpathy-skills (MIT).
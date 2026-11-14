---
name: "grilling"
description: "Grill the user relentlessly about a plan, design, or decision until there is shared understanding. Use when the user wants to stress-test their thinking or says grill me."
---

Interview the user relentlessly until you reach a shared understanding. Map it as a **design tree**: every decision branches into the decisions that hang off it.

Work in **rounds**. The **frontier** is every decision whose prerequisites are settled. Ask the whole frontier in one round, numbered, each with your recommended answer, then wait.

```
❓ **Q1** - **<title>**: <question, with choices if useful>

➡️ <recommended answer>

---

❓ **Q2** - ...
```

Word each question so "yes" accepts your recommendation. After each round, recompute the frontier. A question that depends on another still-open question goes in a later round.

Finding facts is your job: look things up in the code, files or tools yourself (or with a subagent) instead of asking. Decisions are the user's: put each to them.

Done when the frontier is empty and nothing is silently assumed. Don't act on the plan until the user confirms shared understanding.

Adapted from mattpocock/skills (MIT).
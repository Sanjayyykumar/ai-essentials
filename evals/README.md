# Efficiency evals
**1. Context cost (automatic):** `python scripts/evals.py` compares the instruction tokens each task type loads under routing vs reading the whole system. `verify.py` checks every scenario path exists.

**2. End-to-end A/B (manual, the honest number):** run the same task twice on the same model, in fresh sessions:
- A: hub linked (`scripts/link.py`) · B: hub unlinked (`scripts/link.py --unlink`)
- Record in `evals/results.csv`: `date,task,model,arm,input_tokens,output_tokens,turns,passed_verify,minutes`
- Token counts: Claude Code `/cost` (or the usage screen); other tools: their usage view.
- Use 3–5 tasks from `evals/context-cost.json` scenarios; report the median per arm.
Only claim a saving that the CSV shows.

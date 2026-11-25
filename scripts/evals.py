#!/usr/bin/env python3
"""Measure context cost: routed (KERNEL + only the files a task needs) vs naive (load the whole system).
   python scripts/evals.py          table + average saving     ·     --check   exit 1 if a scenario path is missing
Measures instruction tokens loaded, not total spend: model reasoning and tool output come on top.
For real end-to-end numbers run the A/B protocol in evals/README.md."""
import glob, json, os, sys
for _s in (sys.stdout,):
    try: _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception: pass
HUB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HUB, "scripts")); from tokens import count
E = json.load(open(os.path.join(HUB, "evals", "context-cost.json"), encoding="utf-8"))
def expand(pats):
    out = []
    for p in pats: out += sorted(glob.glob(os.path.join(HUB, p))) or [os.path.join(HUB, p)]
    return out
def cost(paths):
    missing = [os.path.relpath(p, HUB) for p in paths if not os.path.exists(p)]
    return sum(count(open(p, encoding="utf-8", errors="replace").read()) for p in paths if os.path.exists(p)), missing
naive, nm = cost(expand(E["naive"])); always, am = cost(expand(E["always"]))
miss = nm + am; rows = []
for s in E["scenarios"]:
    c, m = cost(expand(s["opens"])); miss += m; rows.append((s["task"], s["tier"], always + c))
if "--check" in sys.argv:
    for m in miss: print("missing:", m)
    sys.exit(1 if miss else 0)
print(f"naive (whole system): {naive} tokens per task\n")
print(f"{'task':<36}{'tier':<6}{'routed':>8}{'saving':>9}")
for t, tier, c in rows: print(f"{t:<36}{tier:<6}{c:>8}{100 - 100 * c / naive:>8.0f}%")
avg = sum(r[2] for r in rows) / len(rows)
print(f"\naverage routed {avg:.0f} tokens · saving {100 - 100 * avg / naive:.0f}% of instruction context vs naive")
if miss: print("missing paths:", ", ".join(miss))

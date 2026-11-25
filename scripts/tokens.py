#!/usr/bin/env python3
"""Token cost of the hub's context files.   python scripts/tokens.py   ·   --check (exit 1 if over budget)
Uses tiktoken when installed (close to most vendors), else ~4 chars/token. Budgets keep the always-loaded part tiny."""
import argparse, glob, os, re, sys
HUB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUDGET = {"KERNEL.md": 800, "AI.md": 1800}   # KERNEL is loaded every session; AI.md only when routing
SKILL_DESC_WORDS = 60
try:
    import tiktoken; _enc = tiktoken.get_encoding("cl100k_base"); count = lambda s: len(_enc.encode(s)); METHOD = "tiktoken"
except Exception:
    count = lambda s: (len(s) + 3) // 4; METHOD = "chars/4"
def read(p): return open(p, encoding="utf-8", errors="replace").read()
def report():
    rows, over = [], []
    for f, b in BUDGET.items():
        p = os.path.join(HUB, f)
        if os.path.exists(p):
            n = count(read(p)); rows.append((f, n, b))
            if n > b: over.append(f"{f}: {n} > {b} tokens")
    for p in sorted(glob.glob(os.path.join(HUB, "playbooks", "*.md")) + glob.glob(os.path.join(HUB, "system", "*.md"))):
        rows.append((os.path.relpath(p, HUB), count(read(p)), None))
    desc_total = 0
    for p in sorted(glob.glob(os.path.join(HUB, "skills", "*", "SKILL.md"))):
        m = re.search(r"^description:\s*(.*)$", read(p)[:4000], re.M); d = (m.group(1) if m else "").strip().strip('"')
        desc_total += count(d)
        if len(d.split()) > SKILL_DESC_WORDS: over.append(f"{os.path.relpath(p, HUB)}: description {len(d.split())} words > {SKILL_DESC_WORDS}")
    rows.append(("skills/* descriptions (always listed by hosts)", desc_total, None))
    return rows, over
def main():
    ap = argparse.ArgumentParser(description=__doc__); ap.add_argument("--check", action="store_true"); a = ap.parse_args()
    rows, over = report()
    if not a.check:
        print(f"method: {METHOD}")
        for f, n, b in rows: print(f"  {n:>6}  {f}" + (f"  (budget {b})" if b else ""))
        always = next((n for f, n, _ in rows if f == "KERNEL.md"), 0) + rows[-1][1]
        print(f"always-loaded ≈ {always} tokens (kernel + skill descriptions)")
    for o in over: print("OVER", o)
    sys.exit(1 if over else 0)
if __name__ == "__main__": main()

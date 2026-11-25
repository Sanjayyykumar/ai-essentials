#!/usr/bin/env python3
"""Which model and effort for this task?   python scripts/models.py H   ·   python scripts/models.py M --vendor gemini
   python scripts/models.py --classify "refactor the auth service across 12 files"   (keyword guess at the tier)"""
import argparse, json, os, re, sys
for _s in (sys.stdout,):
    try: _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception: pass
HUB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
M = json.load(open(os.path.join(HUB, "libraries", "models.json"), encoding="utf-8"))
RULES = [("X", r"autonomous|end[- ]to[- ]end build|deep research|from scratch .*(platform|system)|multi-day"),
         ("H", r"architect|design (a|the) system|refactor|migrat|security|vulnerab|race|deadlock|perf(ormance)? regression|root cause|research|compare .* options|across \d+ files|multi-file"),
         ("L", r"rename|typo|format|lookup|what is|where is|list |status|summari[sz]e (this|the) (file|log)|small edit|one-line"),
         ("M", r".")]
def classify(t):
    for tier, rx in RULES:
        if re.search(rx, t, re.I): return tier
def main():
    ap = argparse.ArgumentParser(description=__doc__); ap.add_argument("tier", nargs="?", choices=list("LMHX"))
    ap.add_argument("--vendor"); ap.add_argument("--classify"); a = ap.parse_args()
    tier = a.tier or (classify(a.classify) if a.classify else None)
    if not tier: ap.error("give a tier (L/M/H/X) or --classify \"task text\"")
    t = M["tiers"][tier]
    print(f"Tier {tier} · effort {t['effort']} · {t['use']}")
    for v, d in M["vendors"].items():
        if a.vendor and v != a.vendor: continue
        print(f"  {v:<7} {d[tier]}{'' if d.get('verified') is True else ('  (partly verified: check ' + d.get('sources', ['vendor page'])[0] + ')' if d.get('verified') == 'partial' else '  (class; confirm exact model on vendor page)')}")
        if a.vendor: print(f"          switch: {d['switch']}")
    print(f"models list verified {M['verified']}")
if __name__ == "__main__": main()

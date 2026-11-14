#!/usr/bin/env python3
"""Live status for any AI agent. Usage:
  python scripts/status.py set PHASE "now text" [--step 3/7] [--next "..."] [--blocker "..."] [--done "item"] [--out path]
  python scripts/status.py show
Writes STATUS.md in the current working directory (or $AI_STATUS_FILE)."""
import os, sys, re, datetime, argparse
F = os.environ.get("AI_STATUS_FILE", "STATUS.md")
KEYS = ["phase","step","updated","now","done","next","blockers","assumptions","outputs"]
PHASES = {"INTAKE","RECON","PLAN","BUILD","VERIFY","DELIVERED","BLOCKED"}
def load():
    d = {k: "" for k in KEYS}
    if os.path.exists(F):
        for line in open(F, encoding="utf-8"):
            m = re.match(r"^(\w+):\s?(.*)$", line.rstrip("\n"))
            if m and m.group(1) in d: d[m.group(1)] = m.group(2)
    return d
def lst(s): return [x.strip() for x in s.strip("[]").split(",") if x.strip()]
def save(d):
    with open(F, "w", encoding="utf-8") as f:
        f.write("# STATUS\n```\n" + "\n".join(f"{k}: {d[k]}" for k in KEYS) + "\n```\n")
def main():
    p = argparse.ArgumentParser(); s = p.add_subparsers(dest="cmd", required=True)
    a = s.add_parser("set"); a.add_argument("phase"); a.add_argument("now")
    for o in ["step","next","blocker","done","out","assume"]: a.add_argument("--"+o)
    s.add_parser("show"); x = p.parse_args()
    d = load()
    if x.cmd == "show": print(open(F, encoding="utf-8").read() if os.path.exists(F) else "no STATUS.md"); return
    ph = x.phase.upper()
    if ph not in PHASES: sys.exit(f"phase must be one of {sorted(PHASES)}")
    d.update(phase=ph, now=x.now, updated=datetime.datetime.now().isoformat(timespec="minutes"))
    if x.step: d["step"] = x.step
    if x.next: d["next"] = x.next
    if x.blocker: d["blockers"] = x.blocker
    elif ph != "BLOCKED" and not d["blockers"]: d["blockers"] = "none"
    for key, val in (("done", x.done), ("outputs", x.out), ("assumptions", x.assume)):
        if val: d[key] = "[" + ", ".join(lst(d[key]) + [val]) + "]"
    save(d); print(f"{ph} {d['step']} — {x.now}")
if __name__ == "__main__": main()

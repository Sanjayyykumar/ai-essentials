#!/usr/bin/env python3
"""Project brain: one clear structure for any project, readable by any AI.  Files live in <project>/.ai/
  python project.py init [--name N] [--goal "..."]            create .ai/ (PROJECT, TASKS, STATUS, DECISIONS, HANDOFF)
  python project.py add "Title" --accept "criteria" --verify "cmd" [--deps T-001,T-002] [--tier M] [--epic E1]
  python project.py next | start T-003 | done T-003 | block T-003 "reason" | list [--all] | tree
  python project.py decide "choice" --alt "other options" --why "reason"
Rules: every task has acceptance criteria and a verify command; a task can start only when its deps are done;
STATUS.md is updated on start/done/block so any AI resumes by reading STATUS + the next task only."""
import argparse, datetime, os, re, sys
for _s in (sys.stdout, sys.stderr):
    try: _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception: pass
D = os.path.join(os.getcwd(), ".ai"); TASKS = os.path.join(D, "TASKS.md")
HEAD = "| ID | Epic | Task | Tier | Status | Deps | Acceptance | Verify |\n|---|---|---|---|---|---|---|---|\n"
STATES = {"todo", "doing", "done", "blocked"}
now = lambda: datetime.datetime.now().isoformat(timespec="minutes")

def w(p, s): open(p, "w", encoding="utf-8", newline="\n").write(s)
def load():
    if not os.path.exists(TASKS): sys.exit("no .ai/TASKS.md here: run `project.py init` first")
    rows = []
    for line in open(TASKS, encoding="utf-8"):
        c = [x.strip() for x in line.strip().strip("|").split("|")]
        if len(c) == 8 and re.fullmatch(r"T-\d{3,}", c[0]):
            rows.append(dict(zip(["id", "epic", "task", "tier", "status", "deps", "accept", "verify"], c)))
    return rows
def save(rows):
    txt = open(TASKS, encoding="utf-8").read(); i = txt.find("| ID |")
    pre = txt[:i] if i >= 0 else txt
    w(TASKS, pre + HEAD + "".join(f"| {r['id']} | {r['epic']} | {r['task']} | {r['tier']} | {r['status']} | {r['deps']} | {r['accept']} | {r['verify']} |\n" for r in rows))
def deps_ok(r, rows):
    done = {x["id"] for x in rows if x["status"] == "done"}
    return all(d in done for d in [x.strip() for x in r["deps"].split(",") if x.strip() and x.strip() != "-"])
def status(phase, nowtxt, rows, nxt=None, blocker=None):
    done = [r["id"] for r in rows if r["status"] == "done"]
    n = nxt or next((r for r in rows if r["status"] == "todo" and deps_ok(r, rows)), None)
    p = os.path.join(D, "STATUS.md"); old = open(p, encoding="utf-8").read() if os.path.exists(p) else ""
    keep = {k: v for k, v in re.findall(r"^(assumptions|outputs|proof):\s?(.*)$", old, re.M)}
    w(p, "# STATUS\n```\n" + "\n".join([f"phase: {phase}", f"step: {len(done)}/{len(rows)}", f"updated: {now()}", f"now: {nowtxt}",
        f"done: [{', '.join(done)}]", f"next: {n['id'] + ' ' + n['task'] if n else 'none'}", f"blockers: {blocker or 'none'}",
        f"assumptions: {keep.get('assumptions', '[]')}", f"outputs: {keep.get('outputs', '[]')}", f"proof: {keep.get('proof', 'NONE')}"]) + "\n```\n")

def init(a):
    os.makedirs(D, exist_ok=True); name = a.name or os.path.basename(os.getcwd())
    files = {
      "PROJECT.md": f"# {name}\n- Goal (1 line): {a.goal or ''}\n- Users / audience:\n- Deliverables (path + format):\n- Scope IN:\n- Scope OUT (deferred):\n- Stack / tools:\n- Constraints (deadline, budget, brand, licences):\n- Definition of done: verify.py reaches P2 + domain gate (P3) for every deliverable\n",
      "TASKS.md": "# Tasks\nEpic → Task (≤2 h, one outcome) → steps in the task's own notes. Status: todo · doing · done · blocked.\nEvery task: acceptance criteria (observable) + verify command. Edit with `project.py`, or by hand keeping the table shape.\n\n" + HEAD,
      "DECISIONS.md": "# Decisions (newest last · date | choice | alternatives | why)\n",
      "HANDOFF.md": "# Handoff (update at session end)\n- State:\n- In progress (file/line/command):\n- Next 3 actions:\n- Gotchas:\n",
    }
    for f, body in files.items():
        p = os.path.join(D, f)
        if not os.path.exists(p): w(p, body); print("created", os.path.relpath(p))
        else: print("exists ", os.path.relpath(p))
    status("INTAKE", "project initialised: fill PROJECT.md, then add tasks", load())
def add(a):
    rows = load(); nid = f"T-{max([int(r['id'][2:]) for r in rows] + [0]) + 1:03d}"
    if not a.accept or not a.verify: sys.exit("refused: a task needs --accept (observable criteria) and --verify (command or check)")
    clean = lambda s: (s or "-").replace("|", "/")
    rows.append(dict(id=nid, epic=clean(a.epic), task=clean(a.title), tier=a.tier, status="todo", deps=clean(a.deps), accept=clean(a.accept), verify=clean(a.verify)))
    save(rows); print("added", nid, a.title)
def get(rows, i):
    r = next((x for x in rows if x["id"] == i.upper()), None)
    if not r: sys.exit(f"no task {i}")
    return r
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter); s = ap.add_subparsers(dest="cmd", required=True)
    p = s.add_parser("init"); p.add_argument("--name"); p.add_argument("--goal")
    p = s.add_parser("add"); p.add_argument("title"); p.add_argument("--accept"); p.add_argument("--verify"); p.add_argument("--deps"); p.add_argument("--tier", default="M", choices=list("LMHX")); p.add_argument("--epic")
    for c in ("start", "done"): s.add_parser(c).add_argument("id")
    p = s.add_parser("block"); p.add_argument("id"); p.add_argument("reason")
    s.add_parser("next"); s.add_parser("tree"); s.add_parser("list").add_argument("--all", action="store_true")
    p = s.add_parser("decide"); p.add_argument("choice"); p.add_argument("--alt", default="-"); p.add_argument("--why", required=True)
    a = ap.parse_args()
    if a.cmd == "init": return init(a)
    if a.cmd == "add": return add(a)
    if a.cmd == "decide":
        open(os.path.join(D, "DECISIONS.md"), "a", encoding="utf-8").write(f"- {now()[:10]} | {a.choice} | {a.alt} | {a.why}\n"); return print("logged decision")
    rows = load()
    if a.cmd in ("start", "done", "block"):
        r = get(rows, a.id)
        if a.cmd == "start" and not deps_ok(r, rows): sys.exit(f"{r['id']} waits on: {r['deps']}")
        r["status"] = {"start": "doing", "done": "done", "block": "blocked"}[a.cmd]; save(rows)
        if a.cmd == "start": status("BUILD", f"{r['id']} {r['task']} · accept: {r['accept']}", rows, nxt=r)
        elif a.cmd == "done": status("BUILD" if any(x["status"] != "done" for x in rows) else "VERIFY", f"{r['id']} done (verified by: {r['verify']})", rows)
        else: status("BLOCKED", f"{r['id']} blocked", rows, blocker=a.reason)
        return print(f"{r['id']} -> {r['status']}")
    if a.cmd == "next":
        n = next((r for r in rows if r["status"] == "doing"), None) or next((r for r in rows if r["status"] == "todo" and deps_ok(r, rows)), None)
        return print(f"{n['id']} [{n['tier']}] {n['task']}\n  accept: {n['accept']}\n  verify: {n['verify']}" if n else "nothing ready (all done or blocked)")
    if a.cmd == "tree":
        for e in dict.fromkeys(r["epic"] for r in rows):
            print(e if e != "-" else "(no epic)")
            for r in (x for x in rows if x["epic"] == e): print(f"  {'✓' if r['status']=='done' else '▶' if r['status']=='doing' else '✗' if r['status']=='blocked' else '·'} {r['id']} {r['task']}" + (f"  ← {r['deps']}" if r["deps"] != "-" else ""))
        return
    for r in rows:
        if a.all or r["status"] != "done": print(f"{r['id']} {r['status']:<7} [{r['tier']}] {r['task']}")
if __name__ == "__main__": main()

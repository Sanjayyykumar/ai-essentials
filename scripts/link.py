#!/usr/bin/env python3
"""Register AI Essentials with every AI on this machine, once. After this, each AI loads the kernel
by itself every session; nobody has to say "read AI.md" again.

    python scripts/link.py               # link Claude Code, Gemini CLI/Antigravity, Codex (+ Windsurf if installed)
    python scripts/link.py --dry-run     # show what would change, change nothing
    python scripts/link.py --check       # report link status only
    python scripts/link.py --unlink      # remove every block this script added
    python scripts/link.py --only claude,codex

Safety: writes only between the markers below, backs up a file before its first change
(<file>.bak-<timestamp>), and is idempotent (re-run after editing KERNEL.md to refresh).
Hosts without a global rules file (Cursor, claude.ai, ChatGPT, Grok, Kimi) get dist/PASTE-INSTRUCTIONS.md.
"""
import argparse, datetime, os, re, shutil, sys

for _s in (sys.stdout, sys.stderr):
    try: _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception: pass

HUB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOME = os.path.expanduser("~")
BEGIN, END = "<!-- ai-essentials:begin (managed by scripts/link.py — edit KERNEL.md, then re-run) -->", "<!-- ai-essentials:end -->"
BLOCK_RX = re.compile(re.escape(BEGIN.split(" (")[0]) + r".*?" + re.escape(END) + r"\n?", re.S)

# name -> (rules file, when to link: "always" or a folder that must already exist)
TARGETS = {
    "claude":   (os.path.join(HOME, ".claude", "CLAUDE.md"), "always"),
    "gemini":   (os.path.join(HOME, ".gemini", "GEMINI.md"), "always"),   # Gemini CLI + Antigravity
    "codex":    (os.path.join(HOME, ".codex", "AGENTS.md"), "always"),
    "windsurf": (os.path.join(HOME, ".codeium", "windsurf", "memories", "global_rules.md"), os.path.join(HOME, ".codeium", "windsurf")),
}
AGENTS_SRC, AGENTS_DST = os.path.join(HUB, "agents"), os.path.join(HOME, ".claude", "agents")

def kernel():
    txt = open(os.path.join(HUB, "KERNEL.md"), encoding="utf-8").read()
    return txt.replace("{{HUB}}", HUB.replace("\\", "/")).strip() + "\n"

def block(): return f"{BEGIN}\n{kernel()}{END}\n"

def read(p): return open(p, encoding="utf-8").read() if os.path.exists(p) else ""

def write(p, new, dry):
    if dry: print(f"    would write {p}"); return
    os.makedirs(os.path.dirname(p), exist_ok=True)
    if os.path.exists(p) and not any(f.startswith(os.path.basename(p) + ".bak-") for f in os.listdir(os.path.dirname(p))):
        shutil.copy2(p, p + ".bak-" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
    open(p, "w", encoding="utf-8", newline="\n").write(new)

def status(p):
    cur = read(p); m = BLOCK_RX.search(cur)
    if not m: return "not linked"
    return "linked" if m.group(0).rstrip("\n") == block().rstrip("\n") else "stale (re-run link.py)"

def link_one(name, p, a):
    cur = read(p)
    if a.unlink:
        if BLOCK_RX.search(cur): write(p, BLOCK_RX.sub("", cur).rstrip() + ("\n" if cur.strip() else ""), a.dry_run); return "unlinked"
        return "not linked"
    if status(p) == "linked": return "ok"
    new = BLOCK_RX.sub(block(), cur) if BLOCK_RX.search(cur) else (cur.rstrip() + "\n\n" if cur.strip() else "") + block()
    write(p, new, a.dry_run); return "linked" if not a.dry_run else "would link"

def link_agents(a):
    if not os.path.isdir(AGENTS_SRC): return []
    out = []
    for f in sorted(os.listdir(AGENTS_SRC)):
        if not f.endswith(".md"): continue
        src, dst = os.path.join(AGENTS_SRC, f), os.path.join(AGENTS_DST, "ae-" + f)
        if a.unlink:
            had = os.path.exists(dst)
            if had and not a.dry_run: os.remove(dst)
            out.append((f, ("would remove" if a.dry_run else "removed") if had else "absent")); continue
        same = os.path.exists(dst) and read(dst) == read(src)
        if a.check: out.append((f, "ok" if same else "missing")); continue
        if not same and not a.dry_run:
            os.makedirs(AGENTS_DST, exist_ok=True); shutil.copy2(src, dst)
        out.append((f, "ok" if same else ("would copy" if a.dry_run else "installed")))
    return out

def paste_file(a):
    p = os.path.join(HUB, "dist", "PASTE-INSTRUCTIONS.md")
    body = ("# Paste this into: Cursor (Settings → Rules → User Rules), claude.ai (Project instructions or Settings → "
            "Profile), ChatGPT (Custom instructions), Grok / Kimi (system or custom instructions).\n"
            "# Web apps cannot read your disk: for them, also upload the hub skills zip (scripts/pack.ps1).\n\n" + kernel())
    if not a.dry_run and not a.check and not a.unlink:
        os.makedirs(os.path.dirname(p), exist_ok=True); open(p, "w", encoding="utf-8", newline="\n").write(body)
    return p

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true"); ap.add_argument("--check", action="store_true")
    ap.add_argument("--unlink", action="store_true"); ap.add_argument("--only", help="comma list: " + ",".join(TARGETS))
    a = ap.parse_args()
    only = set(a.only.split(",")) if a.only else set(TARGETS)
    bad = 0
    print(f"AI Essentials link · hub {HUB}")
    for name, (p, cond) in TARGETS.items():
        if name not in only: continue
        if cond != "always" and not os.path.isdir(cond): print(f"  {'skipped':<12} {name:<9} (not installed)"); continue
        st = status(p) if a.check else link_one(name, p, a)
        if a.check and st != "linked": bad += 1
        print(f"  {st:<12} {name:<9} {p}")
    if "claude" in only:
        for f, st in link_agents(a):
            if a.check and st != "ok": bad += 1
            print(f"  {st:<12} agent     {os.path.join(AGENTS_DST, 'ae-' + f)}")
    print(f"  {'paste-file':<12} others    {paste_file(a)}")
    if not a.check and not a.dry_run and not a.unlink:
        print("\nDone. Restart each AI app/CLI once; from now on it loads the kernel automatically.")
    sys.exit(1 if bad else 0)

if __name__ == "__main__": main()

#!/usr/bin/env python3
"""Learning loop: lessons that recur become rules, so the next session is cheaper.
  python learn.py add <domain> "lesson"     add, or bump `seen` if a near-duplicate exists
  python learn.py list [domain]             show lessons, most-seen first
  python learn.py promote                   lessons seen >=3 times + where to turn them into a rule
  python learn.py retro                     4-question session review (what cost extra turns/tokens?)
Stores in $AI_HUB_ROOT/system/LESSONS.md (shared by every project and every AI). Never record secrets."""
import datetime, difflib, os, re, sys
for _s in (sys.stdout,):
    try: _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception: pass
HUB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = os.path.join(HUB, "system", "LESSONS.md")
HEAD = "# Lessons (managed by scripts/learn.py · date | domain | lesson | seen:N)\n"
RX = re.compile(r"^- (\d{4}-\d{2}-\d{2}) \| ([\w/-]+) \| (.+?) \| seen:(\d+)\s*$")
DEST = {"dev": "playbooks/development.md", "code": "playbooks/development.md", "video": "playbooks/video.md", "image": "playbooks/image.md",
        "design": "playbooks/design.md", "logo": "playbooks/logo.md", "svg": "playbooks/svg.md", "audio": "playbooks/audio.md",
        "content": "playbooks/content.md", "animation": "playbooks/animation.md", "research": "recon/RECON.md",
        "tokens": "system/01-token-economy.md", "process": "system/00-lifecycle.md", "decisions": "system/06-precision.md"}
def load():
    rows, other = [], []
    if os.path.exists(F):
        for line in open(F, encoding="utf-8"):
            m = RX.match(line.rstrip("\n"))
            if m: rows.append({"date": m[1], "domain": m[2], "text": m[3], "seen": int(m[4])})
            elif line.strip() and not line.startswith("# Lessons"): other.append(line.rstrip("\n"))
    return rows, other
def save(rows, other):
    body = HEAD + "".join(f"- {r['date']} | {r['domain']} | {r['text']} | seen:{r['seen']}\n" for r in rows)
    if other: body += "\n## Older notes\n" + "\n".join(other) + "\n"
    open(F, "w", encoding="utf-8", newline="\n").write(body)
def main():
    a = sys.argv[1:]
    if not a: sys.exit(__doc__)
    rows, other = load()
    if a[0] == "add" and len(a) >= 3:
        dom, text = a[1].lower(), " ".join(a[2:]).replace("|", "/").strip()
        if re.search(r"(?i)(api[_-]?key|token|password|secret)\s*[:=]", text): sys.exit("refused: looks like a secret")
        best = max(rows, key=lambda r: difflib.SequenceMatcher(None, r["text"].lower(), text.lower()).ratio(), default=None)
        if best and difflib.SequenceMatcher(None, best["text"].lower(), text.lower()).ratio() >= 0.75:
            best["seen"] += 1; best["date"] = datetime.date.today().isoformat(); save(rows, other)
            return print(f"seen again ({best['seen']}x): {best['text']}" + ("  → promote it: python learn.py promote" if best["seen"] >= 3 else ""))
        rows.append({"date": datetime.date.today().isoformat(), "domain": dom, "text": text, "seen": 1}); save(rows, other); return print("learned:", text)
    if a[0] == "list":
        for r in sorted((r for r in rows if len(a) < 2 or r["domain"] == a[1]), key=lambda r: -r["seen"]):
            print(f"{r['seen']:>2}x {r['domain']:<10} {r['text']}")
        return
    if a[0] == "promote":
        hot = [r for r in rows if r["seen"] >= 3]
        if not hot: return print("nothing seen 3+ times yet")
        for r in hot: print(f"{r['seen']}x [{r['domain']}] {r['text']}\n    → add as a rule in {DEST.get(r['domain'], 'the matching playbook')} (or KERNEL.md if it applies to every task), then delete this line")
        return
    if a[0] == "retro":
        return print("Session retro (answer in one line each; add real lessons with `learn.py add`):\n"
                     "1. Which step took extra turns, and what would have avoided it?\n"
                     "2. What did I read or search more than once (should have gone into STATUS)?\n"
                     "3. What failed verify or the user's review, and what rule would have caught it?\n"
                     "4. Was the tier/model right for the work? (python scripts/models.py --classify \"…\")")
    sys.exit(__doc__)
if __name__ == "__main__": main()

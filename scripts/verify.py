#!/usr/bin/env python3
"""One proof command for any AI agent. Evidence, not claims.

    python scripts/verify.py                    # prove this hub (P0-P2)
    python scripts/verify.py --project PATH     # prove a project built with the hub (P0-P2)
    python scripts/verify.py --json             # machine output only

Proof levels (each requires the previous one):
  P0 STRUCTURE  - files parse: Python compiles, JSON loads, Markdown links resolve, SKILL.md frontmatter valid
  P1 GUARDRAILS - no secrets, no committed junk (pycache/.env/keys), no oversized files
  P2 CONTRACT   - hub: Router targets + registry + install manifest valid
                  project: detected build/test commands run and pass
  P3 DELIVERABLE- not automatic: the domain gate in system/03-quality-gates.md, checked by the agent with evidence
Writes evidence to <target>/.proof/verify.json. Exit code 0 only when P2 is reached.
"""
import argparse, datetime, fnmatch, json, os, re, shutil, subprocess, sys

for _s in (sys.stdout, sys.stderr):
    try: _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception: pass

HUB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "dist", "build", "target", ".proof", ".next", ".e2e", ".pytest_cache", ".mypy_cache", ".ruff_cache"}
SECRET_RX = [
    ("private key", re.compile(r"-----BEGIN (RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----")),
    ("AWS key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("GitHub token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{36,}\b")),
    ("Anthropic key", re.compile(r"\bsk-ant-[A-Za-z0-9_-]{20,}")),
    ("OpenAI key", re.compile(r"\bsk-(proj-)?[A-Za-z0-9]{32,}\b")),
    ("Google API key", re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b")),
    ("Slack token", re.compile(r"\bxox[abpr]-[A-Za-z0-9-]{10,}")),
    ("hardcoded secret", re.compile(r"(?i)\b(api[_-]?key|secret|password|token)\b\s*[:=]\s*['\"][^'\"\s$<{]{12,}['\"]")),
]
JUNK = ["*.pyc", ".env", "*.pem", "id_rsa", "*.key", "Thumbs.db", ".DS_Store", "desktop.ini"]
TEXT_EXT = {".py", ".js", ".ts", ".tsx", ".jsx", ".json", ".md", ".yml", ".yaml", ".toml", ".ini", ".cfg",
            ".sh", ".ps1", ".java", ".kt", ".go", ".rs", ".html", ".css", ".env", ".txt", ".xml", ".properties"}
MAX_MB = 5

def load_ignore(root):
    pats = []
    p = os.path.join(root, ".gitignore")
    if os.path.exists(p):
        for line in open(p, encoding="utf-8", errors="replace"):
            line = line.strip()
            if line and not line.startswith(("#", "!")): pats.append(line.rstrip("/"))
    return pats

def ignored(rel, pats):
    parts = rel.replace("\\", "/").split("/")
    for pat in pats:
        pat = pat.lstrip("/")
        if "/" in pat:
            if fnmatch.fnmatch("/".join(parts), pat) or "/".join(parts).startswith(pat + "/"): return True
        elif any(fnmatch.fnmatch(x, pat) for x in parts): return True
    return False

def files(root):
    pats = load_ignore(root)
    for dp, dns, fns in os.walk(root):
        rel_dp = os.path.relpath(dp, root)
        dns[:] = [d for d in dns if d not in SKIP_DIRS and d != "__pycache__"
                  and not ignored(os.path.normpath(os.path.join(rel_dp, d)), pats)]
        for f in fns:
            rel = os.path.normpath(os.path.join(rel_dp, f))
            if not ignored(rel, pats): yield rel

class Report:
    def __init__(self): self.checks = []
    def add(self, level, name, ok, detail=""):
        self.checks.append({"level": level, "check": name, "ok": bool(ok), "detail": detail})
    def level_ok(self, lvl): return all(c["ok"] for c in self.checks if c["level"] == lvl)

def p0(root, fl, r):
    bad = []
    for f in (x for x in fl if x.endswith(".py")):
        try: compile(open(os.path.join(root, f), "rb").read(), f, "exec")
        except SyntaxError as e: bad.append(f"{f}:{e.lineno}: {e.msg}")
        except Exception as e: bad.append(f"{f}: {e}")
    r.add("P0", "python compiles", not bad, "; ".join(bad[:5]))
    bad = []
    for f in (x for x in fl if x.endswith(".json")):
        try: json.load(open(os.path.join(root, f), encoding="utf-8"))
        except Exception as e: bad.append(f"{f}: {e}")
    r.add("P0", "json parses", not bad, "; ".join(bad[:5]))
    bad = []
    link = re.compile(r"\]\(((?!https?:|mailto:|#)[^)\s]+)\)|`((?:system|playbooks|recon|libraries|scripts|templates|studio|skills)/[\w./-]+\.(?:md|py|json|yml))`")
    for f in (x for x in fl if x.endswith(".md")):
        if f.replace("\\", "/").startswith(("opensource/", "skills/")): base_only = True
        else: base_only = False
        txt = open(os.path.join(root, f), encoding="utf-8", errors="replace").read()
        for m in link.finditer(txt):
            if m.group(2) and base_only: continue  # skills/opensource name paths in other repos ($VIDEO_ROOT etc.)
            target = (m.group(1) or m.group(2)).split("#")[0]
            if not target or "<" in target or "*" in target: continue
            cands = [os.path.join(os.path.dirname(os.path.join(root, f)), target)]
            if m.group(2) or not base_only: cands.append(os.path.join(root, target))
            if not any(os.path.exists(c) for c in cands): bad.append(f"{f} -> {target}")
    r.add("P0", "markdown links resolve", not bad, "; ".join(bad[:8]) + (f" (+{len(bad)-8})" if len(bad) > 8 else ""))
    bad = []
    for f in (x for x in fl if os.path.basename(x) == "SKILL.md"):
        head = open(os.path.join(root, f), encoding="utf-8", errors="replace").read(3000)
        m = re.match(r"^---\s*\n(.*?)\n---", head, re.S)
        if not m or not re.search(r"^name:\s*\S", m.group(1), re.M) or not re.search(r"^description:\s*\S", m.group(1), re.M):
            bad.append(f)
    r.add("P0", "SKILL.md frontmatter (name+description)", not bad, "; ".join(bad[:5]))

def p1(root, fl, r):
    hits = []
    for f in fl:
        ext = os.path.splitext(f)[1].lower()
        if ext not in TEXT_EXT or f.replace("\\", "/").startswith(".proof/"): continue
        try: txt = open(os.path.join(root, f), encoding="utf-8", errors="ignore").read(400_000)
        except Exception: continue
        for name, rx in SECRET_RX:
            for m in rx.finditer(txt):
                line = txt[max(0, txt.rfind("\n", 0, m.start())):m.end()]
                if re.search(r"(?i)example|placeholder|your[_-]|xxxx|dummy|os\.environ|getenv|secrets\.", line): continue
                hits.append(f"{f}: {name}")
                break
    r.add("P1", "no secrets", not hits, "; ".join(sorted(set(hits))[:8]))
    junk = [f for f in fl if any(fnmatch.fnmatch(os.path.basename(f), j) for j in JUNK)]
    r.add("P1", "no committed junk (.env, keys, pyc, OS files)", not junk, "; ".join(junk[:8]))
    big = []
    for f in fl:
        try:
            if os.path.getsize(os.path.join(root, f)) > MAX_MB * 1024 * 1024: big.append(f)
        except OSError: pass
    r.add("P1", f"no files > {MAX_MB} MB (use releases/LFS)", not big, "; ".join(big[:5]))

def p2_hub(root, r):
    ai = open(os.path.join(root, "AI.md"), encoding="utf-8").read()
    targets = set(re.findall(r"`((?:system|playbooks|recon|libraries|studio|skills|templates|scripts)/[\w./-]+?)`", ai))
    missing = [t for t in targets if not os.path.exists(os.path.join(root, t.rstrip("/")))]
    r.add("P2", "AI.md router targets exist", not missing, "; ".join(sorted(missing)))
    for redirect in ("CLAUDE.md", "AGENTS.md", "GEMINI.md"):
        p = os.path.join(root, redirect)
        r.add("P2", f"{redirect} redirects to AI.md", os.path.exists(p) and "AI.md" in open(p, encoding="utf-8").read())
    try:
        reg = json.load(open(os.path.join(root, "libraries", "registry.json"), encoding="utf-8"))
        need = {"id", "domain", "use", "upstream", "license"}
        bad = [str(i.get("id", "?")) for i in reg["items"] if not need <= set(i)]
        ids = [i.get("id") for i in reg["items"]]
        dup = sorted({x for x in ids if ids.count(x) > 1})
        r.add("P2", "registry entries complete & unique", not bad and not dup, f"incomplete={bad[:5]} dup={dup[:5]}")
    except Exception as e:
        r.add("P2", "registry entries complete & unique", False, str(e))
    p = os.path.join(root, "libraries", "install.json")
    if os.path.exists(p):
        try: json.load(open(p, encoding="utf-8")); r.add("P2", "install manifest valid", True)
        except Exception as e: r.add("P2", "install manifest valid", False, str(e))
    tk = subprocess.run([sys.executable, os.path.join(root, "scripts", "tokens.py"), "--check"], capture_output=True, text=True, cwd=root)
    r.add("P2", "token budgets (KERNEL ≤800, skill descriptions ≤60 words)", tk.returncode == 0, tk.stdout.strip()[:600])
    kern = os.path.join(root, "KERNEL.md")
    kt = open(kern, encoding="utf-8").read() if os.path.exists(kern) else ""
    kmiss = [t for t in re.findall(r"\{\{HUB\}\}/([\w./-]+)", kt) if not os.path.exists(os.path.join(root, t.rstrip("/.")))]
    r.add("P2", "KERNEL.md exists and its paths resolve", bool(kt) and not kmiss, "; ".join(kmiss))
    try:
        mj = json.load(open(os.path.join(root, "libraries", "models.json"), encoding="utf-8"))
        okm = all(t in v for v in mj["vendors"].values() for t in "LMHX") and set(mj["tiers"]) == set("LMHX")
        r.add("P2", "models.json covers tiers L/M/H/X for every vendor", okm)
    except Exception as e: r.add("P2", "models.json covers tiers L/M/H/X for every vendor", False, str(e))
    bad = []
    for f in sorted(os.listdir(os.path.join(root, "agents"))) if os.path.isdir(os.path.join(root, "agents")) else []:
        h = open(os.path.join(root, "agents", f), encoding="utf-8").read(1500)
        if not all(re.search(rf"^{k}:\s*\S", h, re.M) for k in ("name", "description", "model")): bad.append(f)
    r.add("P2", "agents/*.md frontmatter (name, description, model)", not bad, "; ".join(bad))
    if os.path.exists(os.path.join(root, "scripts", "evals.py")):
        ev = subprocess.run([sys.executable, os.path.join(root, "scripts", "evals.py"), "--check"], capture_output=True, text=True, cwd=root)
        r.add("P2", "eval scenarios reference existing files", ev.returncode == 0, ev.stdout.strip()[:400])
    for s in ("status.py", "find.py"):
        ok = subprocess.run([sys.executable, os.path.join(root, "scripts", s), "--help" if s == "status.py" else "video"],
                            capture_output=True, text=True, cwd=root).returncode == 0
        r.add("P2", f"scripts/{s} runs", ok)

def detect_commands(root):
    """Return the project's own build/test commands. Never invents tests."""
    cmds, has = [], lambda f: os.path.exists(os.path.join(root, f))
    if has("package.json"):
        pkg = json.load(open(os.path.join(root, "package.json"), encoding="utf-8"))
        sc = pkg.get("scripts", {}); pm = "pnpm" if has("pnpm-lock.yaml") else "yarn" if has("yarn.lock") else "npm"
        for s in ("lint", "typecheck", "build"):
            if s in sc: cmds.append(f"{pm} run {s}")
        if "test" in sc and "no test specified" not in sc["test"]: cmds.append(f"{pm} test")
    if has("pyproject.toml") or has("setup.py") or has("pytest.ini") or has("requirements.txt"):
        cmds.append(f"{sys.executable} -m pytest -q")  # exit 5 = no tests collected = not proven
    if has("pom.xml"): cmds.append("mvn -q -B verify" if not has("mvnw") else ("mvnw.cmd -q -B verify" if os.name == "nt" else "./mvnw -q -B verify"))
    if has("build.gradle") or has("build.gradle.kts"): cmds.append(("gradlew.bat" if os.name == "nt" else "./gradlew") + " build" if has("gradlew") else "gradle build")
    if has("go.mod"): cmds.append("go test ./...")
    if has("Cargo.toml"): cmds.append("cargo test")
    if has("Makefile") and not cmds: cmds.append("make test")
    return cmds

def p2_project(root, r, timeout):
    tp = os.path.join(root, ".ai", "TASKS.md")
    if os.path.exists(tp):
        weak = []
        for line in open(tp, encoding="utf-8"):
            c = [x.strip() for x in line.strip().strip("|").split("|")]
            if len(c) == 8 and re.fullmatch(r"T-\d{3,}", c[0]) and (c[6] in ("", "-") or c[7] in ("", "-")): weak.append(c[0])
        r.add("P2", ".ai/TASKS.md: every task has acceptance + verify", not weak, ", ".join(weak[:10]))
    cmds = detect_commands(root)
    if not cmds:
        r.add("P2", "build/test commands detected", False, "none found: add tests or a 'test' script so the work can be proven"); return
    for c in cmds:
        try:
            p = subprocess.run(c, shell=True, cwd=root, capture_output=True, text=True, timeout=timeout, encoding="utf-8", errors="replace")
            tail = (p.stdout + p.stderr).strip().splitlines()[-15:]
            r.add("P2", f"`{c}`", p.returncode == 0, "" if p.returncode == 0 else " | ".join(tail)[:1500])
        except subprocess.TimeoutExpired:
            r.add("P2", f"`{c}`", False, f"timed out after {timeout}s")

def main():
    ap = argparse.ArgumentParser(description="Proof gate (P0-P2).")
    ap.add_argument("--project", help="prove a project folder instead of the hub")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--timeout", type=int, default=900)
    a = ap.parse_args()
    root = os.path.abspath(a.project or HUB); mode = "project" if a.project else "hub"
    fl = list(files(root)); r = Report()
    p0(root, fl, r)
    if r.level_ok("P0"): p1(root, fl, r)
    if r.level_ok("P0") and r.level_ok("P1"):
        p2_hub(root, r) if mode == "hub" else p2_project(root, r, a.timeout)
    reached = "NONE"
    for lvl in ("P0", "P1", "P2"):
        if any(c["level"] == lvl for c in r.checks) and r.level_ok(lvl): reached = lvl
        else: break
    out = {"target": root, "mode": mode, "date": datetime.datetime.now().isoformat(timespec="seconds"),
           "files_scanned": len(fl), "proof_level": reached, "proven_P2": reached == "P2",
           "next": "P3 = check the domain gate in system/03-quality-gates.md with evidence" if reached == "P2" else "fix the first failing check, re-run (max 3 loops)",
           "checks": r.checks}
    try:
        os.makedirs(os.path.join(root, ".proof"), exist_ok=True)
        json.dump(out, open(os.path.join(root, ".proof", "verify.json"), "w", encoding="utf-8"), indent=1)
    except OSError: pass
    if a.json: print(json.dumps(out, indent=1))
    else:
        for c in r.checks:
            print(f"{'PASS' if c['ok'] else 'FAIL'}  {c['level']}  {c['check']}" + (f"\n        {c['detail']}" if c["detail"] and not c["ok"] else ""))
        print(f"\nproof level: {reached}  ({len(fl)} files)  evidence: .proof/verify.json")
        print("next:", out["next"])
    sys.exit(0 if reached == "P2" else 1)

if __name__ == "__main__": main()

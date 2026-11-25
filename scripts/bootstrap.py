"""One command that turns a fresh clone into a working AI workstation (Windows, macOS, Linux, WSL).
Idempotent: safe to re-run; it only installs what is missing. Driven by libraries/install.json.

    python scripts/bootstrap.py              # tools, skills, plugins, video studio, voice model
    python scripts/bootstrap.py --full       # + clone every repo in libraries/registry.json (~800 MB)
    python scripts/bootstrap.py --captions   # + Whisper caption model (~460 MB)
    python scripts/bootstrap.py --check      # report only, change nothing

Flags: --skip-tools --skip-skills --skip-plugins --skip-studio --skip-link --video-root DIR
The link step registers KERNEL.md with every AI (scripts/link.py; backups, reversible with --unlink).
Ends with a checklist and writes .bootstrap.json (agents read it to know setup is done).
"""
import argparse, datetime, json, os, platform, shutil, subprocess, sys

for _s in (sys.stdout, sys.stderr):  # Windows consoles default to cp1252
    try: _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception: pass
HUB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WIN, MAC = os.name == "nt", sys.platform == "darwin"
MAN = json.load(open(os.path.join(HUB, "libraries", "install.json"), encoding="utf-8"))
REG = json.load(open(os.path.join(HUB, "libraries", "registry.json"), encoding="utf-8"))
results = []  # (area, item, status)

def log(area, item, status): results.append((area, item, status)); print(f"  {status:<9} {item}")
def step(t): print(f"\n== {t}")
def exp(p): return os.path.abspath(os.path.expanduser(p))
def which(c): return shutil.which(c)
def sh(cmd, cwd=None, quiet=False):
    try:
        r = subprocess.run(cmd, cwd=cwd, capture_output=quiet, text=True, encoding="utf-8", errors="replace", shell=isinstance(cmd, str))
        return r.returncode == 0
    except FileNotFoundError:
        return False

def refresh_path():
    """Pick up PATH changes made by winget in this same process."""
    if not WIN: return
    import winreg
    parts = []
    for root, key in ((winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment"),
                      (winreg.HKEY_CURRENT_USER, "Environment")):
        try:
            with winreg.OpenKey(root, key) as k: parts.append(os.path.expandvars(winreg.QueryValueEx(k, "Path")[0]))
        except OSError: pass
    links = os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\WinGet\Links")
    os.environ["PATH"] = ";".join(parts + [links, os.environ.get("PATH", "")])

def get_env(name):
    """Env var from this process, else the saved Windows user value (shells opened before setx don't have it)."""
    v = os.environ.get(name)
    if v or not WIN: return v
    import winreg
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as k: return winreg.QueryValueEx(k, name)[0] or None
    except OSError: return None

def set_env(name, value, check):
    os.environ[name] = value
    if check: return
    if WIN: sh(["setx", name, value], quiet=True)
    else:
        line = f'export {name}="{value}"'
        for rc in ("~/.bashrc", "~/.zshrc"):
            p = exp(rc)
            if os.path.exists(p) or rc == "~/.bashrc":
                txt = open(p).read() if os.path.exists(p) else ""
                if f"export {name}=" not in txt:
                    os.makedirs(os.path.dirname(p), exist_ok=True); open(p, "a").write("\n" + line + "\n")

def install_tool(t, check):
    if which(t["cmd"]): return log("tools", t["cmd"], "ok")
    if check: return log("tools", t["cmd"], "missing")
    done = False
    if WIN and t.get("winget") and which("winget"):
        done = sh(["winget", "install", "-e", "--id", t["winget"], "--accept-source-agreements", "--accept-package-agreements", "--silent"])
    elif MAC and t.get("brew") and which("brew"):
        done = sh(["brew", "install", t["brew"]])
    elif t.get("apt") and which("apt-get"):
        done = sh(f"sudo apt-get install -y {t['apt']}")
    if not done and t.get("npm") and which("npm"):
        done = sh([which("npm"), "install", "-g", t["npm"]], quiet=True)
    if not done and t.get("pip"):
        done = sh([sys.executable, "-m", "pip", "install", "--user", "-q", t["pip"]])
    refresh_path()
    log("tools", t["cmd"], "installed" if which(t["cmd"]) else ("optional" if t.get("optional") else "FAILED"))

def clone(repo, dest, check):
    if os.path.exists(dest): return True
    if check: return False
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    env = dict(os.environ, GIT_TERMINAL_PROMPT="0")
    return subprocess.run(["git", "clone", "-q", "--depth", "1", "https://" + repo.removeprefix("https://"), dest], env=env).returncode == 0

def copy_skill(src, name, targets, check):
    if not os.path.exists(os.path.join(src, "SKILL.md")): return "no SKILL.md"
    if check: return "ok" if all(os.path.exists(os.path.join(t, name, "SKILL.md")) for t in targets) else "missing"
    for t in targets:
        os.makedirs(t, exist_ok=True); shutil.copytree(src, os.path.join(t, name), dirs_exist_ok=True,
                                                      ignore=shutil.ignore_patterns(".git", "node_modules"))
    return "ok"

def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    for f in ("full", "captions", "check", "skip-tools", "skip-skills", "skip-plugins", "skip-studio", "skip-link"):
        p.add_argument("--" + f, action="store_true")
    p.add_argument("--video-root"); a = p.parse_args()
    print(f"AI Essentials bootstrap · {platform.system()} {platform.release()} · Python {platform.python_version()}")
    lib = get_env("AI_LIBRARY_ROOT") or os.path.join(HUB, "vendor", "library")
    step("environment"); set_env("AI_HUB_ROOT", HUB, a.check); set_env("AI_LIBRARY_ROOT", lib, a.check)
    repo0 = MAN["repos"][0]
    vroot = exp(a.video_root or get_env(repo0["env"]) or repo0["default_dir"]); set_env(repo0["env"], vroot, a.check)
    for k in ("AI_HUB_ROOT", "AI_LIBRARY_ROOT", "VIDEO_ROOT"): log("env", f"{k}={os.environ[k]}", "ok")

    if not a.skip_tools:
        step("tools"); refresh_path()
        for t in MAN["tools"]: install_tool(t, a.check)

    if not a.skip_studio:
        step("video studio")
        for r in MAN["repos"]:
            d = exp(get_env(r["env"]) or r["default_dir"])
            if not os.path.exists(os.path.join(d, "studio")):
                if os.path.exists(d) and os.listdir(d) and not a.check:
                    log("studio", f"{d} exists without the studio: clone {r['url']} there", "FAILED"); continue
                ok = a.check is False and subprocess.run(["git", "clone", "-q", r["url"], d]).returncode == 0
                log("studio", r["name"], "installed" if ok else "missing")
                if not ok: continue
            else: log("studio", f"{r['name']} at {d}", "ok")
            if a.check: continue
            req = os.path.join(d, r.get("pip_requirements", ""))
            if os.path.isfile(req):
                ok = sh([sys.executable, "-m", "pip", "install", "--user", "-q", "--no-warn-script-location", "-r", req])
                log("studio", "python packages", "ok" if ok else "FAILED")
            for c in r.get("post", []) + (["python studio/get_models.py --captions"] if a.captions else []):
                ok = sh([sys.executable, *c.split()[1:]], cwd=d); log("studio", c, "ok" if ok else "FAILED")
        npx = which("npx")
        for w in MAN.get("npx_warmup", []):
            if a.check or not npx: log("node", "npx " + w, "skipped" if npx else "no npx"); continue
            ok = sh([npx, "-y", *w.split()], quiet=True); log("node", "npx " + w.split()[0], "ok" if ok else "FAILED")

    if a.full:
        step("tool library (all registry repos)")
        for it in REG["items"]:
            up = (it.get("upstream") or "").split(" ")[0]
            if it.get("local_path") and up.startswith("github.com/"):
                ok = clone(up, os.path.join(lib, it["local_path"]), a.check); log("library", it["id"], "ok" if ok else "missing")

    if not a.skip_skills:
        targets = [exp(t) for t in MAN["skills"]["targets"]]
        step("skills -> " + ", ".join(targets))
        own = os.path.join(HUB, "skills")
        for n in sorted(os.listdir(own)):
            if os.path.isdir(os.path.join(own, n)): log("skills", n, copy_skill(os.path.join(own, n), n, targets, a.check))
        for e in MAN["skills"]["external"]:
            d = os.path.join(lib, e["dir"])
            if not clone(e["repo"], d, a.check): log("skills", e["name"], "missing" if a.check else "FAILED"); continue
            log("skills", f"{e['name']}  ({e['license']})", copy_skill(os.path.join(d, e["path"]), e["name"], targets, a.check))

    if not a.skip_plugins:
        step("Claude Code plugins")
        claude = which("claude")
        if not claude: log("plugins", "claude CLI not found (install Claude Code, then re-run)", "skipped")
        else:
            listed = subprocess.run([claude, "plugin", "list"], capture_output=True, text=True, encoding="utf-8", errors="replace").stdout or ""
            for pl in MAN["claude_plugins"]:
                name = pl["plugin"].split("@")[0]
                if name in listed: log("plugins", pl["plugin"], "ok"); continue
                if a.check: log("plugins", pl["plugin"], "missing"); continue
                src = pl["marketplace"]
                if pl.get("local_dir"):  # local marketplaces avoid flaky remote clones
                    local = os.path.join(lib, pl["local_dir"])
                    if clone(pl["repo"], local, False): src = local
                sh([claude, "plugin", "marketplace", "add", src], quiet=True)
                ok = sh([claude, "plugin", "install", pl["plugin"]], quiet=True); log("plugins", pl["plugin"], "installed" if ok else "FAILED")

    if not a.skip_plugins and MAN.get("harness_plugins"):
        step("plugins for other AIs (Gemini, Antigravity, Codex, Kimi, Cursor)")
        for h in MAN["harness_plugins"]:
            cli = which(h["cli"])
            if not cli: log("ai-plugins", f"{h['name']}: {h['cli']} not installed", "skipped"); continue
            if h.get("manual"): log("ai-plugins", f"{h['name']}: {h['manual']}", "manual"); continue
            if h.get("check"):
                out = subprocess.run(h["check"], shell=True, capture_output=True, text=True, encoding="utf-8", errors="replace").stdout or ""
                if h.get("marker", "") in out: log("ai-plugins", h["name"], "ok"); continue
            if a.check: log("ai-plugins", h["name"], "missing"); continue
            ok = sh(h["install"], quiet=True); log("ai-plugins", h["name"], "installed" if ok else "FAILED")

    if not a.skip_link:
        step("link AIs (kernel auto-loads in Claude Code, Gemini CLI/Antigravity, Codex, Windsurf)")
        ok = sh([sys.executable, os.path.join(HUB, "scripts", "link.py")] + (["--check"] if a.check else []))
        log("link", "global rules + Claude agents (scripts/link.py)", "ok" if ok else ("missing" if a.check else "FAILED"))

    bad = [r for r in results if r[2] in ("FAILED", "missing")]
    step("checklist")
    for area in dict.fromkeys(r[0] for r in results):
        items = [r for r in results if r[0] == area]
        print(f"  {area:<8} {sum(r[2] in ('ok', 'installed') for r in items)}/{len(items)} ready"
              + "".join(f"\n           ✗ {r[1]} ({r[2]})" for r in items if r in bad))
    print(f"\n  {MAN['connectors_note']}")
    if not a.check:
        json.dump({"date": datetime.datetime.now().isoformat(timespec="seconds"), "platform": platform.platform(),
                   "ok": not bad, "problems": [f"{r[0]}: {r[1]} ({r[2]})" for r in bad]},
                  open(os.path.join(HUB, ".bootstrap.json"), "w"), indent=2)
        print("\n  Restart your terminal / Claude Code so new PATH entries, skills and plugins load.")
    print("\nREADY" if not bad else f"\n{len(bad)} item(s) need attention (see ✗ above)")
    sys.exit(0 if not bad else 1)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Search the library registry offline. Usage: python scripts/find.py video voice
Prints matching entries with the resolved local path (uses $AI_LIBRARY_ROOT if set)."""
import sys as _sys
for _s in (_sys.stdout, _sys.stderr):  # Windows consoles/pipes default to cp1252
    try: _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception: pass
import json, os, sys
here = os.path.dirname(os.path.abspath(__file__))
reg = json.load(open(os.path.join(here, "..", "libraries", "registry.json"), encoding="utf-8"))
root = os.environ.get(reg["local_root_env"], "")
terms = [t.lower() for t in sys.argv[1:]]
if not terms: sys.exit(__doc__)
hits = [i for i in reg["items"] if all(t in " ".join(i.values()).lower() for t in terms)]
for i in hits:
    loc = os.path.join(root, i["local_path"]) if root else i["local_path"]
    ok = "✓" if root and os.path.exists(loc) else " "
    print(f"{ok} {i['id']:<24} [{i['domain']}] {i['use']}\n    entry: {loc}/{i['entry']}\n    upstream: {i['upstream']}  ({i['license']})")
print(f"{len(hits)} match(es)")

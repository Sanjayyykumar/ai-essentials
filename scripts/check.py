#!/usr/bin/env python3
"""Repo self-check: every relative link in *.md resolves; registry.json parses."""
import os, re, json, sys
root = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."); bad = 0
json.load(open(os.path.join(root, "libraries", "registry.json")))
for dp, _, fs in os.walk(root):
    if ".git" in dp: continue
    for f in fs:
        if not f.endswith(".md"): continue
        p = os.path.join(dp, f)
        for m in re.finditer(r"`((?:system|playbooks|recon|libraries|scripts|templates)/[\w./-]+\.(?:md|py|json))`", open(p, encoding="utf-8").read()):
            if not os.path.exists(os.path.join(root, m.group(1))): print(f"{p}: missing {m.group(1)}"); bad += 1
print("OK" if not bad else f"{bad} broken"); sys.exit(1 if bad else 0)

# Live status protocol
Keep one `STATUS.md` in the user's working folder (template: `templates/STATUS.md`).
Update at: phase change, each completed step, each blocker, delivery. One edit, not a rewrite.

Format (machine + human readable):
```
phase: BUILD          # INTAKE|RECON|PLAN|BUILD|VERIFY|DELIVERED|BLOCKED
step: 3/7             # current/total
updated: 2026-11-12T10:42
now: rendering scene 3
done: [scaffold, assets, scenes 1-2]
next: scene 4 transitions
blockers: none
assumptions: 1080p30, Indian-female voice (hf_alpha)
outputs: [output/film_v1.mp4]
```
CLI: `python scripts/status.py set BUILD "rendering scene 3" --step 3/7` · `python scripts/status.py show`.
In chat: one short line per phase change ("BUILD 3/7 — rendering scene 3"). No narration beyond that.

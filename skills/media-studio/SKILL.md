---
name: "media-studio"
description: "Use first for any image, audio or video creation job: routes the requirement to the right engine and enforces the brief→build→mix→QC contract."
---

# Media Studio

The system is `studio/SYSTEM.md` in ai-essentials (`$AI_HUB_ROOT/studio/SYSTEM.md`). Videos are built with [video-generations](https://github.com/Sanjayyykumar/video-generations) at `$VIDEO_ROOT`.

1. Read `studio/SYSTEM.md` (one file): routing tables, job-folder contract, mix settings, QC checklist and licences.
2. Write `brief.json`, pick ONE route from the tables, then open only that engine's SKILL.md (tool-library skill).
3. Quick path for narrated explainers and shorts: `python $VIDEO_ROOT/studio/new_project.py "<topic>"`, fill `scenes.json`, `python $VIDEO_ROOT/studio/make.py <project>`.
4. Custom builds go in `$VIDEO_ROOT/projects/<YYYY-MM-DD>_<slug>/` in this order: script → voiceover → shots timed to VO → stills check → render → mix → QC.
5. Prefer code-rendered engines. Use cloud AI only for what code can't make, and confirm before spending credits on long or batch jobs.
6. Pair with: pixabay-audio (SFX/music), presenter-voiceover (narration), hyperframes-video (HTML motion).
7. Finish with LOG.md: engine used, render time, what to change next time. If a route was missing or wrong, update SYSTEM.md's tables.

---
name: "reference-style"
description: "Use when the user shares reference videos/reels (links or files) and wants their editing style studied, a brand/style sheet made, or their own raw clips edited in that style (jump cuts, zooms, captions, grade, music)."
---

# Reference style → style sheet → edit

Tools: [video-generations](https://github.com/Sanjayyykumar/video-generations) at `$VIDEO_ROOT` (`studio/reference.py`, `studio/reel.py`). Needs ffmpeg, yt-dlp, faster-whisper (`python studio/doctor.py`).

## 1. Save the references (no tokens)
`python $VIDEO_ROOT/studio/reference.py $VIDEO_ROOT/projects/<date>_<slug>/references <link1> <link2> <link3>`
Downloads each one (yt-dlp) and measures them in code: cuts and shot length, cuts in the first 3 s, silence left in, words per second, loudness, brightness, contrast, saturation, warmth and palette. Writes `analysis.json`, `style.draft.json`, `STYLE.md`, plus `refNN_hook.jpg` (first 3 s) and `refNN_shots.jpg` (one frame per shot).
Only download videos the user has the right to use as a reference, and keep them private (they stay in `projects/`, which is git-ignored).

## 2. Look, don't guess (cheap tokens)
Open **only the contact sheets** (2 images per reference), not the videos. From them, fill the "Observed" section of `STYLE.md`:
jump-cut tightness, zoom/punch-in timing and strength, captions (font, size, colour, position, words per line, animation, emphasised words), motion graphics/emojis/pop-ups/B-roll, colour grade, music/SFX, and the hook.
For detail, `npx hyperframes measure <video>` reports cuts, motion, crops and the look.

## 3. Brand sheet for approval
Write "Our version": keep what makes the style work, change what would make it a copy (own palette, font, caption colours, intro). Adjust `style.draft.json` to match. Ask about anything unclear, then **stop and get approval** before editing.

## 4. Apply
After approval rename to `style.json`, then for each raw clip:
`python $VIDEO_ROOT/studio/reel.py raw.mp4 out.mp4 --style style.json --music bed.mp3`
→ silence-trimmed jump cuts, punch-in every Nth cut, crop to format, grade, word-highlight captions (active word + emphasised words), music ducked under the voice, loudness normalised.
Motion graphics, B-roll and pop-ups beyond that: build them as an overlay with HyperFrames or Remotion (transparent WebM), then overlay with ffmpeg.

## 5. QC
Check 3 frames (hook, middle, end) and the first 3 s; confirm captions are inside the safe area, nothing important is cropped, and loudness is about −14 LUFS. Log what to change in `LOG.md`.

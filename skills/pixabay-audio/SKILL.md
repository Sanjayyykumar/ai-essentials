---
name: "pixabay-audio"
description: "Use when a video or audio build needs sound effects or music: find, download and log royalty-free Pixabay audio and mix it in."
---

# Pixabay sound effects & music

Source: https://pixabay.com/sound-effects/ (SFX) and https://pixabay.com/music/ (music).

## License (check before using)
- Pixabay Content License: free for commercial and non-commercial use, may be modified, attribution not required.
- Not allowed: reselling or redistributing the files as standalone audio (sound packs, stock sites, music files); implying endorsement.
- Some tracks may contain samples or vocals that carry other rights. For a commercial or client video, prefer clear SFX and instrumental music, and keep the track page URL as a record.

## How to reach it
- The cloud workspace shell CANNOT reach pixabay.com (the proxy blocks it). Do not retry with curl/wget/Python.
- Scripted downloads from the PC shell are blocked as bot-check circumvention. Do not script around Pixabay's site.
- Route: a real browser session (e.g. Claude in Chrome). Load the chrome-browser skill first.
  1. Search: `https://pixabay.com/sound-effects/search/<term>/` (spaces as %20). Music: `https://pixabay.com/music/search/<term>/`. Editor's Choice: add `?order=ec`.
  2. Pick by title, duration and tags. Prefer short, clean, Editor's Choice items.
  3. Open the track page and click **Free Download**. The file lands in the Chrome Downloads folder. If Pixabay asks for a login or captcha, stop and ask the user to do that step.
  4. Move the file into the video project's folder under `$VIDEO_ROOT/projects/<project>/audio/sfx/` (or `audio/music/`), renamed `<role>_<short-desc>.mp3` (e.g. `whoosh_transition-01.mp3`).
- If no browser is available, ask the user to download the listed track URLs himself.

## Log every file
Keep `audio\SOURCES.md` in the project folder with one row per file: file name, Pixabay page URL, author, type (SFX/music), date downloaded. This is the license record.

## Useful search terms
- Transitions: whoosh, swoosh, swipe, riser, impact, boom, glitch
- UI / tech: click, pop, notification, typing, digital beep, interface
- Text / reveals: ding, sparkle, shimmer, stamp, paper
- Mood beds (music): corporate upbeat, lofi, cinematic ambient, inspiring piano, Indian flute

## Mixing (ffmpeg, with the presenter-voiceover skill; video-generations `studio/mix.py` does this automatically)
- Convert to WAV 48 kHz first: `ffmpeg -i in.mp3 -ar 48000 -ac 2 sfx.wav`.
- Trim silence: `-af silenceremove=start_periods=1:start_threshold=-50dB`.
- Place an SFX at a shot cut: `adelay=<ms>|<ms>`, then `amix=normalize=0`.
- Levels: voice about -16 LUFS, music bed 18-22 dB under the voice (sidechaincompress or volume=0.12), SFX peaks below the voice. Fade the music in and out (`afade`).
- Don't stack SFX on every cut. Use one per real event (reveal, transition, impact).
- Final loudness: `loudnorm=I=-14:TP=-1.5` for Reels/Shorts.

## Before delivering
- Listen check isn't possible. Check each file with `ffprobe` (duration, channels) and look at the waveform/peak levels (`astats`) so nothing clips.
- Confirm SOURCES.md lists every file used.
---
name: "presenter-voiceover"
description: "Use when writing or generating a voiceover/narration for any video, demo or presentation: presenter-style script rules, pause markup, offline Kokoro voice, polish and fit-to-video mixing."
---

# Presenter voiceover

Tools: `$VIDEO_ROOT/voice/` from [video-generations](https://github.com/Sanjayyykumar/video-generations) (`speak.py`, `speak_cast.py`, `polish_vo.py`, `mix_narration.py`, `el_cache.py`); models in `$VIDEO_ROOT/models` (`python studio/get_models.py`).

## 1. Write like a presenter (the script matters more than the voice)
- **Never read the screen.** On-screen text states the fact; the voice adds meaning, emotion or the story behind it. If a line repeats the screen word for word, rewrite or cut it. Exceptions: product names and the final tagline.
- **One idea per line.** Short sentences, 6–12 words. Spoken English, contractions allowed.
- **Hero thread.** Follow one person (e.g. Aroon, Anita, Dr Rao) and call back to them; people remember stories, not features.
- **End-focus.** Put the key word last in its phrase ("…every team holds *just one*."); the voice naturally lands there. Front-load context: "At … two fourteen, early morning, // Aroon // collapses."
- **Rule of three** for benefits and lists, with even beats.
- **Contrast and turn:** problem → "Now, imagine…" → solution.
- **Openings:** start each section with an anchor ("First, for families.", "Now, step inside the hospital.").
- **Endings:** statements end on a full stop for a falling, finished tone. Close with the promise or tagline, a clear invitation, then "Thank you."
- **Pace (house style):** slow, pause-heavy delivery sounds robotic ("too many pauses, too few words"). Default to fluent presenter pace:
  - speed **1.00** for most lines, **1.02** for long lists/explanations, **0.95–0.97** for taglines and closings, **0.93** only for the single emotional hook.
  - At most one `...` held beat per line, and only at the emotional turn ("At two fourteen, early morning ... Aroon collapses", "What if ... it took just one tap?"). Use `/` sparingly; prefer plain commas.
  - Measured rate at this style: about **2.6–2.8 spoken words per second** (af_kore). Budget = words / 2.7 + 0.35 s polish tail; a line must fit before the next visual beat.
  - Leave a deliberate silence (1–1.5 s, no line) after the problem build-up and after the solution's emotional payoff ("Calmer than that first night.").
  - Density: about 230–250 narrated words for a 2.5-minute film; every scene gets at least one line, so no scene runs silent longer than ~3 s except the planned silences.
- **Honesty:** no invented results; fictional names and figures are demo data.

- **Fast path (to save time):** write all lines → estimate durations with the budget above → fix overruns in the text before generating → generate once. Regenerating on the laptop costs about 25–40 s per line, so most of the time goes to text that gets rewritten.

## 2. Markup (narration file)
`LINES = [(start_s, speed, text), ...]`, `VOICE = '...'`, plus a docstring with delivery notes. Example: `voice/examples/narration_demo.py`.
- `/` = breath pause (0.25 s), `//` = dramatic pause (0.55 s), `...` = held beat (0.8 s).
- Respell names the engine gets wrong in `voice/lexicon.py` (e.g. Arun → "Aroon", Dr → "Doctor") and test one line first.
- Dialogue with several voices: `LINES = [(key, voice, speed, text), ...]` for `speak_cast.py` (`voice/examples/dialogue_demo.py`).

## 3. Voice
- Engine: Kokoro via kokoro-onnx, offline, 50+ voices. Good presenter picks: **af_kore** / **af_heart** (calm, confident female), hm_omega / hm_psi (Indian male), am_onyx (deep male), bm_george (British male), hf_alpha / hf_beta (Indian female). Blends work: `hm_omega:0.6,am_onyx:0.4`.
- For a new voice choice, render 3 representative lines (hook, solution, tagline) per candidate and let the user pick before the full run.
- Word-level stress can't be forced; create it with phrasing, punctuation, pauses and speed. Exact emphasis needs a human recording.
- Premium cloud voice: `voice/el_cache.py` (ElevenLabs; each line billed once, then cached).

## 4. Generate → polish → mix
1. `python voice/speak.py <narration>.py work/vo [voice]` — resumable; each phrase is spoken separately and joined with the marked silences.
2. `python voice/polish_vo.py work/vo work/vo_polished` — trim, warm/clear EQ, gentle compression, subtle room, fade-out tail.
3. `python voice/mix_narration.py <silent.mp4> <music.wav> <narration>.py work/vo_polished <out.mp4>` — places lines, speeds a long line up by at most 1.08×, shifts later lines only as needed, ducks music, −16 LUFS, writes `.srt`.
4. **Check the drift report.** Every line should be within ~0.5 s of its visual. If drift builds up, shorten or cut a line (prefer lines that repeat the screen) and move start times to their visual beats; re-mix without regenerating untouched lines.
   To redo some lines, move their old clips aside and re-run `speak.py`; it fills only missing clips. Keep clip numbering in sync with LINES.
5. Deliver the MP4 and SRT.

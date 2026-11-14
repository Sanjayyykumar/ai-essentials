# Audio playbook
| Need | Tool |
|---|---|
| Offline TTS | Kokoro ONNX (int8), VoiceStudio |
| Online TTS | edge-tts (en-IN-NeerjaNeural etc.) |
| ASR / transcription | Whisper (transformers / faster-whisper) |
| Pick or judge music/SFX you can't hear | earshot |
| Audio LLM (big GPU) | Kimi-Audio-7B |
Voice style: presenter pace ~150 wpm, pauses at commas/scene cuts. Loudness: voice −16 LUFS, final mix −14 LUFS (`ffmpeg -af loudnorm`).

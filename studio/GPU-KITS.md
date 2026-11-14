# GPU kits — engines that switch on when the machine has an NVIDIA GPU

Scripts: `studio/engines/`. Every script reports the device it found and either uses the GPU,
falls back to CPU (TTS only), or exits with a pointer to the cloud route (image/video).

## Check a machine
`nvidia-smi` (PowerShell). No output = no NVIDIA GPU → stay on CPU engines + cloud routes.
Integrated AMD/Intel graphics have no CUDA → GPU kits won't run; TTS still runs on CPU.

## Set up on a GPU laptop (Windows)
1. Clone this repo on that machine.
2. `powershell -ExecutionPolicy Bypass -File studio\engines\setup_gpu.ps1` → creates `C:\media-engines\.venv` with CUDA torch + engines.
3. First run downloads the model from Hugging Face automatically (needs normal internet; weights cached in `%USERPROFILE%\.cache\huggingface`).
If the machine has App Control blocking Python, the venv won't run: use WSL2 (`wsl --install`) and `pip install` inside it.

## Engines
| Script | Model (license) | Makes | VRAM | Notes |
|---|---|---|---|---|
| `image_flux.py` | FLUX.1-schnell (Apache-2.0) | Images, posters, thumbnails, B-roll stills | 16 GB fast · 8–12 GB with offload | 4 steps, ~33 GB first download |
| `video_wan.py` | Wan2.2-TI2V-5B (Apache-2.0) | 5 s text→video or image→video, 720p, 24 fps | 24 GB · 12–16 GB with offload (slow) | Use a FLUX still as `--image` for control |
| `tts_parler.py` | ai4bharat/indic-parler-tts (Apache-2.0) | Hindi, Kannada, Tamil, Bengali... + English narration | 4 GB GPU, or CPU | Installs to `~/media-models` |
| Chatterbox (`pip chatterbox-tts`) | MIT | Clone a voice from a 10 s sample | 4–6 GB, or CPU slow | Consent only |

Other GPU models to consider later (check license first): LTX-Video (fast video; open-weights license with revenue limits),
HunyuanVideo (heavy, 40 GB+), MusicGen (CC-BY-NC, non-commercial), ACE-Step music (Apache-2.0, in digitalsamba toolkit).

## Routing rule (Media Studio)
1. Can code draw it? → code engine (any machine).
2. Needs a real voice? → Kokoro (fast) or Parler (Indian languages) — CPU OK.
3. Needs photoreal image/footage? → GPU kit if `nvidia-smi` shows ≥ 8 GB (image) / ≥ 12 GB (video); otherwise cloud (ElevenLabs/Canva/RunPod, confirm credits).
4. Record model + license in the job's `SOURCES.md`.

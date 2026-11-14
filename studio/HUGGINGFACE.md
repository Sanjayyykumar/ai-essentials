# Hugging Face — how Media Studio uses it

## Access notes for a locked-down Windows PC (example)
- Cloud workspace shell and the device Linux shell: huggingface.co is **blocked**.
- Native Windows **PowerShell can download** from huggingface.co (Invoke-WebRequest).
- Native Windows Python / venvs are **blocked by App Control** (os error 4551). Don't try to run models in Windows Python.
- So the pattern is: **download with PowerShell → run in the device Linux shell** (pip from PyPI works there).
- Store models in `$VIDEO_ROOT/models/<model-name>/`.

Download a model's files (PowerShell, Desktop Commander start_process):
```powershell
$D="$env:VIDEO_ROOT\models\<name>"; New-Item -ItemType Directory -Force $D | Out-Null
foreach($f in '<file1>','<file2>'){ Invoke-WebRequest "https://huggingface.co/<org>/<repo>/resolve/main/$f" -OutFile "$D\$f" -UseBasicParsing }
```
List a repo's files first: `(Invoke-RestMethod https://huggingface.co/api/models/<org>/<repo>).siblings.rfilename`
Check license: `(Invoke-RestMethod https://huggingface.co/api/models/<org>/<repo>).cardData.license`

## Installed / adopted
| Model | Use | Status |
|---|---|---|
| Kokoro-82M (ONNX int8) | Narration, offline. Indian voices hf_alpha, hf_beta (F), hm_omega, hm_psi (M); en voices af_heart, bf_emma, am_michael | in `models/`, used by video-generations |
| Systran/faster-whisper-small | Transcription + word timestamps → word-by-word subtitles, QC of VO vs script | in `models/faster-whisper-small`; run with `pip install faster-whisper` in device shell |

## Worth adding next (fits a CPU-only PC)
| Model (HF repo) | Use | Note |
|---|---|---|
| ResembleAI/chatterbox | Clone your own voice | MIT; CPU slow, short lines only |
| ai4bharat/indic-parler-tts | Natural Hindi, Kannada, Tamil + 18 Indian languages, voice described in words | Apache-2.0; ~3.5 GB, slow on CPU |
| Systran/faster-whisper-medium | Better Hindi/Hinglish subtitles | larger, slower |
| facebook/musicgen-small | Short music stingers | CC-BY-NC: non-commercial only |
| briaai/RMBG-1.4 (ONNX) | Background removal for product shots / thumbnails | non-commercial license; check before client work |

## Not local (needs a GPU) — use cloud
- Image: FLUX, SDXL. Video: Wan 2.2, LTX-2, HunyuanVideo. Use ElevenLabs / Canva connectors or RunPod (credits; confirm first).
- HF Spaces (free GPU demos) can't be called from this setup (HF blocked in the Linux shell, Python blocked on Windows). Open a Space in Chrome manually only for one-off trials, and check the model license before using the output.

## Rules
- Check every model's license before commercial/client use. Record model + license in the job's `SOURCES.md`.
- Voice cloning only with consent (your own voice, or someone who agreed).

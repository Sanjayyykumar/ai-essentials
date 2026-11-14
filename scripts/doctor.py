"""Health check for any machine: tools, Python packages, models, GPU, hub paths.  python scripts/doctor.py"""
import importlib, os, shutil, subprocess
ok = lambda b: "OK " if b else "-- "
hub = os.environ.get("AI_HUB_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
vr = os.environ.get("VIDEO_ROOT", "")
print("AI_HUB_ROOT =", hub); print("VIDEO_ROOT  =", vr or "(not set: run scripts/setup)")
print("\n[tools]")
for t in ("git", "node", "npx", "python3", "python", "ffmpeg", "ffprobe", "uv", "nvidia-smi"):
    print(ok(shutil.which(t)), t)
print("\n[python packages]")
for m in ("numpy", "PIL", "soundfile", "kokoro_onnx", "faster_whisper", "torch", "diffusers", "parler_tts"):
    try: importlib.import_module(m); print("OK ", m)
    except Exception: print("-- ", m)
print("\n[GPU]")
try:
    print(subprocess.run(["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader"], capture_output=True, text=True).stdout.strip() or "none")
except Exception: print("no NVIDIA GPU: GPU kits (FLUX, Wan) off; CPU engines + cloud routes on")
if vr:
    print("\n[models]")
    for f in ("models/kokoro-v1.0.int8.onnx", "models/voices-v1.0.bin", "models/faster-whisper-small/model.bin"):
        print(ok(os.path.exists(os.path.join(vr, f))), f)
print("\n[hub]")
for f in ("AI.md", "studio/SYSTEM.md", "libraries/registry.json", "vendor/library", "skills"):
    print(ok(os.path.exists(os.path.join(hub, f))), f)

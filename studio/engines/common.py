"""Shared helpers: pick the best device on whatever machine runs this."""
import os, torch

def device():
    if torch.cuda.is_available():
        return "cuda"
    if getattr(torch.backends, "mps", None) and torch.backends.mps.is_available():
        return "mps"
    return "cpu"

def vram_gb():
    return torch.cuda.get_device_properties(0).total_memory / 1e9 if torch.cuda.is_available() else 0.0

def dtype():
    d = device()
    if d == "cuda":
        return torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16
    return torch.float32

def report():
    d = device()
    print(f"[studio] device={d} vram={vram_gb():.1f}GB torch={torch.__version__}")
    return d

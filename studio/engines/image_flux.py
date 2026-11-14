"""GPU image generation: FLUX.1-schnell (Apache-2.0, commercial OK), 4 steps.
Needs NVIDIA GPU; >=12 GB VRAM comfortable, 8 GB works with --low-vram (slower). Refuses to run on CPU.
python image_flux.py --prompt "..." --out img.png --w 1080 --h 1920
"""
import argparse, sys, torch
from diffusers import FluxPipeline
from common import report, vram_gb

p = argparse.ArgumentParser()
p.add_argument("--prompt", required=True); p.add_argument("--out", required=True)
p.add_argument("--w", type=int, default=1024); p.add_argument("--h", type=int, default=1024)
p.add_argument("--steps", type=int, default=4); p.add_argument("--seed", type=int, default=0)
p.add_argument("--model", default="black-forest-labs/FLUX.1-schnell"); p.add_argument("--low-vram", action="store_true")
a = p.parse_args()
if report() != "cuda": sys.exit("[studio] No NVIDIA GPU: use the cloud image route (ElevenLabs/Canva) instead.")
pipe = FluxPipeline.from_pretrained(a.model, torch_dtype=torch.bfloat16)
if a.low_vram or vram_gb() < 16: pipe.enable_sequential_cpu_offload() if vram_gb() < 10 else pipe.enable_model_cpu_offload()
else: pipe.to("cuda")
w, h = a.w // 16 * 16, a.h // 16 * 16
img = pipe(a.prompt, width=w, height=h, guidance_scale=0.0, num_inference_steps=a.steps,
           max_sequence_length=256, generator=torch.Generator("cpu").manual_seed(a.seed)).images[0]
img.save(a.out); print("[studio] wrote", a.out)

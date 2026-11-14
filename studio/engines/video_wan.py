"""GPU video generation: Wan2.2-TI2V-5B (Apache-2.0). Text-to-video, or image-to-video with --image.
Needs NVIDIA GPU, ~24 GB VRAM ideal; 12-16 GB works with CPU offload (slow). Refuses to run on CPU.
python video_wan.py --prompt "..." --out clip.mp4 [--image first_frame.png] [--frames 121] [--portrait]
"""
import argparse, sys, torch
from diffusers import AutoencoderKLWan, WanPipeline
from diffusers.utils import export_to_video, load_image
from common import report, vram_gb

p = argparse.ArgumentParser()
p.add_argument("--prompt", required=True); p.add_argument("--out", required=True); p.add_argument("--image")
p.add_argument("--frames", type=int, default=121); p.add_argument("--steps", type=int, default=50)
p.add_argument("--portrait", action="store_true"); p.add_argument("--seed", type=int, default=0)
p.add_argument("--model", default="Wan-AI/Wan2.2-TI2V-5B-Diffusers")
a = p.parse_args()
if report() != "cuda": sys.exit("[studio] No NVIDIA GPU: use code engines or the cloud video route instead.")
vae = AutoencoderKLWan.from_pretrained(a.model, subfolder="vae", torch_dtype=torch.float32)
pipe = WanPipeline.from_pretrained(a.model, vae=vae, torch_dtype=torch.bfloat16)
if vram_gb() < 24: pipe.enable_model_cpu_offload()
else: pipe.to("cuda")
w, h = (704, 1280) if a.portrait else (1280, 704)
kw = dict(prompt=a.prompt, negative_prompt="blurry, low quality, distorted, watermark, text artifacts",
          width=w, height=h, num_frames=a.frames, guidance_scale=5.0, num_inference_steps=a.steps,
          generator=torch.Generator("cpu").manual_seed(a.seed))
if a.image: kw["image"] = load_image(a.image)
frames = pipe(**kw).frames[0]
export_to_video(frames, a.out, fps=24); print("[studio] wrote", a.out)

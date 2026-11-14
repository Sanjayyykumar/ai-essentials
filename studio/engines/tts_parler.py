"""Indic Parler-TTS: Hindi/Kannada/Tamil/... + English, voice described in words.
GPU if present, else CPU (slow: ~1-3 min per line on this laptop).

python tts_parler.py --text "नमस्ते, आज हम..." --desc "Divya speaks in a clear, warm, confident voice at a moderate pace, very clear audio." --out line01.wav
  --model  local folder or HF id (default: local media-models copy)
  --desc-tokenizer local flan-t5-large folder or HF id
Named speakers in the model card (e.g. Hindi: Rohit, Divya; Kannada: Suresh, Anu; English: Thoma, Mary) make the voice consistent across lines.
"""
import argparse, os, soundfile as sf, torch
from transformers import AutoTokenizer
from parler_tts import ParlerTTSForConditionalGeneration
from common import report, dtype

HOME = os.path.expanduser("~")
DEF_MODEL = os.environ.get("PARLER_MODEL", os.path.join(HOME, "mnt", "media-models", "indic-parler-tts"))
DEF_TOK = os.environ.get("PARLER_DESC_TOK", os.path.join(HOME, "mnt", "media-models", "flan-t5-large"))

p = argparse.ArgumentParser()
p.add_argument("--text", required=True); p.add_argument("--desc", required=True); p.add_argument("--out", required=True)
p.add_argument("--model", default=DEF_MODEL); p.add_argument("--desc-tokenizer", default=DEF_TOK); p.add_argument("--seed", type=int, default=7)
a = p.parse_args()

dev = report(); torch.manual_seed(a.seed)
model = ParlerTTSForConditionalGeneration.from_pretrained(a.model, torch_dtype=dtype()).to(dev)
tok = AutoTokenizer.from_pretrained(a.model)
dtok = AutoTokenizer.from_pretrained(a.desc_tokenizer)
d = dtok(a.desc, return_tensors="pt").to(dev); t = tok(a.text, return_tensors="pt").to(dev)
with torch.inference_mode():
    gen = model.generate(input_ids=d.input_ids, attention_mask=d.attention_mask,
                         prompt_input_ids=t.input_ids, prompt_attention_mask=t.attention_mask)
sf.write(a.out, gen.to(torch.float32).cpu().numpy().squeeze(), model.config.sampling_rate)
print("[studio] wrote", a.out)

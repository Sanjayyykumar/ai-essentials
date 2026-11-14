# Image playbook
1. **Brief → prompt** using `libraries/offline/image-prompts.md` formula: subject · action · setting · style · lighting · lens/composition · palette · aspect · negatives.
2. **Tool:** whatever the host AI offers (native image gen, Canva, SD/Flux locally). Without image gen → produce SVG (`svg.md`) or code-rendered art (Pillow/canvas).
3. **Generate 3–4 variants**, pick by brief fit, then iterate on one (change ≤2 variables per round).
4. **Post:** upscale/crop to target, remove background if needed, export PNG (UI) / WebP (web) / JPG (photo).
5. **Verify:** Image gate. Text in images: check spelling letter by letter.
Never imitate a living artist's signature style by name, real people, or brand characters.


## Studio image
Code first (HTML/CSS → PNG, canvas). Photoreal: `studio/engines/image_flux.py` on NVIDIA GPU (`studio/GPU-KITS.md`), else cloud (ElevenLabs/Canva).

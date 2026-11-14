# SVG create & edit playbook
- **Create:** set `viewBox`, no fixed width/height, group with `<g id>`, reuse with `<defs>/<use>`, `currentColor` for themeable icons.
- **Edit:** parse, don't regex — Python `xml.etree` / `lxml`, or `svgpathtools` for paths. Keep IDs stable.
- **Optimize:** `npx svgo in.svg -o out.svg` (keep viewBox). Round coords to 1–2 decimals.
- **Convert:** SVG→PNG `rsvg-convert -w 1024` or `npx @resvg/resvg-js-cli`; PNG→SVG trace `potrace`/`vtracer`.
- **Animate:** CSS on SVG, SMIL (simple), GSAP for timelines.
- **Verify:** SVG gate. Full reference: `libraries/offline/svg.md`.

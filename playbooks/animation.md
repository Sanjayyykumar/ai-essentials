# Animation playbook
| Target | Tech |
|---|---|
| Web UI micro-interactions | CSS transitions/keyframes, View Transitions API, scroll-driven animations |
| Timeline/sequenced web motion | GSAP (`libraries/offline/motion.md`) |
| App/vector loop | Lottie (e2e lottie-animation skill) |
| Character/illustration | rossark-motion skill |
| Clone a site's motion | reanimate (recon the source first) |
| GPU effects | shaders (WebGPU) |
| Video output | render via HyperFrames/video playbook |
Principles: ease-out for enter, ease-in for exit, 150–300 ms UI, 400–800 ms hero; animate transform/opacity only; stagger 40–80 ms; always ship `prefers-reduced-motion`.

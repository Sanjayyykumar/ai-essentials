# Motion reference (CSS + GSAP)
Durations: micro 120–200ms · UI 200–300ms · hero 500–900ms · video title 0.8–1.5s
Easings: enter `cubic-bezier(.16,1,.3,1)` · exit `cubic-bezier(.7,0,.84,0)` · standard `cubic-bezier(.4,0,.2,1)` · GSAP `power3.out`, `expo.inOut`, `back.out(1.7)`
GSAP: `gsap.timeline({defaults:{ease:"power3.out",duration:.6}}).from(".t",{y:40,opacity:0,stagger:.06}).to(".logo",{scale:1},"<0.2")`
ScrollTrigger: `{scrollTrigger:{trigger:el,start:"top 80%",scrub:true}}`
CSS scroll-driven: `animation-timeline: view(); animation-range: entry 0% cover 40%;`
View Transitions: `document.startViewTransition(()=>update())`
Reduced motion: `@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}`
Performance: transform/opacity only; `will-change` sparingly; requestAnimationFrame for JS.
Lottie: export from AE/Bodymovin or generate JSON; play with lottie-web / dotLottie.

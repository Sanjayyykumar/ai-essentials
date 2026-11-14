# SVG reference
Skeleton: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" role="img" aria-label="..."><title>..</title><defs/>...</svg>`
Paths: M x y · L · H · V · C x1 y1 x2 y2 x y · Q · A rx ry rot large sweep x y · Z (lowercase = relative)
Shapes: rect(rx) circle ellipse line polyline polygon · text(text-anchor, dominant-baseline)
Paint: fill/stroke/stroke-width/stroke-linecap=round/linejoin; gradients linear/radial in defs; `currentColor`
Masks/clip: `<clipPath>`, `<mask>` (white=show)
Filters: feGaussianBlur, feDropShadow, feColorMatrix, feTurbulence (noise)
Stroke draw anim: `path{stroke-dasharray:L;stroke-dashoffset:L;animation:d 1.5s ease forwards}@keyframes d{to{stroke-dashoffset:0}}` (L = path.getTotalLength())
Tools: svgo (optimize) · rsvg-convert/resvg (raster) · potrace/vtracer (trace) · xmllint --noout (validate) · Python lxml/svgpathtools (edit)
Icon rules: 24 grid, 2px stroke, 2px padding, round caps.

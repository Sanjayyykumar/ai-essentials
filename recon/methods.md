# Recon methods — copy-paste recipes
## Web fingerprint
```
curl -sI https://site | grep -iE 'server|x-powered|via|cf-|x-vercel|x-nextjs'
curl -s https://site | grep -oiE '(_next|__nuxt|wp-content|shopify|gatsby|astro|webflow|framer)[^"]{0,40}' | sort -u
curl -s https://site/robots.txt; curl -s https://site/sitemap.xml | head
```
## Network/API map (playwright)
`npx playwright open --save-har=site.har https://site` → `jq '.log.entries[].request.url' site.har | grep -i api`
## Design tokens from a page
In browser console: collect `getComputedStyle` color/font-family/font-size of h1,h2,p,button,a → dedupe → palette + type scale.
## Unknown repo in 5 commands
`tree -L 2 -I node_modules` · `cat package.json|pyproject.toml` · `rg -n "main|createApp|app.listen|@SpringBootApplication"` · `git log --oneline -15` · `rg -n "TODO|FIXME" | head`
## Binary / Electron
`file x; strings -n 8 x | rg -i "http|api|key|version"`; Electron: `npx asar extract app.asar out/`.
## Media
`ffprobe -v error -show_format -show_streams in.mp4` · `exiftool in.jpg` · `ffmpeg -i in.mp4 -vf fps=1 f_%03d.png`

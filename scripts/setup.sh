#!/usr/bin/env bash
# AI Essentials — setup on Linux / macOS / WSL.  bash scripts/setup.sh [--fetch-missing] [--engines]
set -u
HUB="$(cd "$(dirname "$0")/.." && pwd)"; LIB="$HUB/vendor/library"; VIDEO_ROOT="${VIDEO_ROOT:-$HOME/video-generations}"
for a in "$@"; do case $a in --fetch-missing) FETCH=1;; --engines) ENG=1;; esac; done
grep -q AI_HUB_ROOT ~/.bashrc 2>/dev/null || printf 'export AI_HUB_ROOT="%s"\nexport AI_LIBRARY_ROOT="%s"\nexport VIDEO_ROOT="%s"\n' "$HUB" "$LIB" "$VIDEO_ROOT" >> ~/.bashrc
export AI_HUB_ROOT="$HUB" AI_LIBRARY_ROOT="$LIB" VIDEO_ROOT
echo "== tools"; for t in git node python3 ffmpeg; do command -v $t >/dev/null && echo "ok  $t" || echo "MISSING $t (apt/brew install $t)"; done
echo "== skills"; mkdir -p ~/.claude/skills && cp -r "$HUB"/skills/*/ ~/.claude/skills/ && ls ~/.claude/skills
if [ "${FETCH:-}" = 1 ]; then echo "== fetch missing repos"
  python3 - "$HUB" <<'P'
import json,os,subprocess,sys
hub=sys.argv[1]; lib=os.path.join(hub,'vendor','library'); r=json.load(open(os.path.join(hub,'libraries','registry.json')))
for it in r['items']:
    lp=it.get('local_path'); up=(it.get('upstream') or '').split(' ')[0]
    if lp and not os.path.exists(os.path.join(lib,lp)) and up.startswith('github.com/'):
        os.makedirs(os.path.dirname(os.path.join(lib,lp)),exist_ok=True); subprocess.run(['git','clone','--depth','1','https://'+up,os.path.join(lib,lp)])
P
fi
echo "== video studio -> $VIDEO_ROOT"
if [ ! -f "$VIDEO_ROOT/studio/make.py" ]; then git clone https://github.com/Sanjayyykumar/video-generations "$VIDEO_ROOT" || echo "clone https://github.com/Sanjayyykumar/video-generations into $VIDEO_ROOT yourself"; fi
mkdir -p "$VIDEO_ROOT/models"; cd "$VIDEO_ROOT/models"
[ -f kokoro-v1.0.int8.onnx ] || curl -fSLO https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.int8.onnx
[ -f voices-v1.0.bin ] || curl -fSLO https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
if [ "${ENG:-}" = 1 ]; then pip install --user kokoro-onnx soundfile faster-whisper numpy pillow; fi
echo "Done. python3 $HUB/scripts/doctor.py"

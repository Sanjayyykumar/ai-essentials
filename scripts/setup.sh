#!/usr/bin/env bash
# AI Essentials — setup on Linux / macOS / WSL.
#   bash scripts/setup.sh [--full] [--captions] [--check] [--video-root DIR]
# Installs Python 3 if missing, then runs scripts/bootstrap.py (tools, skills, plugins, video studio, models).
set -u
HUB="$(cd "$(dirname "$0")/.." && pwd)"
if ! command -v python3 >/dev/null; then
  if command -v brew >/dev/null; then brew install python
  elif command -v apt-get >/dev/null; then sudo apt-get update -qq && sudo apt-get install -y python3 python3-pip
  else echo "Install Python 3 first, then re-run."; exit 1; fi
fi
ARGS=(); for a in "$@"; do [ "$a" = "--fetch-missing" ] && a="--full"; [ "$a" = "--engines" ] && continue; ARGS+=("$a"); done
python3 "$HUB/scripts/bootstrap.py" "${ARGS[@]+"${ARGS[@]}"}"

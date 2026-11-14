#!/usr/bin/env bash
# CPU engines for the device Linux shell on this laptop (no GPU). Installs from PyPI/GitHub only.
set -e
pip install -q --user torch --index-url https://download.pytorch.org/whl/cpu
pip install -q --user sentencepiece protobuf soundfile accelerate faster-whisper \
  git+https://github.com/huggingface/parler-tts.git
python3 -c "import parler_tts, torch; print('parler ok, torch', torch.__version__)"

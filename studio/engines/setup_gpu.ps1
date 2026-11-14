# Run on a Windows laptop with an NVIDIA GPU. Creates C:\media-engines\.venv with CUDA torch + all engines.
$ErrorActionPreference = 'Stop'
$gpu = (nvidia-smi --query-gpu=name,memory.total --format=csv,noheader 2>$null)
if (-not $gpu) { Write-Host "No NVIDIA GPU found (nvidia-smi missing). Use the CPU engines; GPU kits won't run here."; exit 1 }
Write-Host "GPU: $gpu"
$E = 'C:\media-engines'; New-Item -ItemType Directory -Force $E | Out-Null; Set-Location $E
if (-not (Get-Command uv -ErrorAction SilentlyContinue)) { powershell -c "irm https://astral.sh/uv/install.ps1 | iex" }
uv venv --python 3.11
uv pip install --python .venv\Scripts\python.exe torch torchaudio --index-url https://download.pytorch.org/whl/cu124
uv pip install --python .venv\Scripts\python.exe -r "$PSScriptRoot\requirements-gpu.txt"
Copy-Item "$PSScriptRoot\*.py" $E -Force
.venv\Scripts\python.exe -c "import torch;print('CUDA', torch.cuda.is_available(), torch.cuda.get_device_name(0))"
Write-Host "Ready. Example: $E\.venv\Scripts\python.exe $E\image_flux.py --prompt 'a lighthouse at dawn' --out test.png"

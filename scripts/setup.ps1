<#  AI Essentials — one-shot setup on Windows.
    powershell -ExecutionPolicy Bypass -File scripts\setup.ps1 [-Full] [-Captions] [-Engines] [-Check] [-VideoRoot DIR]
    Installs Python if missing, then runs scripts\bootstrap.py (tools, skills, plugins, video studio, models).
      -Full      also clone every repo in libraries\registry.json (~800 MB)
      -Captions  also download the Whisper caption model (~460 MB)
      -Engines   also install media engines (CUDA kits if an NVIDIA GPU is found)
      -Check     report what's installed, change nothing
#>
param([switch]$Full,[switch]$Captions,[switch]$Engines,[switch]$Check,[switch]$FetchMissing,[string]$VideoRoot)
$ErrorActionPreference = 'Continue'
$Hub = Split-Path $PSScriptRoot -Parent
function Step($m){ Write-Host "`n== $m" -ForegroundColor Cyan }
function RefreshPath { $env:Path = [Environment]::GetEnvironmentVariable('Path','Machine') + ';' + [Environment]::GetEnvironmentVariable('Path','User') + ";$env:LOCALAPPDATA\Microsoft\WinGet\Links" }

$py = Get-Command python -ErrorAction SilentlyContinue
if (-not $py -or -not (& python -c "print(1)" 2>$null)) {
  Step "Installing Python (winget)"
  winget install -e --id Python.Python.3.12 --accept-source-agreements --accept-package-agreements --silent; RefreshPath
}
$args2 = @()
if ($Full -or $FetchMissing) { $args2 += '--full' }; if ($Captions) { $args2 += '--captions' }; if ($Check) { $args2 += '--check' }
if ($VideoRoot) { $args2 += @('--video-root', $VideoRoot) }
python (Join-Path $Hub 'scripts\bootstrap.py') @args2
RefreshPath; $VideoRoot = [Environment]::GetEnvironmentVariable('VIDEO_ROOT','User')

if ($Engines) {
  Step "Media engines"
  $gpu = (nvidia-smi --query-gpu=name,memory.total --format=csv,noheader 2>$null)
  if ($gpu) { Write-Host "NVIDIA GPU: $gpu -> CUDA engines"; & (Join-Path $Hub 'studio\engines\setup_gpu.ps1') }
  else {
    Write-Host "No NVIDIA GPU -> CPU engines"
    $E="$env:USERPROFILE\media-engines"; New-Item -ItemType Directory -Force $E | Out-Null
    uv venv "$E\.venv" --python 3.11
    $py="$E\.venv\Scripts\python.exe"
    & $py -c "print('python ok')" 2>$null
    if ($LASTEXITCODE -ne 0) { Write-Host "venv Python blocked (App Control) -> installing into system Python (--user)"; python -m pip install --user soundfile kokoro-onnx faster-whisper numpy pillow }
    else { uv pip install --python $py kokoro-onnx soundfile faster-whisper numpy pillow; Write-Host "CPU engines installed in $E" }
  }
}

Step "Done. Check anytime: python scripts\\bootstrap.py --check"

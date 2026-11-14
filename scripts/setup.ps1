<#  AI Essentials — one-shot setup on any Windows PC.
    Run from the unzipped folder:  powershell -ExecutionPolicy Bypass -File scripts\setup.ps1
    Options:
      -SkipTools        don't install git/node/python/ffmpeg/uv with winget
      -SkipSkills       don't copy skills into %USERPROFILE%\.claude\skills
      -FetchMissing     clone any library repo missing from vendor\library from its upstream (registry.json)
      -Engines          install the media engines (CPU, or CUDA if an NVIDIA GPU is found)
      -VideoRoot <dir>  where the video-generations studio lives (default: %VIDEO_ROOT% or %USERPROFILE%\video-generations)
#>
param([switch]$SkipTools,[switch]$SkipSkills,[switch]$FetchMissing,[switch]$Engines,
      [string]$VideoRoot = $(if ($env:VIDEO_ROOT) { $env:VIDEO_ROOT } else { "$env:USERPROFILE\video-generations" }))
$ErrorActionPreference = 'Continue'
$Hub = Split-Path $PSScriptRoot -Parent
$Lib = Join-Path $Hub 'vendor\library'
function Step($m){ Write-Host "`n== $m" -ForegroundColor Cyan }

Step "1/6 Environment variables"
[Environment]::SetEnvironmentVariable('AI_HUB_ROOT', $Hub, 'User')
[Environment]::SetEnvironmentVariable('AI_LIBRARY_ROOT', $Lib, 'User')
[Environment]::SetEnvironmentVariable('VIDEO_ROOT', $VideoRoot, 'User')
$env:AI_HUB_ROOT=$Hub; $env:AI_LIBRARY_ROOT=$Lib; $env:VIDEO_ROOT=$VideoRoot
Write-Host "AI_HUB_ROOT=$Hub`nAI_LIBRARY_ROOT=$Lib`nVIDEO_ROOT=$VideoRoot"

if (-not $SkipTools) {
  Step "2/6 Core tools (winget)"
  $pkgs = @{ git='Git.Git'; node='OpenJS.NodeJS.LTS'; python='Python.Python.3.11'; ffmpeg='Gyan.FFmpeg'; uv='astral-sh.uv' }
  foreach ($k in $pkgs.Keys) {
    if (Get-Command $k -ErrorAction SilentlyContinue) { Write-Host "ok  $k" }
    elseif (Get-Command winget -ErrorAction SilentlyContinue) { Write-Host "install $k"; winget install -e --id $pkgs[$k] --accept-source-agreements --accept-package-agreements --silent }
    else { Write-Host "MISSING $k (no winget: install manually)" }
  }
} else { Step "2/6 Core tools skipped" }

if (-not $SkipSkills) {
  Step "3/6 Claude skills -> $env:USERPROFILE\.claude\skills"
  $dst = "$env:USERPROFILE\.claude\skills"; New-Item -ItemType Directory -Force $dst | Out-Null
  Get-ChildItem (Join-Path $Hub 'skills') -Directory | % { Copy-Item $_.FullName $dst -Recurse -Force; Write-Host "skill $($_.Name)" }
  Write-Host "Claude Code picks these up automatically. For claude.ai, upload a skill folder as a zip in Settings > Capabilities > Skills."
} else { Step "3/6 Skills skipped" }

Step "4/6 Library repos"
$reg = Get-Content (Join-Path $Hub 'libraries\registry.json') -Raw | ConvertFrom-Json
$missing = @()
foreach ($it in $reg.items) { if ($it.local_path -and -not (Test-Path (Join-Path $Lib $it.local_path))) { $missing += $it } }
Write-Host "$($reg.items.Count) repos in registry, $($missing.Count) missing locally"
if ($FetchMissing) {
  foreach ($it in $missing) {
    $up = ($it.upstream -split ' ')[0]; if ($up -notmatch '^github.com/') { Write-Host "skip $($it.id) (no GitHub upstream)"; continue }
    $dst = Join-Path $Lib $it.local_path; New-Item -ItemType Directory -Force (Split-Path $dst) | Out-Null
    git clone --depth 1 "https://$up" "$dst"
  }
} elseif ($missing.Count) { Write-Host "Re-run with -FetchMissing to clone them." }

Step "5/6 Video studio"
New-Item -ItemType Directory -Force $VideoRoot | Out-Null
if (-not (Test-Path (Join-Path $VideoRoot 'studio\make.py'))) {
  if ((Get-ChildItem $VideoRoot -Force | Measure-Object).Count -eq 0) { git clone https://github.com/Sanjayyykumar/video-generations "$VideoRoot" }
  else { Write-Host "$VideoRoot is not empty and has no studio: clone https://github.com/Sanjayyykumar/video-generations there yourself" }
} else { Write-Host "Studio found at $VideoRoot" }
New-Item -ItemType Directory -Force (Join-Path $VideoRoot 'models') | Out-Null
$m = Join-Path $VideoRoot 'models'
if (-not (Test-Path "$m\kokoro-v1.0.int8.onnx")) {
  Write-Host "Downloading Kokoro voice model (~120 MB, GitHub release)"
  curl.exe -fSL -o "$m\kokoro-v1.0.int8.onnx" https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.int8.onnx
  curl.exe -fSL -o "$m\voices-v1.0.bin" https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
}

if ($Engines) {
  Step "6/6 Media engines"
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
} else { Step "6/6 Engines skipped (add -Engines)" }

Step "Done. Run: python `"$Hub\scripts\doctor.py`""

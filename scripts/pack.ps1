# Zip the whole hub for another machine. Output: Documents\ai-essentials_<date>.zip
param([switch]$Lite)  # -Lite = skip vendor\library (setup.ps1 -FetchMissing re-clones it from GitHub)
$Hub = Split-Path $PSScriptRoot -Parent; $out = Join-Path (Split-Path (Split-Path $Hub)) ("ai-essentials_{0:yyyy-MM-dd}{1}.zip" -f (Get-Date), $(if($Lite){'_lite'}else{''}))
$tmp = Join-Path $env:TEMP 'ai-essentials-pack'; Remove-Item $tmp -Recurse -Force -ErrorAction SilentlyContinue
$x = @('/XD','.git','__pycache__','node_modules','.venv'); if ($Lite) { $x += (Join-Path $Hub 'vendor\library') }
robocopy $Hub "$tmp\ai-essentials" /E @x /NFL /NDL /NJH /NJS /NP | Out-Null
tar -a -c -f $out -C $tmp ai-essentials; Remove-Item $tmp -Recurse -Force
Write-Host "Packed: $out  ($([math]::Round((Get-Item $out).Length/1MB)) MB)"
Write-Host "On the new PC: unzip, then  powershell -ExecutionPolicy Bypass -File ai-essentials\scripts\setup.ps1 -Engines"

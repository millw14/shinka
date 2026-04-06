# ──────────────────────────────────────────────────────────────────────────────
# shinka installer — simple script without try/catch to avoid parsing bugs
# ──────────────────────────────────────────────────────────────────────────────
$ErrorActionPreference = "Continue"

Write-Host "  Installing shinka + local AI..." -ForegroundColor Yellow
Write-Host ""

Write-Host "  [1/4] Checking Python..." -ForegroundColor Cyan
$python = $null
if (Get-Command "python" -ErrorAction SilentlyContinue) { $python = "python" }
elseif (Get-Command "python3" -ErrorAction SilentlyContinue) { $python = "python3" }
elseif (Get-Command "py" -ErrorAction SilentlyContinue) { $python = "py" }

if (-not $python) {
    Write-Host "  ⚠ Python 3 not found. Installing via winget..." -ForegroundColor Yellow
    winget install Python.Python.3.12 --accept-package-agreements --accept-source-agreements
    $python = "python"
}
Write-Host "  ✓ Python ready" -ForegroundColor Green

Write-Host "  [2/4] Checking Ollama..." -ForegroundColor Cyan
if (-not (Get-Command "ollama" -ErrorAction SilentlyContinue)) {
    Write-Host "  ⚠ Ollama not found. Installing..." -ForegroundColor Yellow
    winget install Ollama.Ollama --accept-package-agreements --accept-source-agreements
    if (-not (Get-Command "ollama" -ErrorAction SilentlyContinue)) {
        $exe = "$env:USERPROFILE\Downloads\OllamaSetup.exe"
        Invoke-WebRequest -Uri "https://ollama.com/download/OllamaSetup.exe" -OutFile $exe
        Start-Process -FilePath $exe -Wait
    }
}
Write-Host "  ✓ Ollama ready" -ForegroundColor Green

Write-Host "  [3/4] Pulling local AI model (llama3.2:1b)..." -ForegroundColor Cyan
$ollamaRunning = Invoke-WebRequest -Uri "http://127.0.0.1:11434/api/tags" -TimeoutSec 3 -ErrorAction SilentlyContinue
if (-not $ollamaRunning) {
    Start-Process "ollama" -ArgumentList "serve" -WindowStyle Hidden
    Start-Sleep -Seconds 4
}
ollama pull llama3.2:1b
Write-Host "  ✓ Model ready" -ForegroundColor Green

Write-Host "  [4/4] Installing shinka..." -ForegroundColor Cyan
if (Get-Command "pipx" -ErrorAction SilentlyContinue) {
    pipx install "https://github.com/millw14/shinka/archive/main.zip" --force
} else {
    Write-Host "  ⚠ pipx not found. Installing via pip..." -ForegroundColor Yellow
    & $python -m pip install "https://github.com/millw14/shinka/archive/main.zip" --upgrade --quiet
}
Write-Host "  ✓ shinka installed" -ForegroundColor Green

Write-Host ""
Write-Host "  All done!" -ForegroundColor Green
Write-Host "  Type 'shinka' in any terminal to start." -ForegroundColor Cyan

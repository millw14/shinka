# ──────────────────────────────────────────────────────────────────────────────
# shinka installer — one command to rule them all
# Run:  irm https://raw.githubusercontent.com/.../install.ps1 | iex
# Or locally:  .\install.ps1
# ──────────────────────────────────────────────────────────────────────────────

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "  ██████  ██   ██ ██ ███    ██ ██   ██  █████" -ForegroundColor Cyan
Write-Host " ██       ██   ██ ██ ████   ██ ██  ██  ██   ██" -ForegroundColor Cyan
Write-Host " ███████  ████████ ██ ██ ██  ██ █████   ███████" -ForegroundColor Cyan
Write-Host "      ██  ██   ██ ██ ██  ██ ██ ██  ██  ██   ██" -ForegroundColor Cyan
Write-Host " ██████  ██   ██ ██ ██   ████ ██   ██ ██   ██" -ForegroundColor Cyan
Write-Host ""
Write-Host "  進化 — evolution through design" -ForegroundColor Magenta
Write-Host "  Installing shinka + local AI..." -ForegroundColor Yellow
Write-Host ""

# ── Step 1: Check Python ─────────────────────────────────────────────────────
Write-Host "  [1/4] Checking Python..." -ForegroundColor Cyan

$python = $null
foreach ($cmd in @("python", "python3", "py")) {
    try {
        $ver = & $cmd --version 2>&1
        if ($ver -match "Python 3\.\d+") {
            $python = $cmd
            break
        }
    } catch {}
}

if (-not $python) {
    Write-Host "  ⚠ Python 3 not found. Installing via winget..." -ForegroundColor Yellow
    try {
        winget install Python.Python.3.12 --accept-package-agreements --accept-source-agreements
        $python = "python"
    } catch {
        Write-Host "  ✗ Could not install Python. Please install manually: https://python.org" -ForegroundColor Red
        exit 1
    }
}
Write-Host "  ✓ Python ready ($python)" -ForegroundColor Green

# ── Step 2: Check/Install Ollama ─────────────────────────────────────────────
Write-Host "  [2/4] Checking Ollama..." -ForegroundColor Cyan

$ollamaInstalled = Get-Command ollama -ErrorAction SilentlyContinue

if (-not $ollamaInstalled) {
    Write-Host "  ⚠ Ollama not found. Installing..." -ForegroundColor Yellow
    try {
        winget install Ollama.Ollama --accept-package-agreements --accept-source-agreements
        Write-Host "  ✓ Ollama installed" -ForegroundColor Green
    } catch {
        Write-Host "  ⚠ winget failed. Downloading installer..." -ForegroundColor Yellow
        $installerPath = "$env:USERPROFILE\Downloads\OllamaSetup.exe"
        Invoke-WebRequest -Uri "https://ollama.com/download/OllamaSetup.exe" -OutFile $installerPath
        Start-Process -FilePath $installerPath -Wait
        Write-Host "  ✓ Ollama installed" -ForegroundColor Green
    }
} else {
    Write-Host "  ✓ Ollama already installed" -ForegroundColor Green
}

# ── Step 3: Pull model ───────────────────────────────────────────────────────
Write-Host "  [3/4] Pulling local AI model (llama3.2:1b)..." -ForegroundColor Cyan
Write-Host "         This only happens once. Grab some tea! ☕" -ForegroundColor DarkGray

try {
    # Start Ollama if not running
    $ollamaRunning = $false
    try {
        $response = Invoke-WebRequest -Uri "http://127.0.0.1:11434/api/tags" -TimeoutSec 3 -ErrorAction SilentlyContinue
        $ollamaRunning = $true
    } catch {}

    if (-not $ollamaRunning) {
        Start-Process "ollama" -ArgumentList "serve" -WindowStyle Hidden
        Start-Sleep -Seconds 4
    }

    & ollama pull llama3.2:1b
    Write-Host "  ✓ Model ready" -ForegroundColor Green
} catch {
    Write-Host "  ⚠ Model pull failed. shinka will retry on first run." -ForegroundColor Yellow
}

# ── Step 4: Install shinka ───────────────────────────────────────────────────
Write-Host "  [4/4] Installing shinka..." -ForegroundColor Cyan

$pipx = Get-Command pipx -ErrorAction SilentlyContinue

if ($pipx) {
    & pipx install https://github.com/millw14/shinka/archive/main.zip --force
} else {
    Write-Host "  ⚠ pipx not found (which is recommended for CLI apps)." -ForegroundColor DarkGray
    Write-Host "  Installing via pip instead..." -ForegroundColor Yellow
    & $python -m pip install https://github.com/millw14/shinka/archive/main.zip --upgrade --quiet 2>&1 | Out-Null
}
Write-Host "  ✓ shinka installed" -ForegroundColor Green

# ── Done ─────────────────────────────────────────────────────────────────────
Write-Host ""
Write-Host "  ✧٩(ˊᗜˋ*)و✧  All done!" -ForegroundColor Green
Write-Host ""
Write-Host "  Type 'shinka' in any terminal to start designing." -ForegroundColor Cyan
Write-Host "  Type 'shinka --quick' for express mode." -ForegroundColor DarkGray
Write-Host ""

#!/usr/bin/env bash
# ──────────────────────────────────────────────────────────────────────────────
# shinka installer — macOS / Linux
# Run:  curl -fsSL https://raw.githubusercontent.com/millw14/shinka/main/install.sh | bash
# ──────────────────────────────────────────────────────────────────────────────

set -e
export PYTHONIOENCODING=utf-8
# Colors
CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color

echo ""
echo -e "${CYAN}  ██████  ██   ██ ██ ███    ██ ██   ██  █████${NC}"
echo -e "${CYAN} ██       ██   ██ ██ ████   ██ ██  ██  ██   ██${NC}"
echo -e "${CYAN} ███████  ████████ ██ ██ ██  ██ █████   ███████${NC}"
echo -e "${CYAN}      ██  ██   ██ ██ ██  ██ ██ ██  ██  ██   ██${NC}"
echo -e "${CYAN} ██████  ██   ██ ██ ██   ████ ██   ██ ██   ██${NC}"
echo ""
echo -e "${MAGENTA}  進化 — evolution through design${NC}"
echo -e "${YELLOW}  Installing shinka + local AI...${NC}"
echo ""

# ── Step 1: Check Python ─────────────────────────────────────────────────────
echo -e "${CYAN}  [1/4] Checking Python...${NC}"

if command -v python3 >/dev/null 2>&1; then
    PYTHON_CMD="python3"
elif command -v python >/dev/null 2>&1; then
    PYTHON_CMD="python"
else
    echo -e "${RED}  ✗ Python 3 is required but not installed.${NC}"
    echo "    Please install Python 3 (https://python.org) and try again."
    exit 1
fi

echo -e "${GREEN}  ✓ Python ready ($PYTHON_CMD)${NC}"

# ── Step 2: Check/Install Ollama ─────────────────────────────────────────────
echo -e "${CYAN}  [2/4] Checking Ollama...${NC}"

if ! command -v ollama >/dev/null 2>&1; then
    echo -e "${YELLOW}  ⚠ Ollama not found. Installing...${NC}"
    curl -fsSL https://ollama.com/install.sh | sh
    echo -e "${GREEN}  ✓ Ollama installed${NC}"
else
    echo -e "${GREEN}  ✓ Ollama already installed${NC}"
fi

# ── Step 3: Pull model ───────────────────────────────────────────────────────
echo -e "${CYAN}  [3/4] Pulling local AI model (llama3.2:1b)...${NC}"
echo -e "         This only happens once. Grab some tea! ☕"

# Start Ollama in the background if it's not already running
if ! curl -s http://127.0.0.1:11434/api/tags >/dev/null 2>&1; then
    ollama serve >/dev/null 2>&1 &
    OLLAMA_PID=$!
    sleep 4
fi

ollama pull llama3.2:1b || true
echo -e "${GREEN}  ✓ Model ready${NC}"

# ── Step 4: Install pipx & shinka ────────────────────────────────────────────
echo -e "${CYAN}  [4/4] Installing shinka...${NC}"

if ! command -v pipx >/dev/null 2>&1; then
    echo -e "${YELLOW}  ⚠ pipx not found. Installing pipx...${NC}"
    $PYTHON_CMD -m pip install --user pipx --quiet
    $PYTHON_CMD -m pipx ensurepath --quiet
    
    # Temporarily add pipx bin to PATH for this script 
    # (since ensurepath only applies to future terminal sessions)
    PIPX_BIN_DIR=$($PYTHON_CMD -c "import site; import os; print(os.path.join(site.USER_BASE, 'bin'))" 2>/dev/null || echo "$HOME/.local/bin")
    export PATH="$PIPX_BIN_DIR:$PATH"
fi

echo -e "${CYAN}  Downloading and installing from GitHub...${NC}"
pipx install https://github.com/millw14/shinka/archive/main.zip --force

echo -e "${GREEN}  ✓ shinka installed${NC}"

# ── Done ─────────────────────────────────────────────────────────────────────
echo ""
echo -e "${GREEN}  ✧٩(ˊᗜˋ*)و✧  All done!${NC}"
echo ""
echo -e "${CYAN}  Type 'shinka' in any new terminal to start designing.${NC}"
echo -e "  (If 'shinka' is not found, you may need to restart your terminal first)"
echo ""

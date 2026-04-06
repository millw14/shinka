# Shinka 進化 🪄

> **Your local AI frontend design wizard. Scrape live websites to extract modern styles, animations, and layouts, then generate the ultimate god-tier AI coding prompt.**

Shinka is an automated CLI tool that acts as your personal frontend design architect. It uses a **Playwright headless browser** to scrape actual HTML structures, CSS variables, JS frameworks, and animations from your favorite reference websites. It then combines this extracted code with your project requirements and uses **local AI** (Ollama) to assemble the perfect prompt for tools like Claude, Cursor, or Windsurf.

---

## 🚀 Installation

You do not need to clone this repository to install Shinka. Just copy and paste the command for your operating system into an empty terminal.

**Windows (PowerShell)**:
```powershell
iwr -useb https://raw.githubusercontent.com/millw14/shinka/main/install.ps1 | iex
```

**macOS / Linux (Bash)**:
```bash
curl -fsSL https://raw.githubusercontent.com/millw14/shinka/main/install.sh | bash
```

**What the installer does automatically:**
- ✅ Installs Python (if missing)
- ✅ Installs [Ollama](https://ollama.com/) (if missing)
- ✅ Pulls the rapid `llama3.2:1b` model for local AI thinking
- ✅ Installs `pipx` and globally installs the `shinka` CLI

---

## 🛠️ Usage

After installation, simply run `shinka` in any new terminal window.

```bash
# Start the full 7-level design wizard
shinka

# Quick mode — skips the deep questions
shinka --quick

# Skip AI enhancement (offline mode)
shinka --no-ai

# Save the final prompt to a specific file
shinka --output my_god_tier_prompt.md
```

### The Web Scraper (Level 4: The Cloner)
When you reach the "Cloner" stage of the wizard, simply provide the URL of a website you admire. Shinka will boot up a hidden browser to:
- Render the page to execute WebGL & JS
- Extract inline CSS, text gradients, and CSS variables
- Pull external CSS stylesheets dynamically
- Rip out `@keyframes` and GSAP/Three.js signatures
- Detect custom Google Fonts and global color palettes

It automatically injects these technical specifications into your prompt, guaranteeing that the AI code editor writing your site accurately replicates the aesthetic.

## 📈 The 7 Levels of Frontend Design

| Level | Name | What It Does |
|-------|------|-------------|
| 1 | The Beginner | Establishes project base + anti-AI-slop rules |
| 2 | Vocabulary Builder | Defines design references, fonts, colors, aesthetics |
| 3 | Framework Master | Specifies CSS frameworks, layout grids, typography scales |
| 4 | The Cloner | **Automated Web Scraping:** Pulls source code from live URLs to clone |
| 5 | The Customizer | Determines custom brand assets & micro-interactions |
| 6 | The Orchestrator | Specifies tech stack, animation libs (GSAP), 3D elements |
| 7 | The Frontier | Directs WebGL, complex shaders, procedural animation |

## 🤝 Works Seamlessly With

- **Claude Code** (from Anthropic)
- **Cursor**
- **Windsurf**
- **GitHub Copilot**
- *Any AI code editor that accepts text/markdown prompts*

---

*shinka (進化) — evolution through design* ✨

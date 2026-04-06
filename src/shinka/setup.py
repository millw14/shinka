"""
Auto-setup — checks for and installs Ollama, pulls the local model,
handles all bootstrapping on first run.
"""
import subprocess
import sys
import shutil
import time
import platform
import tempfile
from pathlib import Path

from rich.prompt import Confirm

from shinka.ui import (
    console, animate_install_step, get_download_progress,
    random_kaomoji, section_header, SYM_CHECK, SYM_WARN, SYM_CROSS
)

MODEL_NAME = "llama3.2:1b"
OLLAMA_WIN_URL = "https://ollama.com/download/OllamaSetup.exe"


def is_ollama_installed() -> bool:
    """Check if Ollama is accessible via CLI."""
    return shutil.which("ollama") is not None or (
        platform.system().lower() == "windows"
        and (Path(r"C:\Users") / Path.home().name / "AppData" / "Local" / "Programs" / "Ollama" / "ollama.exe").exists()
    )


def is_ollama_running() -> bool:
    """Check if the Ollama server is responding to API requests."""
    try:
        import httpx
        r = httpx.get("http://127.0.0.1:11434/api/tags", timeout=1.0)
        return r.status_code == 200
    except (httpx.RequestError, ImportError):
        return False


def is_model_available(model: str = MODEL_NAME) -> bool:
    """Check if the local model has been pulled."""
    try:
        import httpx
        r = httpx.get("http://127.0.0.1:11434/api/tags", timeout=2.0)
        if r.status_code == 200:
            models = r.json().get("models", [])
            return any(m.get("name") == model for m in models)
        return False
    except (httpx.RequestError, ImportError):
        return False


def install_ollama():
    """Download and install Ollama based on the OS."""
    system = platform.system().lower()

    if system == "windows":
        console.print(f"\n  [yellow]{SYM_WARN}[/yellow] Ollama is not installed.")
        if not Confirm.ask(f"  [cyan]Install Ollama automatically?[/cyan]"):
            console.print(f"  [dim]Install manually: https://ollama.com/download[/dim]")
            sys.exit(1)

        # Try winget first
        if shutil.which("winget"):
            animate_install_step("Installing Ollama via winget")
            try:
                subprocess.run(
                    ["winget", "install", "Ollama.Ollama", "--accept-package-agreements", "--accept-source-agreements"],
                    check=True,
                    stdout=subprocess.DEVNULL,
                )
                return
            except subprocess.CalledProcessError:
                console.print(f"  [yellow]{SYM_WARN}[/yellow] winget install failed, trying direct download...")

        # Fallback: direct download
        animate_install_step("Downloading Ollama installer")
        try:
            import httpx
            installer_path = Path.home() / "Downloads" / "OllamaSetup.exe"
            with httpx.stream("GET", OLLAMA_WIN_URL, follow_redirects=True, timeout=120) as r:
                total = int(r.headers.get("content-length", 0))
                with get_download_progress() as progress:
                    task = progress.add_task("Downloading Ollama", total=total)
                    with open(installer_path, "wb") as f:
                        for chunk in r.iter_bytes(chunk_size=8192):
                            f.write(chunk)
                            progress.update(task, advance=len(chunk))

            console.print(f"\n  [cyan]Running installer...[/cyan] {random_kaomoji('wait')}")
            console.print(f"  [dim]Please complete the Ollama installer window, then come back here.[/dim]\n")
            subprocess.run([str(installer_path)], check=True)
            animate_install_step("Ollama installed")
        except Exception as e:
            console.print(f"\n  [red]{SYM_CROSS}[/red] Download failed: {e}")
            console.print(f"  [dim]Please install Ollama manually: https://ollama.com/download[/dim]")
            sys.exit(1)

    elif system == "darwin":
        console.print(f"\n  [yellow]{SYM_WARN}[/yellow] Ollama is not installed.")
        if Confirm.ask(f"  [cyan]Install Ollama via brew?[/cyan]"):
            subprocess.run(["brew", "install", "ollama"], check=True)
        else:
            console.print(f"  [dim]Install manually: https://ollama.com/download[/dim]")
            sys.exit(1)

    else:  # Linux
        console.print(f"\n  [yellow]{SYM_WARN}[/yellow] Ollama is not installed.")
        if Confirm.ask(f"  [cyan]Install Ollama automatically?[/cyan]"):
            subprocess.run("curl -fsSL https://ollama.com/install.sh | sh", shell=True, check=True)
        else:
            console.print(f"  [dim]Install manually: https://ollama.com/download[/dim]")
            sys.exit(1)


def start_ollama_server():
    """Start Ollama server in the background if not already running."""
    if is_ollama_running():
        return

    animate_install_step("Starting Ollama server")

    log_file = tempfile.NamedTemporaryFile(delete=False, suffix=".log")
    system = platform.system().lower()
    
    if system == "windows":
        # On Windows, try to start via the app or serve command
        ollama_path = shutil.which("ollama")
        if ollama_path:
            subprocess.Popen(
                ["ollama", "serve"],
                stdout=subprocess.DEVNULL,
                stderr=log_file,
                creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, "CREATE_NO_WINDOW") else 0,
            )
        else:
            # Try default install location
            default_path = Path(r"C:\Users") / Path.home().name / "AppData" / "Local" / "Programs" / "Ollama" / "ollama.exe"
            if default_path.exists():
                subprocess.Popen(
                    [str(default_path), "serve"],
                    stdout=subprocess.DEVNULL,
                    stderr=log_file,
                    creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, "CREATE_NO_WINDOW") else 0,
                )
    else:
        subprocess.Popen(
            ["ollama", "serve"],
            stdout=subprocess.DEVNULL,
            stderr=log_file,
        )

    # Wait for server to come up
    for _ in range(30):
        if is_ollama_running():
            try:
                Path(log_file.name).unlink()
            except Exception:
                pass
            return
        time.sleep(1)

    console.print(f"  [yellow]{SYM_WARN}[/yellow] Ollama server is slow to start. Continuing anyway...")
    
    try:
        err_content = Path(log_file.name).read_text(encoding="utf-8").strip()
        if err_content:
            first_err = err_content.splitlines()[0]
            console.print(f"  [dim]Log: {first_err}[/dim]")
        Path(log_file.name).unlink()
    except Exception:
        pass


def pull_model(model: str = MODEL_NAME):
    """Pull the required model with a progress animation."""
    if is_model_available(model):
        console.print(f"  [green]{SYM_CHECK}[/green] [bold]Model {model} ready[/bold]  {random_kaomoji('happy')}")
        return

    console.print(f"\n  [cyan]Downloading model: [bold]{model}[/bold][/cyan]  {random_kaomoji('wait')}")
    console.print(f"  [dim]This only happens once. Grab some tea! ☕[/dim]\n")

    try:
        import ollama as ollama_lib

        with get_download_progress() as progress:
            task = progress.add_task(f"Pulling {model}", total=None)

            for chunk in ollama_lib.pull(model, stream=True):
                status = chunk.get("status", "")
                total = chunk.get("total", 0)
                completed = chunk.get("completed", 0)

                if total and total > 0:
                    progress.update(task, total=total, completed=completed, description=status)
                else:
                    progress.update(task, description=status)

        console.print(f"\n  [green]{SYM_CHECK}[/green] [bold]Model {model} downloaded![/bold]  {random_kaomoji('done')}")

    except Exception as e:
        console.print(f"\n  [yellow]{SYM_WARN}[/yellow] Model pull via library failed ({e}), trying CLI...")
        try:
            subprocess.run(["ollama", "pull", model], check=True)
            console.print(f"  [green]{SYM_CHECK}[/green] [bold]Model {model} ready[/bold]")
        except subprocess.CalledProcessError:
            console.print(f"  [red]{SYM_CROSS}[/red] Failed to pull model. Run manually: ollama pull {model}")
            sys.exit(1)


def ensure_ready():
    """Full bootstrap: install Ollama, start server, pull model."""
    section_header("Setting Up", "⚡")

    # Step 1: Ollama installed?
    if not is_ollama_installed():
        install_ollama()
    else:
        console.print(f"  [green]{SYM_CHECK}[/green] [bold]Ollama installed[/bold]  {random_kaomoji('happy')}")

    # Step 2: Server running?
    start_ollama_server()
    console.print(f"  [green]{SYM_CHECK}[/green] [bold]Ollama server running[/bold]  {random_kaomoji('happy')}")

    # Step 3: Model available?
    pull_model()

    console.print()
    console.print(f"  [bold green]All systems go![/bold green]  {random_kaomoji('done')}")
    console.print()


def chat_with_model(prompt: str, model: str = MODEL_NAME) -> str:
    """Send a prompt to the local model and return the response."""
    try:
        import ollama as ollama_lib
        response = ollama_lib.chat(
            model=model,
            messages=[{"role": "user", "content": prompt}],
        )
        return response["message"]["content"]
    except Exception as e:
        return f"[Local model unavailable: {e}]"

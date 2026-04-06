"""
Anime-themed terminal UI — mascot art, welcome screen, animations, panels.

Includes automatic Unicode/encoding detection so the design renders
correctly on any terminal (Windows cmd, PowerShell, macOS Terminal,
Linux TTYs, SSH sessions, and CI/CD pipes).
"""
import os
import sys
import time
import random

# ── Force UTF-8 on Windows before importing Rich ─────────────────────────────
# Without this, Python on Windows defaults to the locale codepage (cp1252 etc.)
# and every kaomoji / braille character triggers UnicodeEncodeError.
os.environ.setdefault("PYTHONIOENCODING", "utf-8")
os.environ.setdefault("PYTHONLEGACYWINDOWSSTDIO", "0")

try:
    # Python 3.7+ on Windows — force stdout/stderr to UTF-8
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# On Windows, also try to set the console code page to UTF-8
if sys.platform == "win32":
    try:
        os.system("chcp 65001 >nul 2>&1")
    except Exception:
        pass

from rich.console import Console, Group
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich.columns import Columns
from rich.live import Live
from rich.table import Table
from rich.progress import (
    Progress, SpinnerColumn, TextColumn, BarColumn,
    TaskProgressColumn, TimeRemainingColumn,
)


# ── Unicode Capability Detection ─────────────────────────────────────────────
def _can_render_unicode() -> bool:
    """Test whether the current terminal can render full Unicode (braille, CJK, kaomoji)."""
    try:
        # Check if stdout encoding supports the characters we need
        encoding = getattr(sys.stdout, "encoding", "ascii") or "ascii"
        test_char = "⣿"  # braille character from our mascot
        test_char.encode(encoding)

        # Also check for Windows legacy console (pre-Windows Terminal)
        if sys.platform == "win32":
            # Windows Terminal and modern PowerShell handle Unicode fine
            # Legacy cmd.exe / conhost does not
            # WT_SESSION is set by Windows Terminal; TERM_PROGRAM by others
            if os.environ.get("WT_SESSION") or os.environ.get("TERM_PROGRAM"):
                return True
            # Check if we successfully set codepage 65001
            if encoding.lower() in ("utf-8", "utf8"):
                return True
            return False

        return True
    except (UnicodeEncodeError, UnicodeDecodeError, LookupError):
        return False


UNICODE_OK = _can_render_unicode()

# ── Console — force_terminal ensures colors always render ────────────────────
console = Console(force_terminal=True)


# ── Shinka Mascot ASCII Art ──────────────────────────────────────────────────
# Full Unicode version (braille art)
_MASCOT_UNICODE = r"""
[bold magenta]        ⠀⠀⠀⠀⠀⢀⣤⣶⣿⣿⣶⣤⡀⠀⠀⠀⠀⠀
        ⠀⠀⠀⢀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣦⡀⠀⠀⠀
        ⠀⠀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠀⠀
        ⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀
        ⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇
        ⢸⣿[cyan]⣿⣿⣿[/cyan]⣿⣿⣿⣿⣿⣿⣿[cyan]⣿⣿⣿[/cyan]⣿⣿⡇
        ⠸⣿[bold white]⠿⠿⠿[/bold white]⣿⣿⣿⣿⣿⣿⣿[bold white]⠿⠿⠿[/bold white]⣿⣿⠇
        ⠀⢿⣿⣿⣿⣿⣿⣿[bold red]⣀⣀[/bold red]⣿⣿⣿⣿⣿⣿⡿⠀
        ⠀⠀⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠀⠀
        ⠀⠀⠀⠈⠻⢿⣿⣿⣿⣿⣿⣿⡿⠟⠁⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠈⠉⠛⠛⠉⠁⠀⠀⠀⠀⠀⠀[/bold magenta]"""

# ASCII-safe fallback (works on ANY terminal)
_MASCOT_ASCII = r"""
[bold magenta]            .--------.
           /  .-----.  \
          /  /       \  \
         |  | [cyan]o[/cyan]   [cyan]o[/cyan]  |  |
         |  |       |  |
          \  \ [bold red]---[/bold red] /  /
           \  '-----'  /
            '--------'
       [bold cyan]~ shinka ~[/bold cyan][/bold magenta]"""

MASCOT = _MASCOT_UNICODE if UNICODE_OK else _MASCOT_ASCII

_MASCOT_SMALL_UNICODE = r"""[bold magenta]  ／l
 （ﾟ、 ７   [bold cyan]~ shinka[/bold cyan]
 ｜、ﾞ ~ヽ
 じしf_, )ノ[/bold magenta]"""

_MASCOT_SMALL_ASCII = r"""[bold magenta]  /\
 ( o.o )  [bold cyan]~ shinka[/bold cyan]
  > ^ <[/bold magenta]"""

MASCOT_SMALL = _MASCOT_SMALL_UNICODE if UNICODE_OK else _MASCOT_SMALL_ASCII


# ── Kaomoji reactions ────────────────────────────────────────────────────────
_KAOMOJI_HAPPY_UNICODE = ["(^_^)", "(*_*)", "(>v<)", "(*^_^*)", "(~_~)", "(^o^)", "(^-^)"]
_KAOMOJI_THINKING_UNICODE = ["(o_o)", "(~_~;)", "('_')", "(-_-)", "(._.)"]
_KAOMOJI_DONE_UNICODE = ["(*^_^*)", "(^o^)/", "(*_*)", "(>_<)b", "('-')b"]
_KAOMOJI_WAIT_UNICODE = ["(._. )", "(-_-)", "( '_')", "(^_^ )", "(o_o)"]

if UNICODE_OK:
    KAOMOJI_HAPPY = ["(◕‿◕✿)", "٩(◕‿◕｡)۶", "(ﾉ◕ヮ◕)ﾉ*:・ﾟ✧", "(*≧▽≦)", "( ˘▽˘)っ♨", "(◠‿◠)", "ヽ(>∀<☆)ノ"]
    KAOMOJI_THINKING = ["(⊙_⊙)", "(￣ω￣;)", "(´-ω-`)", "( ˘⌣˘)♡(˘⌣˘ )", "(¬‿¬ )", "┐(￣ヮ￣)┌"]
    KAOMOJI_DONE = ["✧٩(ˊᗜˋ*)و✧", "(ノ´ヮ`)ノ*: ・゚✧", "(*^▽^*)", "☆*:.｡.o(≧▽≦)o.｡.:*☆", "(⌐■_■)"]
    KAOMOJI_WAIT = ["(ᵕ̤ᴗᵕ̤)", "(✿╹◡╹)", "( ˙▿˙ )", "(◕ᴗ◕✿)", "(・ω・)"]
else:
    KAOMOJI_HAPPY = _KAOMOJI_HAPPY_UNICODE
    KAOMOJI_THINKING = _KAOMOJI_THINKING_UNICODE
    KAOMOJI_DONE = _KAOMOJI_DONE_UNICODE
    KAOMOJI_WAIT = _KAOMOJI_WAIT_UNICODE


def random_kaomoji(mood: str = "happy") -> str:
    pool = {
        "happy": KAOMOJI_HAPPY,
        "thinking": KAOMOJI_THINKING,
        "done": KAOMOJI_DONE,
        "wait": KAOMOJI_WAIT,
    }
    return random.choice(pool.get(mood, KAOMOJI_HAPPY))


# ── Safe print helper ────────────────────────────────────────────────────────
def safe_print(markup: str):
    """Print Rich markup, falling back to plain text on encoding errors."""
    try:
        console.print(markup)
    except UnicodeEncodeError:
        # Strip Rich markup tags and print plain
        import re
        plain = re.sub(r'\[/?[^\]]*\]', '', markup)
        print(plain)


# ── Welcome Screen ───────────────────────────────────────────────────────────
_TITLE_ART_UNICODE = r"""
[bold cyan]     ██████  ██   ██ ██ ███    ██ ██   ██  █████
    ██       ██   ██ ██ ████   ██ ██  ██  ██   ██
    ███████  ████████ ██ ██ ██  ██ █████   ███████
         ██  ██   ██ ██ ██  ██ ██ ██  ██  ██   ██
    ██████  ██   ██ ██ ██   ████ ██   ██ ██   ██[/bold cyan]
"""

_TITLE_ART_ASCII = r"""
[bold cyan]  ____  _   _ ___ _   _ _  __    _
 / ___|| | | |_ _| \ | | |/ /   / \
 \___ \| |_| || ||  \| | ' /   / _ \
  ___) |  _  || || |\  | . \  / ___ \
 |____/|_| |_|___|_| \_|_|\_\/_/   \_\[/bold cyan]
"""

TITLE_ART = _TITLE_ART_UNICODE if UNICODE_OK else _TITLE_ART_ASCII

SUBTITLE = "[dim italic]shinka — evolution through design[/dim italic]"
VERSION_LINE = "[dim]v1.0.0 · your frontend design wizard[/dim]"


def show_welcome():
    """Display the full anime welcome screen."""
    console.clear()

    # Build the welcome panel using Group for composing renderables
    content = Group(
        Text.from_markup(TITLE_ART),
        Align.center(Text.from_markup(SUBTITLE)),
        Align.center(Text.from_markup(VERSION_LINE)),
        Text(""),
        Text.from_markup(MASCOT),
        Text(""),
    )

    panel = Panel(
        Align.center(content),
        border_style="bold magenta",
        padding=(1, 4),
        title="[bold white]* Welcome *[/bold white]" if not UNICODE_OK else "[bold white]✦ Welcome ✦[/bold white]",
        subtitle=f"[dim]{random_kaomoji('happy')}[/dim]",
    )
    try:
        console.print(panel)
    except UnicodeEncodeError:
        # Last-resort fallback
        console.print("[bold cyan]SHINKA[/bold cyan] [dim]v1.0.0[/dim]")
        console.print("[dim]evolution through design[/dim]")
    console.print()


def show_welcome_compact():
    """Compact welcome for returning users."""
    console.print()
    console.print(
        Panel(
            f"  {MASCOT_SMALL}\n\n"
            f"  [bold cyan]shinka[/bold cyan] [dim]v1.0.0[/dim]  {random_kaomoji('happy')}",
            border_style="magenta",
            padding=(0, 2),
        )
    )
    console.print()


# ── Safe symbols ─────────────────────────────────────────────────────────────
# Use safe alternatives when Unicode isn't available
SYM_STAR = "✦" if UNICODE_OK else "*"
SYM_CHECK = "✓" if UNICODE_OK else "+"
SYM_CROSS = "✗" if UNICODE_OK else "x"
SYM_WARN = "⚠" if UNICODE_OK else "!"
SYM_ARROW = "›" if UNICODE_OK else ">"
SYM_SPINNER = "⟳" if UNICODE_OK else "~"
SYM_BAR = "━" if UNICODE_OK else "-"


# ── Download / Install Animation ─────────────────────────────────────────────
if UNICODE_OK:
    DOWNLOAD_FRAMES = [
        "[magenta]◜[/magenta]", "[magenta]◠[/magenta]",
        "[cyan]◝[/cyan]", "[cyan]◞[/cyan]",
        "[magenta]◡[/magenta]", "[magenta]◟[/magenta]",
    ]
    INSTALL_SPARKLES = ["✦", "✧", "⋆", "˚", "·", "⊹", "✵", "✶"]
else:
    DOWNLOAD_FRAMES = [
        "[magenta]|[/magenta]", "[magenta]/[/magenta]",
        "[cyan]-[/cyan]", "[cyan]\\[/cyan]",
        "[magenta]|[/magenta]", "[magenta]/[/magenta]",
    ]
    INSTALL_SPARKLES = ["*", "+", ".", "~", "-", "=", "#", "@"]


def get_download_progress() -> Progress:
    """Create a styled progress bar for downloads."""
    return Progress(
        SpinnerColumn("dots", style="magenta"),
        TextColumn("[bold cyan]{task.description}[/bold cyan]"),
        BarColumn(bar_width=40, style="dim", complete_style="magenta", finished_style="green"),
        TaskProgressColumn(),
        TimeRemainingColumn(),
        console=console,
    )


def animate_install_step(message: str, duration: float = 1.5):
    """Show an animated install step with sparkles."""
    frames = []
    for i in range(int(duration * 10)):
        sparkle = random.choice(INSTALL_SPARKLES)
        dot_count = (i % 3) + 1
        dots = "." * dot_count + " " * (3 - dot_count)
        frames.append(f"  [magenta]{sparkle}[/magenta] [cyan]{message}{dots}[/cyan]")

    with Live(console=console, refresh_per_second=10) as live:
        for frame in frames:
            live.update(Text.from_markup(frame))
            time.sleep(0.1)

    console.print(f"  [green]{SYM_CHECK}[/green] [bold]{message}[/bold]  {random_kaomoji('done')}")


def animate_thinking(message: str = "Thinking"):
    """Show an animated thinking indicator. Returns a Live context manager."""
    return Live(
        Text.from_markup(f"  [magenta]{SYM_SPINNER}[/magenta] [cyan]{message}...[/cyan] {random_kaomoji('thinking')}"),
        console=console,
        refresh_per_second=4,
    )


# ── Section Headers ──────────────────────────────────────────────────────────
def section_header(title: str, emoji: str = "✦"):
    """Print a styled section header."""
    # Use safe emoji if Unicode not available
    if not UNICODE_OK and ord(emoji[0]) > 127:
        emoji = "*"
    console.print()
    console.print(
        Panel(
            f"[bold white]{title}[/bold white]",
            border_style="cyan",
            padding=(0, 2),
            title=f"[magenta]{emoji}[/magenta]",
            expand=False,
        )
    )
    console.print()


def phase_header(phase_num: int, title: str):
    """Print a phase header for the wizard."""
    bar = SYM_BAR * 50
    console.print(f"\n  [dim]{bar}[/dim]")
    console.print(f"  [magenta]Phase {phase_num}[/magenta] [bold cyan]{title}[/bold cyan]  {random_kaomoji('wait')}")
    console.print(f"  [dim]{bar}[/dim]\n")


# ── Result Display ───────────────────────────────────────────────────────────
def show_result(prompt_text: str, saved_path: str | None = None, clipboard_ok: bool = False):
    """Display the final generated prompt in a beautiful panel."""
    console.print()

    # Truncated preview
    preview_lines = prompt_text.split("\n")
    if len(preview_lines) > 60:
        preview = "\n".join(preview_lines[:60])
        preview += f"\n\n[dim]... ({len(preview_lines) - 60} more lines)[/dim]"
    else:
        preview = prompt_text

    star = SYM_STAR
    console.print(
        Panel(
            preview,
            title=f"[bold green]{star} YOUR GOD-TIER PROMPT {star}[/bold green]",
            subtitle=f"[dim]{random_kaomoji('done')}[/dim]",
            border_style="green",
            padding=(1, 2),
        )
    )

    console.print()
    if clipboard_ok:
        console.print(f"  [green]{SYM_CHECK}[/green] [bold]Copied to clipboard![/bold]")
    else:
        console.print(f"  [yellow]{SYM_WARN}[/yellow] [dim]Could not copy to clipboard. The prompt was saved to the file below.[/dim]")
    if saved_path:
        console.print(f"  [green]{SYM_CHECK}[/green] [bold]Saved to: [cyan]{saved_path}[/cyan][/bold]")
    console.print()
    console.print(f"  [dim]Paste this into Claude Code, Cursor, Windsurf, or any AI editor.[/dim]")
    console.print(f"  [dim]Happy designing![/dim]  {random_kaomoji('happy')}")
    console.print()


# ── Level Selector Display ───────────────────────────────────────────────────
def show_level_selector(levels_info: list[str]):
    """Display the level selector with anime styling."""
    table = Table(
        show_header=True,
        header_style="bold magenta",
        border_style="dim",
        padding=(0, 1),
        title=f"[bold cyan]Choose Your Level[/bold cyan]  {random_kaomoji('thinking')}",
    )
    table.add_column("Lvl", style="bold cyan", width=4, justify="center")
    table.add_column("Name", style="bold white", width=22)
    table.add_column("Description", style="dim")

    level_styles = [
        ("1", "The Beginner", "Basic prompting with anti-slop rules"),
        ("2", "Vocabulary Builder", "Design references & specific aesthetics"),
        ("3", "Framework Master", "Grids, scales, accessibility, systems"),
        ("4", "The Cloner", "Clone real code from pro sites"),
        ("5", "The Customizer", "Own the design with custom assets"),
        ("6", "The Orchestrator", "Multi-tool workflow orchestration"),
        ("7", "The Frontier", "WebGL, shaders, 3D, bleeding edge"),
    ]

    for lvl, name, desc in level_styles:
        table.add_row(lvl, name, desc)

    console.print()
    console.print(Align.center(table))
    console.print()


def show_choices(title: str, choices: dict[str, str]) -> None:
    """Display a set of choices in a styled format."""
    console.print(f"  [bold cyan]{title}[/bold cyan]")
    for key, desc in choices.items():
        console.print(f"    [magenta]{SYM_ARROW}[/magenta] [bold]{key}[/bold] [dim]— {desc}[/dim]")
    console.print()


def goodbye():
    """Show a goodbye message."""
    console.print(
        Panel(
            f"  [bold cyan]See you next time![/bold cyan]  {random_kaomoji('happy')}\n"
            f"  [dim]Type [bold]shinka[/bold] anytime to create another prompt.[/dim]",
            border_style="magenta",
            padding=(1, 2),
        )
    )

"""
Anime-themed terminal UI — mascot art, welcome screen, animations, panels.
"""
import time
import random
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

console = Console()

# ── Shinka Mascot ASCII Art ──────────────────────────────────────────────────
MASCOT = r"""
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

MASCOT_SMALL = r"""[bold magenta]  ／l
 （ﾟ、 ７   [bold cyan]~ shinka[/bold cyan]
 ｜、ﾞ ~ヽ
 じしf_, )ノ[/bold magenta]"""

# ── Kaomoji reactions ────────────────────────────────────────────────────────
KAOMOJI_HAPPY = ["(◕‿◕✿)", "٩(◕‿◕｡)۶", "(ﾉ◕ヮ◕)ﾉ*:・ﾟ✧", "(*≧▽≦)", "( ˘▽˘)っ♨", "(◠‿◠)", "ヽ(>∀<☆)ノ"]
KAOMOJI_THINKING = ["(⊙_⊙)", "(￣ω￣;)", "(´-ω-`)", "( ˘⌣˘)♡(˘⌣˘ )", "(¬‿¬ )", "┐(￣ヮ￣)┌"]
KAOMOJI_DONE = ["✧٩(ˊᗜˋ*)و✧", "(ノ´ヮ`)ノ*: ・゚✧", "(*^▽^*)", "☆*:.｡.o(≧▽≦)o.｡.:*☆", "(⌐■_■)"]
KAOMOJI_WAIT = ["(ᵕ̤ᴗᵕ̤)", "(✿╹◡╹)", "( ˙▿˙ )", "(◕ᴗ◕✿)", "(・ω・)"]


def random_kaomoji(mood: str = "happy") -> str:
    pool = {
        "happy": KAOMOJI_HAPPY,
        "thinking": KAOMOJI_THINKING,
        "done": KAOMOJI_DONE,
        "wait": KAOMOJI_WAIT,
    }
    return random.choice(pool.get(mood, KAOMOJI_HAPPY))


# ── Welcome Screen ───────────────────────────────────────────────────────────
TITLE_ART = r"""
[bold cyan]     ██████  ██   ██ ██ ███    ██ ██   ██  █████
    ██       ██   ██ ██ ████   ██ ██  ██  ██   ██
    ███████  ████████ ██ ██ ██  ██ █████   ███████
         ██  ██   ██ ██ ██  ██ ██ ██  ██  ██   ██
    ██████  ██   ██ ██ ██   ████ ██   ██ ██   ██[/bold cyan]
"""

SUBTITLE = "[dim italic]進化 — evolution through design[/dim italic]"
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
        title="[bold white]✦ Welcome ✦[/bold white]",
        subtitle=f"[dim]{random_kaomoji('happy')}[/dim]",
    )
    console.print(panel)
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


# ── Download / Install Animation ─────────────────────────────────────────────
DOWNLOAD_FRAMES = [
    "[magenta]◜[/magenta]", "[magenta]◠[/magenta]",
    "[cyan]◝[/cyan]", "[cyan]◞[/cyan]",
    "[magenta]◡[/magenta]", "[magenta]◟[/magenta]",
]

INSTALL_SPARKLES = [
    "✦", "✧", "⋆", "˚", "·", "⊹", "✵", "✶",
]


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

    console.print(f"  [green]✓[/green] [bold]{message}[/bold]  {random_kaomoji('done')}")


def animate_thinking(message: str = "Thinking"):
    """Show an animated thinking indicator. Returns a Live context manager."""
    return Live(
        Text.from_markup(f"  [magenta]⟳[/magenta] [cyan]{message}...[/cyan] {random_kaomoji('thinking')}"),
        console=console,
        refresh_per_second=4,
    )


# ── Section Headers ──────────────────────────────────────────────────────────
def section_header(title: str, emoji: str = "✦"):
    """Print a styled section header."""
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
    bar = "━" * 50
    console.print(f"\n  [dim]{bar}[/dim]")
    console.print(f"  [magenta]Phase {phase_num}[/magenta] [bold cyan]{title}[/bold cyan]  {random_kaomoji('wait')}")
    console.print(f"  [dim]{bar}[/dim]\n")


# ── Result Display ───────────────────────────────────────────────────────────
def show_result(prompt_text: str, saved_path: str | None = None):
    """Display the final generated prompt in a beautiful panel."""
    console.print()

    # Truncated preview
    preview_lines = prompt_text.split("\n")
    if len(preview_lines) > 60:
        preview = "\n".join(preview_lines[:60])
        preview += f"\n\n[dim]... ({len(preview_lines) - 60} more lines)[/dim]"
    else:
        preview = prompt_text

    console.print(
        Panel(
            preview,
            title="[bold green]✦ YOUR GOD-TIER PROMPT ✦[/bold green]",
            subtitle=f"[dim]{random_kaomoji('done')}[/dim]",
            border_style="green",
            padding=(1, 2),
        )
    )

    console.print()
    console.print(f"  [green]✓[/green] [bold]Copied to clipboard![/bold]")
    if saved_path:
        console.print(f"  [green]✓[/green] [bold]Saved to: [cyan]{saved_path}[/cyan][/bold]")
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
        console.print(f"    [magenta]›[/magenta] [bold]{key}[/bold] [dim]— {desc}[/dim]")
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

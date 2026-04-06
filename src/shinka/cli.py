"""
shinka CLI — main entry point.
Handles first-run setup, wizard launch, and prompt output.
"""
import sys
from pathlib import Path
from datetime import datetime

import typer

from shinka.ui import (
    console, show_welcome, show_result, goodbye,
    section_header, random_kaomoji, animate_install_step,
)

app = typer.Typer(
    help="shinka — 7 Levels Frontend Design Prompt Wizard with Local AI",
    no_args_is_help=False,
    add_completion=False,
)


@app.command()
def start(
    skip_ai: bool = typer.Option(False, "--no-ai", help="Skip local AI enhancement"),
    quick: bool = typer.Option(False, "--quick", "-q", help="Quick mode (Level 3 defaults)"),
    output: str = typer.Option("", "--output", "-o", help="Save prompt to this file path"),
):
    """Run the full shinka design wizard."""

    # ── Welcome ──────────────────────────────────────────────────────────
    show_welcome()

    # ── Auto-Setup ───────────────────────────────────────────────────────
    if not skip_ai:
        from shinka.setup import ensure_ready
        ensure_ready()
    else:
        console.print(f"  [dim]Skipping AI setup (--no-ai mode)[/dim]\n")

    # ── Wizard ───────────────────────────────────────────────────────────
    section_header("Design Wizard", "🎨")

    if quick:
        console.print(f"  [cyan]Quick mode — using Level 3 defaults[/cyan]  {random_kaomoji('happy')}\n")
        from shinka.wizard import WizardAnswers
        from rich.prompt import Prompt
        answers = WizardAnswers()
        answers.level = 3
        answers.project_name = Prompt.ask("  [magenta]›[/magenta] Project name")
        answers.description = Prompt.ask("  [magenta]›[/magenta] What does it do?")
        answers.audience = Prompt.ask("  [magenta]›[/magenta] Target audience")
        answers.goal = "showcase"
        answers.sections = ["hero", "features", "social_proof", "cta", "footer"]
        answers.aesthetic = "dark_tech"
        from shinka.templates import AESTHETICS, FONT_PAIRINGS, COLOR_PALETTES, ANIMATION_PRESETS, TYPOGRAPHY_SCALES
        answers.aesthetic_details = AESTHETICS["dark_tech"]
        answers.font_pairing = "tech_premium"
        answers.font_details = FONT_PAIRINGS["tech_premium"]
        answers.color_palette = "midnight_cyan"
        answers.color_details = COLOR_PALETTES["midnight_cyan"]
        answers.animation_intensity = "moderate"
        answers.animation_details = ANIMATION_PRESETS["moderate"]
        answers.grid_system = "8-point"
        answers.typography_scale = "major_third"
        answers.typography_scale_details = TYPOGRAPHY_SCALES["major_third"]
        answers.accessibility = "wcag_aa"
        answers.component_patterns = ["glassmorphic_cards", "scroll_reveal", "floating_navbar"]
    else:
        from shinka.wizard import run_wizard
        answers = run_wizard()

    # ── Build Prompt ─────────────────────────────────────────────────────
    section_header("Building Your Prompt", "⚡")
    animate_install_step("Assembling design specifications")

    from shinka.prompt_builder import build_prompt
    final_prompt = build_prompt(answers, ai_enhance=not skip_ai)

    animate_install_step("Finalizing prompt")

    # ── Output ───────────────────────────────────────────────────────────
    # Copy to clipboard
    try:
        import pyperclip
        pyperclip.copy(final_prompt)
        clipboard_ok = True
    except Exception:
        clipboard_ok = False

    # Save to file
    save_path = None
    if output:
        save_path = output
    else:
        # Auto-save to current directory
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"shinka_{answers.project_name.lower().replace(' ', '_')}_{timestamp}.md"
        save_path = str(Path.cwd() / filename)

    try:
        Path(save_path).write_text(final_prompt, encoding="utf-8")
    except Exception as e:
        console.print(f"  [yellow]⚠[/yellow] Could not save file: {e}")
        save_path = None

    # Display result
    show_result(
        final_prompt,
        saved_path=save_path,
    )

    if not clipboard_ok:
        console.print(f"  [yellow]⚠[/yellow] [dim]Could not copy to clipboard. The prompt was saved to the file above.[/dim]")

    goodbye()


def main():
    """Entry point for the CLI."""
    app()


if __name__ == "__main__":
    main()

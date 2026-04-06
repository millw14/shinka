"""
Interactive questionnaire engine — walks users through design decisions
based on their chosen level (1-7). Each phase unlocks at higher levels.
"""
from rich.prompt import Prompt, Confirm, IntPrompt

from shinka.ui import (
    console, phase_header, show_level_selector, show_choices,
    random_kaomoji,
)
from shinka.templates import (
    AESTHETICS, FONT_PAIRINGS, COLOR_PALETTES, TYPOGRAPHY_SCALES,
    ANIMATION_PRESETS, COMPONENT_PATTERNS, SECTION_TEMPLATES,
    TECH_STACKS, ANIMATION_LIBS,
)
from shinka.levels import LEVELS, get_all_level_summaries


class WizardAnswers:
    """Holds all answers from the wizard."""

    def __init__(self):
        # Phase 1 — Project Identity
        self.project_name: str = ""
        self.description: str = ""
        self.audience: str = ""
        self.goal: str = ""
        self.sections: list[str] = []
        self.level: int = 3

        # Phase 2 — Design Direction
        self.aesthetic: str = ""
        self.aesthetic_details: dict = {}
        self.reference_sites: str = ""
        self.font_pairing: str = ""
        self.font_details: dict = {}
        self.color_palette: str = ""
        self.color_details: dict = {}
        self.animation_intensity: str = ""
        self.animation_details: dict = {}

        # Phase 3 — Design Systems
        self.grid_system: str = ""
        self.typography_scale: str = ""
        self.typography_scale_details: dict = {}
        self.accessibility: str = ""
        self.component_patterns: list[str] = []

        # Phase 4 — Code References (auto-scraped)
        self.scrape_urls: list[str] = []
        self.scraped_data: str = ""
        self.code_snippets: str = ""
        self.effects_to_replicate: str = ""

        # Phase 5 — Custom Assets
        self.custom_colors: str = ""
        self.custom_fonts: str = ""
        self.custom_interactions: str = ""
        self.custom_assets_description: str = ""

        # Phase 6 — External Tools
        self.tech_stack: str = ""
        self.tech_stack_details: dict = {}
        self.animation_lib: str = ""
        self.smooth_scroll: str = ""
        self.three_d_elements: str = ""
        self.component_source: str = ""

        # Phase 7 — Frontier
        self.webgl_requirements: str = ""
        self.shader_effects: str = ""
        self.data_viz: str = ""
        self.procedural_animation: str = ""
        self.performance_budget: str = ""


def run_wizard() -> WizardAnswers:
    """Run the full interactive wizard. Returns collected answers."""
    answers = WizardAnswers()
    level_info = LEVELS

    # ── Level Selection ──────────────────────────────────────────────────
    show_level_selector(get_all_level_summaries())

    answers.level = IntPrompt.ask(
        f"  [magenta]›[/magenta] [bold]Choose your level[/bold]",
        choices=[str(i) for i in range(1, 8)],
        default=3,
    )
    selected_level = level_info[answers.level]
    console.print(
        f"\n  [green]✓[/green] [bold]{selected_level['name']}[/bold] — "
        f"{selected_level['tagline']}  {random_kaomoji('happy')}\n"
    )

    active_phases = selected_level["phases"]

    # ── Phase 1: Project Identity ────────────────────────────────────────
    if 1 in active_phases:
        phase_header(1, "Project Identity")

        answers.project_name = Prompt.ask("  [magenta]›[/magenta] Project name")
        answers.description = Prompt.ask("  [magenta]›[/magenta] What does this project do? (one line)")
        answers.audience = Prompt.ask("  [magenta]›[/magenta] Who is this for? (target audience)")
        answers.goal = Prompt.ask(
            "  [magenta]›[/magenta] Primary goal of this page",
            choices=["waitlist", "sales", "portfolio", "docs", "showcase", "other"],
            default="waitlist",
        )

        # Section selection
        console.print(f"\n  [bold cyan]Available sections:[/bold cyan]")
        section_keys = list(SECTION_TEMPLATES.keys())
        for i, key in enumerate(section_keys, 1):
            console.print(f"    [magenta]{i:2}.[/magenta] [bold]{key}[/bold] [dim]— {SECTION_TEMPLATES[key][:60]}...[/dim]")

        section_input = Prompt.ask(
            "\n  [magenta]›[/magenta] Pick sections (comma-separated numbers, e.g. 1,2,5,7)",
            default="1,2,5,7",
        )
        try:
            indices = [int(x.strip()) - 1 for x in section_input.split(",")]
            answers.sections = [section_keys[i] for i in indices if 0 <= i < len(section_keys)]
        except (ValueError, IndexError):
            answers.sections = ["hero", "features", "cta", "footer"]

        console.print(f"  [green]✓[/green] Sections: [bold]{', '.join(answers.sections)}[/bold]\n")

    # ── Phase 2: Design Direction ────────────────────────────────────────
    if 2 in active_phases:
        phase_header(2, "Design Direction")

        # Aesthetic
        show_choices("Visual Aesthetic:", {
            k: v["description"] for k, v in AESTHETICS.items()
        })
        answers.aesthetic = Prompt.ask(
            "  [magenta]›[/magenta] Choose aesthetic",
            choices=list(AESTHETICS.keys()),
            default="dark_tech",
        )
        answers.aesthetic_details = AESTHETICS[answers.aesthetic]

        # Reference sites
        answers.reference_sites = Prompt.ask(
            "  [magenta]›[/magenta] Any reference sites for inspiration? (URLs or names, or skip)",
            default="",
        )

        # Font pairing
        console.print(f"\n  [bold cyan]Font Pairings:[/bold cyan]")
        for key, val in FONT_PAIRINGS.items():
            console.print(
                f"    [magenta]›[/magenta] [bold]{key}[/bold] — "
                f"{val['heading']} + {val['body']} [dim]({val['note']})[/dim]"
            )
        answers.font_pairing = Prompt.ask(
            "\n  [magenta]›[/magenta] Choose font pairing",
            choices=list(FONT_PAIRINGS.keys()),
            default="tech_premium",
        )
        answers.font_details = FONT_PAIRINGS[answers.font_pairing]

        # Color palette
        console.print(f"\n  [bold cyan]Color Palettes:[/bold cyan]")
        for key, val in COLOR_PALETTES.items():
            console.print(
                f"    [magenta]›[/magenta] [bold]{key}[/bold] — "
                f"[dim]{val['mood']}[/dim]  accent: {val['accent']}"
            )
        answers.color_palette = Prompt.ask(
            "\n  [magenta]›[/magenta] Choose color palette",
            choices=list(COLOR_PALETTES.keys()),
            default="midnight_cyan",
        )
        answers.color_details = COLOR_PALETTES[answers.color_palette]

        # Animation
        console.print(f"\n  [bold cyan]Animation Intensity:[/bold cyan]")
        for key, val in ANIMATION_PRESETS.items():
            console.print(f"    [magenta]›[/magenta] [bold]{key}[/bold] — [dim]{val['description']}[/dim]")
        answers.animation_intensity = Prompt.ask(
            "\n  [magenta]›[/magenta] Animation level",
            choices=list(ANIMATION_PRESETS.keys()),
            default="moderate",
        )
        answers.animation_details = ANIMATION_PRESETS[answers.animation_intensity]

    # ── Phase 3: Design Systems ──────────────────────────────────────────
    if 3 in active_phases:
        phase_header(3, "Design Systems")

        # Grid
        answers.grid_system = Prompt.ask(
            "  [magenta]›[/magenta] Grid system",
            choices=["8-point", "4-point", "custom"],
            default="8-point",
        )

        # Typography scale
        console.print(f"\n  [bold cyan]Typography Scales:[/bold cyan]")
        for key, val in TYPOGRAPHY_SCALES.items():
            console.print(f"    [magenta]›[/magenta] [bold]{key}[/bold] — {val['name']} [dim]({val['feel']})[/dim]")
        answers.typography_scale = Prompt.ask(
            "\n  [magenta]›[/magenta] Typography scale",
            choices=list(TYPOGRAPHY_SCALES.keys()),
            default="major_third",
        )
        answers.typography_scale_details = TYPOGRAPHY_SCALES[answers.typography_scale]

        # Accessibility
        answers.accessibility = Prompt.ask(
            "  [magenta]›[/magenta] Accessibility level",
            choices=["wcag_aa", "wcag_aaa", "none"],
            default="wcag_aa",
        )

        # Component patterns
        console.print(f"\n  [bold cyan]Component Patterns (pick any):[/bold cyan]")
        pattern_keys = list(COMPONENT_PATTERNS.keys())
        for i, key in enumerate(pattern_keys, 1):
            console.print(f"    [magenta]{i:2}.[/magenta] [bold]{key}[/bold] [dim]— {COMPONENT_PATTERNS[key][:70]}...[/dim]")
        pattern_input = Prompt.ask(
            "\n  [magenta]›[/magenta] Patterns (comma-separated numbers, or skip)",
            default="",
        )
        if pattern_input.strip():
            try:
                indices = [int(x.strip()) - 1 for x in pattern_input.split(",")]
                answers.component_patterns = [pattern_keys[i] for i in indices if 0 <= i < len(pattern_keys)]
            except (ValueError, IndexError):
                answers.component_patterns = []

    # ── Phase 4: Code References ─────────────────────────────────────────
    if 4 in active_phases:
        phase_header(4, "Code References (The Cloner)")

        console.print("  [bold cyan]Drop URLs of sites you want to clone.[/bold cyan]")
        console.print("  [dim]Shinka will open a headless browser and auto-extract the HTML/CSS.[/dim]")
        console.print("  [dim]Enter one URL per line. Type 'done' when finished, or 'skip' to skip.[/dim]\n")

        urls = []
        while True:
            url_input = Prompt.ask("  [magenta]›[/magenta] URL", default="done")
            if url_input.lower() in ("done", "skip"):
                break
            url = url_input.strip()
            if not url.startswith("http"):
                url = "https://" + url
            urls.append(url)
            console.print(f"    [green]✓[/green] Added: [bold]{url}[/bold]")

        if urls:
            answers.scrape_urls = urls
            # Auto-scrape the sites
            from shinka.scraper import ensure_playwright, scrape_multiple_urls
            if ensure_playwright():
                console.print(f"\n  [cyan]Scraping {len(urls)} site(s)...[/cyan]  {random_kaomoji('thinking')}")
                answers.scraped_data = scrape_multiple_urls(urls)
            else:
                console.print(f"  [yellow]⚠[/yellow] Browser not available. You can paste code manually instead.")
                console.print("  [dim]Type 'done' when finished, or 'skip'.[/dim]\n")
                lines = []
                while True:
                    line = Prompt.ask("  [magenta]│[/magenta]", default="skip")
                    if line.lower() in ("done", "skip"):
                        break
                    lines.append(line)
                answers.code_snippets = "\n".join(lines) if lines else ""

        answers.effects_to_replicate = Prompt.ask(
            "\n  [magenta]›[/magenta] Specific effects to replicate? (describe or skip)",
            default="",
        )

    # ── Phase 5: Custom Assets ───────────────────────────────────────────
    if 5 in active_phases:
        phase_header(5, "Custom Assets & Brand")

        answers.custom_colors = Prompt.ask(
            "  [magenta]›[/magenta] Custom brand hex colors? (e.g. #ff6b35, #004e98 or skip)",
            default="",
        )
        answers.custom_fonts = Prompt.ask(
            "  [magenta]›[/magenta] Custom font URLs or names? (or skip)",
            default="",
        )
        answers.custom_interactions = Prompt.ask(
            "  [magenta]›[/magenta] Specific micro-interactions to implement? (or skip)",
            default="",
        )
        answers.custom_assets_description = Prompt.ask(
            "  [magenta]›[/magenta] Describe any custom SVG/illustration needs (or skip)",
            default="",
        )

    # ── Phase 6: External Tools ──────────────────────────────────────────
    if 6 in active_phases:
        phase_header(6, "Tech Stack & External Tools")

        show_choices("Tech Stack:", {
            k: f"{v['name']} — {v['description']}" for k, v in TECH_STACKS.items()
        })
        answers.tech_stack = Prompt.ask(
            "  [magenta]›[/magenta] Tech stack",
            choices=list(TECH_STACKS.keys()),
            default="html_css_js",
        )
        answers.tech_stack_details = TECH_STACKS[answers.tech_stack]

        show_choices("Animation Library:", {
            k: f"{v['name']} — {v['description']}" for k, v in ANIMATION_LIBS.items()
        })
        answers.animation_lib = Prompt.ask(
            "  [magenta]›[/magenta] Animation library",
            choices=list(ANIMATION_LIBS.keys()),
            default="css_only",
        )

        answers.smooth_scroll = Prompt.ask(
            "  [magenta]›[/magenta] Smooth scrolling",
            choices=["lenis", "native", "none"],
            default="native",
        )
        answers.three_d_elements = Prompt.ask(
            "  [magenta]›[/magenta] 3D elements?",
            choices=["threejs", "spline", "none"],
            default="none",
        )
        answers.component_source = Prompt.ask(
            "  [magenta]›[/magenta] Pre-built components?",
            choices=["shadcn", "radix", "daisyui", "custom", "none"],
            default="none",
        )

    # ── Phase 7: Frontier ────────────────────────────────────────────────
    if 7 in active_phases:
        phase_header(7, "The Frontier")

        answers.webgl_requirements = Prompt.ask(
            "  [magenta]›[/magenta] WebGL / canvas requirements? (describe or skip)",
            default="",
        )
        answers.shader_effects = Prompt.ask(
            "  [magenta]›[/magenta] Custom shader / GLSL effects? (describe or skip)",
            default="",
        )
        answers.data_viz = Prompt.ask(
            "  [magenta]›[/magenta] Real-time data visualizations? (describe or skip)",
            default="",
        )
        answers.procedural_animation = Prompt.ask(
            "  [magenta]›[/magenta] Procedural animation descriptions? (describe or skip)",
            default="",
        )
        answers.performance_budget = Prompt.ask(
            "  [magenta]›[/magenta] Performance budget? (e.g. '60fps, <3s LCP' or skip)",
            default="60fps, <3s LCP, <500KB JS",
        )

    return answers

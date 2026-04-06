"""
The 7 Levels of Frontend Design — level definitions, unlocked features,
and the knowledge that gets injected into prompts at each level.
"""

LEVELS = {
    1: {
        "name": "The Beginner",
        "tagline": "Basic prompting — describe what you want and hope for the best.",
        "description": (
            "You describe your project and desired sections. The prompt includes "
            "basic structure and the universal anti-AI-slop rules to avoid the worst "
            "generic outputs, but no deep design direction."
        ),
        "unlocks": [
            "Project identity & goals",
            "Page section selection",
            "Universal anti-AI-slop rules",
        ],
        "phases": [1],
    },
    2: {
        "name": "The Vocabulary Builder",
        "tagline": "Design vocabulary — reference real aesthetics and specific styles.",
        "description": (
            "You reference specific visual aesthetics, real-world inspiration sites, "
            "font choices, color moods, and animation intensity. Your prompts go "
            "from vague to specific."
        ),
        "unlocks": [
            "Visual aesthetic selection (dark tech, brutalist, etc.)",
            "Reference site inspiration",
            "Font pairing presets",
            "Color palette presets",
            "Animation intensity level",
        ],
        "phases": [1, 2],
    },
    3: {
        "name": "The Framework Master",
        "tagline": "Design systems — proper grids, scales, accessibility, and principles.",
        "description": (
            "You specify exact design system parameters: 8-point grid, golden ratio "
            "typography scale, WCAG-compliant contrast ratios, Gestalt principles. "
            "Your prompts become surgical."
        ),
        "unlocks": [
            "Grid system specification",
            "Typography scale (ratio-based)",
            "Accessibility requirements (WCAG AA/AAA)",
            "Responsive breakpoint strategy",
            "Component pattern selection",
        ],
        "phases": [1, 2, 3],
    },
    4: {
        "name": "The Cloner",
        "tagline": "Clone real code — stop guessing, start copying techniques.",
        "description": (
            "You paste real code snippets from sites you admire. The AI gets an "
            "exact implementation blueprint instead of guessing how effects work. "
            "Your sites stop looking 'AI-made'."
        ),
        "unlocks": [
            "Paste code snippets from reference sites",
            "Specify exact effects to replicate",
            "URL-based inspiration notes",
        ],
        "phases": [1, 2, 3, 4],
    },
    5: {
        "name": "The Customizer",
        "tagline": "Own the design — inject your brand identity and custom assets.",
        "description": (
            "You bring custom brand colors, fonts, SVG descriptions, micro-interactions "
            "that match YOUR product personality. The design stops being a clone and "
            "starts being yours."
        ),
        "unlocks": [
            "Custom brand hex colors",
            "Custom external font URLs",
            "SVG/Lottie animation descriptions",
            "Specific micro-interaction specs",
        ],
        "phases": [1, 2, 3, 4, 5],
    },
    6: {
        "name": "The Orchestrator",
        "tagline": "External tools — conduct an orchestra of specialized tools.",
        "description": (
            "You specify the exact tech stack, animation libraries, smooth scroll "
            "solution, 3D elements, and pre-built component sources. The AI becomes "
            "a conductor integrating multiple tools."
        ),
        "unlocks": [
            "Tech stack selection (Next.js, Vite, Astro, etc.)",
            "Animation library choice (GSAP, Framer Motion, etc.)",
            "Smooth scrolling solution (Lenis, native)",
            "3D elements (Three.js, Spline)",
            "Pre-built component sources",
        ],
        "phases": [1, 2, 3, 4, 5, 6],
    },
    7: {
        "name": "The Frontier",
        "tagline": "Push the edge — WebGL, shaders, procedural animation, real-time data.",
        "description": (
            "You define WebGL canvas requirements, custom GLSL shaders, real-time "
            "data visualizations, procedural animations, and performance budgets. "
            "Top 0.1% territory."
        ),
        "unlocks": [
            "WebGL / shader requirements",
            "Real-time data visualization specs",
            "Procedural animation descriptions",
            "Performance budget constraints",
            "Post-processing effects (bloom, grain, etc.)",
        ],
        "phases": [1, 2, 3, 4, 5, 6, 7],
    },
}


def get_level_summary(level: int) -> str:
    """Return a short string summarizing a level for display."""
    info = LEVELS[level]
    return f"Level {level}: {info['name']} — {info['tagline']}"


def get_all_level_summaries() -> list[str]:
    """Return summaries for all 7 levels."""
    return [get_level_summary(i) for i in range(1, 8)]

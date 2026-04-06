"""
Curated design knowledge, font pairings, color palettes, anti-AI-slop rules,
animation presets, and component pattern descriptions.
"""

# ── Anti-AI-Slop Rules ──────────────────────────────────────────────────────
# These are ALWAYS injected into every prompt regardless of level.
UNIVERSAL_RULES = [
    "NEVER use generic purple-to-blue gradients — they scream 'AI-generated'.",
    "NEVER use default browser fonts. Always specify a premium font stack.",
    "NEVER create centered-text-over-gradient hero sections — use asymmetric layouts.",
    "NEVER use placeholder stock-photo style imagery or generic icons.",
    "NEVER use equally-sized 3-column feature grids — vary card sizes and layouts.",
    "NEVER default to rounded-corner cards with drop shadows as the only visual element.",
    "DO use intentional, curated color palettes — not random CSS named colors.",
    "DO use proper visual hierarchy: one dominant element per section, clear reading flow.",
    "DO use generous whitespace — at minimum 80px vertical section padding.",
    "DO use micro-animations on interactive elements (hover, focus, active states).",
    "DO use a consistent spacing scale (multiples of 4px or 8px).",
    "DO use proper semantic HTML (header, main, section, article, footer).",
    "DO ensure all text passes WCAG AA contrast (4.5:1 for body, 3:1 for large text).",
    "DO make the design feel alive with subtle motion — not static and flat.",
    "DO use at least 2 font weights to establish hierarchy (e.g. 400 + 700).",
    "DO give every interactive element a visible hover/focus state.",
]

# ── Font Pairings ────────────────────────────────────────────────────────────
FONT_PAIRINGS = {
    "tech_premium": {
        "heading": "Inter",
        "body": "Inter",
        "mono": "JetBrains Mono",
        "note": "Clean, geometric, what Linear/Vercel use. Safe and premium.",
    },
    "editorial_bold": {
        "heading": "Playfair Display",
        "body": "Source Sans 3",
        "mono": "Fira Code",
        "note": "High contrast serif + clean sans. Great for storytelling pages.",
    },
    "modern_geometric": {
        "heading": "Outfit",
        "body": "Plus Jakarta Sans",
        "mono": "IBM Plex Mono",
        "note": "Contemporary geometric feel. Fresh and unique.",
    },
    "minimal_swiss": {
        "heading": "Space Grotesk",
        "body": "DM Sans",
        "mono": "DM Mono",
        "note": "Swiss-inspired minimalism. Refined and elegant.",
    },
    "expressive_display": {
        "heading": "Cabinet Grotesk",
        "body": "General Sans",
        "mono": "Fira Code",
        "note": "Bold display type with a friendly body. Great for SaaS.",
    },
    "classic_professional": {
        "heading": "Fraunces",
        "body": "Commissioner",
        "mono": "JetBrains Mono",
        "note": "Warm serif heading with clean sans body. Trustworthy.",
    },
    "brutalist_raw": {
        "heading": "Syne",
        "body": "Space Grotesk",
        "mono": "Space Mono",
        "note": "Experimental and raw. Great for creative/portfolio sites.",
    },
    "futuristic": {
        "heading": "Exo 2",
        "body": "Nunito Sans",
        "mono": "Source Code Pro",
        "note": "Sci-fi and futuristic feel. Good for tech products.",
    },
}

# ── Color Palettes ───────────────────────────────────────────────────────────
COLOR_PALETTES = {
    "midnight_cyan": {
        "bg": "#0a0a0f",
        "surface": "#12121a",
        "border": "#1e1e2e",
        "text": "#e4e4e7",
        "muted": "#71717a",
        "accent": "#06b6d4",
        "accent_hover": "#22d3ee",
        "gradient": "linear-gradient(135deg, #06b6d4, #8b5cf6)",
        "mood": "Dark tech — premium, sophisticated, modern",
    },
    "warm_ember": {
        "bg": "#0f0a07",
        "surface": "#1a1410",
        "border": "#2e241e",
        "text": "#f5f0eb",
        "muted": "#a39585",
        "accent": "#f59e0b",
        "accent_hover": "#fbbf24",
        "gradient": "linear-gradient(135deg, #f59e0b, #ef4444)",
        "mood": "Warm and bold — energetic, creative, attention-grabbing",
    },
    "forest_sage": {
        "bg": "#070f0a",
        "surface": "#101a14",
        "border": "#1e2e24",
        "text": "#ebf5f0",
        "muted": "#85a395",
        "accent": "#10b981",
        "accent_hover": "#34d399",
        "gradient": "linear-gradient(135deg, #10b981, #06b6d4)",
        "mood": "Natural and calm — sustainable, health, wellness",
    },
    "electric_violet": {
        "bg": "#0a070f",
        "surface": "#14101a",
        "border": "#241e2e",
        "text": "#f0ebf5",
        "muted": "#9585a3",
        "accent": "#a855f7",
        "accent_hover": "#c084fc",
        "gradient": "linear-gradient(135deg, #a855f7, #ec4899)",
        "mood": "Creative and vibrant — art, music, entertainment",
    },
    "arctic_ice": {
        "bg": "#f8fafc",
        "surface": "#ffffff",
        "border": "#e2e8f0",
        "text": "#0f172a",
        "muted": "#64748b",
        "accent": "#3b82f6",
        "accent_hover": "#60a5fa",
        "gradient": "linear-gradient(135deg, #3b82f6, #06b6d4)",
        "mood": "Clean light mode — professional, trustworthy, SaaS",
    },
    "rose_gold": {
        "bg": "#0f0a0b",
        "surface": "#1a1012",
        "border": "#2e1e20",
        "text": "#f5ebec",
        "muted": "#a38587",
        "accent": "#f43f5e",
        "accent_hover": "#fb7185",
        "gradient": "linear-gradient(135deg, #f43f5e, #f59e0b)",
        "mood": "Luxurious and bold — fashion, beauty, lifestyle",
    },
    "monochrome": {
        "bg": "#09090b",
        "surface": "#18181b",
        "border": "#27272a",
        "text": "#fafafa",
        "muted": "#71717a",
        "accent": "#fafafa",
        "accent_hover": "#d4d4d8",
        "gradient": "linear-gradient(135deg, #fafafa, #a1a1aa)",
        "mood": "Ultra-minimal — reduces everything to essentials",
    },
    "ocean_depth": {
        "bg": "#020617",
        "surface": "#0f172a",
        "border": "#1e293b",
        "text": "#f1f5f9",
        "muted": "#64748b",
        "accent": "#0ea5e9",
        "accent_hover": "#38bdf8",
        "gradient": "linear-gradient(135deg, #0ea5e9, #6366f1)",
        "mood": "Deep and immersive — analytics, data, dashboards",
    },
}

# ── Typography Scales ────────────────────────────────────────────────────────
TYPOGRAPHY_SCALES = {
    "minor_second": {"ratio": 1.067, "name": "Minor Second (1.067)", "feel": "Very tight, dense UIs"},
    "major_second": {"ratio": 1.125, "name": "Major Second (1.125)", "feel": "Compact, information-dense"},
    "minor_third": {"ratio": 1.200, "name": "Minor Third (1.200)", "feel": "Balanced, general purpose"},
    "major_third": {"ratio": 1.250, "name": "Major Third (1.250)", "feel": "Clear hierarchy, SaaS apps"},
    "perfect_fourth": {"ratio": 1.333, "name": "Perfect Fourth (1.333)", "feel": "Strong hierarchy, marketing"},
    "golden_ratio": {"ratio": 1.618, "name": "Golden Ratio (1.618)", "feel": "Dramatic, editorial, landing pages"},
}

# ── Animation Presets ────────────────────────────────────────────────────────
ANIMATION_PRESETS = {
    "none": {
        "description": "No animations. Static, fast-loading pages.",
        "css": "",
    },
    "subtle": {
        "description": "Gentle hover states and fade-ins. Professional and quiet.",
        "css": "transition: all 200ms ease; /* hover opacity, scale(1.02), translateY(-2px) */",
        "rules": [
            "Use 200ms ease transitions on hover states",
            "Fade-in elements with opacity 0→1 on scroll (use IntersectionObserver)",
            "Subtle translateY(-2px) lift on card hovers",
            "No transform scale larger than 1.02",
        ],
    },
    "moderate": {
        "description": "Visible animations that enhance without overwhelming.",
        "css": "transition: all 350ms cubic-bezier(0.4, 0, 0.2, 1);",
        "rules": [
            "Use 300-500ms cubic-bezier(0.4, 0, 0.2, 1) for all transitions",
            "Stagger child element fade-ins by 100ms each",
            "Use translateY(20px→0) + opacity for scroll-reveal",
            "Apply scale(1.03-1.05) on interactive card hovers",
            "Add smooth color transitions on button hovers",
            "Use CSS @keyframes for loading states and subtle loops",
        ],
    },
    "cinematic": {
        "description": "Dramatic scroll-driven motion. Award-winning feel.",
        "css": "transition: all 500ms cubic-bezier(0.16, 1, 0.3, 1);",
        "rules": [
            "Use 500-800ms cubic-bezier(0.16, 1, 0.3, 1) for smooth ease-out",
            "Implement scroll-triggered animations with staggered reveals",
            "Use parallax depth layers (translateZ or different scroll speeds)",
            "Apply magnetic cursor effects on buttons and links",
            "Use text reveal animations (clip-path or translateY line-by-line)",
            "Implement smooth page transitions between sections",
            "Add subtle grain/noise texture overlay for depth",
            "Consider Lenis or smooth-scrollbar for buttery scroll",
        ],
    },
}

# ── Visual Aesthetics ────────────────────────────────────────────────────────
AESTHETICS = {
    "dark_tech": {
        "name": "Dark Tech Premium",
        "description": "Linear, Vercel, Raycast — the gold standard of modern SaaS.",
        "references": ["Linear.app", "Vercel.com", "Raycast.com"],
        "key_traits": [
            "Near-black backgrounds (#0a0a0f range)",
            "High-contrast white text on dark surfaces",
            "Subtle border separators (1px, low opacity)",
            "Glassmorphic elements with backdrop-blur",
            "Monochromatic accent with one pop color",
            "Generous negative space",
        ],
    },
    "minimalist_clean": {
        "name": "Minimalist Clean",
        "description": "Apple, Stripe, Notion — elegant restraint.",
        "references": ["Apple.com", "Stripe.com", "Notion.so"],
        "key_traits": [
            "Light backgrounds or very dark with maximum whitespace",
            "Typography-driven design (large headings, small body)",
            "Minimal color — mostly grayscale with one accent",
            "No unnecessary decoration",
            "Focus on content and whitespace rhythm",
            "Sharp, precise spacing",
        ],
    },
    "brutalist": {
        "name": "Brutalist / Raw",
        "description": "Bloomberg, Figma Config — bold, unapologetic, experimental.",
        "references": ["Bloomberg.com", "Config.figma.com"],
        "key_traits": [
            "Oversized typography (often 80-200px headlines)",
            "Raw, unpolished aesthetic",
            "Bold color blocks and stark contrasts",
            "Visible grid/structural elements",
            "Monospace or display typefaces",
            "Intentionally 'imperfect' layouts",
        ],
    },
    "glassmorphic": {
        "name": "Glassmorphism",
        "description": "Frosted glass effects, layered depth, modern UI.",
        "references": ["Arc Browser", "macOS design language"],
        "key_traits": [
            "backdrop-filter: blur(12-20px)",
            "Semi-transparent backgrounds (rgba with 0.1-0.3 alpha)",
            "Subtle border with low-opacity white",
            "Layered depth through overlapping translucent elements",
            "Soft colored glows behind glass panels",
            "Works best on dark backgrounds with colored light sources",
        ],
    },
    "editorial": {
        "name": "Editorial / Magazine",
        "description": "New York Times, Medium — content-first, reading-focused.",
        "references": ["NYTimes.com", "Medium.com", "The Verge"],
        "key_traits": [
            "Strong typographic hierarchy with serif headings",
            "Column-based layouts inspired by print",
            "High-quality imagery as design elements",
            "Generous line-height (1.6-1.8) for readability",
            "Subtle color usage — mostly black/white with editorial accents",
            "Pull quotes and featured text blocks",
        ],
    },
    "playful": {
        "name": "Playful / Friendly",
        "description": "Slack, Mailchimp, Duolingo — warm, approachable, fun.",
        "references": ["Slack.com", "Mailchimp.com", "Duolingo.com"],
        "key_traits": [
            "Rounded corners and soft shapes",
            "Warm, saturated color palette",
            "Illustrated elements and custom icons",
            "Bouncy animations (spring physics)",
            "Friendly, conversational copy",
            "Generous padding and breathing room",
        ],
    },
    "neo_futuristic": {
        "name": "Neo-Futuristic",
        "description": "Cyberpunk, sci-fi — bleeding-edge and forward-looking.",
        "references": ["ui8.net", "Sci-fi movie interfaces"],
        "key_traits": [
            "Neon accents on deep dark backgrounds",
            "Grid lines and geometric patterns",
            "Monospace/tech typefaces",
            "Animated data visualizations",
            "HUD-style UI elements",
            "Scanline/glitch effects (sparingly)",
        ],
    },
}

# ── Component Patterns ───────────────────────────────────────────────────────
COMPONENT_PATTERNS = {
    "glassmorphic_cards": "Cards with backdrop-filter: blur(), semi-transparent backgrounds, subtle borders. Stack with z-index for depth.",
    "bento_grid": "Asymmetric grid layout where cards span different columns/rows. Pinterest/Apple style. Never uniform.",
    "floating_navbar": "Sticky navbar with backdrop-blur, shrinks on scroll, border appears on scroll. Fixed width with rounded corners.",
    "gradient_text": "Background-clip: text with animated or static gradients. Use for headings only, never body text.",
    "scroll_reveal": "Elements fade in + translateY as they enter viewport. Stagger children by 80-120ms. Use IntersectionObserver.",
    "magnetic_buttons": "Buttons that subtly follow cursor position within a radius. Satisfying hover effect.",
    "marquee_strip": "Infinite horizontal scroll of logos/text. CSS animation, duplicated content for seamless loop.",
    "spotlight_effect": "Radial gradient that follows mouse position on a card or section background.",
    "parallax_hero": "Hero with multiple depth layers moving at different speeds on scroll.",
    "text_reveal": "Headlines that animate in word-by-word or line-by-line using clip-path or translateY.",
}

# ── Page Sections ────────────────────────────────────────────────────────────
SECTION_TEMPLATES = {
    "hero": "Main landing section — should contain headline, subheadline, CTA button(s), and optionally a visual element (image, 3D, animation).",
    "features": "Showcase key product features. Use bento grid or asymmetric cards, NOT a boring 3-column grid.",
    "social_proof": "Testimonials, logos, stats. Use a marquee for logos, cards for testimonials, animated counters for stats.",
    "pricing": "Pricing tiers. Highlight the recommended plan. Use toggle for monthly/annual.",
    "cta": "Final call-to-action before footer. Strong headline, clear button, urgency element.",
    "faq": "Frequently asked questions. Use accordion/collapsible pattern.",
    "footer": "Site footer with links, newsletter signup, social icons. Keep minimal.",
    "waitlist": "Email capture section. Single input + button. Show social proof (X people signed up).",
    "showcase": "Product screenshots or demo. Use browser mockup frames or device frames.",
    "stats": "Key metrics with animated counters. Numbers should count up on scroll.",
    "how_it_works": "Step-by-step process. Use numbered cards or timeline layout.",
    "comparison": "Feature comparison table or before/after. Clear visual differentiation.",
}

# ── Tech Stacks ──────────────────────────────────────────────────────────────
TECH_STACKS = {
    "html_css_js": {
        "name": "Plain HTML + CSS + JS",
        "description": "No framework. Single index.html, style.css, script.js. Fastest to ship.",
        "best_for": "Simple landing pages, waitlist pages, one-pagers.",
    },
    "nextjs": {
        "name": "Next.js (React)",
        "description": "Full React framework with SSR/SSG, routing, optimized images.",
        "best_for": "Multi-page apps, SEO-critical sites, complex interactions.",
    },
    "vite_react": {
        "name": "Vite + React",
        "description": "Fast dev server, React components, no SSR overhead.",
        "best_for": "SPAs, dashboards, interactive apps.",
    },
    "astro": {
        "name": "Astro",
        "description": "Static-first, ships zero JS by default, island architecture.",
        "best_for": "Content sites, blogs, marketing pages with minimal JS.",
    },
    "vite_vanilla": {
        "name": "Vite (Vanilla)",
        "description": "Vite's dev server + build pipeline, but with plain HTML/CSS/JS.",
        "best_for": "When you want fast tooling but no framework overhead.",
    },
}

# ── Animation Libraries ──────────────────────────────────────────────────────
ANIMATION_LIBS = {
    "css_only": {
        "name": "CSS Only",
        "description": "Pure CSS animations and transitions. Zero JS overhead.",
    },
    "framer_motion": {
        "name": "Framer Motion",
        "description": "React-specific. Declarative animations, layout animations, gestures.",
    },
    "gsap": {
        "name": "GSAP",
        "description": "Industry-standard JS animation. Timeline sequencing, ScrollTrigger, physics.",
    },
    "animejs": {
        "name": "Anime.js",
        "description": "Lightweight JS animation. Good for SVG and DOM animations.",
    },
}

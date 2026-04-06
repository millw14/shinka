"""
Web scraper — fetches a URL with a headless browser, extracts the fully rendered
HTML, CSS (inline + external stylesheets), JavaScript, and key page sections.
Auto-installs Playwright browsers on first use.
"""
import re
import subprocess
import sys
import concurrent.futures
from typing import Optional

from shinka.ui import (
    console, animate_install_step, get_download_progress,
    random_kaomoji, SYM_WARN, SYM_CHECK, SYM_CROSS,
)
import platform


def _safe_evaluate(page, js_code: str, default=None, timeout: int = 8):
    """Run page.evaluate with a timeout to prevent hangs on complex sites."""
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(page.evaluate, js_code)
        try:
            return future.result(timeout=timeout)
        except (concurrent.futures.TimeoutError, Exception) as e:
            console.print(f"    [yellow]{SYM_WARN}[/yellow] [dim]Extraction timed out, skipping...[/dim]")
            return default if default is not None else ""


def ensure_playwright():
    """Install Playwright browsers if not already installed."""
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            try:
                browser = p.chromium.launch(headless=True)
                browser.close()
                return True
            except Exception:
                pass
    except ImportError:
        console.print(f"  [yellow]{SYM_WARN}[/yellow] Playwright not found. Installing...")
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "playwright"],
            capture_output=True, text=True,
        )

    console.print(f"  [cyan]Installing browser engine (one-time)...[/cyan]  {random_kaomoji('wait')}")
    animate_install_step("Downloading Chromium browser")
    result = subprocess.run(
        [sys.executable, "-m", "playwright", "install", "chromium"],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        console.print(f"  [red]{SYM_CROSS}[/red] Browser install failed.")
        console.print(f"  [dim]Error: {result.stderr[:200]}[/dim]")
        
        # System-specific manual instructions
        if platform.system().lower() == "windows":
            console.print("  [yellow]{SYM_WARN}[/yellow] Ensure you run the terminal as Administrator or run:")
            console.print("  [cyan]playwright install chromium[/cyan]")
        elif platform.system().lower() == "linux":
            console.print("  [yellow]{SYM_WARN}[/yellow] On Linux, you may need system dependencies. Run:")
            console.print("  [cyan]sudo playwright install-deps chromium[/cyan]")
            console.print("  [cyan]playwright install chromium[/cyan]")
        else:
            console.print("  [yellow]{SYM_WARN}[/yellow] Please run manually:")
            console.print("  [cyan]playwright install chromium[/cyan]")
            
        return False

    console.print(f"  [green]{SYM_CHECK}[/green] [bold]Browser engine ready[/bold]  {random_kaomoji('done')}")
    return True


def _clean_html(html: str, max_length: int = 15000) -> str:
    """Clean up extracted HTML — remove scripts, SVG paths, data attributes, etc."""
    # Remove script contents
    html = re.sub(r'<script[^>]*>[\s\S]*?</script>', '', html, flags=re.IGNORECASE)
    # Remove noscript
    html = re.sub(r'<noscript[^>]*>[\s\S]*?</noscript>', '', html, flags=re.IGNORECASE)
    # Remove inline event handlers
    html = re.sub(r'\s+on\w+="[^"]*"', '', html)
    # Remove data-* attributes (noisy)
    html = re.sub(r'\s+data-[\w-]+="[^"]*"', '', html)
    # Remove long SVG paths (keep SVG structure)
    html = re.sub(r'\sd="[^"]{100,}"', ' d="..."', html)
    # Remove base64 images
    html = re.sub(r'src="data:image[^"]{50,}"', 'src="[base64-image]"', html)
    # Remove srcset
    html = re.sub(r'\s+srcset="[^"]*"', '', html)
    # Remove excessive whitespace
    html = re.sub(r'\n\s*\n\s*\n', '\n\n', html)
    # Remove empty class attributes
    html = re.sub(r'\s+class=""', '', html)
    # Remove style attributes that are just display/visibility
    html = re.sub(r'\s+style="(display:\s*none|visibility:\s*hidden)[^"]*"', '', html)

    if len(html) > max_length:
        html = html[:max_length] + "\n\n<!-- ... truncated for brevity -->"

    return html.strip()


def _clean_css(css: str, max_length: int = 10000) -> str:
    """Clean up CSS — remove sourcemaps, minification artifacts."""
    # Remove source map references
    css = re.sub(r'/\*#\s*sourceMappingURL=[^*]*\*/', '', css)
    # Try to add newlines after } for readability if it's minified
    if css.count('\n') < css.count('}') / 3:
        css = re.sub(r'}', '}\n', css)
        css = re.sub(r'{', ' {\n  ', css)
        css = re.sub(r';', ';\n  ', css)
    # Remove excessive whitespace
    css = re.sub(r'\n\s*\n\s*\n', '\n\n', css)

    if len(css) > max_length:
        css = css[:max_length] + "\n\n/* ... truncated */"

    return css.strip()


def _extract_section(page, selector: str, label: str) -> Optional[str]:
    """Try to extract a section by CSS selector, return cleaned HTML or None."""
    try:
        element = page.query_selector(selector)
        if element:
            html = element.evaluate("el => el.outerHTML", timeout=5000)
            cleaned = _clean_html(html, max_length=5000)
            if len(cleaned) > 50:
                return f"<!-- === {label} === -->\n{cleaned}"
    except Exception:
        pass
    return None


def scrape_url(url: str) -> dict:
    """
    Scrape a URL using a headless browser.
    Extracts: HTML sections, all CSS (inline + external), JS framework info,
    fonts, colors, animations, and page metadata.
    """
    from playwright.sync_api import sync_playwright

    console.print(f"\n  [cyan]Opening headless browser...[/cyan]  {random_kaomoji('thinking')}")

    result = {
        "url": url,
        "title": "",
        "sections": {},
        "styles_inline": "",
        "styles_external": [],
        "styles_computed": {},
        "js_frameworks": [],
        "js_animations": "",
        "fonts_used": [],
        "colors_detected": [],
        "meta": {},
        "full_html": "",
    }

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1440, "height": 900},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        )
        page = context.new_page()

        # Collect external resource URLs as they load
        external_css_urls = []
        external_js_urls = []

        def handle_response(response):
            ct = response.headers.get("content-type", "")
            url_str = response.url
            if "css" in ct or url_str.endswith(".css"):
                external_css_urls.append(url_str)
            if "javascript" in ct or url_str.endswith(".js"):
                external_js_urls.append(url_str)

        page.on("response", handle_response)

        try:
            # Navigate — use domcontentloaded instead of networkidle (much faster)
            console.print(f"  [magenta]⟳[/magenta] [cyan]Loading {url[:50]}...[/cyan]")
            page.goto(url, wait_until="domcontentloaded", timeout=20000)
            # Give JS a few seconds to render
            page.wait_for_timeout(3000)

            result["title"] = page.title()
            console.print(f"  [green]✓[/green] [bold]Loaded: {result['title'][:60]}[/bold]")

            # ── Meta tags ────────────────────────────────────────────────
            console.print(f"  [magenta]⟳[/magenta] [cyan]Extracting metadata...[/cyan]")
            result["meta"] = _safe_evaluate(page, """() => {
                const meta = {};
                const desc = document.querySelector('meta[name="description"]');
                if (desc) meta.description = desc.content;
                const theme = document.querySelector('meta[name="theme-color"]');
                if (theme) meta.themeColor = theme.content;
                const og = document.querySelector('meta[property="og:image"]');
                if (og) meta.ogImage = og.content;
                const viewport = document.querySelector('meta[name="viewport"]');
                if (viewport) meta.viewport = viewport.content;
                return meta;
            }""", default={})

            # ── Inline styles ────────────────────────────────────────────
            console.print(f"  [magenta]⟳[/magenta] [cyan]Extracting inline CSS...[/cyan]")
            result["styles_inline"] = _safe_evaluate(page, """() => {
                const results = [];
                document.querySelectorAll('style').forEach(s => {
                    const text = s.textContent.trim();
                    if (text.length > 0 && text.length < 8000) {
                        results.push(text);
                    }
                });
                // Limit cssRules iteration to avoid hangs
                let ruleCount = 0;
                const customProps = [];
                for (const sheet of document.styleSheets) {
                    try {
                        for (const rule of sheet.cssRules) {
                            if (++ruleCount > 2000) break;
                            if (rule.selectorText && (
                                rule.selectorText.includes(':root') ||
                                rule.selectorText === 'html' ||
                                rule.selectorText === 'body'
                            )) {
                                customProps.push(rule.cssText);
                            }
                        }
                    } catch (e) {}
                    if (ruleCount > 2000) break;
                }
                if (customProps.length > 0) {
                    results.push('/* === Root / Body Styles === */');
                    results.push(customProps.join('\\n'));
                }
                return results.join('\\n\\n');
            }""", default="")

            # ── External CSS ─────────────────────────────────────────────
            console.print(f"  [magenta]⟳[/magenta] [cyan]Fetching external CSS ({len(external_css_urls)} files)...[/cyan]")
            for css_url in external_css_urls[:5]:  # Max 5 stylesheets
                try:
                    css_response = context.request.get(css_url, timeout=5000)
                    if css_response.ok:
                        css_text = css_response.text()
                        cleaned = _clean_css(css_text, max_length=8000)
                        if len(cleaned) > 100:
                            result["styles_external"].append({
                                "url": css_url,
                                "css": cleaned,
                            })
                            console.print(f"    [green]✓[/green] CSS: [dim]{css_url[:70]}[/dim]")
                except Exception:
                    pass

            # ── Detect frameworks & animation libraries ──────────────────
            console.print(f"  [magenta]⟳[/magenta] [cyan]Detecting frameworks & animations...[/cyan]")
            result["js_frameworks"] = _safe_evaluate(page, """() => {
                const detected = [];
                try { if (window.React || document.querySelector('[data-reactroot]') || document.querySelector('#__next')) detected.push('React / Next.js'); } catch(e){}
                try { if (window.Vue || document.querySelector('[data-v-]')) detected.push('Vue.js'); } catch(e){}
                try { if (window.__svelte_meta || document.querySelector('[class*="svelte-"]')) detected.push('Svelte'); } catch(e){}
                try { if (window.gsap || window.TweenMax || window.TweenLite) detected.push('GSAP'); } catch(e){}
                try { if (document.querySelector('[data-framer-component-type]') || window.__framer_importFromPackage) detected.push('Framer Motion'); } catch(e){}
                try { if (window.THREE) detected.push('Three.js'); } catch(e){}
                try { if (window.Lenis || document.querySelector('[data-lenis-prevent]')) detected.push('Lenis (smooth scroll)'); } catch(e){}
                try { if (window.LocomotiveScroll) detected.push('Locomotive Scroll'); } catch(e){}
                try { if (document.querySelector('canvas')) detected.push('Canvas/WebGL'); } catch(e){}
                try { if (document.querySelector('.swiper') || window.Swiper) detected.push('Swiper'); } catch(e){}
                try { if (window.anime) detected.push('Anime.js'); } catch(e){}
                return detected;
            }""", default=[])

            if result["js_frameworks"]:
                for fw in result["js_frameworks"]:
                    console.print(f"    [green]✓[/green] Detected: [bold]{fw}[/bold]")

            # ── Extract animation CSS ────────────────────────────────────
            result["js_animations"] = _safe_evaluate(page, """() => {
                const animations = [];
                let count = 0;
                for (const sheet of document.styleSheets) {
                    try {
                        for (const rule of sheet.cssRules) {
                            if (++count > 2000) break;
                            if (rule.type === CSSRule.KEYFRAMES_RULE) {
                                animations.push(rule.cssText);
                            }
                            if (rule.style) {
                                const anim = rule.style.animation || rule.style.animationName;
                                const trans = rule.style.transition;
                                if ((anim && anim !== 'none') || (trans && trans !== 'none' && trans.length > 10)) {
                                    animations.push(rule.cssText);
                                }
                            }
                        }
                    } catch (e) {}
                    if (count > 2000) break;
                }
                return animations.slice(0, 50).join('\\n\\n');
            }""", default="")

            # ── Detect fonts ─────────────────────────────────────────────
            console.print(f"  [magenta]⟳[/magenta] [cyan]Detecting fonts & colors...[/cyan]")
            result["fonts_used"] = _safe_evaluate(page, """() => {
                const fonts = new Set();
                document.querySelectorAll('link[href*="fonts"]').forEach(l => fonts.add(l.href));
                ['h1','h2','h3','p','body','nav','a','button'].forEach(tag => {
                    try {
                        const el = document.querySelector(tag);
                        if (el) {
                            const font = getComputedStyle(el).fontFamily.split(',')[0].trim().replace(/['"]/g, '');
                            fonts.add(font);
                        }
                    } catch(e) {}
                });
                return [...fonts].slice(0, 10);
            }""", default=[])

            # ── Detect colors ────────────────────────────────────────────
            result["colors_detected"] = _safe_evaluate(page, """() => {
                const colors = new Set();
                ['body','main','header','nav','h1','h2','p','a','button','footer','section'].forEach(tag => {
                    try {
                        const el = document.querySelector(tag);
                        if (el) {
                            const s = getComputedStyle(el);
                            colors.add('bg:' + s.backgroundColor);
                            colors.add('text:' + s.color);
                        }
                    } catch(e) {}
                });
                return [...colors].slice(0, 20);
            }""", default=[])

            # ── Extract page sections ────────────────────────────────────
            console.print(f"  [magenta]⟳[/magenta] [cyan]Extracting page sections...[/cyan]")
            section_selectors = {
                "navbar": [
                    "nav", "header nav", "[role='navigation']",
                    "header", ".navbar", ".nav", "#navbar",
                    "[class*='nav']", "[class*='header']",
                ],
                "hero": [
                    ".hero", "#hero", "[class*='hero']", "[class*='banner']",
                    "section:first-of-type",
                    "main > section:first-child", "main > div:first-child",
                ],
                "features": [
                    "[class*='feature']", "[class*='benefit']",
                    "#features", ".features",
                    "section:nth-of-type(2)", "main > section:nth-child(2)",
                ],
                "social_proof": [
                    "[class*='testimonial']", "[class*='social']",
                    "[class*='logo']", "[class*='trust']",
                    "[class*='client']", "[class*='partner']",
                ],
                "cta": [
                    "[class*='cta']", "[class*='call-to-action']",
                    "[class*='signup']", "[class*='waitlist']",
                ],
                "footer": [
                    "footer", "[role='contentinfo']",
                    ".footer", "#footer", "[class*='footer']",
                ],
            }

            for section_name, selectors in section_selectors.items():
                for selector in selectors:
                    extracted = _extract_section(page, selector, section_name)
                    if extracted:
                        result["sections"][section_name] = extracted
                        console.print(f"    [green]✓[/green] Found: [bold]{section_name}[/bold]")
                        break

            # Full HTML fallback
            if len(result["sections"]) < 2:
                console.print(f"  [yellow]⚠[/yellow] Few sections detected, grabbing full page...")
                body_html = page.evaluate("() => document.body.outerHTML")
                result["full_html"] = _clean_html(body_html, max_length=12000)

        except Exception as e:
            console.print(f"  [red]✗[/red] Scrape error: {e}")
        finally:
            browser.close()

    # Summary
    section_count = len(result["sections"])
    css_count = len(result["styles_external"])
    fw_count = len(result["js_frameworks"])
    console.print(
        f"\n  [green]✓[/green] [bold]Scraped {section_count} sections, "
        f"{css_count} stylesheets, {fw_count} frameworks[/bold]  "
        f"{random_kaomoji('done')}"
    )

    return result


def format_scraped_data(data: dict) -> str:
    """Format all scraped data into comprehensive code blocks for the prompt."""
    parts = []

    parts.append(f"## Cloned from: {data['url']}")
    parts.append(f"**Page Title:** {data['title']}")

    # Meta
    if data.get("meta"):
        meta = data["meta"]
        if meta.get("description"):
            parts.append(f"**Description:** {meta['description']}")
        if meta.get("themeColor"):
            parts.append(f"**Theme Color:** {meta['themeColor']}")

    # Detected tech
    if data.get("js_frameworks"):
        parts.append(f"\n**Detected Tech:** {', '.join(data['js_frameworks'])}")

    # Fonts
    if data.get("fonts_used"):
        parts.append(f"**Fonts:** {', '.join(data['fonts_used'])}")

    # Colors
    if data.get("colors_detected"):
        parts.append(f"\n**Colors detected:**")
        for c in data["colors_detected"]:
            parts.append(f"- `{c}`")

    # ── Inline CSS ───────────────────────────────────────────────────────
    if data.get("styles_inline"):
        parts.append("\n### Inline Styles & CSS Variables")
        parts.append("```css")
        parts.append(data["styles_inline"][:6000])
        parts.append("```")

    # ── External CSS ─────────────────────────────────────────────────────
    if data.get("styles_external"):
        parts.append(f"\n### External Stylesheets ({len(data['styles_external'])} files)")
        for sheet in data["styles_external"]:
            parts.append(f"\n#### `{sheet['url'].split('/')[-1][:60]}`")
            parts.append("```css")
            parts.append(sheet["css"])
            parts.append("```")

    # ── Animation CSS ────────────────────────────────────────────────────
    if data.get("js_animations"):
        parts.append("\n### Animations & Transitions")
        parts.append("Replicate these exact animation patterns:")
        parts.append("```css")
        parts.append(data["js_animations"][:4000])
        parts.append("```")

    # ── HTML Sections ────────────────────────────────────────────────────
    if data.get("sections"):
        parts.append("\n### HTML Sections")
        parts.append("Replicate these layout patterns with our branding:")
        for name, html in data["sections"].items():
            parts.append(f"\n#### {name.replace('_', ' ').title()}")
            parts.append(f"```html\n{html}\n```")

    # Full HTML fallback
    if data.get("full_html") and not data.get("sections"):
        parts.append("\n### Full Page HTML")
        parts.append(f"```html\n{data['full_html']}\n```")

    return "\n".join(parts)


def scrape_multiple_urls(urls: list[str]) -> str:
    """Scrape multiple URLs and combine the results."""
    all_results = []

    for i, url in enumerate(urls, 1):
        console.print(f"\n  [magenta]({i}/{len(urls)})[/magenta] Scraping [bold]{url}[/bold]")
        data = scrape_url(url)
        formatted = format_scraped_data(data)
        all_results.append(formatted)

    return "\n\n---\n\n".join(all_results)

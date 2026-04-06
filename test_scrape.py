"""Quick scraper test — output to file."""
import sys
sys.stdout.reconfigure(line_buffering=True)

print("Step 1: Importing playwright...")
from playwright.sync_api import sync_playwright

print("Step 2: Starting...")
with sync_playwright() as p:
    print("Step 3: Launching browser...")
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    
    print("Step 4: Navigating to artemshcherban.com...")
    try:
        page.goto("https://artemshcherban.com/", wait_until="domcontentloaded", timeout=15000)
    except Exception as e:
        print(f"Navigation error (continuing anyway): {e}")
    
    print("Step 5: Waiting 3s for JS...")
    page.wait_for_timeout(3000)
    
    title = page.title()
    print(f"Step 6: Title = {title}")
    
    # Get body length
    body_len = page.evaluate("() => document.body ? document.body.outerHTML.length : 0")
    print(f"Step 7: Body HTML length = {body_len}")
    
    # Get frameworks
    print("Step 8: Detecting frameworks...")
    frameworks = page.evaluate("""() => {
        const d = [];
        try { if (window.gsap) d.push('GSAP'); } catch(e){}
        try { if (window.THREE) d.push('Three.js'); } catch(e){}
        try { if (document.querySelector('canvas')) d.push('Canvas'); } catch(e){}
        try { if (window.React || document.querySelector('#__next')) d.push('Next.js'); } catch(e){}
        return d;
    }""")
    print(f"Step 9: Frameworks = {frameworks}")
    
    # Get body snippet
    snippet = page.evaluate("() => document.body ? document.body.outerHTML.substring(0, 500) : 'empty'")
    print(f"Step 10: Body snippet:\n{snippet}")
    
    browser.close()
    print("DONE!")

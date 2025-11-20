#!/usr/bin/env python3
"""
Test if the site loads properly with Playwright
"""

from playwright.sync_api import sync_playwright
import sys

def test_site():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Collect console messages
        console_messages = []
        page.on("console", lambda msg: console_messages.append(f"{msg.type}: {msg.text}"))

        # Navigate to local site
        try:
            page.goto("http://localhost:8000", wait_until="networkidle", timeout=10000)

            # Get page title
            title = page.title()
            print(f"✓ Page loaded: {title}")

            # Check if CSS loaded
            css_link = page.query_selector('link[href="css/site.css"]')
            print(f"✓ CSS link found: {css_link is not None}")

            # Check computed styles on body
            body = page.query_selector("body")
            if body:
                font_family = page.evaluate("element => window.getComputedStyle(element).fontFamily", body)
                bg_color = page.evaluate("element => window.getComputedStyle(element).backgroundColor", body)
                print(f"✓ Body font: {font_family}")
                print(f"✓ Body background: {bg_color}")

            # Check for images
            images = page.query_selector_all("img")
            local_images = sum(1 for img in images if "images/" in page.evaluate("el => el.src", img))
            print(f"✓ Found {len(images)} images, {local_images} are local")

            # Check for errors
            errors = [msg for msg in console_messages if msg.startswith("error")]
            if errors:
                print(f"\n⚠ Console errors found:")
                for error in errors[:5]:
                    print(f"  {error}")
            else:
                print("\n✅ No console errors!")

            # Take screenshot
            page.screenshot(path="screenshot.png")
            print("\n✓ Screenshot saved to screenshot.png")

        except Exception as e:
            print(f"✗ Error: {e}")
            sys.exit(1)
        finally:
            browser.close()

if __name__ == "__main__":
    test_site()

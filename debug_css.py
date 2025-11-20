#!/usr/bin/env python3
"""
Debug CSS loading issues
"""

from playwright.sync_api import sync_playwright

def debug_css():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Track network requests
        requests = []
        page.on("request", lambda request: requests.append({
            "url": request.url,
            "type": request.resource_type
        }))

        # Navigate
        page.goto("http://localhost:8000", wait_until="networkidle", timeout=10000)

        # Check all CSS files loaded
        css_requests = [r for r in requests if r["type"] == "stylesheet"]
        print(f"CSS files loaded ({len(css_requests)}):")
        for r in css_requests:
            print(f"  {r['url']}")

        # Check if site.css content is actually applied
        print("\nChecking if CSS rules exist:")

        # Try to find a specific Squarespace class style
        result = page.evaluate("""() => {
            const sheets = Array.from(document.styleSheets);
            let foundRules = 0;
            let totalRules = 0;

            for (const sheet of sheets) {
                try {
                    const rules = Array.from(sheet.cssRules || []);
                    totalRules += rules.length;

                    // Look for Squarespace-specific rules
                    const sqsRules = rules.filter(rule =>
                        rule.selectorText && rule.selectorText.includes('sqs-')
                    );
                    foundRules += sqsRules.length;

                    if (sqsRules.length > 0) {
                        console.log(`Sheet ${sheet.href || 'inline'}: ${sqsRules.length} sqs- rules`);
                    }
                } catch(e) {
                    console.log(`Cannot access sheet: ${e.message}`);
                }
            }

            return {foundRules, totalRules, sheetCount: sheets.length};
        }""")

        print(f"  Total stylesheets: {result['sheetCount']}")
        print(f"  Total CSS rules: {result['totalRules']}")
        print(f"  Squarespace rules found: {result['foundRules']}")

        # Check specific element styling
        print("\nChecking header element:")
        header = page.query_selector(".header")
        if header:
            styles = page.evaluate("""(el) => {
                const computed = window.getComputedStyle(el);
                return {
                    display: computed.display,
                    position: computed.position,
                    background: computed.backgroundColor,
                    padding: computed.padding
                };
            }""", header)
            print(f"  Display: {styles['display']}")
            print(f"  Position: {styles['position']}")
            print(f"  Background: {styles['background']}")
            print(f"  Padding: {styles['padding']}")
        else:
            print("  .header element not found!")

        browser.close()

if __name__ == "__main__":
    debug_css()

#!/usr/bin/env python3
"""
CAREFUL removal of Squarespace dependencies - line by line approach
"""

import os
from pathlib import Path

def clean_html_carefully(filepath):
    """Remove only specific Squarespace script tags - very carefully."""

    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    original_count = len(lines)
    cleaned_lines = []
    skip_until_close = False
    skip_context_block = False
    context_depth = 0

    for i, line in enumerate(lines):
        # Skip "This is Squarespace" comment
        if '<!-- This is Squarespace. -->' in line:
            continue

        # Skip polyfiller scripts
        if '@sqs/polyfiller' in line and '<script' in line:
            continue

        # Skip SQUARESPACE_ROLLUPS initialization
        if 'SQUARESPACE_ROLLUPS = {}' in line:
            continue

        # Skip rollup function definitions and script loads
        if '(function(rollups, name)' in line or 'SQUARESPACE_ROLLUPS' in line:
            if '<script' in line:
                skip_until_close = True
                continue

        if skip_until_close:
            if '</script>' in line:
                skip_until_close = False
            continue

        # Skip individual Squarespace script tags
        if 'assets.squarespace.com/universal/scripts-compressed' in line:
            continue

        # Handle Static.SQUARESPACE_CONTEXT carefully
        if 'Static = window.Static' in line and 'SQUARESPACE_CONTEXT' in line:
            skip_context_block = True
            context_depth = 0
            continue

        if skip_context_block:
            # Count braces to know when the object ends
            context_depth += line.count('{') - line.count('}')
            if ';</script>' in line and context_depth <= 0:
                skip_context_block = False
            continue

        # Skip component definition links
        if 'definitions.sqspcdn.com' in line:
            continue

        # Replace Squarespace CSS with local
        if 'static1.squarespace.com/static/versioned-site-css' in line and 'site.css' in line:
            cleaned_lines.append('    <link rel="stylesheet" href="css/site.css">\n')
            continue

        # Skip cookie preferences getter
        if 'data-sqs-type="cookiepreferencesgetter"' in line:
            skip_until_close = True
            continue

        # Skip site-bundle.js
        if 'site-bundle' in line and '.js' in line:
            continue

        # Skip BeyondSpace - but keep our custom scripts
        if 'beyondspace' in line and ('cdn.jsdelivr.net' in line or 'BeyondspaceStudio' in line):
            continue

        # Keep everything else
        cleaned_lines.append(line)

    # Add mobile menu script before </body>
    final_lines = []
    for line in cleaned_lines:
        if '</body>' in line:
            final_lines.append('<script src="js/mobile-menu.js"></script>\n')
        final_lines.append(line)

    # Only write if we actually removed something
    if len(final_lines) < original_count:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(final_lines)
        return True, original_count, len(final_lines)
    return False, original_count, len(final_lines)

def main():
    """Process all HTML files."""

    script_dir = Path(__file__).parent
    os.chdir(script_dir)

    # Download CSS first
    print("Downloading Squarespace CSS...")
    os.system('curl -s "https://static1.squarespace.com/static/vta/5c5a519771c10ba3470d8101/versioned-assets/1763142521180-7KZ6ARD8802Y7ZJ2R6XP/static.css" -o css/site.css')

    # Create mobile menu JS
    print("Creating mobile menu JavaScript...")
    with open('js/mobile-menu.js', 'w') as f:
        f.write('''/**
 * Mobile Menu Toggle
 */
(function() {
    'use strict';

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    function init() {
        const burger = document.querySelector('.header-burger');
        const mobileOverlay = document.querySelector('.header-menu');

        if (!burger || !mobileOverlay) return;

        burger.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            mobileOverlay.classList.toggle('header-menu--active');
            document.body.classList.toggle('header-menu-open');
        });

        document.addEventListener('click', function(e) {
            if (mobileOverlay.classList.contains('header-menu--active')) {
                if (!mobileOverlay.contains(e.target) && !burger.contains(e.target)) {
                    mobileOverlay.classList.remove('header-menu--active');
                    document.body.classList.remove('header-menu-open');
                }
            }
        });

        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && mobileOverlay.classList.contains('header-menu--active')) {
                mobileOverlay.classList.remove('header-menu--active');
                document.body.classList.remove('header-menu-open');
            }
        });
    }
})();
''')

    html_files = list(Path('.').rglob('*.html'))

    print(f"\nProcessing {len(html_files)} HTML files...")

    modified_count = 0
    total_lines_removed = 0

    for filepath in html_files:
        try:
            modified, before, after = clean_html_carefully(filepath)
            if modified:
                modified_count += 1
                removed = before - after
                total_lines_removed += removed
                print(f"✓ {filepath}: {before} → {after} lines ({removed} removed)")
        except Exception as e:
            print(f"✗ Error in {filepath}: {e}")

    print(f"\n✅ Done!")
    print(f"Modified: {modified_count}/{len(html_files)} files")
    print(f"Total lines removed: {total_lines_removed}")

if __name__ == '__main__':
    main()

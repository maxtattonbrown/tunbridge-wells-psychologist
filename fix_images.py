#!/usr/bin/env python3
"""
Download all Squarespace CDN images and update HTML to use local copies.
"""

import os
import re
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

def download_image(url, save_dir):
    """Download an image from URL and return local path."""
    try:
        # Parse URL to get filename
        parsed = urlparse(url)
        # Remove query parameters and get basename
        filename = os.path.basename(parsed.path.split('?')[0])

        # Create save directory if needed
        save_dir.mkdir(parents=True, exist_ok=True)

        # Full save path
        save_path = save_dir / filename

        # Skip if already downloaded
        if save_path.exists():
            print(f"  ✓ Already have: {filename}")
            return str(save_path)

        # Download using curl (handles SSL better than Python)
        print(f"  Downloading: {filename}...")
        result = os.system(f'curl -s "{url}" -o "{save_path}"')

        if result == 0 and save_path.exists() and save_path.stat().st_size > 0:
            print(f"  ✓ Saved: {filename}")
            return str(save_path)
        else:
            print(f"  ✗ Failed to download {filename}")
            if save_path.exists():
                save_path.unlink()
            return None

    except Exception as e:
        print(f"  ✗ Error downloading {url}: {e}")
        return None

def process_html_file(filepath, images_dir):
    """Process a single HTML file - download images and update URLs."""

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all Squarespace CDN image URLs
    image_pattern = r'src="(https://images\.squarespace-cdn\.com/[^"]+)"'
    matches = re.findall(image_pattern, content)

    if not matches:
        return False

    print(f"\nProcessing {filepath}...")
    print(f"Found {len(matches)} external images")

    modified = False
    for url in matches:
        # Download image
        local_path = download_image(url, images_dir)

        if local_path:
            # Convert to relative path from HTML file
            rel_path = os.path.relpath(local_path, os.path.dirname(filepath))

            # Replace in content
            content = content.replace(f'src="{url}"', f'src="{rel_path}"')
            modified = True

    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True

    return False

def main():
    """Process all HTML files."""

    script_dir = Path(__file__).parent
    os.chdir(script_dir)

    images_dir = Path('images')

    # Find all HTML files
    html_files = list(Path('.').rglob('*.html'))

    print(f"Found {len(html_files)} HTML files")

    modified_count = 0
    for filepath in html_files:
        if process_html_file(filepath, images_dir):
            modified_count += 1

    print(f"\n✅ Done!")
    print(f"Modified {modified_count} files")
    print(f"Images saved to: {images_dir}/")

if __name__ == '__main__':
    main()

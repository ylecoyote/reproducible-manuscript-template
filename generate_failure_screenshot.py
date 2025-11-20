#!/usr/bin/env python3
"""
Generate a screenshot showing verification failure for documentation.
This temporarily modifies numerical_claims.yaml, runs verification, and captures the output.
"""

import subprocess
import yaml
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import shutil

# Paths
YAML_PATH = Path("numerical_claims.yaml")
BACKUP_PATH = Path("numerical_claims.yaml.backup")
OUTPUT_IMAGE = Path("docs/assets/failure_screenshot.png")

# Terminal colors (RGB approximations)
COLORS = {
    'reset': (200, 200, 200),
    'red': (255, 85, 85),
    'green': (85, 255, 85),
    'yellow': (255, 255, 85),
    'blue': (85, 170, 255),
    'gray': (150, 150, 150),
    'white': (255, 255, 255),
}

def backup_yaml():
    """Backup current YAML file"""
    shutil.copy(YAML_PATH, BACKUP_PATH)

def restore_yaml():
    """Restore original YAML file"""
    shutil.move(BACKUP_PATH, YAML_PATH)

def create_failing_yaml():
    """Modify YAML to cause verification failure"""
    with open(YAML_PATH) as f:
        data = yaml.safe_load(f)

    # Change the expected value to cause failure
    data['results']['experiment_a']['mean_efficiency'] = 0.950  # Wrong value

    with open(YAML_PATH, 'w') as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False)

def run_verification():
    """Run verification and capture output"""
    result = subprocess.run(
        ['python3', 'verify_manuscript.py'],
        capture_output=True,
        text=True
    )
    return result.stdout + result.stderr

def strip_ansi(text):
    """Remove ANSI escape codes from text"""
    import re
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

def create_terminal_image(output_text, width=1000, line_height=20):
    """Create an image that looks like terminal output"""
    # Strip ANSI codes for cleaner rendering
    clean_text = strip_ansi(output_text)
    lines = clean_text.split('\n')[:40]  # Limit to first 40 lines

    # Calculate image dimensions
    height = len(lines) * line_height + 40

    # Create image with dark terminal background
    img = Image.new('RGB', (width, height), color=(40, 44, 52))
    draw = ImageDraw.Draw(img)

    # Try to use a monospace font
    try:
        font = ImageFont.truetype('/System/Library/Fonts/Menlo.ttc', 14)
    except:
        try:
            font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', 14)
        except:
            font = ImageFont.load_default()

    # Draw text
    y = 20
    for line in lines:
        # Determine color based on content
        color = COLORS['white']
        if '❌' in line or 'FAILED' in line or 'ERROR' in line:
            color = COLORS['red']
        elif '✅' in line or 'PASSED' in line or 'SUCCESS' in line:
            color = COLORS['green']
        elif 'Details:' in line or 'Hint:' in line:
            color = COLORS['yellow']
        elif line.startswith('Category:'):
            color = COLORS['blue']
        elif line.startswith('='):
            color = COLORS['gray']

        # Truncate long lines
        if len(line) > 120:
            line = line[:117] + '...'

        draw.text((10, y), line, font=font, fill=color)
        y += line_height

    return img

def main():
    """Generate the failure screenshot"""
    print("📸 Generating verification failure screenshot...")

    # Backup original YAML
    backup_yaml()

    try:
        # Create failing configuration
        create_failing_yaml()
        print("  ✓ Modified numerical_claims.yaml to cause failure")

        # Run verification
        output = run_verification()
        print("  ✓ Ran verification script")

        # Create image
        img = create_terminal_image(output)
        img.save(OUTPUT_IMAGE)
        print(f"  ✓ Saved screenshot to {OUTPUT_IMAGE}")

        print("\n✅ Screenshot generated successfully!")

    finally:
        # Always restore original YAML
        restore_yaml()
        print("  ✓ Restored original numerical_claims.yaml")

if __name__ == '__main__':
    main()

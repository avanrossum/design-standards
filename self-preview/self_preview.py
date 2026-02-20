#!/usr/bin/env python3
"""
Self-Preview — Reference Implementation

A template render script for the self-preview pattern. Renders visual artifacts
to PNG so an AI agent can inspect its own output using multimodal vision.

This file is a working template. To adapt it for your project:
1. Subclass PreviewRenderer
2. Implement load_artifact(), render_item(), and get_items()
3. Optionally override render_overview() for a custom grid layout

See SELF_PREVIEW.md for the full pattern documentation.

Usage:
    python3 self_preview.py                          # render all items + overview
    python3 self_preview.py --items button spinner   # render specific items
    python3 self_preview.py --overview-only           # just the overview grid
    python3 self_preview.py --size 500                # custom render size
    python3 self_preview.py --no-overlays             # skip reference markers

Dependencies: Pillow (pip install Pillow)
"""

import argparse
import math
import os
import sys
from abc import ABC, abstractmethod

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("Error: Pillow is required. Install with: pip install Pillow")
    sys.exit(1)


# ---------------------------------------------------------------------------
# Configuration — adjust these for your project
# ---------------------------------------------------------------------------

# Output paths (relative to project root)
OUTPUT_DIR = "build/previews"
OVERVIEW_FILENAME = "overview.png"

# Visual defaults
DEFAULT_SIZE = 400         # pixels per item
BG_COLOR = (26, 26, 46)   # dark background (#1a1a2e)
FG_COLOR = (224, 224, 255) # light foreground (#e0e0ff)
LABEL_COLOR = (180, 180, 200)

# Overview grid
GRID_CELL_SIZE = 120       # pixels per cell in overview
GRID_PADDING = 8           # padding between cells
GRID_BG = (20, 20, 35)

# Overlay colors — use distinct colors for different reference types
OVERLAY_COLORS = {
    "primary":   (255, 80, 80, 100),    # red, semi-transparent
    "secondary": (255, 220, 60, 100),   # yellow
    "tertiary":  (80, 220, 120, 100),   # green
    "baseline":  (80, 140, 255, 100),   # blue
    "accent":    (180, 100, 255, 100),  # purple
}


# ---------------------------------------------------------------------------
# Base class — subclass this for your project
# ---------------------------------------------------------------------------

class PreviewRenderer(ABC):
    """Base class for self-preview renderers.

    Subclass and implement:
    - load_artifact()  — load your build output (font file, HTML, SVG, etc.)
    - render_item()    — render one item to a Pillow Image
    - get_items()      — return list of all renderable item names
    """

    def __init__(self, output_dir=OUTPUT_DIR):
        self.output_dir = output_dir
        self.artifact = None

    @abstractmethod
    def load_artifact(self):
        """Load the build artifact. Called once before rendering.

        Store whatever you need on self (e.g., self.font, self.svg_data).
        Return True if successful, False otherwise.
        """
        pass

    @abstractmethod
    def render_item(self, item_name, size, overlays=True):
        """Render a single item to a Pillow Image.

        Args:
            item_name: identifier for the item (e.g., "A", "button", "page-1")
            size: target image size in pixels (square)
            overlays: whether to draw reference markers

        Returns:
            PIL.Image.Image — the rendered preview
        """
        pass

    @abstractmethod
    def get_items(self):
        """Return a list of all renderable item names.

        Returns:
            list[str] — item identifiers (e.g., ["A", "B", "C"] or ["button", "header"])
        """
        pass

    # --- Overlay helpers (use these in your render_item implementation) ---

    @staticmethod
    def draw_horizontal_line(draw, y, width, color, label=None):
        """Draw a horizontal reference line with optional label."""
        draw.line([(0, y), (width, y)], fill=color, width=1)
        if label:
            draw.text((4, y - 14), label, fill=color)

    @staticmethod
    def draw_vertical_line(draw, x, height, color, label=None):
        """Draw a vertical reference line with optional label."""
        draw.line([(x, 0), (x, height)], fill=color, width=1)
        if label:
            draw.text((x + 4, 4), label, fill=color)

    @staticmethod
    def draw_grid(draw, width, height, spacing, color=(60, 60, 80, 80)):
        """Draw a reference grid."""
        for x in range(0, width, spacing):
            draw.line([(x, 0), (x, height)], fill=color, width=1)
        for y in range(0, height, spacing):
            draw.line([(0, y), (width, y)], fill=color, width=1)

    @staticmethod
    def draw_bounding_box(draw, x, y, w, h, color, label=None):
        """Draw a bounding box around a region."""
        draw.rectangle([x, y, x + w, y + h], outline=color, width=1)
        if label:
            draw.text((x, y - 14), label, fill=color)

    @staticmethod
    def draw_label(draw, x, y, text, color=LABEL_COLOR):
        """Draw a text label at the given position."""
        draw.text((x, y), text, fill=color)

    # --- Rendering pipeline ---

    def render_items(self, item_names, size=DEFAULT_SIZE, overlays=True):
        """Render specific items to individual PNGs.

        Args:
            item_names: list of item identifiers to render
            size: target image size in pixels
            overlays: whether to include reference markers
        """
        os.makedirs(self.output_dir, exist_ok=True)

        for name in item_names:
            img = self.render_item(name, size, overlays)
            if img is None:
                print(f"  Warning: render_item returned None for '{name}', skipping")
                continue

            # Sanitize filename
            safe_name = str(name).replace("/", "_").replace("\\", "_")
            path = os.path.join(self.output_dir, f"{safe_name}.png")
            img.save(path)
            print(f"  {name} -> {path}")

    def render_overview(self, size=GRID_CELL_SIZE, overlays=True):
        """Render all items in a grid overview.

        Override this method if you need a custom layout.
        """
        items = self.get_items()
        if not items:
            print("  No items to render in overview")
            return

        n = len(items)
        cols = min(math.ceil(math.sqrt(n * 1.5)), 16)  # wider than tall
        rows = math.ceil(n / cols)

        cell = size + GRID_PADDING
        img_w = cols * cell + GRID_PADDING
        img_h = rows * cell + GRID_PADDING

        overview = Image.new("RGB", (img_w, img_h), GRID_BG)

        for idx, name in enumerate(items):
            col = idx % cols
            row = idx // cols
            x = GRID_PADDING + col * cell
            y = GRID_PADDING + row * cell

            item_img = self.render_item(name, size, overlays=False)
            if item_img is None:
                continue

            # Resize if needed
            if item_img.size != (size, size):
                item_img = item_img.resize((size, size), Image.LANCZOS)

            overview.paste(item_img, (x, y))

            # Label
            draw = ImageDraw.Draw(overview)
            draw.text((x + 2, y + 2), str(name), fill=LABEL_COLOR)

        os.makedirs(self.output_dir, exist_ok=True)
        path = os.path.join(self.output_dir, OVERVIEW_FILENAME)
        overview.save(path)
        print(f"  Overview -> {path} ({overview.width}x{overview.height}px)")

    def run(self, items=None, size=DEFAULT_SIZE, overlays=True,
            overview_only=False, no_overview=False):
        """Main entry point. Handles the full render pipeline."""
        print("Loading artifact...")
        if not self.load_artifact():
            print("Error: Failed to load artifact")
            return False

        if overview_only:
            print("Rendering overview...")
            self.render_overview(overlays=overlays)
        else:
            target_items = items if items else self.get_items()
            print(f"Rendering {len(target_items)} item(s) at {size}px...")
            self.render_items(target_items, size, overlays)

            if not no_overview:
                print("Rendering overview...")
                self.render_overview(overlays=overlays)

        print("Done.")
        return True


# ---------------------------------------------------------------------------
# Example implementation — replace with your own
# ---------------------------------------------------------------------------

class ExampleRenderer(PreviewRenderer):
    """Example: renders colored squares with labels.

    Replace this with your actual renderer. This exists to demonstrate
    the pattern and verify the template works.
    """

    EXAMPLE_ITEMS = ["button", "header", "card", "input", "modal",
                     "sidebar", "footer", "nav", "badge", "tooltip"]

    EXAMPLE_COLORS = [
        (180, 60, 60), (60, 140, 180), (60, 160, 80), (180, 140, 60),
        (140, 80, 180), (180, 100, 60), (80, 80, 160), (160, 60, 120),
        (60, 160, 160), (140, 140, 60),
    ]

    def load_artifact(self):
        # In a real implementation, you'd load your font/HTML/SVG/etc. here
        print("  (Example mode — no real artifact to load)")
        return True

    def render_item(self, item_name, size, overlays=True):
        img = Image.new("RGB", (size, size), BG_COLOR)
        draw = ImageDraw.Draw(img)

        # Draw a placeholder shape
        idx = self.EXAMPLE_ITEMS.index(item_name) if item_name in self.EXAMPLE_ITEMS else 0
        color = self.EXAMPLE_COLORS[idx % len(self.EXAMPLE_COLORS)]
        margin = size // 6
        draw.rounded_rectangle(
            [margin, margin, size - margin, size - margin],
            radius=size // 12,
            fill=color,
            outline=FG_COLOR,
            width=2,
        )

        # Label
        draw.text((margin + 8, margin + 8), item_name, fill=FG_COLOR)

        # Reference overlays
        if overlays:
            center = size // 2
            self.draw_horizontal_line(draw, center, size,
                                      OVERLAY_COLORS["baseline"], "center")
            self.draw_vertical_line(draw, center, size,
                                    OVERLAY_COLORS["tertiary"], "center")
            self.draw_bounding_box(draw, margin, margin,
                                   size - 2 * margin, size - 2 * margin,
                                   OVERLAY_COLORS["primary"], "bounds")

        return img

    def get_items(self):
        return self.EXAMPLE_ITEMS


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_cli():
    """Build the argument parser. Extend with your own arguments."""
    parser = argparse.ArgumentParser(
        description="Self-Preview: Render artifacts to PNG for AI agent inspection.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                          Render all items + overview
  %(prog)s --items button spinner   Render specific items only
  %(prog)s --overview-only          Just the overview grid
  %(prog)s --size 500               Larger renders for detail
  %(prog)s --no-overlays            Clean render, no reference markers
        """,
    )
    parser.add_argument("--items", nargs="+",
                        help="Specific items to render (space-separated)")
    parser.add_argument("--size", type=int, default=DEFAULT_SIZE,
                        help=f"Render size in pixels (default: {DEFAULT_SIZE})")
    parser.add_argument("--overview-only", action="store_true",
                        help="Only render the overview grid")
    parser.add_argument("--no-overview", action="store_true",
                        help="Skip the overview grid")
    parser.add_argument("--no-overlays", action="store_true",
                        help="Skip reference overlay markers")
    return parser


def main():
    parser = build_cli()
    args = parser.parse_args()

    # Replace ExampleRenderer with your own renderer class
    renderer = ExampleRenderer()

    renderer.run(
        items=args.items,
        size=args.size,
        overlays=not args.no_overlays,
        overview_only=args.overview_only,
        no_overview=args.no_overview,
    )


if __name__ == "__main__":
    main()

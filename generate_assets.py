#!/usr/bin/env python3
"""Generate default piggy bank and coin PNG assets using Pillow."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ASSETS_DIR = Path(__file__).parent / "assets"


def generate_piggybank(width: int = 1280, height: int = 720):
    """Draw a cartoon-style piggy bank scene."""
    img = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(img)

    # Gradient background: light blue top to soft teal bottom
    for y in range(height):
        t = y / height
        r = int(200 + (180 - 200) * t)
        g = int(220 + (220 - 220) * t)
        b = int(255 + (240 - 255) * t)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # Simple "table" / surface at the bottom
    table_y = int(height * 0.7)
    draw.rectangle(
        [0, table_y, width, height],
        fill=(120, 100, 80),
    )
    # Table top edge highlight
    draw.rectangle(
        [0, table_y, width, table_y + 4],
        fill=(160, 140, 110),
    )

    # Piggy bank body - large pink ellipse (top right)
    body_cx = int(width * 0.78)
    body_cy = int(height * 0.30)
    body_rx = int(width * 0.15)
    body_ry = int(height * 0.18)

    # Shadow under piggy bank
    shadow_y = body_cy + body_ry + 10
    draw.ellipse(
        [
            body_cx - body_rx - 10,
            shadow_y - 8,
            body_cx + body_rx + 10,
            shadow_y + 10,
        ],
        fill=(170, 195, 220),
    )

    # Body
    pink = (255, 150, 170)
    pink_dark = (230, 120, 140)
    draw.ellipse(
        [
            body_cx - body_rx,
            body_cy - body_ry,
            body_cx + body_rx,
            body_cy + body_ry,
        ],
        fill=pink,
        outline=pink_dark,
        width=3,
    )

    # Snout - smaller ellipse to the right
    snout_cx = body_cx + body_rx - int(body_rx * 0.15)
    snout_cy = body_cy + int(body_ry * 0.15)
    snout_rx = int(body_rx * 0.35)
    snout_ry = int(body_ry * 0.3)
    draw.ellipse(
        [
            snout_cx - snout_rx,
            snout_cy - snout_ry,
            snout_cx + snout_rx,
            snout_cy + snout_ry,
        ],
        fill=(255, 170, 185),
        outline=pink_dark,
        width=2,
    )

    # Nostrils
    nr = 4
    draw.ellipse(
        [snout_cx - 10 - nr, snout_cy - nr, snout_cx - 10 + nr, snout_cy + nr],
        fill=pink_dark,
    )
    draw.ellipse(
        [snout_cx + 10 - nr, snout_cy - nr, snout_cx + 10 + nr, snout_cy + nr],
        fill=pink_dark,
    )

    # Eye
    eye_cx = body_cx + int(body_rx * 0.45)
    eye_cy = body_cy - int(body_ry * 0.25)
    draw.ellipse([eye_cx - 8, eye_cy - 8, eye_cx + 8, eye_cy + 8], fill="white")
    draw.ellipse([eye_cx - 4, eye_cy - 4, eye_cx + 4, eye_cy + 4], fill="black")
    # Eye highlight
    draw.ellipse([eye_cx - 2, eye_cy - 5, eye_cx + 1, eye_cy - 2], fill="white")

    # Ear - triangle-ish on top right
    ear_x = body_cx + int(body_rx * 0.3)
    ear_y = body_cy - body_ry
    draw.polygon(
        [
            (ear_x - 15, ear_y + 5),
            (ear_x + 5, ear_y - 30),
            (ear_x + 25, ear_y + 5),
        ],
        fill=pink,
        outline=pink_dark,
        width=2,
    )
    # Inner ear
    draw.polygon(
        [
            (ear_x - 8, ear_y + 2),
            (ear_x + 5, ear_y - 20),
            (ear_x + 18, ear_y + 2),
        ],
        fill=(255, 130, 155),
    )

    # Coin slot on top
    slot_cx = body_cx
    slot_cy = body_cy - body_ry + 8
    slot_w = int(body_rx * 0.5)
    slot_h = 6
    draw.rounded_rectangle(
        [
            slot_cx - slot_w // 2,
            slot_cy - slot_h // 2,
            slot_cx + slot_w // 2,
            slot_cy + slot_h // 2,
        ],
        radius=3,
        fill=(80, 50, 60),
    )

    # Legs - four small rectangles
    leg_w = int(body_rx * 0.2)
    leg_h = int(body_ry * 0.25)
    for offset in [-0.5, -0.15, 0.15, 0.5]:
        lx = body_cx + int(body_rx * offset)
        ly = body_cy + body_ry - 5
        draw.rounded_rectangle(
            [lx - leg_w // 2, ly, lx + leg_w // 2, ly + leg_h],
            radius=4,
            fill=pink,
            outline=pink_dark,
            width=2,
        )

    # Curly tail on the left
    tail_x = body_cx - body_rx + 5
    tail_y = body_cy - int(body_ry * 0.1)
    draw.arc(
        [tail_x - 25, tail_y - 15, tail_x + 5, tail_y + 15],
        start=0,
        end=300,
        fill=pink_dark,
        width=3,
    )

    # Save
    path = ASSETS_DIR / "piggybank.png"
    img.save(path)
    print(f"Saved: {path}")


def generate_coin(size: int = 80):
    """Draw a gold coin sprite with transparency."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    cx, cy = size // 2, size // 2
    r = size // 2 - 2

    # Outer ring - darker gold
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(200, 170, 50, 255))

    # Inner circle - brighter gold
    ir = r - 5
    draw.ellipse([cx - ir, cy - ir, cx + ir, cy + ir], fill=(240, 200, 60, 255))

    # Highlight arc
    hr = r - 3
    draw.arc(
        [cx - hr, cy - hr, cx + hr, cy + hr],
        start=200,
        end=320,
        fill=(255, 235, 130, 255),
        width=3,
    )

    # Euro symbol
    try:
        font = ImageFont.load_default(size=36)
    except TypeError:
        font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), "€", font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    tx = cx - tw // 2
    ty = cy - th // 2 - 2
    draw.text((tx, ty), "€", font=font, fill=(160, 120, 20, 255))

    path = ASSETS_DIR / "coin.png"
    img.save(path)
    print(f"Saved: {path}")


def main():
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    (ASSETS_DIR / "fonts").mkdir(exist_ok=True)
    generate_piggybank()
    generate_coin()
    print("Asset generation complete.")


if __name__ == "__main__":
    main()

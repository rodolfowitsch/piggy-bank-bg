"""Text rendering with Pillow for high-quality anti-aliased text overlays."""

from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont


_SYSTEM_FONTS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
]


class TextRenderer:
    def __init__(self, font_path: str | None = None, font_size: int = 48):
        self.font = None
        # Try user-provided font first
        if font_path and Path(font_path).exists():
            self.font = ImageFont.truetype(font_path, font_size)
        # Fall back to system fonts that support umlauts
        if self.font is None:
            for path in _SYSTEM_FONTS:
                if Path(path).exists():
                    self.font = ImageFont.truetype(path, font_size)
                    break
        if self.font is None:
            self.font = ImageFont.load_default(size=font_size)

    def render(
        self,
        text: str,
        width: int,
        height: int,
        color: tuple[int, int, int] = (255, 255, 255),
    ) -> np.ndarray:
        """Render text centered near the bottom. Returns BGRA numpy array."""
        img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        bbox = draw.textbbox((0, 0), text, font=self.font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        x = (width - tw) // 2
        y = height - th - 60

        # Background pill behind text for readability
        pad = 16
        draw.rounded_rectangle(
            (x - pad, y - pad, x + tw + pad, y + th + pad),
            radius=12,
            fill=(0, 0, 0, 160),
        )

        # Shadow
        draw.text((x + 2, y + 2), text, font=self.font, fill=(0, 0, 0, 180))
        # Main text
        draw.text((x, y), text, font=self.font, fill=(*color, 255))

        # PIL RGBA -> numpy BGRA
        arr = np.array(img)
        # Swap R and B channels
        arr[:, :, 0], arr[:, :, 2] = arr[:, :, 2].copy(), arr[:, :, 0].copy()
        return arr

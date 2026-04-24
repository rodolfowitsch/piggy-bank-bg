"""Asset loading and management."""

from pathlib import Path

import cv2
import numpy as np


class AssetManager:
    def __init__(self, assets_dir: Path):
        self.assets_dir = assets_dir

    def load_background(self) -> np.ndarray:
        path = self.assets_dir / "piggybank.png"
        img = cv2.imread(str(path), cv2.IMREAD_COLOR)
        if img is None:
            raise FileNotFoundError(
                f"Background image not found: {path}\n"
                "Run: python generate_assets.py"
            )
        return img

    def load_coin(self) -> np.ndarray:
        path = self.assets_dir / "coin.png"
        img = cv2.imread(str(path), cv2.IMREAD_UNCHANGED)  # BGRA
        if img is None:
            raise FileNotFoundError(
                f"Coin image not found: {path}\n"
                "Run: python generate_assets.py"
            )
        if img.shape[2] == 3:
            alpha = np.full(img.shape[:2] + (1,), 255, dtype=np.uint8)
            img = np.concatenate([img, alpha], axis=2)
        return img

    def get_font_path(self) -> str | None:
        fonts_dir = self.assets_dir / "fonts"
        if not fonts_dir.exists():
            return None
        for ext in ("*.ttf", "*.otf"):
            fonts = list(fonts_dir.glob(ext))
            if fonts:
                return str(fonts[0])
        return None

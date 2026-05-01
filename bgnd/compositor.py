"""Compositing pipeline: background + coin + text + person."""

import cv2
import numpy as np


class Compositor:
    def __init__(
        self,
        width: int,
        height: int,
        bg_image: np.ndarray,
        coin_image: np.ndarray,
    ):
        self.width = width
        self.height = height
        self.bg = cv2.resize(bg_image, (width, height))
        self.coin_bgra = coin_image

    def compose(
        self,
        person_frame: np.ndarray,
        mask: np.ndarray,
        anim_state: dict,
        text_layer: np.ndarray | None,
    ) -> np.ndarray:
        # Step 1: start with background
        output = self.bg.copy()

        # Step 2: overlay coin if visible
        if anim_state.get("coin_visible"):
            cx = int(anim_state["coin_x"] * self.width)
            cy = int(anim_state["coin_y"] * self.height)
            angle = anim_state.get("coin_angle", 0.0)
            self._overlay_coin(output, cx, cy, angle)

        # Step 3: composite person
        mask_resized = cv2.resize(mask, (self.width, self.height))
        mask_3ch = mask_resized[:, :, np.newaxis]
        person_resized = cv2.resize(person_frame, (self.width, self.height))

        output = (
            person_resized.astype(np.float32) * mask_3ch
            + output.astype(np.float32) * (1 - mask_3ch)
        )
        output = np.clip(output, 0, 255).astype(np.uint8)

        # Step 4: overlay text above person
        if text_layer is not None and anim_state.get("text_visible"):
            self._alpha_overlay_full(output, text_layer)

        return output

    def _overlay_coin(self, bg: np.ndarray, cx: int, cy: int, angle: float):
        coin = self.coin_bgra
        sh, sw = coin.shape[:2]

        # Rotate coin
        if angle != 0:
            mat = cv2.getRotationMatrix2D((sw / 2, sh / 2), angle, 1.0)
            coin = cv2.warpAffine(
                coin, mat, (sw, sh),
                flags=cv2.INTER_LINEAR,
                borderMode=cv2.BORDER_CONSTANT,
                borderValue=(0, 0, 0, 0),
            )

        self._alpha_overlay_sprite(bg, coin, cx, cy)

    def _alpha_overlay_sprite(
        self, bg: np.ndarray, sprite_bgra: np.ndarray, cx: int, cy: int
    ):
        sh, sw = sprite_bgra.shape[:2]
        x1 = cx - sw // 2
        y1 = cy - sh // 2
        x2, y2 = x1 + sw, y1 + sh

        # Clip to frame
        sx1 = max(0, -x1)
        sy1 = max(0, -y1)
        x1 = max(0, x1)
        y1 = max(0, y1)
        x2 = min(self.width, x2)
        y2 = min(self.height, y2)
        sx2 = sx1 + (x2 - x1)
        sy2 = sy1 + (y2 - y1)

        if x2 <= x1 or y2 <= y1:
            return

        crop = sprite_bgra[sy1:sy2, sx1:sx2]
        alpha = crop[:, :, 3:4].astype(np.float32) / 255.0
        color = crop[:, :, :3].astype(np.float32)
        roi = bg[y1:y2, x1:x2].astype(np.float32)
        bg[y1:y2, x1:x2] = (color * alpha + roi * (1 - alpha)).astype(np.uint8)

    def _alpha_overlay_full(self, bg: np.ndarray, overlay_bgra: np.ndarray):
        alpha = overlay_bgra[:, :, 3:4].astype(np.float32) / 255.0
        color = overlay_bgra[:, :, :3].astype(np.float32)
        bg_f = bg.astype(np.float32)
        blended = color * alpha + bg_f * (1 - alpha)
        np.copyto(bg, blended.astype(np.uint8))

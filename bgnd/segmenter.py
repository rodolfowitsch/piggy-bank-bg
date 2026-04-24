"""Person segmentation using MediaPipe Tasks API."""

import time

import cv2
import mediapipe as mp
import numpy as np


class PersonSegmenter:
    def __init__(self, model_path: str):
        base_options = mp.tasks.BaseOptions(model_asset_path=model_path)
        options = mp.tasks.vision.ImageSegmenterOptions(
            base_options=base_options,
            running_mode=mp.tasks.vision.RunningMode.VIDEO,
            output_category_mask=False,
        )
        self.segmenter = mp.tasks.vision.ImageSegmenter.create_from_options(options)
        self._start_time = time.monotonic()

    def process(self, bgr_frame: np.ndarray) -> np.ndarray:
        """Return a float32 mask (H, W) in [0, 1] where 1 = person."""
        rgb = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        timestamp_ms = int((time.monotonic() - self._start_time) * 1000)
        result = self.segmenter.segment_for_video(mp_image, timestamp_ms)
        # confidence_masks: index 0 = background, index 1 = person
        masks = result.confidence_masks
        if len(masks) > 1:
            mask = masks[1].numpy_view().copy()
        else:
            mask = masks[0].numpy_view().copy()
        mask = cv2.GaussianBlur(mask, (7, 7), 0)
        return mask

    def close(self):
        self.segmenter.close()

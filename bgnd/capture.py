"""Webcam capture via OpenCV."""

import cv2
import numpy as np


class WebcamCapture:
    def __init__(self, device: int = 0, width: int = 1280, height: int = 720):
        self.cap = cv2.VideoCapture(device)
        if not self.cap.isOpened():
            raise RuntimeError(f"Cannot open camera device {device}")
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        print(f"Webcam opened: {self.width}x{self.height} on device {device}")

    def read(self) -> tuple[bool, np.ndarray | None]:
        return self.cap.read()

    def release(self):
        self.cap.release()

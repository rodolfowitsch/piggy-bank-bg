"""Virtual camera output via pyvirtualcam / v4l2loopback."""

import numpy as np
import pyvirtualcam


class VirtualCameraOutput:
    def __init__(
        self,
        width: int,
        height: int,
        fps: float = 30.0,
        device: str | None = None,
    ):
        kwargs = dict(
            width=width,
            height=height,
            fps=fps,
            fmt=pyvirtualcam.PixelFormat.BGR,
        )
        if device:
            kwargs["device"] = device
        self.cam = pyvirtualcam.Camera(**kwargs)
        print(f"Virtual camera started: {self.cam.device}")

    def send(self, bgr_frame: np.ndarray):
        self.cam.send(bgr_frame)
        self.cam.sleep_until_next_frame()

    def close(self):
        self.cam.close()

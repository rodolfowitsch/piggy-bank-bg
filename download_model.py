#!/usr/bin/env python3
"""Download the MediaPipe selfie segmenter model."""

import urllib.request
from pathlib import Path

MODEL_URL = (
    "https://storage.googleapis.com/mediapipe-models/"
    "image_segmenter/selfie_segmenter/float16/latest/"
    "selfie_segmenter.tflite"
)
DEST = Path(__file__).parent / "models" / "selfie_segmenter.tflite"


def main():
    DEST.parent.mkdir(parents=True, exist_ok=True)
    if DEST.exists():
        print(f"Model already exists: {DEST} ({DEST.stat().st_size} bytes)")
        return
    print("Downloading selfie segmenter model...")
    urllib.request.urlretrieve(MODEL_URL, DEST)
    print(f"Saved to {DEST} ({DEST.stat().st_size} bytes)")


if __name__ == "__main__":
    main()

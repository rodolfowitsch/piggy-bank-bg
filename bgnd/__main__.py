"""Entry point for `python -m bgnd`."""

import argparse
from pathlib import Path
from types import SimpleNamespace

from .app import App


def main():
    parser = argparse.ArgumentParser(description="Piggy Bank Virtual Background")
    parser.add_argument("--camera", type=int, default=0, help="Webcam device index")
    parser.add_argument(
        "--vcam-device",
        type=str,
        default=None,
        help="Virtual camera device (e.g., /dev/video10)",
    )
    parser.add_argument(
        "--model",
        type=str,
        default=None,
        help="Path to MediaPipe selfie segmenter model",
    )
    parser.add_argument(
        "--assets",
        type=str,
        default=None,
        help="Path to assets directory",
    )
    parser.add_argument("--width", type=int, default=1280)
    parser.add_argument("--height", type=int, default=720)
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parent.parent

    config = SimpleNamespace(
        camera_device=args.camera,
        vcam_device=args.vcam_device,
        model_path=args.model or str(project_root / "models" / "selfie_segmenter.tflite"),
        assets_dir=Path(args.assets) if args.assets else project_root / "assets",
        width=args.width,
        height=args.height,
    )

    app = App(config)
    app.run()


if __name__ == "__main__":
    main()

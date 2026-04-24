"""Main application: video loop + CLI control thread."""

import threading
from pathlib import Path

from .animation import CoinAnimation
from .assets import AssetManager
from .capture import WebcamCapture
from .compositor import Compositor
from .segmenter import PersonSegmenter
from .text_renderer import TextRenderer
from .virtual_camera import VirtualCameraOutput

DEFAULT_SAYING = "Jeder Cent zählt!"


class App:
    def __init__(self, config):
        self.config = config
        self.lock = threading.Lock()
        self.running = True
        self.animation = CoinAnimation()
        self.current_saying = DEFAULT_SAYING
        self.text_layer = None
        self.text_dirty = True

    def run(self):
        assets = AssetManager(self.config.assets_dir)
        font_path = assets.get_font_path()

        capture = WebcamCapture(
            self.config.camera_device,
            self.config.width,
            self.config.height,
        )
        segmenter = PersonSegmenter(self.config.model_path)
        compositor = Compositor(
            capture.width,
            capture.height,
            assets.load_background(),
            assets.load_coin(),
        )
        vcam = VirtualCameraOutput(
            capture.width,
            capture.height,
            fps=30.0,
            device=self.config.vcam_device,
        )
        text_renderer = TextRenderer(font_path, font_size=48)

        cli_thread = threading.Thread(target=self._cli_loop, daemon=True)
        cli_thread.start()

        print(
            "\nReady! Commands:\n"
            "  drop / d [saying]  - trigger coin drop animation\n"
            "  text / t <saying>  - change the saying text\n"
            "  quit / q           - exit\n"
        )

        try:
            while self.running:
                ok, frame = capture.read()
                if not ok:
                    continue

                mask = segmenter.process(frame)

                with self.lock:
                    anim_state = self.animation.get_state()
                    if self.text_dirty:
                        self.text_layer = text_renderer.render(
                            self.current_saying,
                            capture.width,
                            capture.height,
                        )
                        self.text_dirty = False
                    text_layer = self.text_layer

                output = compositor.compose(frame, mask, anim_state, text_layer)
                vcam.send(output)
        except KeyboardInterrupt:
            print("\nShutting down...")
        finally:
            self.running = False
            capture.release()
            segmenter.close()
            vcam.close()

    def _cli_loop(self):
        while self.running:
            try:
                line = input("> ").strip()
            except (EOFError, KeyboardInterrupt):
                self.running = False
                break
            if not line:
                continue

            parts = line.split(maxsplit=1)
            cmd = parts[0].lower()

            with self.lock:
                if cmd in ("drop", "d"):
                    saying = parts[1] if len(parts) > 1 else self.current_saying
                    self.current_saying = saying
                    self.text_dirty = True
                    self.animation.trigger(saying)
                    print(f"  Coin drop! \"{saying}\"")
                elif cmd in ("text", "t"):
                    if len(parts) > 1:
                        self.current_saying = parts[1]
                        self.text_dirty = True
                        print(f"  Text: \"{self.current_saying}\"")
                    else:
                        print("  Usage: text <saying>")
                elif cmd in ("quit", "q"):
                    self.running = False
                else:
                    print(f"  Unknown: {cmd}")

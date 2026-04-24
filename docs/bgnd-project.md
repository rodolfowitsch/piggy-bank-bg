# Piggy Bank Dynamic Virtual Background for Microsoft Teams

## Context

The user wants a dynamic meeting background for Microsoft Teams: a piggy bank image where, on CLI command, a coin drops into it with an accompanying text/saying. The person is segmented from their real webcam and composited on top. The output goes to a virtual camera that Teams picks up.

## Architecture

**Pipeline (per frame at 30fps):**
```
Webcam -> MediaPipe Segmentation -> Person mask
                                        |
Piggy bank background                   |
  + coin sprite (if animating)          |
  + text overlay (if visible)           |
  + person alpha-blend (using mask) -> Virtual Camera (v4l2loopback)
```

**Control:** CLI thread reads commands (`drop`, `text`, `quit`) while the main thread runs the video loop.

## Tech Stack

- Python 3.12+
- OpenCV (webcam capture, image ops)
- MediaPipe Tasks API (selfie segmenter, person segmentation)
- Pillow (text rendering with anti-aliased fonts)
- pyvirtualcam + v4l2loopback (virtual camera output)
- NumPy (compositing math)

## Project Structure

```
bgnd/
  pyproject.toml
  setup_vcam.sh              # Load v4l2loopback kernel module
  generate_assets.py          # Generate default piggybank + coin PNGs
  assets/
    piggybank.png
    coin.png
    fonts/                    # User can drop a .ttf here
  models/                     # MediaPipe model (downloaded)
    selfie_segmenter.tflite
  bgnd/
    __init__.py
    __main__.py               # Entry point: python -m bgnd
    app.py                    # Main orchestrator (video loop + CLI thread)
    capture.py                # Webcam capture wrapper
    segmenter.py              # MediaPipe selfie segmentation
    compositor.py             # Layer compositing (bg + coin + text + person)
    animation.py              # Coin drop state machine with easing
    text_renderer.py          # Pillow text rendering to BGRA overlay
    virtual_camera.py         # pyvirtualcam output wrapper
    assets.py                 # Asset loading
    easing.py                 # Easing functions for animation
```

## Key Design Decisions

1. **MediaPipe Tasks API** (not legacy `mp.solutions`) — confidence masks give soft edges for natural compositing
2. **Pre-rendered text layer** — only re-rendered when text changes, not every frame
3. **v4l2loopback with `exclusive_caps=1`** — required for Teams to detect the virtual camera
4. **Virtual camera at `/dev/video10`** — avoids conflict with real webcam devices
5. **Pillow for text** — much better font quality than OpenCV's putText
6. **Programmatic asset generation** — default piggy bank + coin images generated via Pillow, user can replace with custom images

## Animation Design

- Coin drops from above the frame to the piggy bank's coin slot
- Easing: accelerating fall (ease-in quadratic) + bounce landing (ease-out bounce)
- Duration: ~1 second for the drop
- Coin rotates during fall (2 full rotations)
- Saying text appears during drop and lingers for 3 seconds after

## CLI Commands

| Command | Action |
|---------|--------|
| `drop [saying]` | Trigger coin drop animation with optional saying text |
| `text <saying>` | Change the current saying without triggering a drop |
| `quit` / `q` | Exit the application |

## Implementation Order

1. Project skeleton + pyproject.toml + dependencies
2. Asset generation script (piggy bank + coin PNGs via Pillow)
3. Webcam capture + virtual camera passthrough (verify Teams sees it)
4. MediaPipe segmentation + person compositing on solid color
5. Static piggy bank background compositing
6. Coin drop animation with easing
7. Text rendering overlay
8. CLI command wiring
9. Setup script + model download

## Verification

1. Run `bash setup_vcam.sh` to create virtual camera
2. Run `python generate_assets.py` to create default assets
3. Run `python -m bgnd --camera 0` 
4. Open Teams, select "PiggyBG" as camera source
5. Verify person is segmented and composited onto piggy bank background
6. Type `drop Sparfuchs!` in terminal — verify coin animation plays with text
7. Type `text Neuer Spruch` — verify text updates
8. Type `quit` — verify clean shutdown

# bgnd — Dynamic Piggy Bank Virtual Background for Microsoft Teams

A virtual camera background that shows a cartoon piggy bank. On command, a coin drops into it with a custom saying. Your real webcam feed is segmented so you appear composited on top of the animated background.

## Prerequisites

- Linux with v4l2loopback support
- Python 3.12+
- A webcam

Install the v4l2loopback kernel module:

```bash
sudo apt install v4l2loopback-dkms
```

## Setup

```bash
# Create virtual environment and install dependencies
python3 -m venv .venv
source .venv/bin/activate
pip install -e .

# Generate default piggy bank and coin images
python generate_assets.py

# Download the MediaPipe selfie segmenter model
python download_model.py

# Load the virtual camera kernel module
bash setup_vcam.sh
```

## Usage

```bash
source .venv/bin/activate
python -m bgnd --camera 0
```

Then in Microsoft Teams, select **PiggyBG** as your camera source.

### CLI commands

| Command | Description |
|---------|-------------|
| `drop [saying]` | Trigger coin drop animation, optionally with a new saying |
| `text <saying>` | Change the saying text without triggering a drop |
| `quit` / `q` | Exit |

### Options

```
--camera DEVICE    Webcam device index (default: 0)
--vcam-device DEV  Virtual camera device path (e.g. /dev/video10)
--model PATH       Path to MediaPipe selfie segmenter model
--assets PATH      Path to assets directory
--width WIDTH      Output width (default: 1280)
--height HEIGHT    Output height (default: 720)
```

## Custom assets

Replace the generated images in `assets/` with your own:

- `piggybank.png` — background image (any resolution, gets resized)
- `coin.png` — coin sprite (RGBA PNG with transparency)

Drop a `.ttf` or `.otf` font file into `assets/fonts/` to use a custom font for the saying text.

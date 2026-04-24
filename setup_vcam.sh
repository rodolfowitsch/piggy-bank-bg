#!/bin/bash
# Load v4l2loopback with a virtual camera device for Teams compatibility.
# Requires: sudo apt install v4l2loopback-dkms
set -e

if lsmod | grep -q v4l2loopback; then
    # Check if /dev/video10 exists and is a valid output device
    if [ -e /dev/video10 ] && v4l2-ctl --device=/dev/video10 --all 2>/dev/null | grep -q "Video Output"; then
        echo "v4l2loopback already loaded and /dev/video10 is ready."
        exit 0
    fi
    echo "v4l2loopback loaded but /dev/video10 is missing or not an output device."
    echo "Reloading with correct options..."
    sudo modprobe -r v4l2loopback
fi

echo "Loading v4l2loopback..."
sudo modprobe v4l2loopback devices=1 video_nr=10 card_label="PiggyBG" exclusive_caps=1
echo "Virtual camera created at /dev/video10"
echo "Devices:"
ls /dev/video*

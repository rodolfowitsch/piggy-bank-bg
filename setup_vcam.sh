#!/bin/bash
# Load v4l2loopback with a virtual camera device for Teams compatibility.
# Requires: sudo apt install v4l2loopback-dkms
set -e

if lsmod | grep -q v4l2loopback; then
    echo "v4l2loopback already loaded."
    echo "Devices:"
    ls /dev/video* 2>/dev/null || echo "  (none)"
    exit 0
fi

echo "Loading v4l2loopback..."
sudo modprobe v4l2loopback devices=1 video_nr=10 card_label="PiggyBG" exclusive_caps=1
echo "Virtual camera created at /dev/video10"
echo "Devices:"
ls /dev/video*

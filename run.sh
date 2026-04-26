#!/usr/bin/env bash

set -e

echo "Start Piggy-Bank"

source .venv/bin/activate
pip install -e .


echo "Initialisiere das Kamerasystem"
./setup_vcam.sh

echo "####################################"
echo "### Starte die Konferenzkamera:"
echo "####################################"
python -m bgnd --camera 0

echo "Fertig."
sleep 3

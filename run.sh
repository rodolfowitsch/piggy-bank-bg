#!/usr/bin/env bash

function fehler() {
  echo ">>> FEHLER!"
  echo ""
  sleep 10
  exit 1
}

echo "Start Piggy-Bank"

cd ${HOME}/git/github/piggy-bank-bg || fehler
source .venv/bin/activate || fehler
pip install -e . || fehler


echo "Initialisiere das Kamerasystem"
./setup_vcam.sh || fehler

echo "####################################"
echo "### Starte die Konferenzkamera:"
echo "### Anschauen kann man sich das auch:"
echo "### VLC starten und dann dort unter"
echo "###    Medien"
echo "###    -> Aufnahmegeraet oeffnen"
echo "###    -> Video-Geraet /dev/video10"
echo "####################################"
python -m bgnd --camera 0 || fehler

echo "Fertig."
sleep 3

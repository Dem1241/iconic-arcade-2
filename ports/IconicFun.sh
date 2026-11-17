#!/bin/bash
# Launcher: Batocera lists every .sh in /userdata/roms/ports under "Ports"
cd "$(dirname "$0")/iconicfun" || exit 1
python3 main.py

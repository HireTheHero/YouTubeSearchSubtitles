#!/bin/sh

conda activate youtube
python collect_transcription.py \
        -q <your-query> -s <add-this-to-query> -t <video-or-playlist> \
        -k <your-key>

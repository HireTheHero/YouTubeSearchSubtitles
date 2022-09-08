# YouTubeSearchSubtitles
Search YouTube with a query and collect subtitles from resulting video / playlist.
## example usage
- Register yourself to [YouTubeDataAPI](https://developers.google.com/youtube/v3/docs)
- Env setup
```
conda create -n youtube
conda install pip
pip install -r requirements.txt
chmod 755 main.sh
```
- run `collect_transcription.py` or main.sh
```
python collect_transcription.py \
        -q <your-query> -s <add-this-to-query> -t <video-or-playlist> \
        -k <your-key>
```

## TBD
- playlist part
"""
# Summary
Extract subtitles from YouTube videos in query results
# Details
## Arguments
## PreRequisites
- Register your account to YouTube Data API and get its key
## Reference
- https://developers.google.com/youtube/v3/docs
- https://gist.github.com/suqingdong/bcf756910321569fb44302bac52edc48
"""
import time

from utils.youtube import get_subtitles, get_videos
from utils.utils import args_generator, get_module_logger, export_json

if __name__ == "__main__":
    t0 = time.time()
    # logger & parser
    logger = get_module_logger(__name__)
    args = args_generator()
    # get video list
    videos = get_videos(args)
    video_ids = videos["video_id"]
    logger.info(f"video list obtained with length {len(video_ids)}")
    # Get subtitles for acquired video ids
    subtitles = get_subtitles(video_ids)
    videos["transcript"] = subtitles
    logger.info(f"Short example for subtitles: {subtitles[0][:100]}")
    # export
    export_json(args, videos)
    logger.info(f"Transcription collected in {round(time.time()-t0, 2)} seconds")

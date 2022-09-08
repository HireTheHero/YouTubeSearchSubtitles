"""
# Summary
YouTube-related functions
# Details
## Reference
- https://gist.github.com/suqingdong/bcf756910321569fb44302bac52edc48
- https://qiita.com/g-k/items/7c98efe21257afac70e9
"""
from typing import List

from apiclient.discovery import build
import numpy as np
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled


class InputTypeException(Exception):
    pass


def build_youtube(args):
    """
    Build YouTube client
    """
    return build("youtube", "v3", developerKey=args.key)


def query_youtube(
    args, youtube, is_first: bool = True, prev_response=None, prev_result=None
):
    """
    Query YouTube
    """
    if is_first:
        response = youtube.search().list(
            part="snippet",
            q=args.query + args.suffix,
            order="relevance",
            type=args.search_type,
            maxResults=args.max,
        )
    else:
        if not prev_response or not prev_result:
            raise InputTypeException("For 2nd~ time search, provide previous result")
        else:
            response = youtube.search().list_next(prev_response, prev_result)
    if response:
        result = response.execute()
    else:
        result = None
    return response, result


def get_videos_in_playlist(args, q_result):
    """
    TBD
    """
    pass


def get_queried_videos(args, q_result):
    """
    Get video information from query result
    TBD: If queried as playlist, first obtain videos in playlist and pass 'em
    """
    types = np.repeat(args.search_type, len(q_result)).tolist()
    if args.search_type == "video":
        playlist_ids = np.repeat("(not_playlist)", len(q_result)).tolist()
    else:
        playlist_ids = q_result["playlist_id"]
    video_ids = []
    titles = []
    for r in q_result["items"]:
        video_ids.append(r["id"]["videoId"])
        titles.append(r["snippet"]["title"])

    return types, playlist_ids, video_ids, titles


def get_videos(args):
    """
    Main pipeline for video extraction
    """
    out = {"type": [], "playlist_id": [], "video_id": [], "title": []}
    youtube = build_youtube(args)
    for idx in range(args.next_count):
        is_first = not bool(idx)
        if is_first:
            response, result = query_youtube(args, youtube, is_first)
        else:
            response, result = query_youtube(args, youtube, is_first, response, result)
        if not response:
            break
        else:
            pass
        if args.search_type == "playlist":
            result_out = get_videos_in_playlist(args, result)
        else:
            result_out = result
        types, playlist_ids, video_ids, titles = get_queried_videos(args, result_out)
        out["type"] += types
        out["playlist_id"] += playlist_ids
        out["video_id"] += video_ids
        out["title"] += titles
    return out


def get_transcripts(video_list: List[str]):
    """
    Get list of transcripts from list of videos
    """
    out = []
    for video in video_list:
        try:
            result = YouTubeTranscriptApi.get_transcript(video)
        except TranscriptsDisabled:
            result = "(Subtitles not available)"
        result_concat = [r["text"] for r in result]
        out.append(" ".join(result_concat))
    return out

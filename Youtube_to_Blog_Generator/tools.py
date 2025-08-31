import os
import re
from datetime import datetime
from typing import List, Dict, Optional

from dotenv import load_dotenv
load_dotenv()  # ensure env vars are available at import time

from crewai.tools import tool
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound, VideoUnavailable
import yt_dlp

# --- ENV ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY is missing from environment. Check your .env file.")
if not YOUTUBE_API_KEY:
    # Not strictly required if you only use the transcript tool, but we keep it to support search.
    print("WARN: YOUTUBE_API_KEY not found. youtube_search will be unavailable.")

# --- Helpers ---
def _extract_video_id(url_or_id: str) -> str:
    """Accepts a full YouTube URL or a plain video ID and returns the video ID."""
    # If it's already a plausible video id
    if re.fullmatch(r"[-_0-9A-Za-z]{11}", url_or_id):
        return url_or_id

    # Try to extract from URL formats
    patterns = [
        r"(?:v=|/v/|youtu\.be/|/shorts/)([-_0-9A-Za-z]{11})",
    ]
    for pat in patterns:
        m = re.search(pat, url_or_id)
        if m:
            return m.group(1)
    raise ValueError("Could not extract a YouTube video ID from the input. Provide a valid YouTube URL or 11-char video ID.")

def _fetch_video_metadata(video_url_or_id: str) -> Dict:
    """Get title, channel, upload_date, duration, description using yt_dlp (no API quota)."""
    vid_input = video_url_or_id if video_url_or_id.startswith("http") else f"https://www.youtube.com/watch?v={video_url_or_id}"

    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "nocheckcertificate": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(vid_input, download=False)
        # upload_date may be like "20240810". Convert if present.
        upload_dt = None
        if info.get("upload_date"):
            try:
                upload_dt = datetime.strptime(info["upload_date"], "%Y%m%d").strftime("%Y-%m-%d")
            except Exception:
                upload_dt = info.get("upload_date")

        return {
            "title": info.get("title"),
            "channel": info.get("channel") or info.get("uploader"),
            "upload_date": upload_dt,
            "duration": info.get("duration"),
            "description": info.get("description"),
            "url": info.get("webpage_url") or vid_input,
            "id": info.get("id")
        }

def _get_transcript_text(video_id: str) -> Optional[str]:
    """
    Try to fetch English transcript (manual or auto). If not found, try any transcript and translate to English.
    Returns a plain text transcript or None.
    """
    try:
        # First try direct English
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["en", "en-US", "en-GB"])
        return " ".join([seg["text"] for seg in transcript if seg.get("text")])
    except (TranscriptsDisabled, NoTranscriptFound, VideoUnavailable):
        pass
    except Exception:
        pass

    # Fallback: use list + translate
    try:
        list_obj = YouTubeTranscriptApi.list_transcripts(video_id)
        # If English available
        try:
            t = list_obj.find_transcript(["en", "en-US", "en-GB"])
            return " ".join([seg["text"] for seg in t.fetch() if seg.get("text")])
        except NoTranscriptFound:
            # Try any language then translate to English
            for tr in list_obj:
                try:
                    tr_en = tr.translate("en")
                    return " ".join([seg["text"] for seg in tr_en.fetch() if seg.get("text")])
                except Exception:
                    continue
    except Exception:
        return None

    return None

# --------------------- TOOLS ---------------------

@tool("YouTube Video Search")
def youtube_search(query: str, max_results: int = 5) -> List[Dict]:
    """
    Search YouTube for videos (uses YouTube Data API v3).
    Returns a list of dicts: {title, url}.
    """
    if not YOUTUBE_API_KEY:
        return [{"error": "YOUTUBE_API_KEY is not set. Add it to your .env"}]

    yt = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    response = yt.search().list(
        q=query,
        part="snippet",
        type="video",
        maxResults=max_results
    ).execute()

    results = []
    for item in response.get("items", []):
        vid_id = item["id"]["videoId"]
        title = item["snippet"]["title"]
        results.append({
            "title": title,
            "url": f"https://www.youtube.com/watch?v={vid_id}"
        })
    return results or [{"info": "No videos found."}]


@tool("YouTube Transcript Fetcher")
def youtube_transcript_fetcher(video_url_or_id: str) -> str:
    """
    Given a YouTube video URL or ID, returns a structured summary-ready bundle:
    - Title, Channel, Upload Date, URL
    - Transcript (if available)
    """
    try:
        vid = _extract_video_id(video_url_or_id)
    except ValueError as e:
        return f"ERROR: {e}"

    meta = _fetch_video_metadata(vid)
    transcript_text = _get_transcript_text(vid)

    header = [
        f"Title: {meta.get('title')}",
        f"Channel: {meta.get('channel')}",
        f"Uploaded: {meta.get('upload_date')}",
        f"URL: {meta.get('url')}",
        "",
        "=== TRANSCRIPT START ===",
    ]
    body = transcript_text or "[No transcript available for this video.]"
    footer = [
        "=== TRANSCRIPT END ===",
        "",
        "Notes: If transcript is missing, write the blog from metadata + description + general topic knowledge."
    ]
    return "\n".join(header + [body] + footer)

"""Transcripts of YouTube videos, a playlist, a channel or a search → one .txt file per video
in ./transcripts, ready for summaries, notes or a RAG index.

Cost: about $0.0025 per transcript (videos without captions are free).
Usage: python youtube_transcripts.py https://www.youtube.com/@channel 10    (source, max videos)
"""

import pathlib
import sys

from _apify import run

source = sys.argv[1] if len(sys.argv) > 1 else "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10

videos = run(
    "tacps126~youtube-transcripts",
    {
        "videos": [source],
        "maxVideosPerSource": limit,
        "includeSegments": False,
        "maxItems": limit,
    },
)

out = pathlib.Path("transcripts")
out.mkdir(exist_ok=True)
for v in videos:
    header = f"{v.get('title')}\n{v.get('channel')} · {v.get('publishedAt')} · {v.get('url')}\n\n"
    (out / f"{v.get('videoId')}.txt").write_text(header + (v.get("transcript") or ""))
print(f"{len(videos)} transcripts → {out}/")

"""YouTube Comment Fetcher Module
Handles fetching comments and video stats from YouTube videos
"""

import pandas as pd
import logging
from functools import lru_cache
from youtube_comment_downloader import YoutubeCommentDownloader

logger = logging.getLogger(__name__)
try:
    from yt_dlp import YoutubeDL
    HAS_YT_DLP = True
except ImportError:
    HAS_YT_DLP = False


class YouTubeCommentFetcher:
    """Handles fetching comments from YouTube videos."""
    
    def __init__(self):
        self.downloader = self._load_downloader()
    
    def fetch_video_stats(self, url):
        """Fetches video statistics from YouTube URL."""
        stats = {'title': 'Unknown', 'views': 0, 'likes': 0, 'comments_count': 0, 'available': False}
        if not HAS_YT_DLP:
            return stats
        try:
            ydl_opts = {'quiet': True, 'no_warnings': True}
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                stats['title'] = info.get('title', 'Unknown')
                stats['views'] = info.get('view_count', 0)
                stats['likes'] = info.get('like_count', 0)
                stats['comments_count'] = info.get('comment_count', 0)
        except Exception:
            pass
        return stats

    @staticmethod
    @lru_cache(maxsize=1)
    def _load_downloader():
        """Attempts to load and cache the comment downloader."""
        try:
            return YoutubeCommentDownloader()
        except Exception:
            return None

    def fetch_comments(self, url, max_results=None):
        """Fetches public comments and their published dates from a YouTube URL."""
        comments_data = []
        
        if not self.downloader:
            return pd.DataFrame(comments_data)
        
        comment_count = 0
        for comment in self.downloader.get_comments_from_url(url):
            # Extract comment text
            text = str(comment.get("text", "")).strip()
            if not text:
                continue
            
            # Extract date - try multiple fields
            date_value = None
            if comment.get("time_parsed"):
                date_value = comment.get("time_parsed")
            elif comment.get("time"):
                date_value = comment.get("time")
            elif comment.get("publishedAt"):
                date_value = comment.get("publishedAt")
            
            # Add comment with date (or NaT if no date found)
            comments_data.append({
                "Comment": text,
                "Date": date_value if date_value else pd.NaT,
            })
            
            comment_count += 1
            if max_results and comment_count >= max_results:
                break
            
        return pd.DataFrame(comments_data)

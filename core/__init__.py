"""
Core Module
Contains sentiment analysis, language detection, data processing, and YouTube fetching
"""

from core.sentiment_analyzer import SentimentAnalyzer
from core.language_detector import LanguageDetector
from core.youtube_fetcher import YouTubeCommentFetcher
from core.data_processor import DataProcessor

__all__ = [
    'SentimentAnalyzer',
    'LanguageDetector',
    'YouTubeCommentFetcher',
    'DataProcessor'
]

"""
Data Processing Module
Handles data processing, language detection, and sentiment analysis
"""

import pandas as pd
import logging
import streamlit as st
from core.language_detector import LanguageDetector
from core.sentiment_analyzer import SentimentAnalyzer


class DataProcessor:
    """Handles data processing including language detection and sentiment analysis."""
    
    def __init__(self):
        self.language_detector = LanguageDetector()
        self.sentiment_analyzer = SentimentAnalyzer()

    def process_data(self, df):
        """Applies language detection and sentiment analysis to dataframe."""
        if df.empty:
            return df

        sentiments = []
        sentiments_confidence = []
        languages = []
        
        progress_bar = st.progress(0)
        for idx, text in enumerate(df['Comment']):
            # 1. Detect Language
            lang = self.language_detector.detect(text)
            languages.append(lang)
            
            # 2. Detect Sentiment using ensemble approach with confidence
            sentiment, confidence = self.sentiment_analyzer.analyze_ensemble(text)
            sentiments.append(sentiment)
            sentiments_confidence.append(confidence)
            
            # Update progress
            progress_bar.progress((idx + 1) / len(df))
        
        progress_bar.empty()
        
        df['Language'] = languages
        df['Sentiment'] = sentiments
        df['Sentiment Confidence %'] = sentiments_confidence
        
        # Parse dates properly - handle various formats
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        
        # Filter out rows with invalid dates (NaT) or epoch dates (1970-01-01)
        epoch_date = pd.Timestamp('1970-01-01')
        df = df[(df['Date'].notna()) & (df['Date'] > epoch_date)].copy()
        
        return df

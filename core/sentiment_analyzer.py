"""
Sentiment Analysis Module
Handles sentiment analysis using VADER and keyword-based methods
"""

from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

# Initialize VADER sentiment analyzer
nltk.download('vader_lexicon', quiet=True)


class SentimentAnalyzer:
    """Handles sentiment analysis using VADER and keyword-based methods."""
    
    def __init__(self):
        self.vader_analyzer = SentimentIntensityAnalyzer()
        self.positive_keywords = {
            'good', 'great', 'love', 'awesome', 'excellent', 'best', 'nice', 'amazing',
            'wonderful', 'fantastic', 'brilliant', 'perfect', 'superb', 'outstanding',
            'beautiful', 'lovely', 'impressive', 'cool', 'exceptional', 'wonderful'
        }
        self.negative_keywords = {
            'bad', 'terrible', 'hate', 'awful', 'worst', 'sucks', 'disappoint',
            'horrible', 'disgusting', 'useless', 'waste', 'pathetic', 'annoying',
            'poor', 'wrong', 'broken', 'fail', 'failed', 'sad', 'worse', 'terrible'
        }

    def analyze_vader(self, text):
        """Analyze sentiment using VADER."""
        scores = self.vader_analyzer.polarity_scores(text)
        compound = scores['compound']
        
        if compound >= 0.05:
            return "Positive"
        elif compound <= -0.05:
            return "Negative"
        else:
            return "Neutral"

    def analyze_keyword(self, text):
        """Analyze sentiment using keyword matching."""
        text_lower = text.lower()
        pos_count = sum(1 for word in self.positive_keywords if word in text_lower)
        neg_count = sum(1 for word in self.negative_keywords if word in text_lower)
        
        if pos_count > neg_count:
            return "Positive"
        elif neg_count > pos_count:
            return "Negative"
        else:
            return "Neutral"

    def analyze_ensemble(self, text):
        """Ensemble method combining VADER and keyword-based analysis with confidence."""
        scores = self.vader_analyzer.polarity_scores(text)
        compound = scores['compound']
        
        # Determine sentiment and get confidence score
        if compound >= 0.05:
            sentiment = "Positive"
            confidence = scores['pos']
        elif compound <= -0.05:
            sentiment = "Negative"
            confidence = scores['neg']
        else:
            sentiment = "Neutral"
            confidence = scores['neu']
        
        # Convert confidence to percentage
        confidence_percent = round(confidence * 100, 1)
        
        return sentiment, confidence_percent

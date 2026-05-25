"""
Language Detection Module
Handles language detection with retry logic and error handling
"""

import logging
from langdetect import detect, LangDetectException

logger = logging.getLogger(__name__)


class LanguageDetector:
    """Handles language detection with robust error handling."""
    
    LANGUAGE_MAP = {
        'en': 'English', 'es': 'Spanish', 'fr': 'French', 'de': 'German',
        'it': 'Italian', 'pt': 'Portuguese', 'ru': 'Russian', 'ja': 'Japanese',
        'ko': 'Korean', 'zh': 'Chinese', 'ar': 'Arabic', 'hi': 'Hindi',
        'bn': 'Bengali', 'pa': 'Punjabi', 'te': 'Telugu', 'mr': 'Marathi',
        'ta': 'Tamil', 'gu': 'Gujarati', 'kn': 'Kannada', 'ml': 'Malayalam',
        'th': 'Thai', 'vi': 'Vietnamese', 'id': 'Indonesian', 'tr': 'Turkish',
        'pl': 'Polish', 'nl': 'Dutch', 'sv': 'Swedish', 'da': 'Danish',
        'no': 'Norwegian', 'fi': 'Finnish', 'cs': 'Czech', 'sk': 'Slovak',
        'ro': 'Romanian', 'hu': 'Hungarian', 'el': 'Greek', 'he': 'Hebrew',
        'uk': 'Ukrainian', 'bg': 'Bulgarian', 'hr': 'Croatian', 'sr': 'Serbian',
    }
    
    @staticmethod
    def detect(text):
        """Detects the language of a given text string with retry logic."""
        if not text or not isinstance(text, str) or len(text.strip()) < 3:
            return "Unknown"
        
        try:
            # Try to detect language
            lang = detect(text)
            if lang:
                lang_lower = lang.lower()
                return LanguageDetector.LANGUAGE_MAP.get(lang_lower, lang_lower.upper())
            return "Unknown"
        except LangDetectException:
            # If detection fails, try with truncated text
            try:
                if len(text) > 20:
                    lang = detect(text[:100])
                    if lang:
                        lang_lower = lang.lower()
                        return LanguageDetector.LANGUAGE_MAP.get(lang_lower, lang_lower.upper())
                    return "Unknown"
            except Exception:
                pass
            return "Unknown"
        except Exception:
            return "Unknown"

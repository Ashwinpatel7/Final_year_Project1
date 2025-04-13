"""
Configuration package for the Language Translator application.
Contains configuration settings, themes, and constants.
"""

# Import theme classes for easy access
from config.theme import ThemeColors, ThemeFonts, ThemeStyles

# Language codes mapping
LANGUAGES = [
    'English',
    'Spanish',
    'French',
    'German',
    'Italian',
    'Portuguese',
    'Russian',
    'Japanese',
    'Korean',
    'Chinese (Simplified)',
    'Chinese (Traditional)',
    'Arabic',
    'Hindi',
    'Bengali',
    'Urdu',
    'Turkish',
    'Dutch',
    'Greek',
    'Hebrew',
    'Polish',
    'Thai',
    'Vietnamese',
    'Swedish',
    'Finnish',
    'Danish',
    'Norwegian'
]

# Language codes for translation APIs
LANGUAGE_CODES = {
    'Auto Detect': 'auto',
    'English': 'en',
    'Spanish': 'es',
    'French': 'fr',
    'German': 'de',
    'Italian': 'it',
    'Portuguese': 'pt',
    'Russian': 'ru',
    'Japanese': 'ja',
    'Korean': 'ko',
    'Chinese (Simplified)': 'zh-CN',
    'Chinese (Traditional)': 'zh-TW',
    'Arabic': 'ar',
    'Hindi': 'hi',
    'Bengali': 'bn',
    'Urdu': 'ur',
    'Turkish': 'tr',
    'Dutch': 'nl',
    'Greek': 'el',
    'Hebrew': 'he',
    'Polish': 'pl',
    'Thai': 'th',
    'Vietnamese': 'vi',
    'Swedish': 'sv',
    'Finnish': 'fi',
    'Danish': 'da',
    'Norwegian': 'no'
}

# Export all for easy importing
__all__ = ['ThemeColors', 'ThemeFonts', 'ThemeStyles', 'LANGUAGES', 'LANGUAGE_CODES']

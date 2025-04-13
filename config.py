"""
Configuration module for the Language Translator application.
Contains constants, theme settings, and language configurations.
"""

# Language configuration
LANGUAGE_CODES = {
    'Afrikaans': 'af', 'Albanian': 'sq', 'Arabic': 'ar', 'Armenian': 'hy',
    'Azerbaijani': 'az', 'Basque': 'eu', 'Belarusian': 'be', 'Bengali': 'bn',
    'Bosnian': 'bs', 'Bulgarian': 'bg', 'Catalan': 'ca', 'Cebuano': 'ceb',
    'Chinese': 'zh-cn', 'Corsican': 'co', 'Croatian': 'hr', 'Czech': 'cs',
    'Danish': 'da', 'Dutch': 'nl', 'English': 'en', 'Esperanto': 'eo',
    'Estonian': 'et', 'Finnish': 'fi', 'French': 'fr', 'Frisian': 'fy',
    'Galician': 'gl', 'Georgian': 'ka', 'German': 'de', 'Greek': 'el',
    'Gujarati': 'gu', 'Haitian Creole': 'ht', 'Hausa': 'ha', 'Hebrew': 'he',
    'Hindi': 'hi', 'Hmong': 'hmn', 'Hungarian': 'hu', 'Icelandic': 'is',
    'Igbo': 'ig', 'Indonesian': 'id', 'Irish': 'ga', 'Italian': 'it',
    'Japanese': 'ja', 'Javanese': 'jv', 'Kannada': 'kn', 'Kazakh': 'kk',
    'Khmer': 'km', 'Korean': 'ko', 'Kurdish': 'ku', 'Kyrgyz': 'ky',
    'Lao': 'lo', 'Latin': 'la', 'Latvian': 'lv', 'Lithuanian': 'lt',
    'Luxembourgish': 'lb', 'Macedonian': 'mk', 'Malagasy': 'mg', 'Malay': 'ms',
    'Malayalam': 'ml', 'Maltese': 'mt', 'Maori': 'mi', 'Marathi': 'mr',
    'Mongolian': 'mn', 'Myanmar': 'my', 'Nepali': 'ne', 'Norwegian': 'no',
    'Pashto': 'ps', 'Persian': 'fa', 'Polish': 'pl', 'Portuguese': 'pt',
    'Punjabi': 'pa', 'Romanian': 'ro', 'Russian': 'ru', 'Samoan': 'sm',
    'Scots Gaelic': 'gd', 'Serbian': 'sr', 'Sesotho': 'st', 'Shona': 'sn',
    'Sindhi': 'sd', 'Sinhala': 'si', 'Slovak': 'sk', 'Slovenian': 'sl',
    'Somali': 'so', 'Spanish': 'es', 'Sundanese': 'su', 'Swahili': 'sw',
    'Swedish': 'sv', 'Tajik': 'tg', 'Tamil': 'ta', 'Telugu': 'te', 'Thai': 'th',
    'Turkish': 'tr', 'Ukrainian': 'uk', 'Urdu': 'ur', 'Uzbek': 'uz',
    'Vietnamese': 'vi', 'Welsh': 'cy', 'Xhosa': 'xh', 'Yiddish': 'yi',
    'Yoruba': 'yo', 'Zulu': 'zu'
}

LANGUAGES = list(LANGUAGE_CODES.keys())

# Vibrant modern color scheme
class ThemeColors:
    # Main colors - Vibrant Gradient Theme
    PRIMARY = "#8A2BE2"  # Vivid purple
    PRIMARY_VARIANT = "#4B0082"  # Indigo
    SECONDARY = "#00CED1"  # Bright turquoise
    SECONDARY_VARIANT = "#20B2AA"  # Light sea green
    ACCENT = "#FF6B6B"  # Coral red

    # Background colors
    BACKGROUND = "#FFFFFF"  # White
    SURFACE = "#F8F9FA"  # Off-white
    ERROR = "#FF5252"  # Bright red

    # Text colors
    ON_PRIMARY = "#FFFFFF"  # White
    ON_SECONDARY = "#000000"  # Black
    ON_BACKGROUND = "#212121"  # Near black
    ON_SURFACE = "#212121"  # Near black
    ON_ERROR = "#FFFFFF"  # White

    # Dark theme colors - Cosmic Dark Theme
    DARK_PRIMARY = "#BB86FC"  # Lavender
    DARK_PRIMARY_VARIANT = "#4A148C"  # Deep purple
    DARK_SECONDARY = "#00E5FF"  # Bright cyan
    DARK_ACCENT = "#FF4081"  # Pink
    DARK_BACKGROUND = "#121212"  # Very dark gray
    DARK_SURFACE = "#1E1E1E"  # Dark gray
    DARK_ERROR = "#FF5252"  # Bright red
    DARK_ON_PRIMARY = "#000000"  # Black
    DARK_ON_SECONDARY = "#000000"  # Black
    DARK_ON_BACKGROUND = "#FFFFFF"  # White
    DARK_ON_SURFACE = "#FFFFFF"  # White
    DARK_ON_ERROR = "#000000"  # Black

    # Additional colors
    SUCCESS = "#00E676"  # Bright green
    WARNING = "#FFAB00"  # Amber
    INFO = "#2979FF"  # Bright blue

    # Gradient colors
    GRADIENT_START = "#8A2BE2"  # Vivid purple
    GRADIENT_END = "#00CED1"  # Bright turquoise
    DARK_GRADIENT_START = "#4A148C"  # Deep purple
    DARK_GRADIENT_END = "#00E5FF"  # Bright cyan

    # UI element colors
    CARD_BORDER = "#E0E0E0"  # Light gray for borders
    CARD_SHADOW = "#E0E0E0"  # Shadow for cards
    BUTTON_HOVER = "#9C4DFF"  # Lighter purple for button hover
    BUTTON_ACTIVE = "#7B1FA2"  # Darker purple for button active

    # Text shades
    TEXT_PRIMARY = "#212121"  # Primary text
    TEXT_SECONDARY = "#757575"  # Secondary text
    TEXT_DISABLED = "#9E9E9E"  # Disabled text
    TEXT_HINT = "#9E9E9E"  # Hint text

    # For backward compatibility
    LIGHT_GRAY = "#E0E0E0"  # Light gray for borders
    MEDIUM_GRAY = "#9E9E9E"  # Medium gray for disabled text
    DARK_GRAY = "#616161"  # Dark gray for secondary text

# Font configurations
class Fonts:
    # Modern font families
    PRIMARY_FAMILY = "Segoe UI"  # Primary font
    SECONDARY_FAMILY = "Calibri"  # Secondary font
    ACCENT_FAMILY = "Verdana"  # Accent font for special elements
    MONOSPACE_FAMILY = "Consolas"  # For code or fixed-width text

    # Font sizes
    TITLE_SIZE = 28
    HEADING_SIZE = 20
    SUBHEADING_SIZE = 16
    BODY_SIZE = 13
    SMALL_SIZE = 11
    TINY_SIZE = 9

    # Font weights
    TITLE_WEIGHT = "bold"
    HEADING_WEIGHT = "bold"
    NORMAL_WEIGHT = "normal"
    LIGHT_WEIGHT = "normal"

    # For buttons and interactive elements
    BUTTON_SIZE = 12
    BUTTON_WEIGHT = "bold"

    # Line heights
    TITLE_LINE_HEIGHT = 1.2
    BODY_LINE_HEIGHT = 1.5

    # Letter spacing
    NORMAL_SPACING = 0
    WIDE_SPACING = 1

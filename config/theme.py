"""
Theme configuration for the Language Translator application.
Defines colors, fonts, and styling elements for a cohesive visual design.
"""

class ThemeColors:
    """Color palette for the application."""
    # Primary colors
    PRIMARY = "#6200EE"  # Deep purple
    PRIMARY_VARIANT = "#3700B3"  # Darker purple
    SECONDARY = "#03DAC6"  # Teal
    SECONDARY_VARIANT = "#018786"  # Darker teal
    
    # Background colors
    BACKGROUND = "#F5F5F7"  # Light gray background
    SURFACE = "#FFFFFF"  # White surface
    SURFACE_VARIANT = "#F9F9FC"  # Slightly off-white
    
    # Dark mode colors
    DARK_BACKGROUND = "#121212"  # Dark background
    DARK_SURFACE = "#1E1E1E"  # Dark surface
    DARK_SURFACE_VARIANT = "#2D2D2D"  # Slightly lighter dark surface
    
    # Text colors
    ON_PRIMARY = "#FFFFFF"  # White text on primary
    ON_SECONDARY = "#000000"  # Black text on secondary
    ON_BACKGROUND = "#212121"  # Dark text on background
    ON_SURFACE = "#212121"  # Dark text on surface
    ON_DARK_BACKGROUND = "#FFFFFF"  # White text on dark background
    ON_DARK_SURFACE = "#FFFFFF"  # White text on dark surface
    
    # Additional colors
    ERROR = "#B00020"  # Error red
    SUCCESS = "#4CAF50"  # Success green
    WARNING = "#FF9800"  # Warning orange
    INFO = "#2196F3"  # Info blue
    
    # Gray scale
    LIGHT_GRAY = "#E0E0E0"
    MEDIUM_GRAY = "#9E9E9E"
    DARK_GRAY = "#616161"
    
    # Gradient colors (for special elements)
    GRADIENT_START = "#6200EE"  # Start with primary
    GRADIENT_END = "#9D50BB"  # End with lighter purple

class ThemeFonts:
    """Font configurations for the application."""
    # Font families (in order of preference)
    FONT_FAMILY = ("Segoe UI", "Roboto", "Helvetica", "Arial", "sans-serif")
    
    # Font sizes
    LARGE_TITLE = 28
    TITLE = 24
    SUBTITLE = 20
    HEADING = 18
    SUBHEADING = 16
    BODY = 14
    SMALL = 12
    TINY = 10
    
    # Font weights (for reference - Tkinter uses strings)
    # "normal", "bold", "italic", "bold italic"
    
    @classmethod
    def get_font(cls, size, weight="normal"):
        """Get a font tuple with the specified size and weight."""
        return (cls.FONT_FAMILY[0], size, weight)

class ThemeStyles:
    """Style configurations for UI elements."""
    # Button styles
    BUTTON_PADDING_X = 15
    BUTTON_PADDING_Y = 8
    BUTTON_CORNER_RADIUS = 20  # Pill-shaped buttons
    
    # Card styles
    CARD_CORNER_RADIUS = 10
    CARD_PADDING = 20
    CARD_SHADOW = "2px 2px 10px rgba(0, 0, 0, 0.1)"  # CSS-style shadow (for reference)
    
    # Input styles
    INPUT_CORNER_RADIUS = 5
    INPUT_PADDING_X = 10
    INPUT_PADDING_Y = 8
    INPUT_BORDER_WIDTH = 1
    
    # Spacing
    SPACING_TINY = 5
    SPACING_SMALL = 10
    SPACING_MEDIUM = 15
    SPACING_LARGE = 20
    SPACING_XLARGE = 30
    
    # Animation durations (in milliseconds)
    ANIMATION_FAST = 150
    ANIMATION_MEDIUM = 300
    ANIMATION_SLOW = 500
    
    # Hover effects
    HOVER_LIGHTEN_FACTOR = 1.1  # Lighten colors by this factor on hover
    HOVER_SCALE_FACTOR = 1.03  # Scale elements by this factor on hover

# Export all classes for easy importing
__all__ = ['ThemeColors', 'ThemeFonts', 'ThemeStyles']

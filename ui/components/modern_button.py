"""
Modern button component for the Language Translator application.
Provides a custom button with modern styling and hover effects.
"""

import tkinter as tk
from config.theme import ThemeColors, ThemeFonts, ThemeStyles

class ModernButton(tk.Frame):
    """Custom modern button with hover effects and rounded corners."""

    def __init__(self, parent, text, command=None, icon=None, bg_color=ThemeColors.PRIMARY,
                 fg_color=ThemeColors.ON_PRIMARY, font=None, width=None, height=None,
                 corner_radius=ThemeStyles.BUTTON_CORNER_RADIUS, **kwargs):
        """Initialize the modern button."""
        super().__init__(parent, bg=parent.cget('bg'))

        # Store width and height
        self.width = width
        self.height = height

        self.parent = parent
        self.text = text
        self.command = command
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.corner_radius = corner_radius
        self.icon = icon

        # Default font if none provided
        if font is None:
            font = ThemeFonts.get_font(ThemeFonts.BODY, "bold")
        self.font = font

        # Create the canvas for the button
        self.canvas = tk.Canvas(
            self,
            bg=parent.cget('bg'),
            highlightthickness=0,
            **kwargs
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Draw the button
        self.draw_button()

        # Bind events
        self.canvas.bind("<Enter>", self._on_enter)
        self.canvas.bind("<Leave>", self._on_leave)
        self.canvas.bind("<Button-1>", self._on_press)
        self.canvas.bind("<ButtonRelease-1>", self._on_release)

    def draw_button(self):
        """Draw the button on the canvas."""
        # Clear canvas
        self.canvas.delete("all")

        # Get dimensions
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        # Use minimum dimensions if not rendered yet
        if width <= 1:
            width = 120 if self.width is None else self.width
        if height <= 1:
            height = 40 if self.height is None else self.height

        # Draw rounded rectangle
        self.canvas.create_rounded_rectangle(
            2, 2, width-2, height-2,
            radius=self.corner_radius,
            fill=self.bg_color,
            outline=""
        )

        # Draw icon if provided
        if self.icon:
            # This would need to be implemented with PhotoImage
            pass

        # Draw text
        self.canvas.create_text(
            width // 2,
            height // 2,
            text=self.text,
            fill=self.fg_color,
            font=self.font
        )

    def _on_enter(self, event):
        """Handle mouse enter event."""
        # Lighten the button color
        lighter_color = self._lighten_color(self.bg_color)

        # Update the button fill
        self.canvas.itemconfig("rounded_rect", fill=lighter_color)

        # Change cursor to hand
        self.canvas.config(cursor="hand2")

    def _on_leave(self, event):
        """Handle mouse leave event."""
        # Restore original color
        self.canvas.itemconfig("rounded_rect", fill=self.bg_color)

        # Reset cursor
        self.canvas.config(cursor="")

    def _on_press(self, event):
        """Handle mouse press event."""
        # Darken the button color
        darker_color = self._darken_color(self.bg_color)

        # Update the button fill
        self.canvas.itemconfig("rounded_rect", fill=darker_color)

    def _on_release(self, event):
        """Handle mouse release event."""
        # Check if release is within button bounds
        if 0 <= event.x <= self.canvas.winfo_width() and 0 <= event.y <= self.canvas.winfo_height():
            # Execute command if provided
            if self.command:
                self.command()

        # Restore hover color
        lighter_color = self._lighten_color(self.bg_color)
        self.canvas.itemconfig("rounded_rect", fill=lighter_color)

    def _hex_to_rgb(self, hex_color):
        """Convert hex color to RGB tuple."""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def _rgb_to_hex(self, rgb):
        """Convert RGB tuple to hex color."""
        return f'#{int(rgb[0]):02x}{int(rgb[1]):02x}{int(rgb[2]):02x}'

    def _lighten_color(self, hex_color, factor=ThemeStyles.HOVER_LIGHTEN_FACTOR):
        """Lighten a color by a factor."""
        rgb = self._hex_to_rgb(hex_color)
        return self._rgb_to_hex((
            min(255, rgb[0] * factor),
            min(255, rgb[1] * factor),
            min(255, rgb[2] * factor)
        ))

    def _darken_color(self, hex_color, factor=0.9):
        """Darken a color by a factor."""
        rgb = self._hex_to_rgb(hex_color)
        return self._rgb_to_hex((
            rgb[0] * factor,
            rgb[1] * factor,
            rgb[2] * factor
        ))

    def set_text(self, text):
        """Update the button text."""
        self.text = text
        self.draw_button()

    def set_command(self, command):
        """Update the button command."""
        self.command = command

    def set_colors(self, bg_color=None, fg_color=None):
        """Update the button colors."""
        if bg_color:
            self.bg_color = bg_color
        if fg_color:
            self.fg_color = fg_color
        self.draw_button()

# Add rounded rectangle method to Canvas class
tk.Canvas.create_rounded_rectangle = lambda self, x1, y1, x2, y2, radius=25, **kwargs: self.create_polygon(
    x1+radius, y1,
    x2-radius, y1,
    x2, y1,
    x2, y1+radius,
    x2, y2-radius,
    x2, y2,
    x2-radius, y2,
    x1+radius, y2,
    x1, y2,
    x1, y2-radius,
    x1, y1+radius,
    x1, y1,
    smooth=True, **kwargs, tags="rounded_rect"
)

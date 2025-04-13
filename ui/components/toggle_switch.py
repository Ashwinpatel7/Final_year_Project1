"""
Toggle switch component for the Language Translator application.
Provides a custom toggle switch for settings like dark mode.
"""

import tkinter as tk
from config.theme import ThemeColors, ThemeFonts, ThemeStyles

class ToggleSwitch(tk.Frame):
    """Custom toggle switch with modern styling."""
    
    def __init__(self, parent, text="Toggle", command=None, initial_state=False, 
                 width=50, height=24, bg_color=None, **kwargs):
        """Initialize the toggle switch."""
        # Use parent's background if none provided
        if bg_color is None:
            bg_color = parent.cget('bg')
        
        super().__init__(parent, bg=bg_color, **kwargs)
        
        self.parent = parent
        self.text = text
        self.command = command
        self.state = initial_state
        self.width = width
        self.height = height
        
        # Create container frame
        self.container = tk.Frame(self, bg=bg_color)
        self.container.pack(side=tk.LEFT, padx=5)
        
        # Create label
        self.label = tk.Label(
            self.container,
            text=text,
            font=ThemeFonts.get_font(ThemeFonts.BODY),
            bg=bg_color,
            fg=ThemeColors.ON_BACKGROUND
        )
        self.label.pack(side=tk.LEFT, padx=(0, 10))
        
        # Create canvas for the switch
        self.canvas = tk.Canvas(
            self.container,
            width=width,
            height=height,
            bg=bg_color,
            highlightthickness=0
        )
        self.canvas.pack(side=tk.LEFT)
        
        # Draw the switch
        self.draw_switch()
        
        # Bind click event
        self.canvas.bind("<Button-1>", self.toggle)
    
    def draw_switch(self):
        """Draw the toggle switch on the canvas."""
        # Clear canvas
        self.canvas.delete("all")
        
        # Calculate dimensions
        track_height = self.height * 0.6
        track_y = (self.height - track_height) / 2
        
        # Draw track (background)
        track_color = ThemeColors.PRIMARY if self.state else ThemeColors.MEDIUM_GRAY
        self.canvas.create_rounded_rectangle(
            0, track_y,
            self.width, track_y + track_height,
            radius=track_height / 2,
            fill=track_color,
            outline=""
        )
        
        # Calculate thumb position
        thumb_radius = track_height * 0.8
        thumb_padding = (track_height - thumb_radius * 2) / 2
        
        if self.state:
            thumb_x = self.width - thumb_radius - thumb_padding
        else:
            thumb_x = thumb_radius + thumb_padding
        
        thumb_y = self.height / 2
        
        # Draw thumb (circle)
        self.canvas.create_oval(
            thumb_x - thumb_radius, thumb_y - thumb_radius,
            thumb_x + thumb_radius, thumb_y + thumb_radius,
            fill=ThemeColors.ON_PRIMARY if self.state else ThemeColors.ON_BACKGROUND,
            outline=""
        )
    
    def toggle(self, event=None):
        """Toggle the switch state."""
        self.state = not self.state
        self.draw_switch()
        
        if self.command:
            self.command(self.state)
    
    def get(self):
        """Get the current state of the switch."""
        return self.state
    
    def set(self, state):
        """Set the state of the switch."""
        if state != self.state:
            self.state = state
            self.draw_switch()

# Add rounded rectangle method to Canvas class if not already added
if not hasattr(tk.Canvas, 'create_rounded_rectangle'):
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
        smooth=True, **kwargs
    )

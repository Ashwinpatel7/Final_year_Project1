"""
Modern card component for the Language Translator application.
Provides a custom card with modern styling and hover effects.
"""

import tkinter as tk
from config.theme import ThemeColors, ThemeFonts, ThemeStyles

class ModernCard(tk.Frame):
    """Custom modern card with hover effects and rounded corners."""
    
    def __init__(self, parent, title=None, icon=None, bg_color=ThemeColors.SURFACE, 
                 fg_color=ThemeColors.ON_SURFACE, width=None, height=None, 
                 corner_radius=ThemeStyles.CARD_CORNER_RADIUS, on_click=None, **kwargs):
        """Initialize the modern card."""
        # Create a frame with padding
        super().__init__(
            parent, 
            bg=parent.cget('bg'),
            width=width,
            height=height,
            padx=ThemeStyles.SPACING_SMALL,
            pady=ThemeStyles.SPACING_SMALL,
            **kwargs
        )
        
        self.parent = parent
        self.title = title
        self.icon = icon
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.corner_radius = corner_radius
        self.on_click = on_click
        
        # Create the inner frame with rounded corners and shadow effect
        self.inner_frame = tk.Frame(
            self,
            bg=bg_color,
            bd=1,
            relief=tk.SOLID,
            highlightbackground=ThemeColors.LIGHT_GRAY,
            highlightthickness=1
        )
        self.inner_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # Add title if provided
        if title:
            self.title_label = tk.Label(
                self.inner_frame,
                text=title,
                font=ThemeFonts.get_font(ThemeFonts.SUBHEADING, "bold"),
                bg=bg_color,
                fg=fg_color,
                anchor=tk.CENTER
            )
            self.title_label.pack(fill=tk.X, padx=ThemeStyles.SPACING_MEDIUM, pady=ThemeStyles.SPACING_MEDIUM)
        
        # Create content frame
        self.content_frame = tk.Frame(
            self.inner_frame,
            bg=bg_color
        )
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=ThemeStyles.SPACING_MEDIUM, pady=ThemeStyles.SPACING_MEDIUM)
        
        # Add hover effect if on_click is provided
        if on_click:
            self.inner_frame.bind("<Enter>", self._on_enter)
            self.inner_frame.bind("<Leave>", self._on_leave)
            self.inner_frame.bind("<Button-1>", self._on_click)
            self.inner_frame.config(cursor="hand2")
            
            # Make all child widgets also trigger the click event
            for child in self.inner_frame.winfo_children():
                child.bind("<Button-1>", self._on_click)
                child.config(cursor="hand2")
    
    def _on_enter(self, event):
        """Handle mouse enter event."""
        # Add shadow effect (change border color)
        self.inner_frame.config(highlightbackground=ThemeColors.PRIMARY)
        
        # Scale effect is not directly supported in Tkinter, but we can simulate with padding
        self.inner_frame.pack_configure(padx=0, pady=0)
        self.config(padx=ThemeStyles.SPACING_SMALL+2, pady=ThemeStyles.SPACING_SMALL+2)
    
    def _on_leave(self, event):
        """Handle mouse leave event."""
        # Remove shadow effect
        self.inner_frame.config(highlightbackground=ThemeColors.LIGHT_GRAY)
        
        # Reset scale
        self.inner_frame.pack_configure(padx=2, pady=2)
        self.config(padx=ThemeStyles.SPACING_SMALL, pady=ThemeStyles.SPACING_SMALL)
    
    def _on_click(self, event):
        """Handle click event."""
        if self.on_click:
            self.on_click()
    
    def add_widget(self, widget):
        """Add a widget to the card's content area."""
        widget.pack(in_=self.content_frame, fill=tk.BOTH, expand=True)
        
        # If card is clickable, make the widget clickable too
        if self.on_click:
            widget.bind("<Button-1>", self._on_click)
            widget.config(cursor="hand2")
        
        return widget

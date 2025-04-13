"""
Animated button widget for the Language Translator application.
Provides a custom button with animations and hover effects.
"""

import tkinter as tk
import threading
import time
from config import ThemeColors

class AnimatedButton(tk.Frame):
    """Custom animated button widget."""
    
    def __init__(self, parent, text, command, bg_color=ThemeColors.PRIMARY, 
                 fg_color=ThemeColors.ON_PRIMARY, font=None, width=150, height=40,
                 icon=None, animate=True, corner_radius=10, **kwargs):
        """Initialize the animated button."""
        super().__init__(parent, bg=parent.cget('bg'), width=width, height=height)
        
        self.parent = parent
        self.text = text
        self.command = command
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.font = font
        self.icon = icon
        self.animate = animate
        self.corner_radius = corner_radius
        self.is_pulsing = False
        self.pulse_thread = None
        self.original_bg = bg_color
        
        # Create the button
        self.button = tk.Button(
            self, 
            text=text,
            font=font,
            bg=bg_color,
            fg=fg_color,
            bd=0,
            relief=tk.RAISED,
            padx=15,
            pady=8,
            cursor='hand2',
            command=self._on_click,
            **kwargs
        )
        self.button.pack(fill=tk.BOTH, expand=True)
        
        # Add hover effect
        self.button.bind("<Enter>", self._on_enter)
        self.button.bind("<Leave>", self._on_leave)
        
        # Start animation if enabled
        if animate:
            self.start_animation()
    
    def _on_enter(self, event):
        """Handle mouse enter event."""
        hover_color = self._lighten_color(self.bg_color)
        self.button.config(bg=hover_color)
    
    def _on_leave(self, event):
        """Handle mouse leave event."""
        self.button.config(bg=self.bg_color)
    
    def _on_click(self):
        """Handle button click event."""
        # Flash effect
        original_bg = self.button.cget('bg')
        self.button.config(bg=self._lighten_color(original_bg, 1.5))
        
        # Schedule reset after a short delay
        self.after(100, lambda: self.button.config(bg=original_bg))
        
        # Call the command
        if self.command:
            self.command()
    
    def start_animation(self):
        """Start the pulsing animation."""
        if not self.is_pulsing:
            self.is_pulsing = True
            self.pulse_thread = threading.Thread(target=self._pulse_animation, daemon=True)
            self.pulse_thread.start()
    
    def stop_animation(self):
        """Stop the pulsing animation."""
        self.is_pulsing = False
        if self.pulse_thread:
            self.pulse_thread.join(0.1)
    
    def _pulse_animation(self):
        """Animate the button with a pulsing effect."""
        original_color = self.bg_color
        pulse_color = self._lighten_color(original_color)
        
        while self.is_pulsing:
            try:
                # Pulse from original to lighter color
                for i in range(10):
                    if not self.is_pulsing or not self.winfo_exists():
                        return
                    current_color = self._blend_colors(original_color, pulse_color, i/10)
                    self.after_idle(lambda c=current_color: self.button.config(bg=c) if self.winfo_exists() else None)
                    time.sleep(0.05)
                
                # Pulse from lighter back to original color
                for i in range(10):
                    if not self.is_pulsing or not self.winfo_exists():
                        return
                    current_color = self._blend_colors(pulse_color, original_color, i/10)
                    self.after_idle(lambda c=current_color: self.button.config(bg=c) if self.winfo_exists() else None)
                    time.sleep(0.05)
            except Exception:
                # Handle any exceptions to prevent thread crashes
                pass
    
    def set_text(self, text):
        """Update the button text."""
        self.text = text
        self.button.config(text=text)
    
    def set_loading(self, is_loading=True):
        """Set the button to loading state."""
        if is_loading:
            self.original_text = self.button.cget('text')
            self.set_text("⏳ Loading...")
            self.button.config(state=tk.DISABLED)
        else:
            self.set_text(self.original_text)
            self.button.config(state=tk.NORMAL)
    
    def _hex_to_rgb(self, hex_color):
        """Convert hex color to RGB tuple."""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def _rgb_to_hex(self, rgb):
        """Convert RGB tuple to hex color."""
        return f'#{int(rgb[0]):02x}{int(rgb[1]):02x}{int(rgb[2]):02x}'
    
    def _lighten_color(self, hex_color, factor=1.3):
        """Lighten a color by a factor."""
        rgb = self._hex_to_rgb(hex_color)
        return self._rgb_to_hex((
            min(255, rgb[0] * factor),
            min(255, rgb[1] * factor),
            min(255, rgb[2] * factor)
        ))
    
    def _darken_color(self, hex_color, factor=0.7):
        """Darken a color by a factor."""
        rgb = self._hex_to_rgb(hex_color)
        return self._rgb_to_hex((
            rgb[0] * factor,
            rgb[1] * factor,
            rgb[2] * factor
        ))
    
    def _blend_colors(self, color1, color2, ratio):
        """Blend two colors with the given ratio (0-1)."""
        rgb1 = self._hex_to_rgb(color1)
        rgb2 = self._hex_to_rgb(color2)
        
        blended = (
            rgb1[0] * (1 - ratio) + rgb2[0] * ratio,
            rgb1[1] * (1 - ratio) + rgb2[1] * ratio,
            rgb1[2] * (1 - ratio) + rgb2[2] * ratio
        )
        
        return self._rgb_to_hex(blended)

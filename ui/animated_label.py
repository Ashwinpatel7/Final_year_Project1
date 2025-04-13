"""
Animated label widget for the Language Translator application.
Provides a custom label with animations and effects.
"""

import tkinter as tk
import threading
import time

class AnimatedLabel(tk.Frame):
    """Custom animated label widget."""
    
    def __init__(self, parent, text="", font=None, fg_color="#000000", 
                 bg_color=None, width=None, height=None, animation="fade",
                 anchor="center", **kwargs):
        """Initialize the animated label."""
        # If no bg_color is provided, use parent's background
        if bg_color is None:
            bg_color = parent.cget('bg')
        
        super().__init__(parent, bg=bg_color, width=width, height=height)
        
        self.parent = parent
        self.text = text
        self.font = font
        self.fg_color = fg_color
        self.bg_color = bg_color
        self.animation = animation
        self.anchor = anchor
        self.is_animating = False
        self.animation_thread = None
        
        # Create the label
        self.label = tk.Label(
            self, 
            text=text,
            font=font,
            fg=fg_color,
            bg=bg_color,
            anchor=anchor,
            **kwargs
        )
        self.label.pack(fill=tk.BOTH, expand=True)
        
        # Start with 0 opacity if using fade animation
        if animation == "fade":
            self.label.config(fg=bg_color)  # Start invisible
    
    def set_text(self, text, animate=True):
        """Update the label text with animation."""
        self.text = text
        
        if animate and self.animation == "fade":
            self._animate_text_change(text)
        elif animate and self.animation == "typewriter":
            self._animate_typewriter(text)
        else:
            self.label.config(text=text)
    
    def _animate_text_change(self, new_text):
        """Animate text change with a fade effect."""
        # Stop any ongoing animation
        self.is_animating = False
        if self.animation_thread and self.animation_thread.is_alive():
            self.animation_thread.join(0.1)
        
        # Start new animation
        self.is_animating = True
        self.animation_thread = threading.Thread(
            target=self._fade_animation,
            args=(new_text,),
            daemon=True
        )
        self.animation_thread.start()
    
    def _fade_animation(self, new_text):
        """Perform fade out/in animation."""
        try:
            # Fade out
            for i in range(10, -1, -1):
                if not self.is_animating or not self.winfo_exists():
                    return
                
                # Calculate intermediate color
                fade_color = self._blend_colors(self.fg_color, self.bg_color, i/10)
                
                # Update on main thread
                self.after_idle(lambda c=fade_color: 
                    self.label.config(fg=c) if self.winfo_exists() else None)
                
                time.sleep(0.02)
            
            # Change text
            self.after_idle(lambda t=new_text: 
                self.label.config(text=t) if self.winfo_exists() else None)
            
            # Fade in
            for i in range(11):
                if not self.is_animating or not self.winfo_exists():
                    return
                
                # Calculate intermediate color
                fade_color = self._blend_colors(self.bg_color, self.fg_color, i/10)
                
                # Update on main thread
                self.after_idle(lambda c=fade_color: 
                    self.label.config(fg=c) if self.winfo_exists() else None)
                
                time.sleep(0.02)
        except Exception:
            # Handle any exceptions to prevent thread crashes
            pass
    
    def _animate_typewriter(self, new_text):
        """Animate text change with a typewriter effect."""
        # Stop any ongoing animation
        self.is_animating = False
        if self.animation_thread and self.animation_thread.is_alive():
            self.animation_thread.join(0.1)
        
        # Start new animation
        self.is_animating = True
        self.animation_thread = threading.Thread(
            target=self._typewriter_animation,
            args=(new_text,),
            daemon=True
        )
        self.animation_thread.start()
    
    def _typewriter_animation(self, new_text):
        """Perform typewriter animation."""
        try:
            # Clear the label first
            self.after_idle(lambda: 
                self.label.config(text="") if self.winfo_exists() else None)
            
            # Type out the new text character by character
            for i in range(len(new_text) + 1):
                if not self.is_animating or not self.winfo_exists():
                    return
                
                current_text = new_text[:i]
                
                # Update on main thread
                self.after_idle(lambda t=current_text: 
                    self.label.config(text=t) if self.winfo_exists() else None)
                
                # Adjust typing speed based on character
                delay = 0.05
                if i < len(new_text) and new_text[i-1] in ['.', '!', '?', ',', ';', ':']:
                    delay = 0.15
                
                time.sleep(delay)
        except Exception:
            # Handle any exceptions to prevent thread crashes
            pass
    
    def _hex_to_rgb(self, hex_color):
        """Convert hex color to RGB tuple."""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def _rgb_to_hex(self, rgb):
        """Convert RGB tuple to hex color."""
        return f'#{int(rgb[0]):02x}{int(rgb[1]):02x}{int(rgb[2]):02x}'
    
    def _blend_colors(self, color1, color2, ratio):
        """Blend two colors with the given ratio (0-1)."""
        try:
            rgb1 = self._hex_to_rgb(color1)
            rgb2 = self._hex_to_rgb(color2)
            
            blended = (
                rgb1[0] * (1 - ratio) + rgb2[0] * ratio,
                rgb1[1] * (1 - ratio) + rgb2[1] * ratio,
                rgb1[2] * (1 - ratio) + rgb2[2] * ratio
            )
            
            return self._rgb_to_hex(blended)
        except Exception:
            # Fallback to original color on error
            return color1

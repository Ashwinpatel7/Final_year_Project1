"""
Microphone animation widget for the Language Translator application.
Provides a custom canvas with microphone animation.
"""

import tkinter as tk
import threading
import time
import math
import random
from config import ThemeColors

class MicrophoneAnimation(tk.Canvas):
    """Custom microphone animation widget."""
    
    def __init__(self, parent, width=150, height=150, bg_color=None, 
                 active_color=ThemeColors.ERROR, inactive_color=ThemeColors.MEDIUM_GRAY,
                 **kwargs):
        """Initialize the microphone animation."""
        # If no bg_color is provided, use parent's background
        if bg_color is None:
            bg_color = parent.cget('bg')
        
        super().__init__(
            parent, 
            width=width, 
            height=height, 
            bg=bg_color, 
            highlightthickness=0,
            **kwargs
        )
        
        self.parent = parent
        self.width = width
        self.height = height
        self.bg_color = bg_color
        self.active_color = active_color
        self.inactive_color = inactive_color
        
        self.is_active = False
        self.is_animating = False
        self.animation_thread = None
        self.wave_height = 0
        self.wave_items = []
        
        # Draw initial microphone
        self.draw_microphone(active=False)
        
        # Bind click event
        self.bind("<Button-1>", self.toggle)
    
    def toggle(self, event=None):
        """Toggle the microphone state."""
        self.is_active = not self.is_active
        
        if self.is_active:
            self.start_animation()
        else:
            self.stop_animation()
            self.draw_microphone(active=False)
        
        # Call the command if provided
        if hasattr(self, 'command') and self.command:
            self.command()
    
    def set_active(self, active):
        """Set the microphone state."""
        if active != self.is_active:
            self.toggle()
    
    def draw_microphone(self, active=False):
        """Draw the microphone icon."""
        # Clear canvas
        self.delete("all")
        self.wave_items = []
        
        # Calculate dimensions
        center_x = self.width / 2
        center_y = self.height / 2
        mic_width = self.width / 4
        mic_height = self.height / 2.5
        
        # Draw microphone body
        color = self.active_color if active else self.inactive_color
        
        # Microphone body (rounded rectangle)
        self.create_rounded_rectangle(
            center_x - mic_width/2,
            center_y - mic_height/2,
            center_x + mic_width/2,
            center_y + mic_height/2,
            radius=mic_width/4,
            fill=color,
            outline=""
        )
        
        # Microphone stand
        stand_width = mic_width / 3
        stand_height = mic_height / 3
        self.create_rectangle(
            center_x - stand_width/2,
            center_y + mic_height/2,
            center_x + stand_width/2,
            center_y + mic_height/2 + stand_height,
            fill=color,
            outline=""
        )
        
        # Microphone base
        base_width = mic_width * 1.2
        base_height = stand_height / 2
        self.create_rounded_rectangle(
            center_x - base_width/2,
            center_y + mic_height/2 + stand_height,
            center_x + base_width/2,
            center_y + mic_height/2 + stand_height + base_height,
            radius=base_height/2,
            fill=color,
            outline=""
        )
        
        # Draw sound waves if active
        if active:
            self.draw_sound_waves()
    
    def draw_sound_waves(self):
        """Draw sound waves around the microphone."""
        center_x = self.width / 2
        center_y = self.height / 2
        
        # Clear previous wave items
        for item in self.wave_items:
            self.delete(item)
        self.wave_items = []
        
        # Draw 3 waves with different radii
        wave_radii = [self.width/3, self.width/2.5, self.width/2]
        for radius in wave_radii:
            # Create wave with varying heights
            wave_item = self.create_oval(
                center_x - radius,
                center_y - radius,
                center_x + radius,
                center_y + radius,
                outline=self.active_color,
                width=2,
                dash=(5, 5)
            )
            self.wave_items.append(wave_item)
    
    def start_animation(self):
        """Start the microphone animation."""
        self.is_active = True
        self.draw_microphone(active=True)
        
        if not self.is_animating:
            self.is_animating = True
            self.animation_thread = threading.Thread(
                target=self._run_animation,
                daemon=True
            )
            self.animation_thread.start()
    
    def stop_animation(self):
        """Stop the microphone animation."""
        self.is_animating = False
        self.is_active = False
        if self.animation_thread and self.animation_thread.is_alive():
            self.animation_thread.join(0.1)
    
    def _run_animation(self):
        """Run the animation loop."""
        try:
            while self.is_animating and self.winfo_exists():
                # Animate the waves
                self._animate_waves()
                time.sleep(0.05)
        except Exception:
            # Handle any exceptions to prevent thread crashes
            pass
    
    def _animate_waves(self):
        """Animate the sound waves."""
        if not self.wave_items or not self.winfo_exists():
            return
        
        center_x = self.width / 2
        center_y = self.height / 2
        
        # Animate each wave with different speeds
        for i, item in enumerate(self.wave_items):
            # Calculate new radius with some randomness
            base_radius = (self.width/3) * (i + 1) / len(self.wave_items)
            variation = random.uniform(0.9, 1.1)
            radius = base_radius * variation
            
            # Update wave position
            self.after_idle(lambda i=item, r=radius: 
                self.coords(i, 
                           center_x - r, 
                           center_y - r, 
                           center_x + r, 
                           center_y + r) if self.winfo_exists() else None)
    
    def create_rounded_rectangle(self, x1, y1, x2, y2, radius=25, **kwargs):
        """Create a rounded rectangle on the canvas."""
        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1
        ]
        
        return self.create_polygon(points, smooth=True, **kwargs)
    
    def set_command(self, command):
        """Set the command to be called when the microphone is toggled."""
        self.command = command

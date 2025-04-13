"""
Base screen class for the Language Translator application.
Provides common functionality for all screens.
"""

import tkinter as tk
from tkinter import font as tkfont
import time
from config import ThemeColors, Fonts

class BaseScreen(tk.Frame):
    """Base class for all screens in the application."""

    def __init__(self, parent, controller):
        """Initialize the base screen."""
        tk.Frame.__init__(self, parent, bg=ThemeColors.BACKGROUND)
        self.controller = controller
        self.dark_mode = False

        # Initialize fonts
        self.setup_fonts()

        # Initialize colors based on theme
        self.update_colors()

    def setup_fonts(self):
        """Set up fonts for the screen."""
        self.title_font = tkfont.Font(family=Fonts.PRIMARY_FAMILY, size=Fonts.TITLE_SIZE, weight=Fonts.TITLE_WEIGHT)
        self.heading_font = tkfont.Font(family=Fonts.PRIMARY_FAMILY, size=Fonts.HEADING_SIZE, weight=Fonts.HEADING_WEIGHT)
        self.subheading_font = tkfont.Font(family=Fonts.PRIMARY_FAMILY, size=Fonts.SUBHEADING_SIZE, weight=Fonts.HEADING_WEIGHT)
        self.body_font = tkfont.Font(family=Fonts.SECONDARY_FAMILY, size=Fonts.BODY_SIZE)
        self.small_font = tkfont.Font(family=Fonts.SECONDARY_FAMILY, size=Fonts.SMALL_SIZE)
        self.tiny_font = tkfont.Font(family=Fonts.SECONDARY_FAMILY, size=Fonts.TINY_SIZE)
        self.button_font = tkfont.Font(family=Fonts.ACCENT_FAMILY, size=Fonts.BUTTON_SIZE, weight=Fonts.BUTTON_WEIGHT)
        self.monospace_font = tkfont.Font(family=Fonts.MONOSPACE_FAMILY, size=Fonts.BODY_SIZE)

    def update_colors(self):
        """Update colors based on the current theme."""
        if self.dark_mode:
            self.bg_color = ThemeColors.DARK_BACKGROUND
            self.fg_color = ThemeColors.DARK_ON_BACKGROUND
            self.primary_color = ThemeColors.DARK_PRIMARY
            self.secondary_color = ThemeColors.DARK_SECONDARY
            self.surface_color = ThemeColors.DARK_SURFACE
            self.error_color = ThemeColors.DARK_ERROR
            self.on_primary = ThemeColors.DARK_ON_PRIMARY
            self.on_secondary = ThemeColors.DARK_ON_SECONDARY
            self.on_surface = ThemeColors.DARK_ON_SURFACE
        else:
            self.bg_color = ThemeColors.BACKGROUND
            self.fg_color = ThemeColors.ON_BACKGROUND
            self.primary_color = ThemeColors.PRIMARY
            self.secondary_color = ThemeColors.SECONDARY
            self.surface_color = ThemeColors.SURFACE
            self.error_color = ThemeColors.ERROR
            self.on_primary = ThemeColors.ON_PRIMARY
            self.on_secondary = ThemeColors.ON_SECONDARY
            self.on_surface = ThemeColors.ON_SURFACE

        # Additional colors
        self.success_color = ThemeColors.SUCCESS
        self.warning_color = ThemeColors.WARNING
        self.info_color = ThemeColors.INFO

        # Update the background color of the frame
        self.configure(bg=self.bg_color)

    def toggle_theme(self):
        """Toggle between light and dark themes."""
        self.dark_mode = not self.dark_mode
        self.update_colors()
        self.update_ui_for_theme()

    def update_ui_for_theme(self):
        """Update UI elements for the current theme. To be implemented by subclasses."""
        pass

    def create_header(self, title="Language Translator", subtitle="Translate text between languages"):
        """Create a header with title and subtitle."""
        # Header frame with solid background
        self.header = tk.Frame(self, bg=self.primary_color, height=90)
        self.header.pack(fill=tk.X)

        # Title and subtitle
        title_frame = tk.Frame(self.header, bg=self.primary_color)
        title_frame.pack(side=tk.LEFT, padx=25, pady=10)

        # Logo/icon (placeholder for now)
        logo_text = "FF"
        logo_frame = tk.Frame(title_frame, bg=ThemeColors.ACCENT if not self.dark_mode else ThemeColors.DARK_ACCENT,
                           width=40, height=40, highlightthickness=0)
        logo_frame.pack(side=tk.LEFT, padx=(0, 15))
        logo_frame.pack_propagate(False)

        logo_label = tk.Label(logo_frame, text=logo_text, font=tkfont.Font(family=Fonts.PRIMARY_FAMILY, size=16, weight='bold'),
                            bg=ThemeColors.ACCENT if not self.dark_mode else ThemeColors.DARK_ACCENT, fg='white')
        logo_label.place(relx=0.5, rely=0.5, anchor='center')

        # Title and subtitle
        text_frame = tk.Frame(title_frame, bg=self.primary_color)
        text_frame.pack(side=tk.LEFT)

        self.title_label = tk.Label(text_frame, text=title, font=self.title_font,
                                  bg=self.primary_color, fg=self.on_primary)
        self.title_label.pack(anchor='w')

        self.subtitle_label = tk.Label(text_frame, text=subtitle,
                                     font=self.small_font, bg=self.primary_color,
                                     fg=self.on_primary)
        self.subtitle_label.pack(anchor='w')

        # Right side controls
        self.control_frame = tk.Frame(self.header, bg=self.primary_color)
        self.control_frame.pack(side=tk.RIGHT, padx=25, pady=10)

        # Theme toggle button
        self.theme_btn = tk.Button(self.control_frame, text="☀️" if not self.dark_mode else "🌙",
                                 font=('Segoe UI', 14), command=self.toggle_theme,
                                 bg=self.primary_color, fg=self.on_primary, bd=0,
                                 activebackground=self.primary_color, activeforeground=self.on_primary,
                                 cursor='hand2')
        self.theme_btn.pack(side=tk.RIGHT, padx=10)

    def create_footer(self, status_text="Ready"):
        """Create a footer with status text."""
        # Footer frame
        self.footer = tk.Frame(self, bg=self.surface_color, height=40,
                              highlightbackground=ThemeColors.CARD_BORDER, highlightthickness=1)
        self.footer.pack(fill=tk.X, side=tk.BOTTOM)

        # Status bar
        self.status = tk.Label(self.footer, text=status_text, font=self.small_font,
                             bg=self.surface_color, fg=ThemeColors.TEXT_SECONDARY)
        self.status.pack(side=tk.LEFT, padx=25, pady=10)

        # Version info
        version = tk.Label(self.footer, text="Final Fusion Translator v2.0", font=self.small_font,
                         bg=self.surface_color, fg=ThemeColors.TEXT_SECONDARY)
        version.pack(side=tk.RIGHT, padx=25, pady=10)

    def update_status(self, message, error=False):
        """Update the status message in the footer in a thread-safe way."""
        if hasattr(self, 'status'):
            # Schedule the UI update on the main thread
            def update():
                self.status.config(text=message, fg=self.error_color if error else ThemeColors.TEXT_SECONDARY)
            self.after(0, update)

            if not error:
                # Schedule auto-clear after 5 seconds
                def schedule_clear():
                    import time
                    time.sleep(5)
                    if hasattr(self, 'status') and self.status['text'] == message:
                        def clear():
                            self.status.config(text="Ready", fg=ThemeColors.TEXT_SECONDARY)
                        self.after(0, clear)

                threading = __import__('threading')
                threading.Thread(target=schedule_clear, daemon=True).start()

    def create_modern_button(self, parent, text, command, bg_color=None, fg_color=None,
                           width=None, height=None, padx=15, pady=8,
                           icon=None, is_outlined=False):
        """Create a modern-looking button with hover effect and animations."""
        if bg_color is None:
            bg_color = self.primary_color
        if fg_color is None:
            fg_color = self.on_primary

        # Create a wrapper function to ensure the command is called correctly
        def command_wrapper():
            if command:
                command()

        # Create the actual button directly in the parent
        if is_outlined:
            # Outlined button style
            button = tk.Button(parent, text=text, font=self.button_font, command=command_wrapper,
                             bg=self.bg_color, fg=bg_color, bd=2, padx=padx, pady=pady,
                             activebackground=self.lighten_color(self.bg_color) if not self.dark_mode
                                            else self.darken_color(self.bg_color),
                             activeforeground=bg_color, cursor='hand2', relief=tk.FLAT,
                             highlightbackground=bg_color, highlightthickness=1)
        else:
            # Filled button style
            button = tk.Button(parent, text=text, font=self.button_font, command=command_wrapper,
                             bg=bg_color, fg=fg_color, bd=0, padx=padx, pady=pady,
                             activebackground=self.darken_color(bg_color) if not self.dark_mode
                                            else self.lighten_color(bg_color),
                             activeforeground=fg_color, cursor='hand2', relief=tk.RAISED)

        # Store the original command to prevent garbage collection
        button.original_command = command

        # Set button size if specified
        if width:
            button.config(width=width)
        if height:
            button.config(height=height)

        # Add icon if provided
        if icon:
            button.config(compound=tk.LEFT, padx=padx+5)
            # Icon would be added here if we had image support

        # Add hover effect with smooth transition
        hover_color = self.darken_color(bg_color) if not self.dark_mode else self.lighten_color(bg_color)
        leave_color = bg_color

        if is_outlined:
            hover_color = self.lighten_color(self.bg_color) if not self.dark_mode else self.darken_color(self.bg_color)
            leave_color = self.bg_color

        # Simplified hover effect without animation for better performance
        button.bind("<Enter>", lambda e: button.config(bg=hover_color))
        button.bind("<Leave>", lambda e: button.config(bg=leave_color))

        # Apply rounded corners
        self.round_button_corners(button)

        return button

    def darken_color(self, hex_color, factor=0.8):
        """Darken a color by a factor."""
        # Convert hex to RGB
        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[5:7], 16)

        # Darken
        r = int(r * factor)
        g = int(g * factor)
        b = int(b * factor)

        # Convert back to hex
        return f"#{r:02x}{g:02x}{b:02x}"

    def lighten_color(self, hex_color, factor=1.2):
        """Lighten a color by a factor."""
        # Convert hex to RGB
        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[5:7], 16)

        # Lighten
        r = min(255, int(r * factor))
        g = min(255, int(g * factor))
        b = min(255, int(b * factor))

        # Convert back to hex
        return f"#{r:02x}{g:02x}{b:02x}"

    def hex_to_rgb(self, hex_color):
        """Convert hex color to RGB tuple."""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def draw_gradient(self, canvas, start_color, end_color, width=None, height=None):
        """Draw a horizontal gradient on a canvas."""
        if width is None:
            width = canvas.winfo_width()
            if width <= 1:  # Canvas not rendered yet
                width = 1200

        if height is None:
            height = canvas.winfo_height()
            if height <= 1:  # Canvas not rendered yet
                height = 100

        # Create gradient by drawing many thin rectangles
        start_rgb = self.hex_to_rgb(start_color)
        end_rgb = self.hex_to_rgb(end_color)

        steps = 100
        for i in range(steps):
            # Calculate color for this step
            r = start_rgb[0] + (end_rgb[0] - start_rgb[0]) * i / steps
            g = start_rgb[1] + (end_rgb[1] - start_rgb[1]) * i / steps
            b = start_rgb[2] + (end_rgb[2] - start_rgb[2]) * i / steps
            color = f'#{int(r):02x}{int(g):02x}{int(b):02x}'

            # Draw rectangle
            x0 = i * width / steps
            x1 = (i + 1) * width / steps
            canvas.create_rectangle(x0, 0, x1, height, fill=color, outline=color)

    def round_button_corners(self, button, radius=10):
        """Apply rounded corners to a button (visual effect only)."""
        # This is a simplified version since tkinter doesn't directly support rounded corners
        # For a real implementation, you would need to use a canvas or custom widget
        button.config(relief=tk.FLAT)

        # Add padding to simulate rounded corners
        current_padx = button.cget('padx')
        current_pady = button.cget('pady')
        button.config(padx=current_padx+radius//2, pady=current_pady+radius//2)

    def create_text_with_shadow(self, parent, text, font, fg_color, shadow_color, shadow_offset=2):
        """Create text with shadow effect."""
        frame = tk.Frame(parent, bg=parent.cget('bg'))

        # Shadow label (placed behind)
        shadow = tk.Label(frame, text=text, font=font, fg=shadow_color, bg=parent.cget('bg'))
        shadow.place(x=shadow_offset, y=shadow_offset)

        # Main label
        label = tk.Label(frame, text=text, font=font, fg=fg_color, bg=parent.cget('bg'))
        label.pack()

        return frame

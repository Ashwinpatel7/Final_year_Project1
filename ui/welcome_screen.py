"""
Welcome screen for the Language Translator application.
Displays a menu of available translation options.
"""

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
from config import ThemeColors
from ui.base_screen import BaseScreen
from utils import show_message

class WelcomeScreen(BaseScreen):
    """Welcome screen with menu of translation options."""

    def __init__(self, parent, controller):
        """Initialize the welcome screen."""
        super().__init__(parent, controller)
        self.controller = controller

        # Create UI elements
        self.create_header("Final Fusion Translator", "Advanced Language Translation Suite")
        self.create_content()
        self.create_footer("Welcome! Select a translation option to begin.")

    def create_content(self):
        """Create the main content area with menu options."""
        # Main content frame with padding
        self.content_frame = tk.Frame(self, bg=self.bg_color)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=30)

        # Welcome message
        welcome_label = tk.Label(self.content_frame,
                               text="Welcome to Final Fusion Translator",
                               font=self.heading_font,
                               bg=self.bg_color,
                               fg=self.primary_color)
        welcome_label.pack(pady=(0, 30))

        # Options frame using grid layout
        self.options_frame = tk.Frame(self.content_frame, bg=self.bg_color)
        self.options_frame.pack(fill=tk.BOTH, expand=True)

        # Define the menu options
        options = [
            {
                "title": "Text Translation",
                "description": "Translate text between different languages with advanced options",
                "emoji": "📝",
                "command": lambda: self.controller.show_frame("TranslatorScreen")
            },
            {
                "title": "Voice Translation",
                "description": "Translate spoken language in real-time with speech recognition",
                "emoji": "🎤",
                "command": lambda: self.controller.show_frame("VoiceScreen")
            },
            {
                "title": "Document Translation",
                "description": "Upload and translate documents including PDF, DOCX, and TXT files",
                "emoji": "📄",
                "command": lambda: self.controller.show_frame("DocumentScreen")
            },
            {
                "title": "Image Translation",
                "description": "Extract and translate text from images using OCR technology",
                "emoji": "🖼️",
                "command": lambda: self.controller.show_frame("ImageScreen")
            }
        ]

        # Create option cards
        for i, option in enumerate(options):
            # Calculate grid position (2x2 grid)
            row, col = divmod(i, 2)

            # Create simple card
            card = tk.Frame(self.options_frame, bg=self.surface_color,
                          highlightbackground=self.primary_color,
                          highlightthickness=1, padx=20, pady=20)

            # Position the card
            card.grid(row=row, column=col, padx=20, pady=20, sticky="nsew")

            # Card content frame
            card_content = tk.Frame(card, bg=self.surface_color)
            card_content.pack(fill=tk.BOTH, expand=True)

            # Use emoji as icon
            icon_frame = tk.Frame(card_content, bg=self.surface_color, width=48, height=48)
            icon_frame.pack(side=tk.LEFT, padx=(0, 15))
            icon_frame.pack_propagate(False)

            # Display emoji
            emoji = option.get('emoji', '📄')  # Default to document emoji if not specified
            icon_label = tk.Label(icon_frame, text=emoji, font=("Segoe UI Emoji", 24),
                                bg=self.surface_color, fg=self.primary_color)
            icon_label.pack(fill=tk.BOTH, expand=True)

            # Text content frame
            text_frame = tk.Frame(card_content, bg=self.surface_color)
            text_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            # Option title
            title_label = tk.Label(text_frame, text=option["title"],
                                 font=self.subheading_font,
                                 bg=self.surface_color,
                                 fg=self.fg_color,
                                 anchor="w", justify="left")
            title_label.pack(anchor="w", pady=(0, 5), fill="x")

            # Option description
            desc_label = tk.Label(text_frame, text=option["description"],
                                font=self.small_font,
                                bg=self.surface_color,
                                fg=ThemeColors.TEXT_SECONDARY,
                                wraplength=350, justify="left",
                                anchor="w")
            desc_label.pack(anchor="w", pady=(0, 15), fill="x")

            # Option button
            select_btn = self.create_modern_button(
                text_frame, "Select", option["command"],
                bg_color=self.primary_color,
                fg_color=self.on_primary
            )
            select_btn.pack(anchor="e")

            # Make the entire card clickable
            widgets_to_bind = [card, card_content, text_frame, title_label, desc_label, icon_frame]
            if 'icon_label' in locals():
                widgets_to_bind.append(icon_label)

            for widget in widgets_to_bind:
                widget.bind("<Button-1>", lambda e, cmd=option["command"]: cmd())
                widget.bind("<Enter>", lambda e, c=card: self.on_card_enter(c))
                widget.bind("<Leave>", lambda e, c=card: self.on_card_leave(c))

        # Configure grid weights
        self.options_frame.grid_columnconfigure(0, weight=1)
        self.options_frame.grid_columnconfigure(1, weight=1)
        self.options_frame.grid_rowconfigure(0, weight=1)
        self.options_frame.grid_rowconfigure(1, weight=1)

    def on_card_enter(self, card):
        """Handle mouse enter event on a card."""
        # Change border color
        card.config(highlightbackground=self.secondary_color)
        # Change cursor
        card.config(cursor="hand2")

    def on_card_leave(self, card):
        """Handle mouse leave event on a card."""
        # Restore border color
        card.config(highlightbackground=self.primary_color)
        # Restore cursor
        card.config(cursor="")

    def update_ui_for_theme(self):
        """Update UI elements for the current theme."""
        # Update header
        if hasattr(self, 'header'):
            self.header.config(bg=self.primary_color)
            for child in self.header.winfo_children():
                if isinstance(child, tk.Frame):
                    child.config(bg=self.primary_color)
                    for subchild in child.winfo_children():
                        if isinstance(subchild, tk.Label):
                            subchild.config(bg=self.primary_color, fg=self.on_primary)
                        elif isinstance(subchild, tk.Button):
                            subchild.config(bg=self.primary_color, fg=self.on_primary,
                                          activebackground=self.primary_color,
                                          activeforeground=self.on_primary)

        # Update theme button text
        if hasattr(self, 'theme_btn'):
            self.theme_btn.config(text="🌙" if not self.dark_mode else "☀️")

        # Update content frame
        if hasattr(self, 'content_frame'):
            self.content_frame.config(bg=self.bg_color)
            for child in self.content_frame.winfo_children():
                if isinstance(child, tk.Label):
                    child.config(bg=self.bg_color, fg=self.primary_color)
                elif isinstance(child, tk.Frame):
                    child.config(bg=self.bg_color)

        # Update options frame and cards
        if hasattr(self, 'options_frame'):
            self.options_frame.config(bg=self.bg_color)

            # Update all cards
            for child in self.options_frame.winfo_children():
                if isinstance(child, tk.Frame):  # Card frame
                    child.config(bg=self.surface_color,
                               highlightbackground=self.primary_color if not self.dark_mode else ThemeColors.MEDIUM_GRAY)

                    # Update card contents
                    for card_child in child.winfo_children():
                        if isinstance(card_child, tk.Frame):  # Card content frame
                            card_child.config(bg=self.surface_color)

                            # Update content elements
                            for content_child in card_child.winfo_children():
                                if isinstance(content_child, tk.Frame):  # Icon or text frame
                                    content_child.config(bg=self.surface_color)

                                    # Update labels and buttons in the frames
                                    for element in content_child.winfo_children():
                                        if isinstance(element, tk.Label):
                                            if element.cget("font") == self.subheading_font:
                                                # Title label
                                                element.config(bg=self.surface_color, fg=self.fg_color)
                                            elif element.cget("font") == self.small_font:
                                                # Description label
                                                element.config(bg=self.surface_color,
                                                            fg=ThemeColors.DARK_GRAY if not self.dark_mode else ThemeColors.MEDIUM_GRAY)
                                            else:
                                                # Icon label
                                                element.config(bg=self.surface_color, fg=self.primary_color)
                                        elif isinstance(element, tk.Button):
                                            # Select button
                                            element.config(bg=self.primary_color, fg=self.on_primary,
                                                        activebackground=self.primary_color,
                                                        activeforeground=self.on_primary)

                                            # Update hover bindings
                                            hover_color = self.darken_color(self.primary_color) if not self.dark_mode else self.lighten_color(self.primary_color)
                                            element.bind("<Enter>", lambda e, btn=element: btn.config(bg=hover_color))
                                            element.bind("<Leave>", lambda e, btn=element: btn.config(bg=self.primary_color))

        # Update footer
        if hasattr(self, 'footer'):
            self.footer.config(bg=self.surface_color, highlightbackground=ThemeColors.LIGHT_GRAY)
            for child in self.footer.winfo_children():
                if isinstance(child, tk.Label):
                    child.config(bg=self.surface_color, fg=ThemeColors.MEDIUM_GRAY)

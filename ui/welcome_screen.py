"""
Welcome screen for the Language Translator application.
Displays a menu of available translation options.
"""

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
from config.theme import ThemeColors, ThemeFonts, ThemeStyles
from ui.base_screen import BaseScreen
from ui.components import ModernButton, ModernCard, ToggleSwitch
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
        self.content_frame = tk.Frame(self, bg=ThemeColors.BACKGROUND)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=ThemeStyles.SPACING_XLARGE, pady=ThemeStyles.SPACING_XLARGE)

        # Header container with logo and dark mode toggle
        header_container = tk.Frame(self.content_frame, bg=ThemeColors.BACKGROUND)
        header_container.pack(fill=tk.X, pady=(0, ThemeStyles.SPACING_LARGE))

        # App logo and title
        logo_frame = tk.Frame(header_container, bg=ThemeColors.BACKGROUND)
        logo_frame.pack(side=tk.LEFT)

        # Logo placeholder (would be replaced with actual logo)
        logo_label = tk.Label(
            logo_frame,
            text="FF",
            font=ThemeFonts.get_font(ThemeFonts.LARGE_TITLE, "bold"),
            bg=ThemeColors.PRIMARY,
            fg=ThemeColors.ON_PRIMARY,
            width=2,
            padx=10
        )
        logo_label.pack(side=tk.LEFT, padx=(0, 10))

        # App title
        title_label = tk.Label(
            logo_frame,
            text="Final Fusion",
            font=ThemeFonts.get_font(ThemeFonts.TITLE, "bold"),
            bg=ThemeColors.BACKGROUND,
            fg=ThemeColors.ON_BACKGROUND
        )
        title_label.pack(side=tk.LEFT)

        # Dark mode toggle
        self.dark_mode_toggle = ToggleSwitch(
            header_container,
            text="Dark Mode",
            command=self.toggle_dark_mode,
            initial_state=self.dark_mode,
            bg_color=ThemeColors.BACKGROUND
        )
        self.dark_mode_toggle.pack(side=tk.RIGHT)

        # Welcome message
        welcome_label = tk.Label(
            self.content_frame,
            text="Welcome to Final Fusion Translator",
            font=ThemeFonts.get_font(ThemeFonts.SUBTITLE, "bold"),
            bg=ThemeColors.BACKGROUND,
            fg=ThemeColors.PRIMARY
        )
        welcome_label.pack(pady=(0, ThemeStyles.SPACING_LARGE))

        # Description
        description_label = tk.Label(
            self.content_frame,
            text="Select a translation option to begin your language journey",
            font=ThemeFonts.get_font(ThemeFonts.BODY),
            bg=ThemeColors.BACKGROUND,
            fg=ThemeColors.ON_BACKGROUND
        )
        description_label.pack(pady=(0, ThemeStyles.SPACING_XLARGE))

        # Options frame using grid layout
        self.options_frame = tk.Frame(self.content_frame, bg=ThemeColors.BACKGROUND)
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

            # Create modern card with shadow effect
            card_container = tk.Frame(self.options_frame, bg=ThemeColors.BACKGROUND, padx=2, pady=2)
            card_container.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")

            # Create the actual card with rounded corners (simulated with border)
            card = tk.Frame(card_container,
                          bg=ThemeColors.SURFACE,
                          highlightbackground="#E0E0E0",
                          highlightthickness=1,
                          padx=20, pady=20,
                          relief=tk.RAISED,
                          bd=1)
            card.pack(fill=tk.BOTH, expand=True)

            # Card content frame
            card_content = tk.Frame(card, bg=ThemeColors.SURFACE)
            card_content.pack(fill=tk.BOTH, expand=True)

            # Top row with icon and title
            top_row = tk.Frame(card_content, bg=ThemeColors.SURFACE)
            top_row.pack(fill=tk.X, pady=(0, 10))

            # Use emoji as icon with colored background
            icon_frame = tk.Frame(top_row, bg=ThemeColors.PRIMARY, width=48, height=48)
            icon_frame.pack(side=tk.LEFT, padx=(0, 15))
            icon_frame.pack_propagate(False)

            # Display emoji
            emoji = option.get('emoji', '📄')  # Default to document emoji if not specified
            icon_label = tk.Label(icon_frame, text=emoji, font=("Segoe UI Emoji", 24),
                                bg=ThemeColors.PRIMARY, fg="white")
            icon_label.place(relx=0.5, rely=0.5, anchor="center")

            # Option title with better typography
            title_label = tk.Label(top_row, text=option["title"],
                                 font=("Segoe UI", 16, "bold"),
                                 bg=ThemeColors.SURFACE,
                                 fg="#212121",
                                 anchor="w", justify="left")
            title_label.pack(side=tk.LEFT, fill="x", expand=True)

            # Option description with better typography and spacing
            desc_label = tk.Label(card_content, text=option["description"],
                                font=("Segoe UI", 12),
                                bg=ThemeColors.SURFACE,
                                fg="#616161",
                                wraplength=350, justify="left",
                                anchor="w")
            desc_label.pack(fill="x", pady=(0, 15))

            # Button container for alignment
            button_container = tk.Frame(card_content, bg=ThemeColors.SURFACE)
            button_container.pack(fill=tk.X)

            # Modern pill-shaped button
            select_btn = tk.Button(
                button_container,
                text="Select",
                font=("Segoe UI", 12, "bold"),
                bg=ThemeColors.PRIMARY,
                fg="white",
                padx=20,
                pady=8,
                relief=tk.FLAT,
                bd=0,
                command=option["command"]
            )
            select_btn.pack(side=tk.RIGHT)

            # Make the entire card clickable with modern hover effects
            widgets_to_bind = [card_container, card, card_content, top_row, title_label, desc_label, icon_frame, button_container]
            if 'icon_label' in locals():
                widgets_to_bind.append(icon_label)
            # Note: text_frame is no longer used in our new design

            for widget in widgets_to_bind:
                widget.bind("<Button-1>", lambda e, cmd=option["command"]: cmd())
                widget.bind("<Enter>", lambda e, c=card, cc=card_container, sb=select_btn: self.on_modern_card_enter(c, cc, sb))
                widget.bind("<Leave>", lambda e, c=card, cc=card_container, sb=select_btn: self.on_modern_card_leave(c, cc, sb))

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

    def on_modern_card_enter(self, card, card_container, select_btn):
        """Handle mouse enter event on a modern card."""
        # Add shadow effect by increasing padding
        card_container.config(padx=4, pady=4)

        # Change border color to primary color
        card.config(highlightbackground=ThemeColors.PRIMARY)

        # Highlight the button
        select_btn.config(bg="#7B1FA2")  # Slightly darker purple

        # Change cursor
        card.config(cursor="hand2")

    def on_modern_card_leave(self, card, card_container, select_btn):
        """Handle mouse leave event on a modern card."""
        # Remove shadow effect
        card_container.config(padx=2, pady=2)

        # Restore border color
        card.config(highlightbackground="#E0E0E0")

        # Restore button color
        select_btn.config(bg=ThemeColors.PRIMARY)

        # Restore cursor
        card.config(cursor="")

    def update_ui_for_theme(self):
        """Update UI elements for the current theme."""
        # Update background colors based on theme
        bg_color = ThemeColors.DARK_BACKGROUND if self.dark_mode else ThemeColors.BACKGROUND
        surface_color = ThemeColors.DARK_SURFACE if self.dark_mode else ThemeColors.SURFACE
        text_color = ThemeColors.ON_DARK_BACKGROUND if self.dark_mode else ThemeColors.ON_BACKGROUND

        # Update main content frame
        if hasattr(self, 'content_frame'):
            self.content_frame.config(bg=bg_color)

            # Update header container
            for child in self.content_frame.winfo_children():
                if isinstance(child, tk.Frame):
                    child.config(bg=bg_color)

                    # Update elements in the header
                    for subchild in child.winfo_children():
                        if isinstance(subchild, tk.Label):
                            # Don't change the logo label
                            if subchild.cget("text") != "FF":
                                subchild.config(bg=bg_color, fg=text_color)
                        elif isinstance(subchild, tk.Frame):
                            subchild.config(bg=bg_color)

                            # Update nested elements
                            for element in subchild.winfo_children():
                                if isinstance(element, tk.Label):
                                    if element.cget("text") != "FF":
                                        element.config(bg=bg_color, fg=text_color)
                        elif isinstance(subchild, ToggleSwitch):
                            # Update toggle switch background
                            subchild.container.config(bg=bg_color)
                            subchild.label.config(bg=bg_color, fg=text_color)
                elif isinstance(child, tk.Label):
                    # Update welcome and description labels
                    if child.cget("text").startswith("Welcome"):
                        child.config(bg=bg_color, fg=ThemeColors.PRIMARY)
                    else:
                        child.config(bg=bg_color, fg=text_color)

        # Update header
        if hasattr(self, 'header'):
            header_bg = ThemeColors.PRIMARY_VARIANT if self.dark_mode else ThemeColors.PRIMARY
            self.header.config(bg=header_bg)
            for child in self.header.winfo_children():
                if isinstance(child, tk.Frame):
                    child.config(bg=header_bg)
                    for subchild in child.winfo_children():
                        if isinstance(subchild, tk.Label):
                            subchild.config(bg=header_bg, fg=ThemeColors.ON_PRIMARY)
                        elif isinstance(subchild, tk.Button):
                            subchild.config(bg=header_bg, fg=ThemeColors.ON_PRIMARY,
                                          activebackground=header_bg,
                                          activeforeground=ThemeColors.ON_PRIMARY)

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
            self.options_frame.config(bg=bg_color)

            # Update all card containers
            for card_container in self.options_frame.winfo_children():
                if isinstance(card_container, tk.Frame):
                    # Update card container background
                    card_container.config(bg=bg_color)

                    # Update the actual card
                    for card in card_container.winfo_children():
                        if isinstance(card, tk.Frame):
                            # Update card background and border
                            card.config(bg=surface_color, highlightbackground="#555555" if self.dark_mode else "#E0E0E0")

                            # Update card content
                            for content_child in card.winfo_children():
                                if isinstance(content_child, tk.Frame):
                                    content_child.config(bg=surface_color)

                                    # Update all elements in the card content
                                    for element in content_child.winfo_children():
                                        if isinstance(element, tk.Frame):
                                            # Top row or button container
                                            element.config(bg=surface_color)

                                            # Update elements in the frame
                                            for sub_element in element.winfo_children():
                                                if isinstance(sub_element, tk.Label):
                                                    # Title label
                                                    if "Title" in sub_element.cget("text"):
                                                        sub_element.config(bg=surface_color, fg="#E0E0E0" if self.dark_mode else "#212121")
                                                elif isinstance(sub_element, tk.Frame):
                                                    # Icon frame
                                                    sub_element.config(bg=ThemeColors.PRIMARY)

                                                    # Update icon label
                                                    for icon in sub_element.winfo_children():
                                                        if isinstance(icon, tk.Label):
                                                            icon.config(bg=ThemeColors.PRIMARY, fg="white")
                                                elif isinstance(sub_element, tk.Button):
                                                    # Select button - keep primary color
                                                    pass
                                        elif isinstance(element, tk.Label):
                                            # Description label
                                            element.config(bg=surface_color, fg="#AAAAAA" if self.dark_mode else "#616161")
                                        elif isinstance(element, tk.Button):
                                            # Select button
                                            element.config(bg=ThemeColors.PRIMARY, fg="white")

        # Update footer
        if hasattr(self, 'footer'):
            self.footer.config(bg=self.surface_color, highlightbackground=ThemeColors.LIGHT_GRAY)
            for child in self.footer.winfo_children():
                if isinstance(child, tk.Label):
                    child.config(bg=self.surface_color, fg=ThemeColors.MEDIUM_GRAY)

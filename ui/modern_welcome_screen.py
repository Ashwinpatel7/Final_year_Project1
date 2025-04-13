"""
Modern welcome screen for the Language Translator application.
Displays a menu of available translation options with modern UI components.
"""

import tkinter as tk
from config.theme import ThemeColors, ThemeFonts, ThemeStyles
from ui.base_screen import BaseScreen
from ui.components import ModernButton, ModernCard, ToggleSwitch
from utils import show_message

class ModernWelcomeScreen(BaseScreen):
    """Modern welcome screen with menu of translation options."""

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
                "description": "Record speech and translate it to different languages",
                "emoji": "🎤",
                "command": lambda: self.controller.show_frame("VoiceScreen")
            },
            {
                "title": "Document Translation",
                "description": "Upload and translate documents in various formats",
                "emoji": "📄",
                "command": lambda: self.controller.show_frame("DocumentScreen")
            },
            {
                "title": "Image Translation",
                "description": "Extract and translate text from images",
                "emoji": "🖼️",
                "command": lambda: self.controller.show_frame("ImageScreen")
            }
        ]

        # Create option cards
        for i, option in enumerate(options):
            # Calculate grid position (2x2 grid)
            row, col = divmod(i, 2)
            
            # Get emoji from option
            emoji = option.get("emoji", "📄")  # Default to document emoji
            
            # Create a modern card
            card = ModernCard(
                self.options_frame,
                bg_color=ThemeColors.SURFACE,
                fg_color=ThemeColors.ON_SURFACE,
                corner_radius=ThemeStyles.CARD_CORNER_RADIUS,
                on_click=option["command"]
            )
            card.grid(row=row, column=col, sticky="nsew", padx=ThemeStyles.SPACING_MEDIUM, pady=ThemeStyles.SPACING_MEDIUM)
            
            # Create content frame
            content_frame = tk.Frame(card.content_frame, bg=ThemeColors.SURFACE)
            content_frame.pack(fill=tk.BOTH, expand=True, padx=ThemeStyles.SPACING_MEDIUM, pady=ThemeStyles.SPACING_MEDIUM)
            
            # Create top row with icon and title
            top_row = tk.Frame(content_frame, bg=ThemeColors.SURFACE)
            top_row.pack(fill=tk.X, pady=(0, ThemeStyles.SPACING_SMALL))
            
            # Emoji icon
            icon_label = tk.Label(
                top_row, 
                text=emoji, 
                font=("Segoe UI Emoji", 28),
                bg=ThemeColors.SURFACE, 
                fg=ThemeColors.PRIMARY,
                width=2
            )
            icon_label.pack(side=tk.LEFT, padx=(0, ThemeStyles.SPACING_SMALL))
            
            # Option title
            title_label = tk.Label(
                top_row, 
                text=option["title"],
                font=ThemeFonts.get_font(ThemeFonts.SUBHEADING, "bold"),
                bg=ThemeColors.SURFACE,
                fg=ThemeColors.ON_SURFACE,
                anchor="w"
            )
            title_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            # Option description
            desc_label = tk.Label(
                content_frame, 
                text=option["description"],
                font=ThemeFonts.get_font(ThemeFonts.BODY),
                bg=ThemeColors.SURFACE,
                fg=ThemeColors.DARK_GRAY,
                wraplength=350, 
                justify="left",
                anchor="w"
            )
            desc_label.pack(fill=tk.X, pady=ThemeStyles.SPACING_SMALL)
            
            # Button container for alignment
            button_container = tk.Frame(content_frame, bg=ThemeColors.SURFACE)
            button_container.pack(fill=tk.X, pady=ThemeStyles.SPACING_SMALL)
            
            # Select button
            select_btn = ModernButton(
                button_container,
                text="Select",
                command=option["command"],
                bg_color=ThemeColors.PRIMARY,
                fg_color=ThemeColors.ON_PRIMARY,
                font=ThemeFonts.get_font(ThemeFonts.BODY, "bold"),
                corner_radius=ThemeStyles.BUTTON_CORNER_RADIUS
            )
            select_btn.pack(side=tk.RIGHT)

        # Configure grid weights
        self.options_frame.grid_columnconfigure(0, weight=1)
        self.options_frame.grid_columnconfigure(1, weight=1)
        self.options_frame.grid_rowconfigure(0, weight=1)
        self.options_frame.grid_rowconfigure(1, weight=1)

    def toggle_dark_mode(self, state=None):
        """Toggle between light and dark mode."""
        if state is not None:
            self.dark_mode = state
        else:
            self.dark_mode = not self.dark_mode
        
        # Update UI colors
        self.update_theme()
        
        # Update the toggle switch state if needed
        if hasattr(self, 'dark_mode_toggle') and self.dark_mode_toggle.get() != self.dark_mode:
            self.dark_mode_toggle.set(self.dark_mode)
    
    def update_theme(self):
        """Update the UI colors based on the current theme."""
        # Update background colors
        bg_color = ThemeColors.DARK_BACKGROUND if self.dark_mode else ThemeColors.BACKGROUND
        surface_color = ThemeColors.DARK_SURFACE if self.dark_mode else ThemeColors.SURFACE
        fg_color = ThemeColors.ON_DARK_BACKGROUND if self.dark_mode else ThemeColors.ON_BACKGROUND
        
        # Update main frame
        self.config(bg=bg_color)
        
        # Update content frame
        if hasattr(self, 'content_frame'):
            self.content_frame.config(bg=bg_color)
            
            # Update all direct children of content frame
            for child in self.content_frame.winfo_children():
                if isinstance(child, tk.Frame):
                    child.config(bg=bg_color)
                elif isinstance(child, tk.Label):
                    child.config(bg=bg_color, fg=fg_color)
        
        # Update options frame
        if hasattr(self, 'options_frame'):
            self.options_frame.config(bg=bg_color)
            
            # Update all cards
            for child in self.options_frame.winfo_children():
                if isinstance(child, ModernCard):
                    # Update card colors
                    child.bg_color = surface_color
                    child.fg_color = fg_color
                    child.inner_frame.config(bg=surface_color)
                    
                    # Update all elements in the card
                    for element in child.content_frame.winfo_children():
                        if isinstance(element, tk.Frame):
                            element.config(bg=surface_color)
                            
                            # Update all elements in the frame
                            for sub_element in element.winfo_children():
                                if isinstance(sub_element, tk.Label):
                                    sub_element.config(bg=surface_color)
                                    if 'text' in sub_element.keys() and sub_element['text'] != 'FF':
                                        sub_element.config(fg=fg_color)
                                elif isinstance(sub_element, tk.Frame):
                                    sub_element.config(bg=surface_color)
                                    
                                    # Update buttons in the frame
                                    for button in sub_element.winfo_children():
                                        if isinstance(button, ModernButton):
                                            # Keep button colors as they are
                                            pass
        
        # Update header
        if hasattr(self, 'header'):
            header_bg = ThemeColors.PRIMARY_VARIANT if self.dark_mode else ThemeColors.PRIMARY
            self.header.config(bg=header_bg)
            
            # Update all elements in the header
            for child in self.header.winfo_children():
                child.config(bg=header_bg)
                
                # Update all elements in the child frames
                if isinstance(child, tk.Frame):
                    for element in child.winfo_children():
                        element.config(bg=header_bg)
        
        # Update footer
        if hasattr(self, 'footer'):
            footer_bg = ThemeColors.DARK_SURFACE if self.dark_mode else ThemeColors.SURFACE
            self.footer.config(bg=footer_bg)
            
            # Update all elements in the footer
            for child in self.footer.winfo_children():
                if isinstance(child, tk.Label):
                    child.config(bg=footer_bg, fg=fg_color)

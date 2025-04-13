"""
Text translator screen for the Language Translator application.
Provides functionality to translate text between different languages.
"""

import tkinter as tk
from tkinter import ttk
import threading
from config import ThemeColors, LANGUAGES
from ui.base_screen import BaseScreen
from utils import translate_text, text_to_speech, speech_to_text, copy_to_clipboard, show_message

class TranslatorScreen(BaseScreen):
    """Screen for translating text between languages."""

    def __init__(self, parent, controller):
        """Initialize the translator screen."""
        super().__init__(parent, controller)
        self.controller = controller

        # Speech recognition
        self.recognizer = controller.recognizer
        self.microphone = controller.microphone
        self.is_listening = False

        # Dictionary to store button references
        self.buttons = {}

        # Create UI elements
        self.create_header("Text Translator", "Translate text between different languages")
        self.create_content()
        self.create_footer("Ready to translate")

        # Add back button to header
        self.back_btn = tk.Button(self.control_frame, text="Back to Menu", font=self.button_font,
                               command=lambda: controller.show_frame("WelcomeScreen"),
                               bg=self.primary_color, fg=self.on_primary,
                               bd=0, padx=10, pady=5, cursor='hand2')
        self.back_btn.pack(side=tk.RIGHT, padx=10)

    def create_content(self):
        """Create the main content area with translation interface."""
        # Main container with padding
        self.main_frame = tk.Frame(self, bg=self.bg_color)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)

        # Language selection frame
        self.create_language_selection()

        # Text areas frame
        self.create_text_areas()

        # Button frame
        self.create_button_panel()

    def create_language_selection(self):
        """Create the language selection dropdown menus."""
        self.lang_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        self.lang_frame.pack(fill=tk.X, pady=(0, 15))

        # From language
        from_label = tk.Label(self.lang_frame, text="SOURCE LANGUAGE", font=self.small_font,
                            bg=self.bg_color, fg=ThemeColors.TEXT_SECONDARY)
        from_label.grid(row=0, column=0, sticky=tk.W, padx=(0, 10))

        # Create style for combobox
        self.style = ttk.Style()
        self.update_combobox_style()

        self.from_lang = ttk.Combobox(self.lang_frame, values=['Auto Detect'] + LANGUAGES,
                                     state='readonly', font=self.body_font,
                                     style='Translator.TCombobox')
        self.from_lang.current(0)
        self.from_lang.grid(row=1, column=0, sticky=tk.EW, padx=(0, 20))

        # Swap button
        self.swap_btn = tk.Button(self.lang_frame, text="⇄", font=('Segoe UI', 16, 'bold'),
                                command=self.swap_languages, bg=self.bg_color, fg=self.primary_color,
                                bd=0, padx=8, pady=2, activebackground=self.bg_color,
                                cursor='hand2')
        self.swap_btn.grid(row=1, column=1, padx=5)

        # To language
        to_label = tk.Label(self.lang_frame, text="TARGET LANGUAGE", font=self.small_font,
                          bg=self.bg_color, fg=ThemeColors.TEXT_SECONDARY)
        to_label.grid(row=0, column=2, sticky=tk.W)

        self.to_lang = ttk.Combobox(self.lang_frame, values=LANGUAGES,
                                   state='readonly', font=self.body_font,
                                   style='Translator.TCombobox')
        self.to_lang.current(LANGUAGES.index('English'))
        self.to_lang.grid(row=1, column=2, sticky=tk.EW)

        # Configure grid weights
        self.lang_frame.columnconfigure(0, weight=1)
        self.lang_frame.columnconfigure(2, weight=1)

    def create_text_areas(self):
        """Create the input and output text areas."""
        self.text_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        self.text_frame.pack(fill=tk.BOTH, expand=True)

        # Input text area with shadow effect
        input_outer_frame = tk.Frame(self.text_frame, bg=self.darken_color(self.surface_color, 0.9),
                                   padx=2, pady=2, bd=0)
        input_outer_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        self.input_frame = tk.Frame(input_outer_frame, bg=self.surface_color, bd=0, relief=tk.FLAT,
                                  highlightbackground=ThemeColors.CARD_BORDER, highlightthickness=1)
        self.input_frame.pack(fill=tk.BOTH, expand=True)

        # Input text header
        input_header = tk.Frame(self.input_frame, bg=self.primary_color, height=30)
        input_header.pack(fill=tk.X)

        # Input text label with modern styling
        self.input_label = tk.Label(input_header, text="Enter text to translate",
                                   font=self.small_font, bg=self.primary_color,
                                   fg=self.on_primary, padx=15, pady=5)
        self.input_label.pack(side=tk.LEFT)

        # Input text area with improved styling
        self.input_text = tk.Text(self.input_frame, height=15, font=self.body_font,
                                wrap=tk.WORD, padx=15, pady=15, bd=0,
                                bg=self.surface_color, fg=self.fg_color, insertbackground=self.primary_color,
                                insertwidth=2, relief=tk.FLAT)
        self.input_text.pack(fill=tk.BOTH, expand=True)

        # Input text scrollbar with custom styling
        self.input_scroll = ttk.Scrollbar(self.input_frame, command=self.input_text.yview)
        self.input_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.input_text.config(yscrollcommand=self.input_scroll.set)

        # Output text area with shadow effect
        output_outer_frame = tk.Frame(self.text_frame, bg=self.darken_color(self.surface_color, 0.9),
                                    padx=2, pady=2, bd=0)
        output_outer_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))

        self.output_frame = tk.Frame(output_outer_frame, bg=self.surface_color, bd=0, relief=tk.FLAT,
                                   highlightbackground=ThemeColors.CARD_BORDER, highlightthickness=1)
        self.output_frame.pack(fill=tk.BOTH, expand=True)

        # Output text header
        output_header = tk.Frame(self.output_frame, bg=self.secondary_color, height=30)
        output_header.pack(fill=tk.X)

        # Output text label with modern styling
        self.output_label = tk.Label(output_header, text="Translation",
                                    font=self.small_font, bg=self.secondary_color,
                                    fg=self.on_secondary, padx=15, pady=5)
        self.output_label.pack(side=tk.LEFT)

        # Output text area with improved styling
        self.output_text = tk.Text(self.output_frame, height=15, font=self.body_font,
                                 wrap=tk.WORD, padx=15, pady=15, bd=0,
                                 bg=self.surface_color, fg=self.fg_color, insertbackground=self.primary_color,
                                 insertwidth=2, relief=tk.FLAT)
        self.output_text.pack(fill=tk.BOTH, expand=True)

        # Add a dedicated translate button between input and output - DIRECT APPROACH
        self.translate_btn_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        self.translate_btn_frame.pack(fill=tk.X, pady=10)

        # Create a simple, direct button that will definitely be visible
        self.translate_btn = tk.Button(
            self.translate_btn_frame,
            text="🔄 TRANSLATE NOW",
            font=("Arial", 14, "bold"),
            command=self.translate,
            bg="#FF5722",  # Bright orange
            fg="white",
            padx=20,
            pady=10,
            relief=tk.RAISED,
            bd=2
        )
        self.translate_btn.pack(pady=10, ipadx=10, ipady=5)

        # Output text scrollbar with custom styling
        self.output_scroll = ttk.Scrollbar(self.output_frame, command=self.output_text.yview)
        self.output_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.output_text.config(yscrollcommand=self.output_scroll.set)

        # Bind text change event
        self.input_text.bind('<KeyRelease>', self.update_char_count)

    def create_button_panel(self):
        """Create the button panel with action buttons."""
        self.btn_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        self.btn_frame.pack(fill=tk.X, pady=(15, 0))

        # Buttons with their respective colors and icons
        buttons = [
            ("Translate", self.translate, self.primary_color, "🔄"),
            ("Clear", self.clear, ThemeColors.TEXT_DISABLED, "🗑️"),
            ("Copy", self.copy, self.success_color, "📋"),
            ("Read Aloud", self.text_to_speech, self.warning_color, "🔊"),
            ("Voice Input", self.speech_to_text, self.info_color, "🎤")
        ]

        # Create buttons with modern styling
        for text, command, color, icon in buttons:
            # Create button with icon
            btn_text = f"{icon} {text}" if icon else text

            # Create the button directly
            btn = tk.Button(self.btn_frame, text=btn_text, font=self.button_font,
                          command=command, bg=color,
                          fg=ThemeColors.ON_PRIMARY if color != ThemeColors.TEXT_DISABLED else ThemeColors.ON_BACKGROUND,
                          bd=0, padx=15, pady=8, cursor='hand2', relief=tk.RAISED)

            # Add hover effect
            hover_color = self.lighten_color(color)
            btn.bind("<Enter>", lambda e, b=btn, c=hover_color: b.config(bg=c))
            btn.bind("<Leave>", lambda e, b=btn, c=color: b.config(bg=c))

            # Store a reference to the button
            self.buttons[text] = btn
            btn.pack(side=tk.LEFT, padx=5, pady=5)

        # Character count
        self.char_count = tk.Label(self.btn_frame, text="0 characters", font=self.small_font,
                                  bg=self.bg_color, fg=ThemeColors.TEXT_SECONDARY)
        self.char_count.pack(side=tk.RIGHT)

    def update_combobox_style(self):
        """Update the combobox style based on the current theme."""
        if self.dark_mode:
            self.style.configure('Translator.TCombobox',
                              fieldbackground=self.surface_color,
                              background=self.surface_color,
                              foreground=self.fg_color,
                              selectbackground=self.primary_color,
                              selectforeground=self.on_primary,
                              font=self.body_font,
                              padding=5)

            self.style.map('Translator.TCombobox',
                        fieldbackground=[('readonly', self.surface_color)],
                        selectbackground=[('readonly', self.primary_color)],
                        foreground=[('readonly', self.fg_color)])
        else:
            self.style.configure('Translator.TCombobox',
                              fieldbackground=self.surface_color,
                              background=self.surface_color,
                              foreground=self.fg_color,
                              selectbackground=self.primary_color,
                              selectforeground=self.on_primary,
                              font=self.body_font,
                              padding=5)

            self.style.map('Translator.TCombobox',
                        fieldbackground=[('readonly', self.surface_color)],
                        selectbackground=[('readonly', self.primary_color)],
                        foreground=[('readonly', self.fg_color)])

    def update_ui_for_theme(self):
        """Update UI elements for the current theme."""
        # Update header and footer
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

        # Update main frame
        if hasattr(self, 'main_frame'):
            self.main_frame.config(bg=self.bg_color)

        # Update language frame
        if hasattr(self, 'lang_frame'):
            self.lang_frame.config(bg=self.bg_color)
            for child in self.lang_frame.winfo_children():
                if isinstance(child, tk.Label):
                    child.config(bg=self.bg_color,
                               fg=ThemeColors.DARK_GRAY if not self.dark_mode else ThemeColors.MEDIUM_GRAY)
                elif isinstance(child, tk.Button):  # Swap button
                    child.config(bg=self.bg_color, fg=self.primary_color,
                               activebackground=self.bg_color)

        # Update combobox style
        if hasattr(self, 'style'):
            self.update_combobox_style()

        # Update text frame
        if hasattr(self, 'text_frame'):
            self.text_frame.config(bg=self.bg_color)

        # Update input and output frames
        for frame_name, label_name, text_name in [
            ('input_frame', 'input_label', 'input_text'),
            ('output_frame', 'output_label', 'output_text')
        ]:
            if hasattr(self, frame_name):
                frame = getattr(self, frame_name)
                frame.config(bg=self.surface_color, highlightbackground=ThemeColors.LIGHT_GRAY)

                if hasattr(self, label_name):
                    label = getattr(self, label_name)
                    label.config(bg=self.surface_color,
                               fg=ThemeColors.DARK_GRAY if not self.dark_mode else ThemeColors.MEDIUM_GRAY)

                if hasattr(self, text_name):
                    text = getattr(self, text_name)
                    text.config(bg=self.surface_color, fg=self.fg_color, insertbackground=self.primary_color)

        # Update button frame
        if hasattr(self, 'btn_frame'):
            self.btn_frame.config(bg=self.bg_color)

            # Update character count
            if hasattr(self, 'char_count'):
                self.char_count.config(bg=self.bg_color,
                                     fg=ThemeColors.DARK_GRAY if not self.dark_mode else ThemeColors.MEDIUM_GRAY)

            # Update buttons
            button_colors = [
                self.primary_color,
                ThemeColors.MEDIUM_GRAY,
                self.success_color,
                self.warning_color,
                self.info_color
            ]

            i = 0
            for child in self.btn_frame.winfo_children():
                if isinstance(child, tk.Button) and i < len(button_colors):
                    color = button_colors[i]
                    fg_color = ThemeColors.ON_PRIMARY if color != ThemeColors.MEDIUM_GRAY else ThemeColors.ON_BACKGROUND
                    child.config(bg=color, fg=fg_color, activebackground=color, activeforeground=fg_color)

                    # Update hover bindings
                    hover_color = self.darken_color(color) if not self.dark_mode else self.lighten_color(color)
                    child.bind("<Enter>", lambda e, btn=child, hc=hover_color: btn.config(bg=hc))
                    child.bind("<Leave>", lambda e, btn=child, c=color: btn.config(bg=c))

                    i += 1

        # Update footer
        if hasattr(self, 'footer'):
            self.footer.config(bg=self.surface_color, highlightbackground=ThemeColors.LIGHT_GRAY)
            for child in self.footer.winfo_children():
                if isinstance(child, tk.Label):
                    child.config(bg=self.surface_color, fg=ThemeColors.MEDIUM_GRAY)

    def swap_languages(self):
        """Swap the source and target languages."""
        current_from = self.from_lang.get()
        current_to = self.to_lang.get()

        if current_from != 'Auto Detect':
            self.to_lang.set(current_from)
            self.from_lang.set(current_to)
        else:
            self.to_lang.set('English')
            self.from_lang.set(current_to)

        # Also swap the text content
        input_text = self.input_text.get('1.0', tk.END).strip()
        output_text = self.output_text.get('1.0', tk.END).strip()

        self.input_text.delete('1.0', tk.END)
        self.output_text.delete('1.0', tk.END)

        self.input_text.insert(tk.END, output_text)
        self.output_text.insert(tk.END, input_text)

        self.update_status("Languages swapped")

    def update_char_count(self, event=None):  # event parameter used by event binding
        """Update the character count display."""
        text = self.input_text.get('1.0', 'end-1c')
        count = len(text)
        self.char_count.config(text=f"{count} characters")

    def translate(self):
        """Translate the input text with thread-safe UI updates."""
        try:
            # Show a loading indicator on the translate button
            if hasattr(self, 'translate_btn'):
                original_text = self.translate_btn['text']
                self.after(0, lambda: self.translate_btn.config(text="⏳ Translating..."))

            text = self.input_text.get('1.0', tk.END).strip()
            if not text:
                self.update_status("Please enter text to translate", error=True)
                show_message("Warning", "Please enter text to translate", "warning")
                if hasattr(self, 'translate_btn'):
                    self.after(0, lambda: self.translate_btn.config(text=original_text))
                return

            src_lang = self.from_lang.get()
            dest_lang = self.to_lang.get()

            self.update_status("Translating...")

            def do_translation():
                try:
                    # Perform the actual translation
                    translated = translate_text(text, src_lang, dest_lang)

                    # Schedule UI updates on the main thread
                    self.after(0, lambda: self.output_text.delete('1.0', tk.END))
                    self.after(0, lambda: self.output_text.insert(tk.END, translated))
                    self.after(0, lambda: self.update_status(f"Translated from {src_lang} to {dest_lang}"))

                    # Reset the button text
                    if hasattr(self, 'translate_btn'):
                        self.after(0, lambda: self.translate_btn.config(text=original_text))
                except Exception as e:
                    self.after(0, lambda: self.update_status(f"Translation error: {str(e)}", error=True))
                    self.after(0, lambda: show_message("Error", str(e), "error"))

                    # Reset the button text on error
                    if hasattr(self, 'translate_btn'):
                        self.after(0, lambda: self.translate_btn.config(text=original_text))

            threading.Thread(target=do_translation, daemon=True).start()

        except Exception as e:
            self.update_status(f"Error: {str(e)}", error=True)
            show_message("Error", str(e), "error")

    def clear(self):
        """Clear the input and output text areas."""
        self.input_text.delete('1.0', tk.END)
        self.output_text.delete('1.0', tk.END)
        self.char_count.config(text="0 characters")
        self.update_status("Cleared all text")

    def copy(self):
        """Copy the translated text to clipboard."""
        text = self.output_text.get('1.0', tk.END).strip()
        success, message = copy_to_clipboard(text)

        if success:
            self.update_status("Text copied to clipboard")
            show_message("Success", "Text copied to clipboard", "info")
        else:
            self.update_status(message, error=True)
            show_message("Warning", message, "warning")

    def text_to_speech(self):
        """Convert the translated text to speech."""
        try:
            text = self.output_text.get('1.0', tk.END).strip()
            if not text:
                self.update_status("No translated text to read", error=True)
                show_message("Warning", "No translated text to read", "warning")
                return

            from config import LANGUAGE_CODES
            try:
                lang = LANGUAGE_CODES[self.to_lang.get()]
            except KeyError:
                self.update_status("Language not supported for speech", error=True)
                show_message("Warning", "Selected language is not supported for speech synthesis", "warning")
                return

            self.update_status("Generating speech...")

            def do_tts():
                success, message = text_to_speech(text, lang)
                if success:
                    self.update_status("Speech generated successfully")
                else:
                    self.update_status(message, error=True)
                    show_message("Error", message, "error")

            threading.Thread(target=do_tts, daemon=True).start()

        except Exception as e:
            self.update_status(f"Error: {str(e)}", error=True)
            show_message("Error", str(e), "error")

    def speech_to_text(self):
        """Convert speech to text using the microphone."""
        if self.is_listening:
            self.update_status("Already listening...", error=True)
            return

        try:
            self.is_listening = True
            self.update_status("Listening... Speak now (5 second timeout)")

            def do_stt():
                try:
                    success, result = speech_to_text(self.recognizer, self.microphone)

                    if success:
                        self.input_text.delete('1.0', tk.END)
                        self.input_text.insert(tk.END, result)
                        self.update_status("Speech recognized successfully")
                        self.translate()
                    else:
                        self.update_status(result, error=True)
                        show_message("Error", result, "error")
                finally:
                    self.is_listening = False

            threading.Thread(target=do_stt, daemon=True).start()

        except Exception as e:
            self.is_listening = False
            self.update_status(f"Error: {str(e)}", error=True)
            show_message("Error", str(e), "error")

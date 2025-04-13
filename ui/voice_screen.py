"""
Voice translator screen for the Language Translator application.
Provides functionality to translate spoken language in real-time.
"""

import tkinter as tk
from tkinter import ttk
import threading
import time
from config import ThemeColors, LANGUAGES
from ui.base_screen import BaseScreen
from utils import translate_text, text_to_speech, speech_to_text, copy_to_clipboard, show_message

class VoiceScreen(BaseScreen):
    """Screen for translating spoken language in real-time."""

    def __init__(self, parent, controller):
        """Initialize the voice translator screen."""
        super().__init__(parent, controller)
        self.controller = controller

        # Speech recognition
        self.recognizer = controller.recognizer
        self.microphone = controller.microphone
        self.is_listening = False

        # Voice variables
        self.recognized_text = ""
        self.translated_text = ""

        # Dictionary to store button references
        self.buttons = {}

        # Create UI elements
        self.create_header("Voice Translator", "Translate spoken language in real-time")
        self.create_content()
        self.create_footer("Ready to listen")

        # Add back button to header
        self.back_btn = tk.Button(self.control_frame, text="Back to Menu", font=self.button_font,
                               command=lambda: controller.show_frame("WelcomeScreen"),
                               bg=self.primary_color, fg=self.on_primary,
                               bd=0, padx=10, pady=5, cursor='hand2')
        self.back_btn.pack(side=tk.RIGHT, padx=10)

    def create_content(self):
        """Create the main content area with voice translation interface."""
        # Main container with padding
        self.main_frame = tk.Frame(self, bg=self.bg_color)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)

        # Language selection panel
        self.create_language_panel()

        # Voice recognition panel
        self.create_voice_panel()

        # Translation panel
        self.create_translation_panel()

        # Button panel
        self.create_button_panel()

    def create_language_panel(self):
        """Create the language selection panel."""
        lang_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        lang_frame.pack(fill=tk.X, pady=(0, 20))

        # Create style for combobox
        self.style = ttk.Style()
        self.update_combobox_style()

        # From language
        from_frame = tk.Frame(lang_frame, bg=self.bg_color)
        from_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        from_label = tk.Label(from_frame, text="SOURCE LANGUAGE", font=self.small_font,
                            bg=self.bg_color, fg=ThemeColors.DARK_GRAY if not self.dark_mode else ThemeColors.MEDIUM_GRAY)
        from_label.pack(anchor=tk.W, pady=(0, 5))

        self.from_lang = ttk.Combobox(from_frame, values=['Auto Detect'] + LANGUAGES,
                                     state='readonly', font=self.body_font,
                                     style='Voice.TCombobox')
        self.from_lang.current(0)
        self.from_lang.pack(fill=tk.X)

        # To language
        to_frame = tk.Frame(lang_frame, bg=self.bg_color)
        to_frame.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(10, 0))

        to_label = tk.Label(to_frame, text="TARGET LANGUAGE", font=self.small_font,
                          bg=self.bg_color, fg=ThemeColors.DARK_GRAY if not self.dark_mode else ThemeColors.MEDIUM_GRAY)
        to_label.pack(anchor=tk.W, pady=(0, 5))

        self.to_lang = ttk.Combobox(to_frame, values=LANGUAGES,
                                   state='readonly', font=self.body_font,
                                   style='Voice.TCombobox')
        self.to_lang.current(LANGUAGES.index('English'))
        self.to_lang.pack(fill=tk.X)

    def create_voice_panel(self):
        """Create the voice recognition panel."""
        voice_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        voice_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))

        # Voice status frame
        status_frame = tk.Frame(voice_frame, bg=self.surface_color, bd=1, relief=tk.SOLID,
                              highlightbackground=ThemeColors.LIGHT_GRAY, highlightthickness=1)
        status_frame.pack(fill=tk.X, pady=(0, 15), ipady=20)

        # Voice status label
        self.voice_status = tk.Label(status_frame, text="Click 'Start Listening' to begin",
                                   font=self.heading_font, bg=self.surface_color,
                                   fg=self.fg_color)
        self.voice_status.pack(pady=20)

        # Microphone animation canvas
        self.mic_canvas = tk.Canvas(status_frame, width=100, height=100,
                                  bg=self.surface_color, highlightthickness=0)
        self.mic_canvas.pack()

        # Draw microphone icon
        self.draw_microphone(active=False)

        # Recognized text frame
        recognized_frame = tk.Frame(voice_frame, bg=self.surface_color, bd=1, relief=tk.SOLID,
                                  highlightbackground=ThemeColors.LIGHT_GRAY, highlightthickness=1)
        recognized_frame.pack(fill=tk.BOTH, expand=True)

        # Recognized text label
        recognized_label = tk.Label(recognized_frame, text="Recognized Speech",
                                  font=self.small_font, bg=self.surface_color,
                                  fg=ThemeColors.DARK_GRAY if not self.dark_mode else ThemeColors.MEDIUM_GRAY)
        recognized_label.place(x=15, y=10)

        # Recognized text area
        self.recognized_text_widget = tk.Text(recognized_frame, height=6, font=self.body_font,
                                           wrap=tk.WORD, padx=15, pady=15, bd=0,
                                           bg=self.surface_color, fg=self.fg_color, insertbackground=self.primary_color)
        self.recognized_text_widget.pack(fill=tk.BOTH, expand=True, pady=(30, 0))

        # Recognized text scrollbar
        recognized_scroll = ttk.Scrollbar(recognized_frame, command=self.recognized_text_widget.yview)
        recognized_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.recognized_text_widget.config(yscrollcommand=recognized_scroll.set)

        # Add a direct Start Listening button
        listen_btn_container = tk.Frame(self.main_frame, bg=self.bg_color)
        listen_btn_container.pack(fill=tk.X, pady=10)

        # Create a simple, direct button that will definitely be visible
        self.listen_btn = tk.Button(
            listen_btn_container,
            text="🎤 START LISTENING",
            font=("Arial", 14, "bold"),
            command=self.toggle_listening,
            bg="#FF5722",  # Bright orange
            fg="white",
            padx=20,
            pady=10,
            relief=tk.RAISED,
            bd=2
        )
        self.listen_btn.pack(pady=10, ipadx=10, ipady=5)

        # Add a dedicated translate button - DIRECT APPROACH
        translate_btn_container = tk.Frame(self.main_frame, bg=self.bg_color)
        translate_btn_container.pack(fill=tk.X, pady=10)

        # Create a simple, direct button that will definitely be visible
        self.translate_btn = tk.Button(
            translate_btn_container,
            text="🔄 TRANSLATE SPEECH",
            font=("Arial", 14, "bold"),
            command=self.translate_speech,
            bg="#4CAF50",  # Bright green
            fg="white",
            padx=20,
            pady=10,
            relief=tk.RAISED,
            bd=2
        )
        self.translate_btn.pack(pady=10, ipadx=10, ipady=5)

    def create_translation_panel(self):
        """Create the translation panel."""
        trans_frame = tk.Frame(self.main_frame, bg=self.surface_color, bd=1, relief=tk.SOLID,
                             highlightbackground=ThemeColors.LIGHT_GRAY, highlightthickness=1)
        trans_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))

        # Translation label
        trans_label = tk.Label(trans_frame, text="Translation",
                             font=self.small_font, bg=self.surface_color,
                             fg=ThemeColors.DARK_GRAY if not self.dark_mode else ThemeColors.MEDIUM_GRAY)
        trans_label.place(x=15, y=10)

        # Translation text area
        self.trans_text = tk.Text(trans_frame, height=6, font=self.body_font,
                                wrap=tk.WORD, padx=15, pady=15, bd=0,
                                bg=self.surface_color, fg=self.fg_color, insertbackground=self.primary_color)
        self.trans_text.pack(fill=tk.BOTH, expand=True, pady=(30, 0))

        # Translation text scrollbar
        trans_scroll = ttk.Scrollbar(trans_frame, command=self.trans_text.yview)
        trans_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.trans_text.config(yscrollcommand=trans_scroll.set)

    def create_button_panel(self):
        """Create the button panel with action buttons."""
        self.btn_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        self.btn_frame.pack(fill=tk.X, pady=(0, 0))

        # Buttons with their respective colors
        buttons = [
            ("Start Listening", self.toggle_listening, self.primary_color),
            ("Translate", self.translate_speech, self.primary_color),
            ("Clear", self.clear, ThemeColors.MEDIUM_GRAY),
            ("Copy Translation", self.copy_translation, self.success_color),
            ("Read Aloud", self.read_translation, self.warning_color)
        ]

        # Create buttons
        for text, command, color in buttons:
            # Create the button directly
            btn = tk.Button(self.btn_frame, text=text, font=self.button_font,
                          command=command, bg=color,
                          fg=ThemeColors.ON_PRIMARY if color != ThemeColors.MEDIUM_GRAY else ThemeColors.ON_BACKGROUND,
                          bd=0, padx=15, pady=8, cursor='hand2', relief=tk.RAISED)

            # Add hover effect
            hover_color = self.lighten_color(color)
            btn.bind("<Enter>", lambda e, b=btn, c=hover_color: b.config(bg=c))
            btn.bind("<Leave>", lambda e, b=btn, c=color: b.config(bg=c))

            # Store a reference to the button
            self.buttons[text] = btn
            btn.pack(side=tk.LEFT, padx=5)

        # Store reference to the listen button for toggling
        self.listen_btn = self.buttons["Start Listening"]

    def update_combobox_style(self):
        """Update the combobox style based on the current theme."""
        if self.dark_mode:
            self.style.configure('Voice.TCombobox',
                              fieldbackground=self.surface_color,
                              background=self.surface_color,
                              foreground=self.fg_color,
                              selectbackground=self.primary_color,
                              selectforeground=self.on_primary,
                              font=self.body_font,
                              padding=5)

            self.style.map('Voice.TCombobox',
                        fieldbackground=[('readonly', self.surface_color)],
                        selectbackground=[('readonly', self.primary_color)],
                        foreground=[('readonly', self.fg_color)])
        else:
            self.style.configure('Voice.TCombobox',
                              fieldbackground=self.surface_color,
                              background=self.surface_color,
                              foreground=self.fg_color,
                              selectbackground=self.primary_color,
                              selectforeground=self.on_primary,
                              font=self.body_font,
                              padding=5)

            self.style.map('Voice.TCombobox',
                        fieldbackground=[('readonly', self.surface_color)],
                        selectbackground=[('readonly', self.primary_color)],
                        foreground=[('readonly', self.fg_color)])

    def draw_microphone(self, active=False):
        """Draw a microphone icon on the canvas."""
        self.mic_canvas.delete("all")

        # Microphone base color
        mic_color = self.primary_color if active else ThemeColors.MEDIUM_GRAY

        # Draw microphone body
        self.mic_canvas.create_rectangle(40, 30, 60, 70, fill=mic_color, outline="")

        # Draw microphone top
        self.mic_canvas.create_oval(35, 20, 65, 40, fill=mic_color, outline="")

        # Draw microphone stand
        self.mic_canvas.create_rectangle(48, 70, 52, 80, fill=mic_color, outline="")
        self.mic_canvas.create_oval(40, 80, 60, 90, fill=mic_color, outline="")

        # Draw sound waves if active
        if active:
            # Inner wave
            self.mic_canvas.create_arc(30, 30, 70, 70, start=45, extent=90,
                                     style="arc", outline=self.primary_color, width=2)
            # Middle wave
            self.mic_canvas.create_arc(20, 20, 80, 80, start=45, extent=90,
                                     style="arc", outline=self.primary_color, width=2)
            # Outer wave
            self.mic_canvas.create_arc(10, 10, 90, 90, start=45, extent=90,
                                     style="arc", outline=self.primary_color, width=2)

    def animate_microphone(self):
        """Animate the microphone icon while listening."""
        if not self.is_listening:
            return

        # Toggle between different wave patterns
        for i in range(3):
            if not self.is_listening:
                break

            self.draw_microphone(active=True)
            time.sleep(0.3)

            if not self.is_listening:
                break

            self.mic_canvas.delete("all")
            self.draw_microphone(active=False)
            time.sleep(0.2)

        # Continue animation if still listening
        if self.is_listening:
            self.after(100, self.animate_microphone)

    def update_ui_for_theme(self):
        """Update UI elements for the current theme."""
        # Update header and footer (from BaseScreen)
        super().update_ui_for_theme()

        # Update main frame
        if hasattr(self, 'main_frame'):
            self.main_frame.config(bg=self.bg_color)

            # Update all frames
            for child in self.main_frame.winfo_children():
                if isinstance(child, tk.Frame):
                    child.config(bg=self.bg_color)

                    # Update labels in frames
                    for subchild in child.winfo_children():
                        if isinstance(subchild, tk.Label):
                            subchild.config(bg=self.bg_color,
                                         fg=ThemeColors.DARK_GRAY if not self.dark_mode else ThemeColors.MEDIUM_GRAY)
                        elif isinstance(subchild, tk.Frame):
                            if 'highlightbackground' in subchild.keys():
                                # This is a content frame with border
                                subchild.config(bg=self.surface_color, highlightbackground=ThemeColors.LIGHT_GRAY)

                                # Update elements in content frames
                                for element in subchild.winfo_children():
                                    if isinstance(element, tk.Label):
                                        if element == self.voice_status:
                                            element.config(bg=self.surface_color, fg=self.fg_color)
                                        else:
                                            element.config(bg=self.surface_color,
                                                        fg=ThemeColors.DARK_GRAY if not self.dark_mode else ThemeColors.MEDIUM_GRAY)
                                    elif isinstance(element, tk.Text):
                                        element.config(bg=self.surface_color, fg=self.fg_color,
                                                    insertbackground=self.primary_color)
                                    elif isinstance(element, tk.Canvas):
                                        element.config(bg=self.surface_color)
                                        # Redraw microphone with current theme colors
                                        self.draw_microphone(active=self.is_listening)

        # Update combobox style
        if hasattr(self, 'style'):
            self.update_combobox_style()

        # Update button frame
        if hasattr(self, 'btn_frame'):
            self.btn_frame.config(bg=self.bg_color)

            # Update buttons
            button_colors = [
                self.primary_color,
                self.primary_color,
                ThemeColors.MEDIUM_GRAY,
                self.success_color,
                self.warning_color
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

    def toggle_listening(self):
        """Toggle between listening and not listening states."""
        try:
            if self.is_listening:
                # Stop listening
                self.is_listening = False
                self.listen_btn.config(text="🎤 START LISTENING")
                self.voice_status.config(text="Listening stopped")
                self.draw_microphone(active=False)
                self.update_status("Listening stopped")
            else:
                # Start listening
                self.is_listening = True
                self.listen_btn.config(text="⏹ STOP LISTENING")
                self.voice_status.config(text="Listening... Speak now")
                self.update_status("Listening started - speak now")

                # Start microphone animation
                threading.Thread(target=self.animate_microphone, daemon=True).start()

                # Start speech recognition
                threading.Thread(target=self.listen_for_speech, daemon=True).start()
        except Exception as e:
            self.update_status(f"Error toggling listening: {str(e)}", error=True)
            self.is_listening = False
            self.listen_btn.config(text="🎤 START LISTENING")

    def listen_for_speech(self):
        """Listen for speech and recognize it with thread-safe UI updates."""
        while self.is_listening:
            try:
                # Update UI to show we're listening
                self.after(0, lambda: self.voice_status.config(text="Listening... Speak now"))
                self.after(0, lambda: self.update_status("Listening for speech..."))

                # Call speech_to_text function
                success, result = speech_to_text(self.recognizer, self.microphone)

                if success:
                    # Update recognized text in a thread-safe way
                    self.recognized_text = result
                    self.after(0, lambda: self.recognized_text_widget.delete('1.0', tk.END))
                    self.after(0, lambda: self.recognized_text_widget.insert(tk.END, result))
                    self.after(0, lambda: self.update_status("Speech recognized successfully"))

                    # Auto-translate if text is recognized
                    self.after(0, self.translate_speech)
                else:
                    # If there was an error, update status but continue listening
                    self.after(0, lambda: self.update_status(result, error=True))
            except Exception as e:
                self.after(0, lambda: self.update_status(f"Error: {str(e)}", error=True))
                time.sleep(1)  # Pause before trying again

    def translate_speech(self):
        """Translate the recognized speech with thread-safe UI updates."""
        try:
            # Show a loading indicator on the translate button
            if hasattr(self, 'translate_btn'):
                original_text = self.translate_btn['text']
                self.after(0, lambda: self.translate_btn.config(text="⏳ Translating..."))

            text = self.recognized_text_widget.get('1.0', tk.END).strip()
            if not text:
                self.update_status("No speech to translate", error=True)
                show_message("Error", "Please speak or enter text first", "error")
                if hasattr(self, 'translate_btn'):
                    self.after(0, lambda: self.translate_btn.config(text=original_text))
                return

            src_lang = self.from_lang.get()
            dest_lang = self.to_lang.get()

            self.update_status(f"Translating to {dest_lang}...")

            def do_translation():
                try:
                    # Perform the actual translation
                    translated = translate_text(text, src_lang, dest_lang)
                    self.translated_text = translated

                    # Schedule UI updates on the main thread
                    self.after(0, lambda: self.trans_text.delete('1.0', tk.END))
                    self.after(0, lambda: self.trans_text.insert(tk.END, translated))
                    self.after(0, lambda: self.update_status(f"Speech translated to {dest_lang}"))

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
            if hasattr(self, 'translate_btn'):
                self.after(0, lambda: self.translate_btn.config(text=original_text))

    def clear(self):
        """Clear all text areas."""
        self.recognized_text_widget.delete('1.0', tk.END)
        self.trans_text.delete('1.0', tk.END)
        self.recognized_text = ""
        self.translated_text = ""
        self.update_status("Cleared all text")

    def copy_translation(self):
        """Copy the translated text to clipboard."""
        text = self.trans_text.get('1.0', tk.END).strip()
        success, message = copy_to_clipboard(text)

        if success:
            self.update_status("Translation copied to clipboard")
            show_message("Success", "Translation copied to clipboard", "info")
        else:
            self.update_status(message, error=True)
            show_message("Warning", message, "warning")

    def read_translation(self):
        """Read the translated text aloud."""
        text = self.trans_text.get('1.0', tk.END).strip()
        if not text:
            self.update_status("No translation to read", error=True)
            show_message("Warning", "No translation to read", "warning")
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

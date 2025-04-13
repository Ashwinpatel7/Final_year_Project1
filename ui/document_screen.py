"""
Document translator screen for the Language Translator application.
Provides functionality to translate documents (PDF, DOCX, TXT).
"""

import tkinter as tk
from tkinter import ttk, filedialog
import threading
import os
from config import ThemeColors, LANGUAGES
from ui.base_screen import BaseScreen
from utils import (
    translate_text, copy_to_clipboard, show_message,
    extract_text_from_docx, extract_text_from_pdf
)

class DocumentScreen(BaseScreen):
    """Screen for translating documents."""

    def __init__(self, parent, controller):
        """Initialize the document translator screen."""
        super().__init__(parent, controller)
        self.controller = controller

        # Document variables
        self.file_path = None
        self.file_text = ""
        self.translated_text = ""

        # Dictionary to store button references
        self.buttons = {}

        # Create UI elements
        self.create_header("Document Translator", "Translate PDF, DOCX, and TXT files")
        self.create_content()
        self.create_footer("Ready to translate documents")

        # Add back button to header
        self.back_btn = tk.Button(self.control_frame, text="Back to Menu", font=self.button_font,
                               command=lambda: controller.show_frame("WelcomeScreen"),
                               bg=self.primary_color, fg=self.on_primary,
                               bd=0, padx=10, pady=5, cursor='hand2')
        self.back_btn.pack(side=tk.RIGHT, padx=10)

    def create_content(self):
        """Create the main content area with document translation interface."""
        # Main container with padding
        self.main_frame = tk.Frame(self, bg=self.bg_color)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)

        # Top panel with file selection and language options
        self.create_top_panel()

        # Text areas for document content and translation
        self.create_text_areas()

        # Button panel
        self.create_button_panel()

    def create_top_panel(self):
        """Create the top panel with file selection and language options."""
        top_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        top_frame.pack(fill=tk.X, pady=(0, 15))

        # File selection section
        file_frame = tk.Frame(top_frame, bg=self.bg_color)
        file_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)

        file_label = tk.Label(file_frame, text="DOCUMENT", font=self.small_font,
                            bg=self.bg_color, fg=ThemeColors.MEDIUM_GRAY)
        file_label.pack(anchor=tk.W, pady=(0, 5))

        file_select_frame = tk.Frame(file_frame, bg=self.bg_color)
        file_select_frame.pack(fill=tk.X)

        self.file_entry = tk.Entry(file_select_frame, font=self.body_font,
                                 bg=self.surface_color, fg=self.fg_color,
                                 bd=1, relief=tk.SOLID, highlightthickness=0)
        self.file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        browse_btn = self.create_modern_button(
            file_select_frame, "Browse", self.browse_file,
            bg_color=self.secondary_color,
            fg_color=self.on_secondary
        )
        browse_btn.pack(side=tk.RIGHT)

        # Language selection section
        lang_frame = tk.Frame(top_frame, bg=self.bg_color)
        lang_frame.pack(side=tk.RIGHT, padx=(20, 0))

        # Create style for combobox
        self.style = ttk.Style()
        self.update_combobox_style()

        # Target language
        to_label = tk.Label(lang_frame, text="TARGET LANGUAGE", font=self.small_font,
                          bg=self.bg_color, fg=ThemeColors.MEDIUM_GRAY)
        to_label.pack(anchor=tk.W, pady=(0, 5))

        self.to_lang = ttk.Combobox(lang_frame, values=LANGUAGES,
                                   state='readonly', font=self.body_font,
                                   style='Document.TCombobox', width=20)
        self.to_lang.current(LANGUAGES.index('English'))
        self.to_lang.pack(fill=tk.X)

    def create_text_areas(self):
        """Create the document content and translation text areas."""
        self.text_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        self.text_frame.pack(fill=tk.BOTH, expand=True)

        # Document content area
        self.doc_frame = tk.Frame(self.text_frame, bg=self.surface_color, bd=1, relief=tk.SOLID,
                                highlightbackground=ThemeColors.LIGHT_GRAY, highlightthickness=1)
        self.doc_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        self.doc_text = tk.Text(self.doc_frame, height=15, font=self.body_font,
                              wrap=tk.WORD, padx=15, pady=15, bd=0,
                              bg=self.surface_color, fg=self.fg_color, insertbackground=self.primary_color)
        self.doc_text.pack(fill=tk.BOTH, expand=True)

        # Document text scrollbar
        self.doc_scroll = ttk.Scrollbar(self.doc_frame, command=self.doc_text.yview)
        self.doc_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.doc_text.config(yscrollcommand=self.doc_scroll.set)

        # Document text label
        self.doc_label = tk.Label(self.doc_frame, text="Document Content",
                                font=self.small_font, bg=self.surface_color,
                                fg=ThemeColors.MEDIUM_GRAY)
        self.doc_label.place(x=15, y=10)

        # Add a direct Load Document button
        load_btn_container = tk.Frame(self.main_frame, bg=self.bg_color)
        load_btn_container.pack(fill=tk.X, pady=10)

        # Create a simple, direct button that will definitely be visible
        self.load_btn = tk.Button(
            load_btn_container,
            text="📂 LOAD DOCUMENT",
            font=("Arial", 14, "bold"),
            command=self.browse_file,
            bg="#E91E63",  # Bright pink
            fg="white",
            padx=20,
            pady=10,
            relief=tk.RAISED,
            bd=2
        )
        self.load_btn.pack(pady=10, ipadx=10, ipady=5)

        # Translation area
        self.trans_frame = tk.Frame(self.text_frame, bg=self.surface_color, bd=1, relief=tk.SOLID,
                                  highlightbackground=ThemeColors.LIGHT_GRAY, highlightthickness=1)
        self.trans_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))

        self.trans_text = tk.Text(self.trans_frame, height=15, font=self.body_font,
                                wrap=tk.WORD, padx=15, pady=15, bd=0,
                                bg=self.surface_color, fg=self.fg_color, insertbackground=self.primary_color)
        self.trans_text.pack(fill=tk.BOTH, expand=True)

        # Translation text scrollbar
        self.trans_scroll = ttk.Scrollbar(self.trans_frame, command=self.trans_text.yview)
        self.trans_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.trans_text.config(yscrollcommand=self.trans_scroll.set)

        # Add a dedicated translate button - DIRECT APPROACH
        translate_btn_container = tk.Frame(self.main_frame, bg=self.bg_color)
        translate_btn_container.pack(fill=tk.X, pady=10)

        # Create a simple, direct button that will definitely be visible
        self.translate_btn = tk.Button(
            translate_btn_container,
            text="🔄 TRANSLATE DOCUMENT",
            font=("Arial", 14, "bold"),
            command=self.translate_document,
            bg="#2196F3",  # Bright blue
            fg="white",
            padx=20,
            pady=10,
            relief=tk.RAISED,
            bd=2
        )
        self.translate_btn.pack(pady=10, ipadx=10, ipady=5)

        # Translation text label
        self.trans_label = tk.Label(self.trans_frame, text="Translation",
                                  font=self.small_font, bg=self.surface_color,
                                  fg=ThemeColors.MEDIUM_GRAY)
        self.trans_label.place(x=15, y=10)

    def create_button_panel(self):
        """Create the button panel with action buttons."""
        self.btn_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        self.btn_frame.pack(fill=tk.X, pady=(15, 0))

        # Buttons with their respective colors
        buttons = [
            ("Load Document", self.load_document, self.primary_color),
            ("Translate", self.translate_document, self.primary_color),
            ("Clear", self.clear, ThemeColors.MEDIUM_GRAY),
            ("Copy Translation", self.copy_translation, self.success_color),
            ("Save Translation", self.save_translation, self.info_color)
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

        # File info
        self.file_info = tk.Label(self.btn_frame, text="No file selected", font=self.small_font,
                                bg=self.bg_color, fg=ThemeColors.MEDIUM_GRAY)
        self.file_info.pack(side=tk.RIGHT)

    def update_combobox_style(self):
        """Update the combobox style based on the current theme."""
        if self.dark_mode:
            self.style.configure('Document.TCombobox',
                              fieldbackground=self.surface_color,
                              background=self.surface_color,
                              foreground=self.fg_color,
                              selectbackground=self.primary_color,
                              selectforeground=self.on_primary,
                              font=self.body_font,
                              padding=5)

            self.style.map('Document.TCombobox',
                        fieldbackground=[('readonly', self.surface_color)],
                        selectbackground=[('readonly', self.primary_color)],
                        foreground=[('readonly', self.fg_color)])
        else:
            self.style.configure('Document.TCombobox',
                              fieldbackground=self.surface_color,
                              background=self.surface_color,
                              foreground=self.fg_color,
                              selectbackground=self.primary_color,
                              selectforeground=self.on_primary,
                              font=self.body_font,
                              padding=5)

            self.style.map('Document.TCombobox',
                        fieldbackground=[('readonly', self.surface_color)],
                        selectbackground=[('readonly', self.primary_color)],
                        foreground=[('readonly', self.fg_color)])

    def update_ui_for_theme(self):
        """Update UI elements for the current theme."""
        # Update header and footer (from BaseScreen)
        super().update_ui_for_theme()

        # Update main frame
        if hasattr(self, 'main_frame'):
            self.main_frame.config(bg=self.bg_color)

            # Update all child frames
            for child in self.main_frame.winfo_children():
                if isinstance(child, tk.Frame):
                    child.config(bg=self.bg_color)

                    # Update labels in frames
                    for subchild in child.winfo_children():
                        if isinstance(subchild, tk.Label):
                            subchild.config(bg=self.bg_color,
                                         fg=ThemeColors.DARK_GRAY if not self.dark_mode else ThemeColors.MEDIUM_GRAY)
                        elif isinstance(subchild, tk.Frame):
                            subchild.config(bg=self.bg_color)

                            # Update entry and buttons in subframes
                            for element in subchild.winfo_children():
                                if isinstance(element, tk.Entry):
                                    element.config(bg=self.surface_color, fg=self.fg_color)

        # Update combobox style
        if hasattr(self, 'style'):
            self.update_combobox_style()

        # Update text areas
        for frame_name, label_name, text_name in [
            ('doc_frame', 'doc_label', 'doc_text'),
            ('trans_frame', 'trans_label', 'trans_text')
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

            # Update file info
            if hasattr(self, 'file_info'):
                self.file_info.config(bg=self.bg_color,
                                    fg=ThemeColors.DARK_GRAY if not self.dark_mode else ThemeColors.MEDIUM_GRAY)

            # Update buttons
            button_colors = [
                self.primary_color,
                self.primary_color,
                ThemeColors.MEDIUM_GRAY,
                self.success_color,
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

    def browse_file(self):
        """Open file dialog to select a document."""
        file_types = [
            ("Document Files", "*.pdf;*.docx;*.txt"),
            ("PDF Files", "*.pdf"),
            ("Word Documents", "*.docx"),
            ("Text Files", "*.txt"),
            ("All Files", "*.*")
        ]

        file_path = filedialog.askopenfilename(
            title="Select Document",
            filetypes=file_types
        )

        if file_path:
            self.file_path = file_path
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, file_path)

            # Update file info
            file_name = os.path.basename(file_path)
            file_size = os.path.getsize(file_path) / 1024  # KB

            if file_size < 1024:
                size_str = f"{file_size:.1f} KB"
            else:
                size_str = f"{file_size/1024:.1f} MB"

            self.file_info.config(text=f"{file_name} ({size_str})")

            # Auto-load the document
            self.load_document()

    def load_document(self):
        """Load the selected document and extract text with thread-safe UI updates."""
        try:
            # Show a loading indicator on the button if it exists
            if hasattr(self, 'buttons') and 'Load Document' in self.buttons:
                load_btn = self.buttons['Load Document']
                original_text = load_btn['text']
                self.after(0, lambda: load_btn.config(text="⏳ Loading..."))

            if not self.file_path:
                self.update_status("No document selected", error=True)
                show_message("Error", "Please select a document first", "error")
                # Reset button text
                if hasattr(self, 'buttons') and 'Load Document' in self.buttons:
                    self.after(0, lambda: load_btn.config(text=original_text))
                return

            self.update_status(f"Loading document: {os.path.basename(self.file_path)}...")

            def do_load():
                try:
                    file_ext = os.path.splitext(self.file_path)[1].lower()

                    if file_ext == '.pdf':
                        text = extract_text_from_pdf(self.file_path)
                    elif file_ext == '.docx':
                        text = extract_text_from_docx(self.file_path)
                    elif file_ext == '.txt':
                        with open(self.file_path, 'r', encoding='utf-8') as f:
                            text = f.read()
                    else:
                        raise Exception(f"Unsupported file format: {file_ext}")

                    self.file_text = text

                    # Schedule UI updates on the main thread
                    self.after(0, lambda: self.doc_text.delete('1.0', tk.END))
                    self.after(0, lambda: self.doc_text.insert(tk.END, text))
                    self.after(0, lambda: self.update_status(f"Document loaded successfully: {os.path.basename(self.file_path)}"))

                    # Reset button text
                    if hasattr(self, 'buttons') and 'Load Document' in self.buttons:
                        self.after(0, lambda: load_btn.config(text=original_text))
                except Exception as e:
                    self.after(0, lambda: self.update_status(f"Error loading document: {str(e)}", error=True))
                    self.after(0, lambda: show_message("Error", f"Failed to load document: {str(e)}", "error"))

                    # Reset button text on error
                    if hasattr(self, 'buttons') and 'Load Document' in self.buttons:
                        self.after(0, lambda: load_btn.config(text=original_text))

            threading.Thread(target=do_load, daemon=True).start()

        except Exception as e:
            self.update_status(f"Error: {str(e)}", error=True)
            show_message("Error", str(e), "error")

    def translate_document(self):
        """Translate the loaded document with thread-safe UI updates."""
        try:
            # Show a loading indicator on the translate button
            if hasattr(self, 'translate_btn'):
                original_text = self.translate_btn['text']
                self.after(0, lambda: self.translate_btn.config(text="⏳ Translating..."))

            if not self.file_text:
                self.update_status("No document content to translate", error=True)
                show_message("Error", "Please load a document first", "error")
                if hasattr(self, 'translate_btn'):
                    self.after(0, lambda: self.translate_btn.config(text=original_text))
                return

            dest_lang = self.to_lang.get()
            self.update_status(f"Translating document to {dest_lang}...")

            def do_translation():
                try:
                    # Perform the actual translation
                    translated = translate_text(self.file_text, 'Auto Detect', dest_lang)
                    self.translated_text = translated

                    # Schedule UI updates on the main thread
                    self.after(0, lambda: self.trans_text.delete('1.0', tk.END))
                    self.after(0, lambda: self.trans_text.insert(tk.END, translated))
                    self.after(0, lambda: self.update_status(f"Document translated successfully to {dest_lang}"))

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
        """Clear the document and translation text areas."""
        self.doc_text.delete('1.0', tk.END)
        self.trans_text.delete('1.0', tk.END)
        self.file_text = ""
        self.translated_text = ""
        self.file_path = None
        self.file_entry.delete(0, tk.END)
        self.file_info.config(text="No file selected")
        self.update_status("Cleared all content")

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

    def save_translation(self):
        """Save the translated text to a file."""
        if not self.translated_text:
            self.update_status("No translation to save", error=True)
            show_message("Error", "Please translate a document first", "error")
            return

        file_types = [
            ("Text Files", "*.txt"),
            ("All Files", "*.*")
        ]

        save_path = filedialog.asksaveasfilename(
            title="Save Translation",
            filetypes=file_types,
            defaultextension=".txt"
        )

        if save_path:
            try:
                with open(save_path, 'w', encoding='utf-8') as f:
                    f.write(self.translated_text)

                self.update_status(f"Translation saved to {os.path.basename(save_path)}")
                show_message("Success", f"Translation saved to {save_path}", "info")
            except Exception as e:
                self.update_status(f"Error saving translation: {str(e)}", error=True)
                show_message("Error", f"Failed to save translation: {str(e)}", "error")

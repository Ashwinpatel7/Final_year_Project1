"""
Image translator screen for the Language Translator application.
Provides functionality to extract and translate text from images.
"""

import tkinter as tk
from tkinter import ttk, filedialog
import threading
import os
from PIL import Image, ImageTk
from config import ThemeColors, LANGUAGES
from ui.base_screen import BaseScreen
from utils import translate_text, copy_to_clipboard, show_message, extract_text_from_image

class ImageScreen(BaseScreen):
    """Screen for extracting and translating text from images."""

    def __init__(self, parent, controller):
        """Initialize the image translator screen."""
        super().__init__(parent, controller)
        self.controller = controller

        # Image variables
        self.image_path = None
        self.extracted_text = ""
        self.translated_text = ""
        self.image_preview = None

        # Dictionary to store button references
        self.buttons = {}

        # Create UI elements
        self.create_header("Image Translator", "Extract and translate text from images")
        self.create_content()
        self.create_footer("Ready to process images")

        # Add back button to header
        self.back_btn = tk.Button(self.control_frame, text="Back to Menu", font=self.button_font,
                               command=lambda: controller.show_frame("WelcomeScreen"),
                               bg=self.primary_color, fg=self.on_primary,
                               bd=0, padx=10, pady=5, cursor='hand2')
        self.back_btn.pack(side=tk.RIGHT, padx=10)

    def create_content(self):
        """Create the main content area with image translation interface."""
        # Main container with padding
        self.main_frame = tk.Frame(self, bg=self.bg_color)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)

        # Top panel with file selection and language options
        self.create_top_panel()

        # Middle panel with image preview and extracted text
        self.create_middle_panel()

        # Bottom panel with translation
        self.create_bottom_panel()

        # Button panel
        self.create_button_panel()

    def create_top_panel(self):
        """Create the top panel with file selection and language options."""
        top_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        top_frame.pack(fill=tk.X, pady=(0, 15))

        # File selection section
        file_frame = tk.Frame(top_frame, bg=self.bg_color)
        file_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)

        file_label = tk.Label(file_frame, text="IMAGE", font=self.small_font,
                            bg=self.bg_color, fg=ThemeColors.DARK_GRAY if not self.dark_mode else ThemeColors.MEDIUM_GRAY)
        file_label.pack(anchor=tk.W, pady=(0, 5))

        file_select_frame = tk.Frame(file_frame, bg=self.bg_color)
        file_select_frame.pack(fill=tk.X)

        self.file_entry = tk.Entry(file_select_frame, font=self.body_font,
                                 bg=self.surface_color, fg=self.fg_color,
                                 bd=1, relief=tk.SOLID, highlightthickness=0)
        self.file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        browse_btn = self.create_modern_button(
            file_select_frame, "Browse", self.browse_image,
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
                          bg=self.bg_color, fg=ThemeColors.DARK_GRAY if not self.dark_mode else ThemeColors.MEDIUM_GRAY)
        to_label.pack(anchor=tk.W, pady=(0, 5))

        self.to_lang = ttk.Combobox(lang_frame, values=LANGUAGES,
                                   state='readonly', font=self.body_font,
                                   style='Image.TCombobox', width=20)
        self.to_lang.current(LANGUAGES.index('English'))
        self.to_lang.pack(fill=tk.X)

    def create_middle_panel(self):
        """Create the middle panel with image preview and extracted text."""
        middle_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        middle_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))

        # Image preview section
        preview_frame = tk.Frame(middle_frame, bg=self.surface_color, bd=1, relief=tk.SOLID,
                               highlightbackground=ThemeColors.LIGHT_GRAY, highlightthickness=1)
        preview_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # Image preview label
        preview_label = tk.Label(preview_frame, text="Image Preview",
                               font=self.small_font, bg=self.surface_color,
                               fg=ThemeColors.DARK_GRAY if not self.dark_mode else ThemeColors.MEDIUM_GRAY)
        preview_label.place(x=15, y=10)

        # Image canvas for preview
        self.image_canvas = tk.Canvas(preview_frame, bg=self.surface_color,
                                    bd=0, highlightthickness=0)
        self.image_canvas.pack(fill=tk.BOTH, expand=True, padx=15, pady=35)

        # Placeholder text for canvas
        self.canvas_placeholder = self.image_canvas.create_text(
            200, 150, text="No image selected",
            font=self.body_font, fill=ThemeColors.MEDIUM_GRAY
        )

        # Add a direct Extract Text button
        extract_btn_container = tk.Frame(preview_frame, bg=self.surface_color)
        extract_btn_container.pack(fill=tk.X, pady=10)

        # Create a simple, direct button that will definitely be visible
        self.extract_btn = tk.Button(
            extract_btn_container,
            text="🔍 EXTRACT TEXT",
            font=("Arial", 14, "bold"),
            command=self.extract_text,
            bg="#FF9800",  # Bright orange
            fg="white",
            padx=20,
            pady=10,
            relief=tk.RAISED,
            bd=2
        )
        self.extract_btn.pack(pady=10, ipadx=10, ipady=5)

        # Extracted text section
        extracted_frame = tk.Frame(middle_frame, bg=self.surface_color, bd=1, relief=tk.SOLID,
                                 highlightbackground=ThemeColors.LIGHT_GRAY, highlightthickness=1)
        extracted_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))

        # Extracted text label
        extracted_label = tk.Label(extracted_frame, text="Extracted Text",
                                 font=self.small_font, bg=self.surface_color,
                                 fg=ThemeColors.DARK_GRAY if not self.dark_mode else ThemeColors.MEDIUM_GRAY)
        extracted_label.place(x=15, y=10)

        # Extracted text area
        self.extracted_text_widget = tk.Text(extracted_frame, height=10, font=self.body_font,
                                          wrap=tk.WORD, padx=15, pady=15, bd=0,
                                          bg=self.surface_color, fg=self.fg_color, insertbackground=self.primary_color)
        self.extracted_text_widget.pack(fill=tk.BOTH, expand=True, pady=(30, 0))

        # Extracted text scrollbar
        extracted_scroll = ttk.Scrollbar(extracted_frame, command=self.extracted_text_widget.yview)
        extracted_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.extracted_text_widget.config(yscrollcommand=extracted_scroll.set)

        # Add a dedicated translate button - DIRECT APPROACH
        translate_btn_container = tk.Frame(self.main_frame, bg=self.bg_color)
        translate_btn_container.pack(fill=tk.X, pady=10)

        # Create a simple, direct button that will definitely be visible
        self.translate_btn = tk.Button(
            translate_btn_container,
            text="🔄 TRANSLATE IMAGE TEXT",
            font=("Arial", 14, "bold"),
            command=self.translate_text,
            bg="#9C27B0",  # Bright purple
            fg="white",
            padx=20,
            pady=10,
            relief=tk.RAISED,
            bd=2
        )
        self.translate_btn.pack(pady=10, ipadx=10, ipady=5)

    def create_bottom_panel(self):
        """Create the bottom panel with translation text area."""
        bottom_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        bottom_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))

        # Translation area
        trans_frame = tk.Frame(bottom_frame, bg=self.surface_color, bd=1, relief=tk.SOLID,
                             highlightbackground=ThemeColors.LIGHT_GRAY, highlightthickness=1)
        trans_frame.pack(fill=tk.BOTH, expand=True)

        # Translation label
        trans_label = tk.Label(trans_frame, text="Translation",
                             font=self.small_font, bg=self.surface_color,
                             fg=ThemeColors.DARK_GRAY if not self.dark_mode else ThemeColors.MEDIUM_GRAY)
        trans_label.place(x=15, y=10)

        # Translation text area
        self.trans_text = tk.Text(trans_frame, height=8, font=self.body_font,
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
            ("Extract Text", self.extract_text, self.primary_color),
            ("Translate", self.translate_text, self.primary_color),
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
        self.file_info = tk.Label(self.btn_frame, text="No image selected", font=self.small_font,
                                bg=self.bg_color, fg=ThemeColors.DARK_GRAY if not self.dark_mode else ThemeColors.MEDIUM_GRAY)
        self.file_info.pack(side=tk.RIGHT)

    def update_combobox_style(self):
        """Update the combobox style based on the current theme."""
        if self.dark_mode:
            self.style.configure('Image.TCombobox',
                              fieldbackground=self.surface_color,
                              background=self.surface_color,
                              foreground=self.fg_color,
                              selectbackground=self.primary_color,
                              selectforeground=self.on_primary,
                              font=self.body_font,
                              padding=5)

            self.style.map('Image.TCombobox',
                        fieldbackground=[('readonly', self.surface_color)],
                        selectbackground=[('readonly', self.primary_color)],
                        foreground=[('readonly', self.fg_color)])
        else:
            self.style.configure('Image.TCombobox',
                              fieldbackground=self.surface_color,
                              background=self.surface_color,
                              foreground=self.fg_color,
                              selectbackground=self.primary_color,
                              selectforeground=self.on_primary,
                              font=self.body_font,
                              padding=5)

            self.style.map('Image.TCombobox',
                        fieldbackground=[('readonly', self.surface_color)],
                        selectbackground=[('readonly', self.primary_color)],
                        foreground=[('readonly', self.fg_color)])

    def update_ui_for_theme(self):
        """Update UI elements for the current theme."""
        # Update header and footer (from BaseScreen)
        super().update_ui_for_theme()

        # Update main frame and all its children
        if hasattr(self, 'main_frame'):
            self.main_frame.config(bg=self.bg_color)

            # Update all frames
            for child in self.main_frame.winfo_children():
                if isinstance(child, tk.Frame):
                    child.config(bg=self.bg_color)

                    # Update all elements in each frame
                    for subchild in child.winfo_children():
                        if isinstance(subchild, tk.Label):
                            subchild.config(bg=self.bg_color,
                                         fg=ThemeColors.DARK_GRAY if not self.dark_mode else ThemeColors.MEDIUM_GRAY)
                        elif isinstance(subchild, tk.Frame):
                            if 'highlightbackground' in subchild.keys():
                                # This is a content frame with border
                                subchild.config(bg=self.surface_color, highlightbackground=ThemeColors.LIGHT_GRAY)

                                # Update labels and text widgets in content frames
                                for element in subchild.winfo_children():
                                    if isinstance(element, tk.Label):
                                        element.config(bg=self.surface_color,
                                                    fg=ThemeColors.DARK_GRAY if not self.dark_mode else ThemeColors.MEDIUM_GRAY)
                                    elif isinstance(element, tk.Text):
                                        element.config(bg=self.surface_color, fg=self.fg_color,
                                                    insertbackground=self.primary_color)
                                    elif isinstance(element, tk.Canvas):
                                        element.config(bg=self.surface_color)
                                        # Update canvas placeholder text color
                                        if hasattr(self, 'canvas_placeholder'):
                                            element.itemconfig(self.canvas_placeholder, fill=ThemeColors.MEDIUM_GRAY)
                            else:
                                # This is a regular frame
                                subchild.config(bg=self.bg_color)

                                # Update elements in regular frames
                                for element in subchild.winfo_children():
                                    if isinstance(element, tk.Entry):
                                        element.config(bg=self.surface_color, fg=self.fg_color)

        # Update combobox style
        if hasattr(self, 'style'):
            self.update_combobox_style()

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

        # If we have an image loaded, refresh the preview
        if self.image_path and os.path.exists(self.image_path):
            self.display_image_preview()

    def browse_image(self):
        """Open file dialog to select an image."""
        file_types = [
            ("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif"),
            ("PNG Files", "*.png"),
            ("JPEG Files", "*.jpg;*.jpeg"),
            ("BMP Files", "*.bmp"),
            ("GIF Files", "*.gif"),
            ("All Files", "*.*")
        ]

        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=file_types
        )

        if file_path:
            self.image_path = file_path
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

            # Display image preview
            self.display_image_preview()

    def display_image_preview(self):
        """Display the selected image in the preview canvas."""
        if not self.image_path or not os.path.exists(self.image_path):
            return

        try:
            # Clear canvas
            self.image_canvas.delete("all")

            # Load and resize image for preview
            img = Image.open(self.image_path)

            # Get canvas dimensions
            canvas_width = self.image_canvas.winfo_width()
            canvas_height = self.image_canvas.winfo_height()

            # If canvas hasn't been rendered yet, use default dimensions
            if canvas_width <= 1:
                canvas_width = 400
            if canvas_height <= 1:
                canvas_height = 300

            # Calculate aspect ratio
            img_width, img_height = img.size
            aspect_ratio = img_width / img_height

            # Determine new dimensions to fit in canvas
            if img_width > img_height:
                new_width = min(img_width, canvas_width)
                new_height = int(new_width / aspect_ratio)

                if new_height > canvas_height:
                    new_height = canvas_height
                    new_width = int(new_height * aspect_ratio)
            else:
                new_height = min(img_height, canvas_height)
                new_width = int(new_height * aspect_ratio)

                if new_width > canvas_width:
                    new_width = canvas_width
                    new_height = int(new_width / aspect_ratio)

            # Resize image
            img = img.resize((new_width, new_height), Image.LANCZOS)

            # Convert to PhotoImage
            self.image_preview = ImageTk.PhotoImage(img)

            # Calculate position to center the image
            x_pos = (canvas_width - new_width) // 2
            y_pos = (canvas_height - new_height) // 2

            # Display image
            self.image_canvas.create_image(x_pos, y_pos, anchor=tk.NW, image=self.image_preview)

        except Exception as e:
            self.image_canvas.delete("all")
            self.canvas_placeholder = self.image_canvas.create_text(
                200, 150, text=f"Error loading image: {str(e)}",
                font=self.body_font, fill=self.error_color
            )

    def extract_text(self):
        """Extract text from the selected image with thread-safe UI updates."""
        try:
            # Show a loading indicator on the extract button if it exists
            if hasattr(self, 'buttons') and 'Extract Text' in self.buttons:
                extract_btn = self.buttons['Extract Text']
                original_text = extract_btn['text']
                self.after(0, lambda: extract_btn.config(text="⏳ Extracting..."))

            if not self.image_path:
                self.update_status("No image selected", error=True)
                show_message("Error", "Please select an image first", "error")
                # Reset button text
                if hasattr(self, 'buttons') and 'Extract Text' in self.buttons:
                    self.after(0, lambda: extract_btn.config(text=original_text))
                return

            self.update_status(f"Extracting text from image: {os.path.basename(self.image_path)}...")

            def do_extract():
                try:
                    # Perform the actual text extraction
                    text = extract_text_from_image(self.image_path)
                    self.extracted_text = text

                    # Schedule UI updates on the main thread
                    self.after(0, lambda: self.extracted_text_widget.delete('1.0', tk.END))
                    self.after(0, lambda: self.extracted_text_widget.insert(tk.END, text))
                    self.after(0, lambda: self.update_status("Text extracted successfully"))

                    # Reset the button text
                    if hasattr(self, 'buttons') and 'Extract Text' in self.buttons:
                        self.after(0, lambda: extract_btn.config(text=original_text))
                except Exception as e:
                    self.after(0, lambda: self.update_status(f"Error extracting text: {str(e)}", error=True))
                    self.after(0, lambda: show_message("Error", f"Failed to extract text: {str(e)}", "error"))

                    # Reset the button text on error
                    if hasattr(self, 'buttons') and 'Extract Text' in self.buttons:
                        self.after(0, lambda: extract_btn.config(text=original_text))

            threading.Thread(target=do_extract, daemon=True).start()

        except Exception as e:
            self.update_status(f"Error: {str(e)}", error=True)
            show_message("Error", str(e), "error")
            if hasattr(self, 'buttons') and 'Extract Text' in self.buttons:
                self.after(0, lambda: extract_btn.config(text=original_text))

    def translate_text(self):
        """Translate the extracted text with thread-safe UI updates."""
        try:
            # Show a loading indicator on the translate button
            if hasattr(self, 'translate_btn'):
                original_text = self.translate_btn['text']
                self.after(0, lambda: self.translate_btn.config(text="⏳ Translating..."))

            text = self.extracted_text_widget.get('1.0', tk.END).strip()
            if not text:
                self.update_status("No text to translate", error=True)
                show_message("Error", "Please extract text from an image first", "error")
                if hasattr(self, 'translate_btn'):
                    self.after(0, lambda: self.translate_btn.config(text=original_text))
                return

            dest_lang = self.to_lang.get()
            self.update_status(f"Translating text to {dest_lang}...")

            def do_translation():
                try:
                    # Perform the actual translation
                    translated = translate_text(text, 'Auto Detect', dest_lang)
                    self.translated_text = translated

                    # Schedule UI updates on the main thread
                    self.after(0, lambda: self.trans_text.delete('1.0', tk.END))
                    self.after(0, lambda: self.trans_text.insert(tk.END, translated))
                    self.after(0, lambda: self.update_status(f"Text translated successfully to {dest_lang}"))

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
        """Clear all content."""
        # Clear image preview
        self.image_canvas.delete("all")
        self.canvas_placeholder = self.image_canvas.create_text(
            200, 150, text="No image selected",
            font=self.body_font, fill=ThemeColors.MEDIUM_GRAY
        )

        # Clear text areas
        self.extracted_text_widget.delete('1.0', tk.END)
        self.trans_text.delete('1.0', tk.END)

        # Reset variables
        self.image_path = None
        self.extracted_text = ""
        self.translated_text = ""
        self.image_preview = None

        # Clear file entry and info
        self.file_entry.delete(0, tk.END)
        self.file_info.config(text="No image selected")

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
        text = self.trans_text.get('1.0', tk.END).strip()
        if not text:
            self.update_status("No translation to save", error=True)
            show_message("Error", "Please translate text first", "error")
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
                    f.write(text)

                self.update_status(f"Translation saved to {os.path.basename(save_path)}")
                show_message("Success", f"Translation saved to {save_path}", "info")
            except Exception as e:
                self.update_status(f"Error saving translation: {str(e)}", error=True)
                show_message("Error", f"Failed to save translation: {str(e)}", "error")

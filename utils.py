"""
Utility functions for the Language Translator application.
Contains helper functions for translation, file operations, and UI utilities.
"""

import os
import tempfile
import threading
import time
import platform
from tkinter import messagebox
import pyperclip as pc
from deep_translator import GoogleTranslator
from gtts import gTTS
import speech_recognition as sr
import pytesseract
from PIL import Image
import docx
import pdf2image
from config import LANGUAGE_CODES

# Translation utilities
def translate_text(text, source_lang, target_lang):
    """Translate text using Google Translator."""
    if not text:
        return ""

    try:
        translator = GoogleTranslator(
            source='auto' if source_lang == 'Auto Detect' else LANGUAGE_CODES[source_lang],
            target=LANGUAGE_CODES[target_lang]
        )
        return translator.translate(text)
    except Exception as e:
        raise Exception(f"Translation error: {str(e)}")

# Speech utilities
def text_to_speech(text, lang_code):
    """Convert text to speech and play it."""
    if not text:
        return False, "No text to convert to speech"

    try:
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_file:
            temp_path = temp_file.name

        tts = gTTS(text=text, lang=lang_code, slow=False)
        tts.save(temp_path)

        if platform.system() == 'Darwin':  # macOS
            os.system(f'afplay "{temp_path}"')
        elif platform.system() == 'Windows':  # Windows
            os.system(f'start "" "{temp_path}"')
        else:  # Linux
            os.system(f'xdg-open "{temp_path}"')

        # Clean up the temporary file after a delay
        def cleanup():
            time.sleep(2)
            try:
                os.remove(temp_path)
            except:
                pass

        threading.Thread(target=cleanup, daemon=True).start()
        return True, "Speech generated successfully"
    except Exception as e:
        return False, f"Speech error: {str(e)}"

def speech_to_text(recognizer, microphone, timeout=5):
    """Convert speech to text using Google's speech recognition."""
    try:
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=timeout)

        text = recognizer.recognize_google(audio)
        return True, text
    except sr.UnknownValueError:
        return False, "Could not understand audio"
    except sr.RequestError as e:
        return False, f"Speech service error: {str(e)}"
    except sr.WaitTimeoutError:
        return False, "Listening timed out"
    except Exception as e:
        return False, f"Error: {str(e)}"

# Document utilities
def extract_text_from_docx(file_path):
    """Extract text from a DOCX file."""
    try:
        doc = docx.Document(file_path)
        full_text = []
        for para in doc.paragraphs:
            full_text.append(para.text)
        return "\n".join(full_text)
    except Exception as e:
        raise Exception(f"Error extracting text from DOCX: {str(e)}")

def extract_text_from_pdf(file_path):
    """Extract text from a PDF file using OCR."""
    try:
        # Convert PDF to images
        images = pdf2image.convert_from_path(file_path)
        text = ""

        # Extract text from each image
        for img in images:
            text += pytesseract.image_to_string(img) + "\n\n"

        return text
    except Exception as e:
        raise Exception(f"Error extracting text from PDF: {str(e)}")

def extract_text_from_image(file_path):
    """Extract text from an image using OCR."""
    try:
        img = Image.open(file_path)
        text = pytesseract.image_to_string(img)
        return text
    except Exception as e:
        raise Exception(f"Error extracting text from image: {str(e)}")

# Clipboard utilities
def copy_to_clipboard(text):
    """Copy text to clipboard."""
    if not text:
        return False, "No text to copy"

    try:
        pc.copy(text)
        return True, "Text copied to clipboard"
    except Exception as e:
        return False, f"Error copying to clipboard: {str(e)}"

# UI utilities
def show_message(title, message, message_type="info"):
    """Show a message dialog."""
    if message_type == "info":
        messagebox.showinfo(title, message)
    elif message_type == "warning":
        messagebox.showwarning(title, message)
    elif message_type == "error":
        messagebox.showerror(title, message)

def create_rounded_rectangle(canvas, x1, y1, x2, y2, radius=25, **kwargs):
    """Draw a rounded rectangle on a canvas."""
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
    return canvas.create_polygon(points, **kwargs, smooth=True)

def apply_hover_effect(widget, enter_color, leave_color):
    """Apply hover effect to a widget."""
    widget.bind("<Enter>", lambda e: widget.config(bg=enter_color))
    widget.bind("<Leave>", lambda e: widget.config(bg=leave_color))

def create_animated_button(parent, text, command, bg_color, fg_color, font, width=150, height=40):
    """Create an animated button with pulsing effect."""
    import tkinter as tk
    import threading
    import time

    # Create a frame to hold the button
    frame = tk.Frame(parent, width=width, height=height, bg=parent.cget('bg'))

    # Create the button
    btn = tk.Button(frame, text=text, font=font, command=command,
                  bg=bg_color, fg=fg_color, bd=0, padx=15, pady=8,
                  cursor='hand2', relief=tk.RAISED, width=width//10)
    btn.pack(fill=tk.BOTH, expand=True)

    # Add hover effect
    def on_enter(e):
        btn.config(bg=lighten_color(bg_color))

    def on_leave(e):
        btn.config(bg=bg_color)

    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

    # Add pulsing animation
    def pulse_animation():
        original_color = bg_color
        pulse_color = lighten_color(bg_color)

        while True:
            # Pulse from original to lighter color
            for i in range(10):
                if not btn.winfo_exists():
                    return
                current_color = blend_colors(original_color, pulse_color, i/10)
                btn.config(bg=current_color)
                time.sleep(0.05)

            # Pulse from lighter back to original color
            for i in range(10):
                if not btn.winfo_exists():
                    return
                current_color = blend_colors(pulse_color, original_color, i/10)
                btn.config(bg=current_color)
                time.sleep(0.05)

    # Start animation in a separate thread
    animation_thread = threading.Thread(target=pulse_animation, daemon=True)
    animation_thread.start()

    return frame, btn

def lighten_color(hex_color, factor=1.3):
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

def blend_colors(color1, color2, ratio):
    """Blend two colors with the given ratio (0-1)."""
    # Convert hex to RGB
    r1 = int(color1[1:3], 16)
    g1 = int(color1[3:5], 16)
    b1 = int(color1[5:7], 16)

    r2 = int(color2[1:3], 16)
    g2 = int(color2[3:5], 16)
    b2 = int(color2[5:7], 16)

    # Blend
    r = int(r1 * (1 - ratio) + r2 * ratio)
    g = int(g1 * (1 - ratio) + g2 * ratio)
    b = int(b1 * (1 - ratio) + b2 * ratio)

    # Convert back to hex
    return f"#{r:02x}{g:02x}{b:02x}"

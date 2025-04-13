import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter import font as tkfont
import os
import threading
import time
import platform
import pyperclip as pc
from deep_translator import GoogleTranslator
from gtts import gTTS
import speech_recognition as sr
import pytesseract
from PIL import Image, ImageTk
import docx
import pdf2image

# Language codes for translation
LANGUAGE_CODES = {
    'Auto Detect': 'auto',
    'English': 'en',
    'Spanish': 'es',
    'French': 'fr',
    'German': 'de',
    'Italian': 'it',
    'Portuguese': 'pt',
    'Russian': 'ru',
    'Japanese': 'ja',
    'Korean': 'ko',
    'Chinese (Simplified)': 'zh-CN',
    'Chinese (Traditional)': 'zh-TW',
    'Arabic': 'ar',
    'Hindi': 'hi',
    'Bengali': 'bn',
    'Urdu': 'ur',
    'Turkish': 'tr',
    'Dutch': 'nl',
    'Greek': 'el',
    'Hebrew': 'he',
    'Polish': 'pl',
    'Thai': 'th',
    'Vietnamese': 'vi',
    'Swedish': 'sv',
    'Finnish': 'fi',
    'Danish': 'da',
    'Norwegian': 'no'
}

class SimpleTranslator:
    def __init__(self, root):
        self.root = root
        self.root.title('Final Fusion - Advanced Translator')
        self.root.geometry('1200x750+100+50')
        self.root.minsize(1000, 650)
        self.root.configure(bg='#f5f5f5')
        
        # Custom fonts
        self.title_font = tkfont.Font(family='Segoe UI', size=26, weight='bold')
        self.subtitle_font = tkfont.Font(family='Segoe UI', size=11)
        self.label_font = tkfont.Font(family='Segoe UI', size=11, weight='bold')
        self.button_font = tkfont.Font(family='Segoe UI', size=11, weight='bold')
        self.text_font = tkfont.Font(family='Segoe UI', size=13)
        
        # Modern color scheme - Vibrant colors
        self.primary_color = '#8A2BE2'  # Vivid purple
        self.secondary_color = '#6c757d'
        self.success_color = '#00E676'  # Bright green
        self.warning_color = '#FFAB00'  # Amber
        self.danger_color = '#FF5252'  # Bright red
        self.info_color = '#2979FF'  # Bright blue
        self.light_bg = '#ffffff'
        self.dark_bg = '#121212'
        self.text_color = '#212121'
        self.light_text = '#f8f9fa'
        self.input_bg = '#ffffff'
        self.dark_input_bg = '#1E1E1E'
        
        # Theme variables
        self.dark_mode = False
        
        # Speech recognition
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.is_listening = False
        
        # Create UI elements
        self.create_header()
        self.create_main_content()
        self.create_footer()
        
    def create_header(self):
        # Header frame with solid background
        self.header = tk.Frame(self.root, bg=self.primary_color, height=90)
        self.header.pack(fill=tk.X)
        
        # Title and subtitle
        title_frame = tk.Frame(self.header, bg=self.primary_color)
        title_frame.pack(side=tk.LEFT, padx=25, pady=10)
        
        # Logo/icon (placeholder for now)
        logo_text = "FF"
        logo_frame = tk.Frame(title_frame, bg=self.info_color, width=40, height=40)
        logo_frame.pack(side=tk.LEFT, padx=(0, 15))
        logo_frame.pack_propagate(False)
        
        logo_label = tk.Label(logo_frame, text=logo_text, font=tkfont.Font(family='Segoe UI', size=16, weight='bold'),
                            bg=self.info_color, fg='white')
        logo_label.place(relx=0.5, rely=0.5, anchor='center')
        
        # Title and subtitle
        text_frame = tk.Frame(title_frame, bg=self.primary_color)
        text_frame.pack(side=tk.LEFT)
        
        self.title_label = tk.Label(text_frame, text="Final Fusion", font=self.title_font, 
                                  bg=self.primary_color, fg='white')
        self.title_label.pack(anchor='w')
        
        self.subtitle_label = tk.Label(text_frame, text="Advanced Language Translator", 
                                     font=self.subtitle_font, bg=self.primary_color, 
                                     fg='#e8f0fe')
        self.subtitle_label.pack(anchor='w')
        
        # Right side controls
        self.control_frame = tk.Frame(self.header, bg=self.primary_color)
        self.control_frame.pack(side=tk.RIGHT, padx=25, pady=10)
        
        # Theme toggle button
        self.theme_btn = tk.Button(self.control_frame, text="🌞" if not self.dark_mode else "🌙", 
                                 font=('Segoe UI', 14), command=self.toggle_theme, 
                                 bg=self.primary_color, fg='white', bd=0, 
                                 activebackground=self.primary_color, activeforeground='white',
                                 cursor='hand2')
        self.theme_btn.pack(side=tk.RIGHT, padx=10)
        
    def create_main_content(self):
        # Main container with padding
        self.main_frame = tk.Frame(self.root, bg=self.light_bg, padx=20, pady=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Language selection frame
        self.lang_frame = tk.Frame(self.main_frame, bg=self.light_bg)
        self.lang_frame.pack(fill=tk.X, pady=(0, 15))
        
        # From language
        from_frame = tk.Frame(self.lang_frame, bg=self.light_bg)
        from_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        from_label = tk.Label(from_frame, text="Translate from:", font=self.label_font, 
                            bg=self.light_bg, fg=self.text_color)
        from_label.pack(anchor='w', pady=(0, 5))
        
        self.from_lang = ttk.Combobox(from_frame, values=list(LANGUAGE_CODES.keys()), 
                                    font=self.text_font, state="readonly", width=20)
        self.from_lang.pack(anchor='w', fill=tk.X)
        self.from_lang.current(0)  # Set to 'Auto Detect'
        
        # Swap button
        swap_frame = tk.Frame(self.lang_frame, bg=self.light_bg, width=100)
        swap_frame.pack(side=tk.LEFT, padx=20)
        
        self.swap_btn = tk.Button(swap_frame, text="🔄", font=('Segoe UI', 16), 
                                command=self.swap_languages, bg=self.light_bg, 
                                fg=self.primary_color, bd=0, padx=10, pady=5,
                                activebackground=self.light_bg, activeforeground=self.primary_color,
                                cursor='hand2')
        self.swap_btn.pack(pady=10)
        
        # To language
        to_frame = tk.Frame(self.lang_frame, bg=self.light_bg)
        to_frame.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        
        to_label = tk.Label(to_frame, text="Translate to:", font=self.label_font, 
                          bg=self.light_bg, fg=self.text_color)
        to_label.pack(anchor='w', pady=(0, 5))
        
        self.to_lang = ttk.Combobox(to_frame, values=list(LANGUAGE_CODES.keys())[1:], 
                                  font=self.text_font, state="readonly", width=20)
        self.to_lang.pack(anchor='w', fill=tk.X)
        self.to_lang.current(0)  # Set to 'English'
        
        # Text areas frame
        self.text_frame = tk.Frame(self.main_frame, bg=self.light_bg)
        self.text_frame.pack(fill=tk.BOTH, expand=True)
        
        # Input container
        self.input_container = tk.Frame(self.text_frame, bg=self.light_bg)
        self.input_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Input label
        self.input_label = tk.Label(self.input_container, text="Enter text", font=self.label_font, 
                                  bg=self.light_bg, fg=self.text_color)
        self.input_label.pack(anchor='w', pady=(0, 5))
        
        # Input text frame with enhanced styling
        self.input_frame = tk.Frame(self.input_container, bg=self.input_bg, bd=0,
                                   highlightbackground=self.primary_color, highlightthickness=1)
        self.input_frame.pack(fill=tk.BOTH, expand=True)
        
        # Add a header bar for visual appeal
        input_header = tk.Frame(self.input_frame, bg=self.primary_color, height=5)
        input_header.pack(fill=tk.X)
        
        self.input_text = tk.Text(self.input_frame, height=15, font=self.text_font,
                                wrap=tk.WORD, padx=15, pady=15, bd=0,
                                bg=self.input_bg, fg=self.text_color,
                                insertbackground=self.primary_color, insertwidth=2)
        self.input_text.pack(fill=tk.BOTH, expand=True)
        
        # Input scrollbar
        input_scroll = ttk.Scrollbar(self.input_frame, command=self.input_text.yview)
        input_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.input_text.config(yscrollcommand=input_scroll.set)
        
        # Output container
        self.output_container = tk.Frame(self.text_frame, bg=self.light_bg)
        self.output_container.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Output label
        self.output_label = tk.Label(self.output_container, text="Translation", font=self.label_font, 
                                   bg=self.light_bg, fg=self.text_color)
        self.output_label.pack(anchor='w', pady=(0, 5))
        
        # Output text frame with enhanced styling
        self.output_frame = tk.Frame(self.output_container, bg=self.input_bg, bd=0,
                                   highlightbackground=self.success_color, highlightthickness=1)
        self.output_frame.pack(fill=tk.BOTH, expand=True)
        
        # Add a header bar for visual appeal
        output_header = tk.Frame(self.output_frame, bg=self.success_color, height=5)
        output_header.pack(fill=tk.X)
        
        self.output_text = tk.Text(self.output_frame, height=15, font=self.text_font,
                                 wrap=tk.WORD, padx=15, pady=15, bd=0,
                                 bg=self.input_bg, fg=self.text_color,
                                 insertbackground=self.success_color, insertwidth=2)
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        # Output scrollbar
        output_scroll = ttk.Scrollbar(self.output_frame, command=self.output_text.yview)
        output_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.output_text.config(yscrollcommand=output_scroll.set)
        
        # Button frame
        self.btn_frame = tk.Frame(self.main_frame, bg=self.light_bg, pady=15)
        self.btn_frame.pack(fill=tk.X)
        
        # Modern buttons with consistent styling and icons
        buttons = [
            ("🔄 Translate", self.translate, self.primary_color),
            ("🗑️ Clear", self.clear, self.secondary_color),
            ("📋 Copy", self.copy, self.success_color),
            ("🔊 Read Aloud", self.text_to_speech, self.warning_color),
            ("🎤 Voice Input", self.speech_to_text, self.info_color)
        ]
        
        for text, command, color in buttons:
            # Create a frame for the button to add shadow effect
            btn_frame = tk.Frame(self.btn_frame, bg=self.light_bg, bd=0)
            btn_frame.pack(side=tk.LEFT, padx=8, pady=5)
            
            # Create the actual button with modern styling
            btn = tk.Button(btn_frame, text=text, font=self.button_font,
                          command=command, bg=color, fg='white',
                          bd=0, padx=20, pady=10, activebackground=self.darken_color(color),
                          cursor='hand2', relief=tk.RAISED)
            btn.pack(fill=tk.BOTH, expand=True)
            
            # Add hover effect
            btn.bind("<Enter>", lambda e, b=btn, c=color: b.config(bg=self.lighten_color(c)))
            btn.bind("<Leave>", lambda e, b=btn, c=color: b.config(bg=c))
        
        # Character count
        self.char_count = tk.Label(self.btn_frame, text="0 characters", font=self.label_font, 
                                  bg=self.light_bg, fg=self.secondary_color)
        self.char_count.pack(side=tk.RIGHT)
        
        # Bind text change event
        self.input_text.bind('<KeyRelease>', self.update_char_count)
        
    def create_footer(self):
        # Footer frame
        self.footer = tk.Frame(self.root, bg=self.light_bg, height=50, 
                              highlightbackground='#dadce0', highlightthickness=1)
        self.footer.pack(fill=tk.X, side=tk.BOTTOM)
        
        # Status bar
        self.status = tk.Label(self.footer, text="Ready", font=self.subtitle_font, 
                             bg=self.light_bg, fg=self.secondary_color)
        self.status.pack(side=tk.LEFT, padx=25, pady=10)
        
        # Version info
        version = tk.Label(self.footer, text="Final Fusion v2.0", font=self.subtitle_font, 
                         bg=self.light_bg, fg=self.secondary_color)
        version.pack(side=tk.RIGHT, padx=25, pady=10)
        
    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        
        if self.dark_mode:
            # Dark theme colors
            bg_color = self.dark_bg
            text_bg = self.dark_input_bg
            text_fg = self.light_text
            btn_bg = '#3c4043'
            header_bg = self.primary_color
            footer_bg = self.dark_bg
            border_color = '#3c4043'
            light_bg = self.dark_bg
            secondary_color = '#9aa0a6'
            
            # Update theme button
            self.theme_btn.config(text="🌙")
        else:
            # Light theme colors
            bg_color = self.light_bg
            text_bg = self.input_bg
            text_fg = self.text_color
            btn_bg = '#f1f3f4'
            header_bg = self.primary_color
            footer_bg = self.light_bg
            border_color = '#dadce0'
            light_bg = self.light_bg
            secondary_color = self.secondary_color
            
            # Update theme button
            self.theme_btn.config(text="🌞")
        
        # Update all widgets
        self.root.config(bg=bg_color)
        self.main_frame.config(bg=bg_color)
        self.lang_frame.config(bg=bg_color)
        self.text_frame.config(bg=bg_color)
        self.btn_frame.config(bg=bg_color)
        
        # Update text widgets
        self.input_text.config(bg=text_bg, fg=text_fg, insertbackground=text_fg)
        self.output_text.config(bg=text_bg, fg=text_fg, insertbackground=text_fg)
        self.input_frame.config(bg=text_bg, highlightbackground=border_color)
        self.output_frame.config(bg=text_bg, highlightbackground=border_color)
        self.input_label.config(bg=bg_color, fg=text_fg)
        self.output_label.config(bg=bg_color, fg=text_fg)
        
        # Update language selection
        from_frame = self.lang_frame.winfo_children()[0]
        swap_frame = self.lang_frame.winfo_children()[1]
        to_frame = self.lang_frame.winfo_children()[2]
        
        for frame in [from_frame, swap_frame, to_frame]:
            frame.config(bg=bg_color)
            for child in frame.winfo_children():
                if isinstance(child, tk.Label):
                    child.config(bg=bg_color, fg=text_fg)
                elif isinstance(child, tk.Button):
                    child.config(bg=bg_color, activebackground=bg_color)
        
        # Update footer
        self.footer.config(bg=footer_bg, highlightbackground=border_color)
        for child in self.footer.winfo_children():
            child.config(bg=footer_bg, fg=secondary_color)
        
        # Update character count
        self.char_count.config(bg=bg_color, fg=secondary_color)
        
    def swap_languages(self):
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
    
    def update_char_count(self, event=None):
        text = self.input_text.get('1.0', 'end-1c')
        count = len(text)
        self.char_count.config(text=f"{count} characters")
    
    def translate(self):
        try:
            text = self.input_text.get('1.0', tk.END).strip()
            if not text:
                self.update_status("Please enter text to translate", error=True)
                messagebox.showwarning("Warning", "Please enter text to translate")
                return

            src_lang = self.from_lang.get()
            dest_lang = self.to_lang.get()
            
            self.update_status("Translating...")
            
            def do_translation():
                try:
                    translator = GoogleTranslator(
                        source='auto' if src_lang == 'Auto Detect' else LANGUAGE_CODES[src_lang],
                        target=LANGUAGE_CODES[dest_lang]
                    )
                    translated = translator.translate(text)
                    
                    self.output_text.delete('1.0', tk.END)
                    self.output_text.insert(tk.END, translated)
                    self.update_status(f"Translated from {src_lang} to {dest_lang}")
                except Exception as e:
                    self.update_status(f"Translation error: {str(e)}", error=True)
                    messagebox.showerror("Error", str(e))
            
            threading.Thread(target=do_translation, daemon=True).start()
            
        except Exception as e:
            self.update_status(f"Error: {str(e)}", error=True)
            messagebox.showerror("Error", str(e))
    
    def clear(self):
        self.input_text.delete('1.0', tk.END)
        self.output_text.delete('1.0', tk.END)
        self.update_status("Cleared")
        self.update_char_count()
    
    def copy(self):
        text = self.output_text.get('1.0', tk.END).strip()
        if not text:
            self.update_status("No text to copy", error=True)
            messagebox.showwarning("Warning", "No text to copy")
            return
            
        pc.copy(text)
        self.update_status("Text copied to clipboard")
    
    def text_to_speech(self):
        try:
            text = self.output_text.get('1.0', tk.END).strip()
            if not text:
                self.update_status("No translated text to read", error=True)
                messagebox.showwarning("Warning", "No translated text to read")
                return
                
            dest_lang = self.to_lang.get()
            lang_code = LANGUAGE_CODES[dest_lang]
            
            self.update_status("Generating speech...")
            
            def do_tts():
                try:
                    temp_path = os.path.join(os.getcwd(), "temp_speech.mp3")
                    tts = gTTS(text=text, lang=lang_code, slow=False)
                    tts.save(temp_path)
                    
                    if platform.system() == 'Darwin':  # macOS
                        os.system(f'afplay "{temp_path}"')
                    elif platform.system() == 'Windows':  # Windows
                        os.system(f'start "" "{temp_path}"')
                    else:  # Linux
                        os.system(f'xdg-open "{temp_path}"')
                    
                    self.update_status("Speech generated successfully")
                except Exception as e:
                    self.update_status(f"Speech error: {str(e)}", error=True)
                    messagebox.showerror("Error", f"Failed to generate speech: {str(e)}")
                finally:
                    try:
                        time.sleep(2)
                        os.remove(temp_path)
                    except:
                        pass
            
            threading.Thread(target=do_tts, daemon=True).start()
            
        except Exception as e:
            self.update_status(f"Error: {str(e)}", error=True)
            messagebox.showerror("Error", str(e))

    def speech_to_text(self):
        if self.is_listening:
            self.update_status("Already listening...", error=True)
            return
            
        try:
            self.is_listening = True
            self.update_status("Listening... Speak now (5 second timeout)")
            
            def do_stt():
                try:
                    with self.microphone as source:
                        self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                        self.update_status("Listening... Speak now", error=False)
                        audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                    
                    text = self.recognizer.recognize_google(audio)
                    self.input_text.delete('1.0', tk.END)
                    self.input_text.insert(tk.END, text)
                    self.update_status("Speech recognized successfully")
                    self.translate()
                except sr.UnknownValueError:
                    self.update_status("Could not understand audio", error=True)
                    messagebox.showerror("Error", "Could not understand audio")
                except sr.RequestError as e:
                    self.update_status("Speech service unavailable", error=True)
                    messagebox.showerror("Error", f"Speech service error: {str(e)}")
                except sr.WaitTimeoutError:
                    self.update_status("Listening timed out", error=True)
                    messagebox.showwarning("Warning", "Listening timed out. Please try again.")
                except Exception as e:
                    self.update_status(f"Error: {str(e)}", error=True)
                    messagebox.showerror("Error", str(e))
                finally:
                    self.is_listening = False
            
            threading.Thread(target=do_stt, daemon=True).start()
            
        except Exception as e:
            self.is_listening = False
            self.update_status(f"Error: {str(e)}", error=True)
            messagebox.showerror("Error", str(e))
    
    def update_status(self, message, error=False):
        if error:
            self.status.config(text=message, fg=self.danger_color)
        else:
            self.status.config(text=message, fg=self.secondary_color)
            
            # Auto-clear status after 5 seconds
            def clear_status():
                time.sleep(5)
                if self.status['text'] == message:
                    self.status.config(text="Ready", fg=self.secondary_color)
            
            threading.Thread(target=clear_status, daemon=True).start()
    
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

def main():
    root = tk.Tk()
    app = SimpleTranslator(root)
    root.mainloop()

if __name__ == "__main__":
    main()

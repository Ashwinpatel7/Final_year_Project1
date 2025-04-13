import tkinter as tk
from tkinter import ttk, messagebox
from deep_translator import GoogleTranslator
import pyperclip as pc
from gtts import gTTS
import os
import speech_recognition as spr
import webbrowser
from tkinter import font as tkfont
import platform
import threading
import time
import tempfile

# Language configuration
LANGUAGE_CODES = {
    'Afrikaans': 'af', 'Albanian': 'sq', 'Arabic': 'ar', 'Armenian': 'hy',
    'Azerbaijani': 'az', 'Basque': 'eu', 'Belarusian': 'be', 'Bengali': 'bn',
    'Bosnian': 'bs', 'Bulgarian': 'bg', 'Catalan': 'ca', 'Cebuano': 'ceb',
    'Chinese': 'zh-cn', 'Corsican': 'co', 'Croatian': 'hr', 'Czech': 'cs',
    'Danish': 'da', 'Dutch': 'nl', 'English': 'en', 'Esperanto': 'eo',
    'Estonian': 'et', 'Finnish': 'fi', 'French': 'fr', 'Frisian': 'fy',
    'Galician': 'gl', 'Georgian': 'ka', 'German': 'de', 'Greek': 'el',
    'Gujarati': 'gu', 'Haitian Creole': 'ht', 'Hausa': 'ha', 'Hebrew': 'he',
    'Hindi': 'hi', 'Hmong': 'hmn', 'Hungarian': 'hu', 'Icelandic': 'is',
    'Igbo': 'ig', 'Indonesian': 'id', 'Irish': 'ga', 'Italian': 'it',
    'Japanese': 'ja', 'Javanese': 'jv', 'Kannada': 'kn', 'Kazakh': 'kk',
    'Khmer': 'km', 'Korean': 'ko', 'Kurdish': 'ku', 'Kyrgyz': 'ky',
    'Lao': 'lo', 'Latin': 'la', 'Latvian': 'lv', 'Lithuanian': 'lt',
    'Luxembourgish': 'lb', 'Macedonian': 'mk', 'Malagasy': 'mg', 'Malay': 'ms',
    'Malayalam': 'ml', 'Maltese': 'mt', 'Maori': 'mi', 'Marathi': 'mr',
    'Mongolian': 'mn', 'Myanmar': 'my', 'Nepali': 'ne', 'Norwegian': 'no',
    'Pashto': 'ps', 'Persian': 'fa', 'Polish': 'pl', 'Portuguese': 'pt',
    'Punjabi': 'pa', 'Romanian': 'ro', 'Russian': 'ru', 'Samoan': 'sm',
    'Scots Gaelic': 'gd', 'Serbian': 'sr', 'Sesotho': 'st', 'Shona': 'sn',
    'Sindhi': 'sd', 'Sinhala': 'si', 'Slovak': 'sk', 'Slovenian': 'sl',
    'Somali': 'so', 'Spanish': 'es', 'Sundanese': 'su', 'Swahili': 'sw',
    'Swedish': 'sv', 'Tajik': 'tg', 'Tamil': 'ta', 'Telugu': 'te', 'Thai': 'th',
    'Turkish': 'tr', 'Ukrainian': 'uk', 'Urdu': 'ur', 'Uzbek': 'uz',
    'Vietnamese': 'vi', 'Welsh': 'cy', 'Xhosa': 'xh', 'Yiddish': 'yi',
    'Yoruba': 'yo', 'Zulu': 'zu'
}

LANGUAGES = list(LANGUAGE_CODES.keys())

class PolyGlotPro:
    def __init__(self, root):
        self.root = root
        self.root.title('PolyGlot Pro - Advanced Translator')
        self.root.geometry('1200x750+100+50')
        self.root.minsize(1000, 650)
        self.root.configure(bg='#f5f5f5')
        
        # Custom fonts
        self.title_font = tkfont.Font(family='Helvetica', size=24, weight='bold')
        self.subtitle_font = tkfont.Font(family='Helvetica', size=10)
        self.label_font = tkfont.Font(family='Helvetica', size=10, weight='bold')
        self.button_font = tkfont.Font(family='Helvetica', size=10, weight='bold')
        self.text_font = tkfont.Font(family='Helvetica', size=12)
        
        # Colors
        self.primary_color = '#4285f4'
        self.secondary_color = '#757575'
        self.success_color = '#34a853'
        self.warning_color = '#fbbc05'
        self.danger_color = '#ea4335'
        self.info_color = '#17a2b8'
        self.light_bg = '#ffffff'
        self.dark_bg = '#202124'
        self.text_color = '#202124'
        self.light_text = '#f8f9fa'
        self.input_bg = '#ffffff'
        self.dark_input_bg = '#303134'
        
        # Theme variables
        self.dark_mode = False
        
        # Speech recognition
        self.recognizer = spr.Recognizer()
        self.microphone = spr.Microphone()
        self.is_listening = False
        
        # Setup UI
        self.create_header()
        self.setup_ui()
        self.create_footer()
        
        # Configure styles
        self.configure_styles()
        
    def configure_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Combobox styles
        style.configure('TCombobox', 
                      fieldbackground=self.input_bg, 
                      background=self.input_bg, 
                      foreground=self.text_color,
                      selectbackground='#e8f0fe',
                      font=self.text_font,
                      padding=5)
        
        style.map('TCombobox', 
                fieldbackground=[('readonly', self.input_bg)],
                selectbackground=[('readonly', '#e8f0fe')],
                foreground=[('readonly', self.text_color)])
        
        # Dark theme combobox
        style.configure('Dark.TCombobox', 
                      fieldbackground=self.dark_input_bg, 
                      background=self.dark_input_bg, 
                      foreground=self.light_text,
                      selectbackground='#3c4043',
                      font=self.text_font,
                      padding=5)
        
        style.map('Dark.TCombobox', 
                fieldbackground=[('readonly', self.dark_input_bg)],
                selectbackground=[('readonly', '#3c4043')],
                foreground=[('readonly', self.light_text)])
        
    def create_header(self):
        # Header frame
        self.header = tk.Frame(self.root, bg=self.primary_color, height=90)
        self.header.pack(fill=tk.X)
        
        # Title and subtitle
        title_frame = tk.Frame(self.header, bg=self.primary_color)
        title_frame.pack(side=tk.LEFT, padx=25, pady=10)
        
        self.title_label = tk.Label(title_frame, text="PolyGlot Pro", font=self.title_font, 
                                  bg=self.primary_color, fg='white')
        self.title_label.pack(anchor='w')
        
        self.subtitle_label = tk.Label(title_frame, text="Advanced Language Translator", 
                                     font=self.subtitle_font, bg=self.primary_color, 
                                     fg='#e8f0fe')
        self.subtitle_label.pack(anchor='w')
        
        # Right side controls
        control_frame = tk.Frame(self.header, bg=self.primary_color)
        control_frame.pack(side=tk.RIGHT, padx=25, pady=10)
        
        # Theme toggle
        self.theme_btn = tk.Button(control_frame, text="☀️", font=('Arial', 14), 
                                 command=self.toggle_theme, bg=self.primary_color, 
                                 fg='white', bd=0, activebackground=self.primary_color, 
                                 activeforeground='white', cursor='hand2')
        self.theme_btn.pack(side=tk.RIGHT, padx=10)
        
        # GitHub button
        self.github_btn = tk.Button(control_frame, text="GitHub", font=self.button_font, 
                                  command=lambda: webbrowser.open("https://github.com"), 
                                  bg=self.primary_color, fg='white', bd=0, 
                                  activebackground=self.primary_color, activeforeground='white',
                                  cursor='hand2')
        self.github_btn.pack(side=tk.RIGHT, padx=10)
        
    def setup_ui(self):
        # Main container
        self.main_frame = tk.Frame(self.root, bg=self.light_bg)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=25, pady=(0, 20))
        
        # Language selection frame
        self.lang_frame = tk.Frame(self.main_frame, bg=self.light_bg)
        self.lang_frame.pack(fill=tk.X, pady=(0, 15))
        
        # From language
        tk.Label(self.lang_frame, text="SOURCE LANGUAGE", font=self.label_font, 
                bg=self.light_bg, fg=self.secondary_color).grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        
        self.from_lang = ttk.Combobox(self.lang_frame, values=['Auto Detect'] + LANGUAGES, 
                                     state='readonly', font=self.text_font)
        self.from_lang.current(0)
        self.from_lang.grid(row=1, column=0, sticky=tk.EW, padx=(0, 20))
        
        # Swap button
        self.swap_btn = tk.Button(self.lang_frame, text="⇄", font=('Arial', 14, 'bold'), 
                                command=self.swap_languages, bg=self.light_bg, fg=self.primary_color,
                                bd=0, padx=8, pady=2, activebackground=self.light_bg,
                                cursor='hand2')
        self.swap_btn.grid(row=1, column=1, padx=5)
        
        # To language
        tk.Label(self.lang_frame, text="TARGET LANGUAGE", font=self.label_font, 
                bg=self.light_bg, fg=self.secondary_color).grid(row=0, column=2, sticky=tk.W)
        
        self.to_lang = ttk.Combobox(self.lang_frame, values=LANGUAGES, 
                                   state='readonly', font=self.text_font)
        self.to_lang.current(LANGUAGES.index('English'))
        self.to_lang.grid(row=1, column=2, sticky=tk.EW)
        
        # Configure grid weights
        self.lang_frame.columnconfigure(0, weight=1)
        self.lang_frame.columnconfigure(2, weight=1)
        
        # Text areas frame
        self.text_frame = tk.Frame(self.main_frame, bg=self.light_bg)
        self.text_frame.pack(fill=tk.BOTH, expand=True)
        
        # Input text area
        self.input_frame = tk.Frame(self.text_frame, bg=self.input_bg, bd=1, relief=tk.SOLID, 
                                  highlightbackground='#dadce0', highlightthickness=1)
        self.input_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        self.input_text = tk.Text(self.input_frame, height=15, font=self.text_font, 
                                wrap=tk.WORD, padx=15, pady=15, bd=0,
                                bg=self.input_bg, fg=self.text_color, insertbackground=self.primary_color)
        self.input_text.pack(fill=tk.BOTH, expand=True)
        
        # Input text scrollbar
        self.input_scroll = ttk.Scrollbar(self.input_frame, command=self.input_text.yview)
        self.input_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.input_text.config(yscrollcommand=self.input_scroll.set)
        
        # Input text label
        self.input_label = tk.Label(self.input_frame, text="Enter text to translate", 
                                   font=self.label_font, bg=self.input_bg, fg=self.secondary_color)
        self.input_label.place(x=15, y=10)
        
        # Output text area
        self.output_frame = tk.Frame(self.text_frame, bg=self.input_bg, bd=1, relief=tk.SOLID, 
                                    highlightbackground='#dadce0', highlightthickness=1)
        self.output_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        self.output_text = tk.Text(self.output_frame, height=15, font=self.text_font, 
                                 wrap=tk.WORD, padx=15, pady=15, bd=0,
                                 bg=self.input_bg, fg=self.text_color, insertbackground=self.primary_color)
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        # Output text scrollbar
        self.output_scroll = ttk.Scrollbar(self.output_frame, command=self.output_text.yview)
        self.output_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.output_text.config(yscrollcommand=self.output_scroll.set)
        
        # Output text label
        self.output_label = tk.Label(self.output_frame, text="Translation", 
                                    font=self.label_font, bg=self.input_bg, fg=self.secondary_color)
        self.output_label.place(x=15, y=10)
        
        # Button frame
        self.btn_frame = tk.Frame(self.main_frame, bg=self.light_bg)
        self.btn_frame.pack(fill=tk.X, pady=(15, 0))
        
        # Buttons
        buttons = [
            ("Translate", self.translate, self.primary_color),
            ("Clear", self.clear, self.secondary_color),
            ("Copy", self.copy, self.success_color),
            ("Read Aloud", self.text_to_speech, self.warning_color),
            ("Voice Input", self.speech_to_text, self.info_color)
        ]
        
        for text, command, color in buttons:
            btn = tk.Button(self.btn_frame, text=text, font=self.button_font, 
                          command=command, bg=color, fg='white',
                          bd=0, padx=20, pady=8, activebackground=color,
                          cursor='hand2')
            btn.pack(side=tk.LEFT, padx=5)
        
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
        self.status.pack(side=tk.LEFT, padx=25)
        
        # Version info
        version = tk.Label(self.footer, text="PolyGlot Pro v1.0", font=self.subtitle_font, 
                         bg=self.light_bg, fg=self.secondary_color)
        version.pack(side=tk.RIGHT, padx=25)
        
    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        
        if self.dark_mode:
            # Dark theme colors
            bg_color = self.dark_bg
            text_bg = self.dark_input_bg
            text_fg = self.light_text
            btn_bg = '#3c4043'
            header_bg = '#1a73e8'
            footer_bg = self.dark_bg
            border_color = '#3c4043'
            light_bg = self.dark_bg
            secondary_color = '#9aa0a6'
            
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
            self.input_label.config(bg=text_bg, fg=secondary_color)
            self.output_label.config(bg=text_bg, fg=secondary_color)
            
            # Update header and footer
            self.header.config(bg=header_bg)
            for child in self.header.winfo_children():
                if isinstance(child, (tk.Label, tk.Frame)):
                    child.config(bg=header_bg)
            
            self.footer.config(bg=footer_bg, highlightbackground=border_color)
            for child in self.footer.winfo_children():
                child.config(bg=footer_bg, fg=secondary_color)
            
            # Update buttons
            self.theme_btn.config(text='🌙', bg=header_bg)
            self.github_btn.config(bg=header_bg)
            
            # Update combobox style
            self.from_lang.config(style='Dark.TCombobox')
            self.to_lang.config(style='Dark.TCombobox')
            
            # Update button colors
            for child in self.btn_frame.winfo_children():
                if isinstance(child, tk.Button):
                    child.config(bg=child.cget('bg'), fg='white')
            
            # Update character count and swap button
            self.char_count.config(bg=bg_color, fg=secondary_color)
            self.swap_btn.config(bg=bg_color)
            
        else:
            # Light theme colors
            bg_color = '#f5f5f5'
            text_bg = self.input_bg
            text_fg = self.text_color
            btn_bg = self.primary_color
            header_bg = self.primary_color
            footer_bg = self.light_bg
            border_color = '#dadce0'
            light_bg = self.light_bg
            secondary_color = self.secondary_color
            
            # Update all widgets
            self.root.config(bg=bg_color)
            self.main_frame.config(bg=light_bg)
            self.lang_frame.config(bg=light_bg)
            self.text_frame.config(bg=light_bg)
            self.btn_frame.config(bg=light_bg)
            
            # Update text widgets
            self.input_text.config(bg=text_bg, fg=text_fg, insertbackground=self.primary_color)
            self.output_text.config(bg=text_bg, fg=text_fg, insertbackground=self.primary_color)
            self.input_frame.config(bg=text_bg, highlightbackground=border_color)
            self.output_frame.config(bg=text_bg, highlightbackground=border_color)
            self.input_label.config(bg=text_bg, fg=secondary_color)
            self.output_label.config(bg=text_bg, fg=secondary_color)
            
            # Update header and footer
            self.header.config(bg=header_bg)
            for child in self.header.winfo_children():
                if isinstance(child, (tk.Label, tk.Frame)):
                    child.config(bg=header_bg)
            
            self.footer.config(bg=footer_bg, highlightbackground=border_color)
            for child in self.footer.winfo_children():
                if isinstance(child, tk.Label):
                    child.config(bg=footer_bg, fg=secondary_color)
            
            # Update buttons
            self.theme_btn.config(text='☀️', bg=header_bg)
            self.github_btn.config(bg=header_bg)
            
            # Update combobox style
            self.from_lang.config(style='TCombobox')
            self.to_lang.config(style='TCombobox')
            
            # Update button colors
            for child in self.btn_frame.winfo_children():
                if isinstance(child, tk.Button):
                    child.config(fg='white')
            
            # Update character count and swap button
            self.char_count.config(bg=light_bg, fg=secondary_color)
            self.swap_btn.config(bg=light_bg)
    
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
        self.char_count.config(text="0 characters")
        self.update_status("Cleared all text")

    def copy(self):
        text = self.output_text.get('1.0', tk.END).strip()
        if text:
            pc.copy(text)
            self.update_status("Text copied to clipboard")
            messagebox.showinfo("Success", "Text copied to clipboard")
        else:
            self.update_status("No text to copy", error=True)
            messagebox.showwarning("Warning", "No text to copy")

    def text_to_speech(self):
        try:
            text = self.output_text.get('1.0', tk.END).strip()
            if not text:
                self.update_status("No translated text to read", error=True)
                messagebox.showwarning("Warning", "No translated text to read")
                return

            try:
                lang = LANGUAGE_CODES[self.to_lang.get()]
            except KeyError:
                self.update_status("Language not supported for speech", error=True)
                messagebox.showwarning("Warning", "Selected language is not supported for speech synthesis")
                return

            self.update_status("Generating speech...")
            
            def do_tts():
                try:
                    with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_file:
                        temp_path = temp_file.name
                    
                    tts = gTTS(text=text, lang=lang, slow=False)
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
                except spr.UnknownValueError:
                    self.update_status("Could not understand audio", error=True)
                    messagebox.showerror("Error", "Could not understand audio")
                except spr.RequestError as e:
                    self.update_status("Speech service unavailable", error=True)
                    messagebox.showerror("Error", f"Speech service error: {str(e)}")
                except spr.WaitTimeoutError:
                    self.update_status("Listening timed out", error=True)
                    messagebox.showerror("Error", "No speech detected within timeout")
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
        self.status.config(text=message, fg=self.danger_color if error else self.secondary_color)
        
        if not error:
            def clear_status():
                time.sleep(5)
                if self.status['text'] == message:
                    self.status.config(text="Ready", fg=self.secondary_color)
            
            threading.Thread(target=clear_status, daemon=True).start()

if __name__ == "__main__":
    root = tk.Tk()
    
    # Set window icon
    try:
        if platform.system() == 'Windows':
            root.iconbitmap(default='icon.ico')
    except:
        pass
    
    app = PolyGlotPro(root)
    root.mainloop()
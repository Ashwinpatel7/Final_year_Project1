"""
Main entry point for the Language Translator application.
Initializes the application and starts the main event loop.
"""

import tkinter as tk
import platform
import speech_recognition as sr
import os
from tkinter import font as tkfont

from ui import (
    WelcomeScreen,
    TranslatorScreen,
    DocumentScreen,
    ImageScreen,
    VoiceScreen
)

class LanguageTranslatorApp:
    """Main application class for the Language Translator."""
    
    def __init__(self, root):
        """Initialize the application."""
        self.root = root
        self.root.title('Final Fusion - Advanced Translator')
        self.root.geometry('1200x750+100+50')
        self.root.minsize(1000, 650)
        
        # Set application icon
        self.set_app_icon()
        
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.is_listening = False
        
        # Create container for frames
        self.container = tk.Frame(root)
        self.container.pack(fill=tk.BOTH, expand=True)
        
        # Initialize frames dictionary
        self.frames = {}
        
        # Create and add frames
        for F in (WelcomeScreen, TranslatorScreen, DocumentScreen, ImageScreen, VoiceScreen):
            frame = F(self.container, self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        # Configure grid
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        # Show welcome screen initially
        self.show_frame("WelcomeScreen")
    
    def set_app_icon(self):
        """Set the application icon based on the platform."""
        try:
            if platform.system() == 'Windows':
                if os.path.exists('assets/icon.ico'):
                    self.root.iconbitmap(default='assets/icon.ico')
            elif platform.system() == 'Darwin':  # macOS
                # macOS uses .icns format
                pass
            else:  # Linux
                # Linux typically uses .png format
                pass
        except Exception:
            # If icon setting fails, continue without an icon
            pass
    
    def show_frame(self, cont):
        """Show the specified frame."""
        frame = self.frames[cont]
        frame.tkraise()
        
        # Update status if applicable
        if hasattr(frame, 'update_status'):
            frame.update_status("Ready")

def main():
    """Main function to start the application."""
    root = tk.Tk()
    app = LanguageTranslatorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

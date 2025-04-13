# Final Fusion Translator

A modern, feature-rich language translation application with a sleek UI and multiple translation modes.

## Features

- **Text Translation**: Translate text between different languages
- **Voice Translation**: Translate spoken language in real-time
- **Document Translation**: Upload and translate documents (PDF, DOCX, TXT)
- **Image Translation**: Extract and translate text from images using OCR
- **Modern UI**: Sleek, responsive interface with light and dark themes
- **Text-to-Speech**: Listen to translations in their native accent
- **Speech Recognition**: Convert speech to text for translation

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/Ashwinpatel7/Final_year_Project1.git
   ```

2. Install Python (version 3.10 or later) from the [official website](https://www.python.org/downloads/)

3. Install the required dependencies:
   ```
   pip install deep-translator gtts pyperclip SpeechRecognition pillow pytesseract pdf2image python-docx
   ```

4. For OCR functionality (image and PDF translation), install Tesseract OCR:
   - Windows: Download and install from [here](https://github.com/UB-Mannheim/tesseract/wiki)
   - macOS: `brew install tesseract`
   - Linux: `sudo apt install tesseract-ocr`

5. Run the application:
   ```
   python main.py
   ```

## Project Structure

The project follows a modular architecture:

```
language-translator/
├── assets/                # Icons and resources
├── ui/                    # UI components
│   ├── __init__.py        # UI package initialization
│   ├── base_screen.py     # Base screen class
│   ├── welcome_screen.py  # Welcome screen with menu
│   ├── translator_screen.py # Text translation screen
│   ├── document_screen.py # Document translation screen
│   ├── image_screen.py    # Image translation screen
│   └── voice_screen.py    # Voice translation screen
├── config.py              # Configuration and constants
├── utils.py               # Utility functions
├── main.py                # Main application entry point
└── README.md              # Project documentation
```

## Usage

1. Launch the application by running `python main.py`
2. Select the desired translation mode from the welcome screen
3. Follow the on-screen instructions for each mode:
   - **Text Translation**: Enter text, select languages, and click "Translate"
   - **Voice Translation**: Click "Start Listening", speak, and view the translation
   - **Document Translation**: Upload a document, select target language, and translate
   - **Image Translation**: Upload an image, extract text, and translate

## Implementation

The Final Fusion Translator is built with a modern, modular architecture that separates concerns and makes the codebase maintainable and extensible:

- **UI Layer**: Built with Tkinter, featuring a responsive design with light and dark themes
- **Translation Engine**: Uses Google Translate API through the deep-translator library
- **OCR Capabilities**: Integrates Tesseract OCR for extracting text from images and PDFs
- **Document Processing**: Handles various document formats including PDF, DOCX, and TXT
- **Speech Processing**: Incorporates speech recognition and text-to-speech functionality

## Screenshots

(Screenshots will be added after running the application)

## Dependencies

- deep-translator: For translation services
- gtts: For text-to-speech functionality
- pyperclip: For clipboard operations
- SpeechRecognition: For speech-to-text functionality
- pillow: For image processing
- pytesseract: For OCR (optical character recognition)
- pdf2image: For converting PDFs to images
- python-docx: For processing Word documents

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Google Translate API for translation services
- Tesseract OCR for text extraction from images
- All the open-source libraries that made this project possible

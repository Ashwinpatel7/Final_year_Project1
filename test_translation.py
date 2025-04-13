from deep_translator import GoogleTranslator

def test_translation():
    translator = GoogleTranslator(source='en', target='es')
    result = translator.translate("Hello, world!")
    print(f"Translation: {result}")

if __name__ == "__main__":
    test_translation()

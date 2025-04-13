import axios from 'axios';

// Define the supported languages
export const LANGUAGES = {
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
};

// Function to translate text
export async function translateText(text: string, sourceLang: string, targetLang: string) {
  try {
    const response = await axios.post('/api/translate', {
      text,
      sourceLang,
      targetLang
    });
    
    return response.data.translatedText;
  } catch (error) {
    console.error('Translation error:', error);
    throw new Error('Failed to translate text');
  }
}

// Function to speak text using the Web Speech API
export function speakText(text: string, lang: string) {
  return new Promise((resolve, reject) => {
    if (!('speechSynthesis' in window)) {
      reject(new Error('Your browser does not support text-to-speech'));
      return;
    }

    // Stop any ongoing speech
    window.speechSynthesis.cancel();

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = lang;
    utterance.rate = 1.0;
    utterance.pitch = 1.0;
    
    utterance.onend = () => {
      resolve(true);
    };
    
    utterance.onerror = (event) => {
      reject(new Error(`Speech synthesis error: ${event.error}`));
    };
    
    window.speechSynthesis.speak(utterance);
  });
}

// Function to copy text to clipboard
export function copyToClipboard(text: string) {
  return navigator.clipboard.writeText(text);
}

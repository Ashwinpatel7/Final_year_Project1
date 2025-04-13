import { NextRequest, NextResponse } from 'next/server';
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

export async function POST(request: NextRequest) {
  try {
    const { text, sourceLang, targetLang } = await request.json();

    if (!text) {
      return NextResponse.json({ error: 'Text is required' }, { status: 400 });
    }

    if (!targetLang) {
      return NextResponse.json({ error: 'Target language is required' }, { status: 400 });
    }

    // Use a free translation API (LibreTranslate)
    const response = await axios.post('https://libretranslate.com/translate', {
      q: text,
      source: sourceLang || 'auto',
      target: targetLang,
      format: 'text',
      api_key: '' // Free tier doesn't require API key for small requests
    });

    return NextResponse.json({ 
      translatedText: response.data.translatedText,
      detectedLanguage: response.data.detectedLanguage?.language
    });
  } catch (error) {
    console.error('Translation error:', error);
    return NextResponse.json(
      { error: 'Failed to translate text' }, 
      { status: 500 }
    );
  }
}

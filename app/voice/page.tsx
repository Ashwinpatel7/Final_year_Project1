'use client';

import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { FaMicrophone, FaMicrophoneSlash, FaSync, FaCopy, FaVolumeUp, FaTrash } from 'react-icons/fa';
import Header from '@/components/Header';
import Footer from '@/components/Footer';
import LanguageSelector from '@/components/LanguageSelector';
import TranslateButton from '@/components/TranslateButton';
import { translateText, speakText, copyToClipboard } from '@/utils/translation';

export default function VoicePage() {
  // State
  const [darkMode, setDarkMode] = useState(false);
  const [recognizedText, setRecognizedText] = useState('');
  const [translatedText, setTranslatedText] = useState('');
  const [sourceLang, setSourceLang] = useState('auto');
  const [targetLang, setTargetLang] = useState('en');
  const [isListening, setIsListening] = useState(false);
  const [isTranslating, setIsTranslating] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [status, setStatus] = useState('Ready');
  const [isError, setIsError] = useState(false);
  
  // Speech recognition
  const [recognition, setRecognition] = useState<any>(null);
  
  // Initialize speech recognition
  useEffect(() => {
    if (typeof window !== 'undefined') {
      // Check if browser supports speech recognition
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      
      if (SpeechRecognition) {
        const recognitionInstance = new SpeechRecognition();
        recognitionInstance.continuous = true;
        recognitionInstance.interimResults = true;
        
        recognitionInstance.onresult = (event: any) => {
          let interimTranscript = '';
          let finalTranscript = '';
          
          for (let i = event.resultIndex; i < event.results.length; i++) {
            const transcript = event.results[i][0].transcript;
            
            if (event.results[i].isFinal) {
              finalTranscript += transcript;
            } else {
              interimTranscript += transcript;
            }
          }
          
          if (finalTranscript) {
            setRecognizedText((prev) => prev + ' ' + finalTranscript);
          }
        };
        
        recognitionInstance.onerror = (event: any) => {
          console.error('Speech recognition error', event.error);
          setStatus(`Speech recognition error: ${event.error}`);
          setIsError(true);
          setIsListening(false);
        };
        
        recognitionInstance.onend = () => {
          if (isListening) {
            recognitionInstance.start();
          }
        };
        
        setRecognition(recognitionInstance);
      } else {
        setStatus('Speech recognition is not supported in your browser');
        setIsError(true);
      }
    }
    
    // Cleanup
    return () => {
      if (recognition) {
        recognition.stop();
      }
    };
  }, []);
  
  // Toggle dark mode
  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
  };
  
  // Swap languages
  const swapLanguages = () => {
    if (sourceLang !== 'auto') {
      const temp = sourceLang;
      setSourceLang(targetLang);
      setTargetLang(temp);
      
      // Also swap the text content
      setRecognizedText(translatedText);
      setTranslatedText(recognizedText);
      
      setStatus('Languages swapped');
    }
  };
  
  // Toggle listening
  const toggleListening = () => {
    if (!recognition) {
      setStatus('Speech recognition is not supported in your browser');
      setIsError(true);
      return;
    }
    
    if (isListening) {
      recognition.stop();
      setIsListening(false);
      setStatus('Listening stopped');
    } else {
      setRecognizedText('');
      recognition.start();
      setIsListening(true);
      setStatus('Listening... Speak now');
    }
  };
  
  // Handle translation
  const handleTranslate = async () => {
    if (!recognizedText.trim()) {
      setStatus('No speech to translate');
      setIsError(true);
      return;
    }
    
    try {
      setIsTranslating(true);
      setStatus('Translating...');
      setIsError(false);
      
      const translated = await translateText(recognizedText, sourceLang, targetLang);
      setTranslatedText(translated);
      
      setStatus(`Speech translated to ${targetLang}`);
    } catch (error) {
      console.error('Translation error:', error);
      setStatus('Translation failed. Please try again.');
      setIsError(true);
    } finally {
      setIsTranslating(false);
    }
  };
  
  // Handle text-to-speech
  const handleSpeak = async () => {
    if (!translatedText.trim()) {
      setStatus('No translated text to read');
      setIsError(true);
      return;
    }
    
    try {
      setIsSpeaking(true);
      setStatus('Speaking...');
      setIsError(false);
      
      await speakText(translatedText, targetLang);
      
      setStatus('Text read successfully');
    } catch (error) {
      console.error('Speech error:', error);
      setStatus('Failed to read text. Please try again.');
      setIsError(true);
    } finally {
      setIsSpeaking(false);
    }
  };
  
  // Handle copy to clipboard
  const handleCopy = async () => {
    if (!translatedText.trim()) {
      setStatus('No text to copy');
      setIsError(true);
      return;
    }
    
    try {
      await copyToClipboard(translatedText);
      setStatus('Text copied to clipboard');
      setIsError(false);
    } catch (error) {
      console.error('Copy error:', error);
      setStatus('Failed to copy text');
      setIsError(true);
    }
  };
  
  // Handle clear
  const handleClear = () => {
    setRecognizedText('');
    setTranslatedText('');
    setStatus('Text cleared');
    setIsError(false);
  };
  
  return (
    <div className={`flex flex-col min-h-screen ${darkMode ? 'bg-gray-900 text-white' : 'bg-gray-50 text-gray-900'}`}>
      <Header darkMode={darkMode} toggleDarkMode={toggleDarkMode} />
      
      <main className="flex-grow container mx-auto px-4 py-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className={`p-6 rounded-xl shadow-lg ${darkMode ? 'bg-gray-800' : 'bg-white'}`}
        >
          <LanguageSelector
            sourceLang={sourceLang}
            targetLang={targetLang}
            onSourceLangChange={setSourceLang}
            onTargetLangChange={setTargetLang}
            onSwapLanguages={swapLanguages}
            darkMode={darkMode}
          />
          
          {/* Microphone section */}
          <div className="flex flex-col items-center justify-center mb-8">
            <motion.div
              className={`w-24 h-24 rounded-full flex items-center justify-center mb-4 cursor-pointer ${
                isListening 
                  ? 'bg-red-500 animate-pulse' 
                  : darkMode ? 'bg-gray-700' : 'bg-gray-200'
              }`}
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.9 }}
              onClick={toggleListening}
            >
              {isListening ? (
                <FaMicrophoneSlash className="text-white text-3xl" />
              ) : (
                <FaMicrophone className={`text-3xl ${darkMode ? 'text-white' : 'text-gray-700'}`} />
              )}
            </motion.div>
            
            <p className={`text-lg font-medium ${isListening ? 'text-red-500' : ''}`}>
              {isListening ? 'Listening... Click to stop' : 'Click to start listening'}
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
            {/* Recognized text area */}
            <div className="flex flex-col">
              <label 
                htmlFor="recognizedText" 
                className={`block mb-2 font-medium ${darkMode ? 'text-gray-200' : 'text-gray-700'}`}
              >
                Recognized Speech
              </label>
              <textarea
                id="recognizedText"
                value={recognizedText}
                onChange={(e) => setRecognizedText(e.target.value)}
                className={`w-full h-48 p-4 border rounded-lg resize-none focus:ring-2 focus:outline-none ${
                  darkMode 
                    ? 'bg-gray-700 border-gray-600 text-white focus:ring-purple-600' 
                    : 'bg-white border-gray-300 text-gray-900 focus:ring-purple-500'
                }`}
                placeholder="Speak or type text here..."
              />
            </div>
            
            {/* Translated text area */}
            <div className="flex flex-col">
              <label 
                htmlFor="translatedText" 
                className={`block mb-2 font-medium ${darkMode ? 'text-gray-200' : 'text-gray-700'}`}
              >
                Translation
              </label>
              <textarea
                id="translatedText"
                value={translatedText}
                readOnly
                className={`w-full h-48 p-4 border rounded-lg resize-none focus:outline-none ${
                  darkMode 
                    ? 'bg-gray-700 border-gray-600 text-white' 
                    : 'bg-white border-gray-300 text-gray-900'
                }`}
                placeholder="Translation will appear here..."
              />
            </div>
          </div>
          
          {/* Translate button */}
          <div className="flex flex-col items-center justify-center my-6">
            <TranslateButton
              onClick={handleTranslate}
              isLoading={isTranslating}
              text="Translate Speech"
              className="w-64 h-12 text-lg"
            />
          </div>
          
          {/* Action buttons */}
          <div className="flex flex-wrap justify-center gap-4">
            <motion.button
              onClick={handleClear}
              className={`flex items-center px-4 py-2 rounded-lg ${
                darkMode 
                  ? 'bg-gray-700 text-white hover:bg-gray-600' 
                  : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
              }`}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              <FaTrash className="mr-2" />
              Clear
            </motion.button>
            
            <motion.button
              onClick={handleCopy}
              className={`flex items-center px-4 py-2 rounded-lg ${
                darkMode 
                  ? 'bg-green-700 text-white hover:bg-green-600' 
                  : 'bg-green-500 text-white hover:bg-green-600'
              }`}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              <FaCopy className="mr-2" />
              Copy
            </motion.button>
            
            <motion.button
              onClick={handleSpeak}
              disabled={isSpeaking}
              className={`flex items-center px-4 py-2 rounded-lg ${
                darkMode 
                  ? 'bg-blue-700 text-white hover:bg-blue-600' 
                  : 'bg-blue-500 text-white hover:bg-blue-600'
              } disabled:opacity-70 disabled:cursor-not-allowed`}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              <FaVolumeUp className="mr-2" />
              {isSpeaking ? 'Speaking...' : 'Read Aloud'}
            </motion.button>
          </div>
        </motion.div>
      </main>
      
      <Footer darkMode={darkMode} status={status} isError={isError} />
    </div>
  );
}

'use client';

import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { FaSync, FaCopy, FaVolumeUp, FaTrash } from 'react-icons/fa';
import Header from '@/components/Header';
import Footer from '@/components/Footer';
import LanguageSelector from '@/components/LanguageSelector';
import TranslateButton from '@/components/TranslateButton';
import { translateText, speakText, copyToClipboard } from '@/utils/translation';

export default function Home() {
  // State
  const [darkMode, setDarkMode] = useState(false);
  const [inputText, setInputText] = useState('');
  const [outputText, setOutputText] = useState('');
  const [sourceLang, setSourceLang] = useState('auto');
  const [targetLang, setTargetLang] = useState('en');
  const [isTranslating, setIsTranslating] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [status, setStatus] = useState('Ready');
  const [isError, setIsError] = useState(false);
  const [charCount, setCharCount] = useState(0);

  // Update character count when input text changes
  useEffect(() => {
    setCharCount(inputText.length);
  }, [inputText]);

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
      setInputText(outputText);
      setOutputText(inputText);
      
      setStatus('Languages swapped');
    }
  };

  // Handle translation
  const handleTranslate = async () => {
    if (!inputText.trim()) {
      setStatus('Please enter text to translate');
      setIsError(true);
      return;
    }

    try {
      setIsTranslating(true);
      setStatus('Translating...');
      setIsError(false);

      const translated = await translateText(inputText, sourceLang, targetLang);
      setOutputText(translated);
      
      setStatus(`Translated from ${sourceLang === 'auto' ? 'Auto Detect' : sourceLang} to ${targetLang}`);
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
    if (!outputText.trim()) {
      setStatus('No translated text to read');
      setIsError(true);
      return;
    }

    try {
      setIsSpeaking(true);
      setStatus('Speaking...');
      setIsError(false);

      await speakText(outputText, targetLang);
      
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
    if (!outputText.trim()) {
      setStatus('No text to copy');
      setIsError(true);
      return;
    }

    try {
      await copyToClipboard(outputText);
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
    setInputText('');
    setOutputText('');
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
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
            {/* Input text area */}
            <div className="flex flex-col">
              <label 
                htmlFor="inputText" 
                className={`block mb-2 font-medium ${darkMode ? 'text-gray-200' : 'text-gray-700'}`}
              >
                Enter text
              </label>
              <textarea
                id="inputText"
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                className={`w-full h-64 p-4 border rounded-lg resize-none focus:ring-2 focus:outline-none ${
                  darkMode 
                    ? 'bg-gray-700 border-gray-600 text-white focus:ring-purple-600' 
                    : 'bg-white border-gray-300 text-gray-900 focus:ring-purple-500'
                }`}
                placeholder="Type or paste text here..."
              />
              <div className="text-right mt-2 text-sm text-gray-500">
                {charCount} characters
              </div>
            </div>
            
            {/* Output text area */}
            <div className="flex flex-col">
              <label 
                htmlFor="outputText" 
                className={`block mb-2 font-medium ${darkMode ? 'text-gray-200' : 'text-gray-700'}`}
              >
                Translation
              </label>
              <textarea
                id="outputText"
                value={outputText}
                readOnly
                className={`w-full h-64 p-4 border rounded-lg resize-none focus:outline-none ${
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
              text="Translate Now"
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

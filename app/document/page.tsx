'use client';

import React, { useState, useRef } from 'react';
import { motion } from 'framer-motion';
import { FaFileUpload, FaSync, FaCopy, FaVolumeUp, FaTrash, FaDownload } from 'react-icons/fa';
import Header from '@/components/Header';
import Footer from '@/components/Footer';
import LanguageSelector from '@/components/LanguageSelector';
import TranslateButton from '@/components/TranslateButton';
import { translateText, speakText, copyToClipboard } from '@/utils/translation';

export default function DocumentPage() {
  // State
  const [darkMode, setDarkMode] = useState(false);
  const [documentText, setDocumentText] = useState('');
  const [translatedText, setTranslatedText] = useState('');
  const [fileName, setFileName] = useState('');
  const [sourceLang, setSourceLang] = useState('auto');
  const [targetLang, setTargetLang] = useState('en');
  const [isTranslating, setIsTranslating] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [status, setStatus] = useState('Ready');
  const [isError, setIsError] = useState(false);
  
  // File input ref
  const fileInputRef = useRef<HTMLInputElement>(null);
  
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
      setDocumentText(translatedText);
      setTranslatedText(documentText);
      
      setStatus('Languages swapped');
    }
  };
  
  // Handle file upload
  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    
    setIsLoading(true);
    setStatus(`Loading document: ${file.name}...`);
    setIsError(false);
    setFileName(file.name);
    
    try {
      // Read file content
      const text = await readFileContent(file);
      setDocumentText(text);
      setStatus(`Document loaded successfully: ${file.name}`);
    } catch (error) {
      console.error('Error loading document:', error);
      setStatus('Failed to load document. Please try again.');
      setIsError(true);
    } finally {
      setIsLoading(false);
    }
  };
  
  // Read file content
  const readFileContent = (file: File): Promise<string> => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      
      reader.onload = (event) => {
        const content = event.target?.result as string;
        resolve(content);
      };
      
      reader.onerror = (error) => {
        reject(error);
      };
      
      // Read as text
      reader.readAsText(file);
    });
  };
  
  // Handle translation
  const handleTranslate = async () => {
    if (!documentText.trim()) {
      setStatus('No document content to translate');
      setIsError(true);
      return;
    }
    
    try {
      setIsTranslating(true);
      setStatus(`Translating document to ${targetLang}...`);
      setIsError(false);
      
      const translated = await translateText(documentText, sourceLang, targetLang);
      setTranslatedText(translated);
      
      setStatus(`Document translated successfully to ${targetLang}`);
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
    setDocumentText('');
    setTranslatedText('');
    setFileName('');
    setStatus('Document cleared');
    setIsError(false);
    
    // Reset file input
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };
  
  // Handle download translated document
  const handleDownload = () => {
    if (!translatedText.trim()) {
      setStatus('No translated text to download');
      setIsError(true);
      return;
    }
    
    try {
      const element = document.createElement('a');
      const file = new Blob([translatedText], { type: 'text/plain' });
      element.href = URL.createObjectURL(file);
      
      // Create filename with language code
      const originalName = fileName || 'document';
      const extension = originalName.includes('.') ? originalName.split('.').pop() : 'txt';
      const nameWithoutExtension = originalName.includes('.')
        ? originalName.substring(0, originalName.lastIndexOf('.'))
        : originalName;
      
      element.download = `${nameWithoutExtension}_${targetLang}.${extension}`;
      document.body.appendChild(element);
      element.click();
      document.body.removeChild(element);
      
      setStatus('Translated document downloaded');
      setIsError(false);
    } catch (error) {
      console.error('Download error:', error);
      setStatus('Failed to download document');
      setIsError(true);
    }
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
          
          {/* File upload section */}
          <div className="flex flex-col items-center justify-center mb-8">
            <input
              type="file"
              ref={fileInputRef}
              onChange={handleFileUpload}
              accept=".txt,.doc,.docx,.pdf"
              className="hidden"
              id="file-upload"
            />
            
            <motion.label
              htmlFor="file-upload"
              className={`flex flex-col items-center justify-center w-full h-32 border-2 border-dashed rounded-lg cursor-pointer ${
                darkMode 
                  ? 'bg-gray-700 border-gray-600 hover:bg-gray-600' 
                  : 'bg-gray-50 border-gray-300 hover:bg-gray-100'
              }`}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
            >
              <div className="flex flex-col items-center justify-center pt-5 pb-6">
                <FaFileUpload className={`w-10 h-10 mb-3 ${darkMode ? 'text-gray-400' : 'text-gray-500'}`} />
                <p className={`mb-2 text-sm ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>
                  <span className="font-semibold">Click to upload</span> or drag and drop
                </p>
                <p className={`text-xs ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>
                  TXT, DOC, DOCX, or PDF (max. 10MB)
                </p>
              </div>
            </motion.label>
            
            {fileName && (
              <p className="mt-2 text-sm text-gray-500">
                Selected file: {fileName}
              </p>
            )}
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
            {/* Document text area */}
            <div className="flex flex-col">
              <label 
                htmlFor="documentText" 
                className={`block mb-2 font-medium ${darkMode ? 'text-gray-200' : 'text-gray-700'}`}
              >
                Document Content
              </label>
              <textarea
                id="documentText"
                value={documentText}
                onChange={(e) => setDocumentText(e.target.value)}
                className={`w-full h-64 p-4 border rounded-lg resize-none focus:ring-2 focus:outline-none ${
                  darkMode 
                    ? 'bg-gray-700 border-gray-600 text-white focus:ring-purple-600' 
                    : 'bg-white border-gray-300 text-gray-900 focus:ring-purple-500'
                }`}
                placeholder="Document content will appear here..."
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
              text="Translate Document"
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
            
            <motion.button
              onClick={handleDownload}
              className={`flex items-center px-4 py-2 rounded-lg ${
                darkMode 
                  ? 'bg-purple-700 text-white hover:bg-purple-600' 
                  : 'bg-purple-600 text-white hover:bg-purple-700'
              }`}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              <FaDownload className="mr-2" />
              Download
            </motion.button>
          </div>
        </motion.div>
      </main>
      
      <Footer darkMode={darkMode} status={status} isError={isError} />
    </div>
  );
}

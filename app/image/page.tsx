'use client';

import React, { useState, useRef } from 'react';
import { motion } from 'framer-motion';
import { FaImage, FaSync, FaCopy, FaVolumeUp, FaTrash, FaDownload, FaSearch } from 'react-icons/fa';
import Header from '@/components/Header';
import Footer from '@/components/Footer';
import LanguageSelector from '@/components/LanguageSelector';
import TranslateButton from '@/components/TranslateButton';
import { translateText, speakText, copyToClipboard } from '@/utils/translation';

export default function ImagePage() {
  // State
  const [darkMode, setDarkMode] = useState(false);
  const [imageUrl, setImageUrl] = useState<string | null>(null);
  const [extractedText, setExtractedText] = useState('');
  const [translatedText, setTranslatedText] = useState('');
  const [fileName, setFileName] = useState('');
  const [sourceLang, setSourceLang] = useState('auto');
  const [targetLang, setTargetLang] = useState('en');
  const [isTranslating, setIsTranslating] = useState(false);
  const [isExtracting, setIsExtracting] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
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
      setExtractedText(translatedText);
      setTranslatedText(extractedText);
      
      setStatus('Languages swapped');
    }
  };
  
  // Handle image upload
  const handleImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    
    setFileName(file.name);
    
    // Create object URL for preview
    const objectUrl = URL.createObjectURL(file);
    setImageUrl(objectUrl);
    
    // Reset text fields
    setExtractedText('');
    setTranslatedText('');
    
    setStatus(`Image loaded: ${file.name}`);
    setIsError(false);
    
    // Clean up previous object URL
    return () => {
      if (imageUrl) {
        URL.revokeObjectURL(imageUrl);
      }
    };
  };
  
  // Handle text extraction
  const handleExtractText = async () => {
    if (!imageUrl) {
      setStatus('No image selected');
      setIsError(true);
      return;
    }
    
    try {
      setIsExtracting(true);
      setStatus('Extracting text from image...');
      setIsError(false);
      
      // In a real implementation, you would use an OCR service like Tesseract.js or Google Cloud Vision
      // For this demo, we'll simulate text extraction with a timeout
      
      // Simulated OCR result
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      // Sample extracted text based on the image name
      let simulatedText = '';
      
      if (fileName.toLowerCase().includes('receipt')) {
        simulatedText = 'RECEIPT\nStore: Global Market\nDate: 2023-04-13\nItems:\n- Apples $2.99\n- Bread $3.49\n- Milk $4.29\nTotal: $10.77';
      } else if (fileName.toLowerCase().includes('menu')) {
        simulatedText = 'MENU\nAppetizers:\n- Garlic Bread $5.99\n- Mozzarella Sticks $7.99\nMain Courses:\n- Spaghetti Bolognese $14.99\n- Grilled Salmon $18.99\nDesserts:\n- Tiramisu $6.99\n- Ice Cream $4.99';
      } else if (fileName.toLowerCase().includes('sign')) {
        simulatedText = 'CAUTION\nWet Floor\nPlease use alternative route';
      } else {
        simulatedText = 'Sample text extracted from image.\nThis is a demonstration of OCR functionality.\nIn a real application, this would use an actual OCR service.';
      }
      
      setExtractedText(simulatedText);
      setStatus('Text extracted successfully');
    } catch (error) {
      console.error('Text extraction error:', error);
      setStatus('Failed to extract text from image');
      setIsError(true);
    } finally {
      setIsExtracting(false);
    }
  };
  
  // Handle translation
  const handleTranslate = async () => {
    if (!extractedText.trim()) {
      setStatus('No text to translate');
      setIsError(true);
      return;
    }
    
    try {
      setIsTranslating(true);
      setStatus('Translating text...');
      setIsError(false);
      
      const translated = await translateText(extractedText, sourceLang, targetLang);
      setTranslatedText(translated);
      
      setStatus(`Text translated successfully to ${targetLang}`);
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
    setImageUrl(null);
    setExtractedText('');
    setTranslatedText('');
    setFileName('');
    setStatus('Image and text cleared');
    setIsError(false);
    
    // Reset file input
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
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
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
            {/* Image upload and preview section */}
            <div className="flex flex-col">
              <label 
                className={`block mb-2 font-medium ${darkMode ? 'text-gray-200' : 'text-gray-700'}`}
              >
                Image Preview
              </label>
              
              <div 
                className={`relative w-full h-64 border rounded-lg overflow-hidden ${
                  darkMode ? 'bg-gray-700 border-gray-600' : 'bg-gray-100 border-gray-300'
                }`}
              >
                {imageUrl ? (
                  <img 
                    src={imageUrl} 
                    alt="Uploaded image" 
                    className="w-full h-full object-contain"
                  />
                ) : (
                  <div className="flex flex-col items-center justify-center h-full">
                    <FaImage className={`w-12 h-12 mb-3 ${darkMode ? 'text-gray-500' : 'text-gray-400'}`} />
                    <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>
                      No image selected
                    </p>
                  </div>
                )}
                
                <input
                  type="file"
                  ref={fileInputRef}
                  onChange={handleImageUpload}
                  accept="image/*"
                  className="hidden"
                  id="image-upload"
                />
                
                <motion.label
                  htmlFor="image-upload"
                  className={`absolute bottom-3 right-3 p-2 rounded-full cursor-pointer ${
                    darkMode ? 'bg-gray-600 hover:bg-gray-500' : 'bg-white hover:bg-gray-200'
                  } shadow-md`}
                  whileHover={{ scale: 1.1 }}
                  whileTap={{ scale: 0.9 }}
                >
                  <FaImage className={`w-5 h-5 ${darkMode ? 'text-white' : 'text-gray-700'}`} />
                </motion.label>
              </div>
              
              {fileName && (
                <p className="mt-2 text-sm text-gray-500">
                  Selected image: {fileName}
                </p>
              )}
              
              {/* Extract text button */}
              <motion.button
                onClick={handleExtractText}
                disabled={!imageUrl || isExtracting}
                className={`mt-4 flex items-center justify-center px-4 py-2 font-medium rounded-lg ${
                  !imageUrl || isExtracting
                    ? 'bg-gray-400 text-gray-200 cursor-not-allowed'
                    : darkMode
                      ? 'bg-orange-600 text-white hover:bg-orange-700'
                      : 'bg-orange-500 text-white hover:bg-orange-600'
                }`}
                whileHover={{ scale: imageUrl && !isExtracting ? 1.05 : 1 }}
                whileTap={{ scale: imageUrl && !isExtracting ? 0.95 : 1 }}
              >
                <FaSearch className={`mr-2 ${isExtracting ? 'animate-spin' : ''}`} />
                {isExtracting ? 'Extracting Text...' : 'Extract Text'}
              </motion.button>
            </div>
            
            {/* Extracted text area */}
            <div className="flex flex-col">
              <label 
                htmlFor="extractedText" 
                className={`block mb-2 font-medium ${darkMode ? 'text-gray-200' : 'text-gray-700'}`}
              >
                Extracted Text
              </label>
              <textarea
                id="extractedText"
                value={extractedText}
                onChange={(e) => setExtractedText(e.target.value)}
                className={`w-full h-64 p-4 border rounded-lg resize-none focus:ring-2 focus:outline-none ${
                  darkMode 
                    ? 'bg-gray-700 border-gray-600 text-white focus:ring-purple-600' 
                    : 'bg-white border-gray-300 text-gray-900 focus:ring-purple-500'
                }`}
                placeholder="Extracted text will appear here..."
              />
            </div>
          </div>
          
          {/* Translated text area */}
          <div className="mb-6">
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
              className={`w-full h-32 p-4 border rounded-lg resize-none focus:outline-none ${
                darkMode 
                  ? 'bg-gray-700 border-gray-600 text-white' 
                  : 'bg-white border-gray-300 text-gray-900'
              }`}
              placeholder="Translation will appear here..."
            />
          </div>
          
          {/* Translate button */}
          <div className="flex flex-col items-center justify-center my-6">
            <TranslateButton
              onClick={handleTranslate}
              isLoading={isTranslating}
              text="Translate Image Text"
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

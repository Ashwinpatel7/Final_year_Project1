import React from 'react';
import { motion } from 'framer-motion';
import { FaExchangeAlt } from 'react-icons/fa';
import { LANGUAGES } from '@/utils/translation';

interface LanguageSelectorProps {
  sourceLang: string;
  targetLang: string;
  onSourceLangChange: (lang: string) => void;
  onTargetLangChange: (lang: string) => void;
  onSwapLanguages: () => void;
  darkMode: boolean;
}

const LanguageSelector: React.FC<LanguageSelectorProps> = ({
  sourceLang,
  targetLang,
  onSourceLangChange,
  onTargetLangChange,
  onSwapLanguages,
  darkMode
}) => {
  return (
    <div className="flex flex-col md:flex-row items-center justify-between w-full gap-4 mb-6">
      <div className="w-full md:w-2/5">
        <label 
          htmlFor="sourceLang" 
          className={`block mb-2 font-medium ${darkMode ? 'text-gray-200' : 'text-gray-700'}`}
        >
          Translate from:
        </label>
        <select
          id="sourceLang"
          value={sourceLang}
          onChange={(e) => onSourceLangChange(e.target.value)}
          className={`w-full p-3 border rounded-lg focus:ring-2 focus:outline-none ${
            darkMode 
              ? 'bg-gray-800 border-gray-700 text-white focus:ring-purple-600' 
              : 'bg-white border-gray-300 text-gray-900 focus:ring-purple-500'
          }`}
        >
          {Object.entries(LANGUAGES).map(([name, code]) => (
            <option key={code} value={code}>
              {name}
            </option>
          ))}
        </select>
      </div>

      <div className="flex items-center justify-center">
        <motion.button
          onClick={onSwapLanguages}
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.9 }}
          className={`p-3 rounded-full ${
            darkMode ? 'bg-gray-700 text-purple-400' : 'bg-gray-100 text-purple-600'
          }`}
          aria-label="Swap languages"
        >
          <FaExchangeAlt className="text-xl" />
        </motion.button>
      </div>

      <div className="w-full md:w-2/5">
        <label 
          htmlFor="targetLang" 
          className={`block mb-2 font-medium ${darkMode ? 'text-gray-200' : 'text-gray-700'}`}
        >
          Translate to:
        </label>
        <select
          id="targetLang"
          value={targetLang}
          onChange={(e) => onTargetLangChange(e.target.value)}
          className={`w-full p-3 border rounded-lg focus:ring-2 focus:outline-none ${
            darkMode 
              ? 'bg-gray-800 border-gray-700 text-white focus:ring-purple-600' 
              : 'bg-white border-gray-300 text-gray-900 focus:ring-purple-500'
          }`}
        >
          {Object.entries(LANGUAGES)
            .filter(([name]) => name !== 'Auto Detect')
            .map(([name, code]) => (
              <option key={code} value={code}>
                {name}
              </option>
            ))}
        </select>
      </div>
    </div>
  );
};

export default LanguageSelector;

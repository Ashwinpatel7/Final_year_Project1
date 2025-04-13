import React from 'react';
import Link from 'next/link';
import { motion } from 'framer-motion';
import { FaMoon, FaSun } from 'react-icons/fa';

interface HeaderProps {
  darkMode: boolean;
  toggleDarkMode: () => void;
}

const Header: React.FC<HeaderProps> = ({ darkMode, toggleDarkMode }) => {
  return (
    <header className={`w-full py-4 px-6 ${darkMode ? 'bg-purple-900' : 'bg-purple-700'} text-white shadow-lg`}>
      <div className="container mx-auto flex justify-between items-center">
        <div className="flex items-center space-x-4">
          <motion.div
            className={`w-10 h-10 rounded-md flex items-center justify-center ${darkMode ? 'bg-blue-600' : 'bg-blue-500'}`}
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.95 }}
          >
            <span className="text-xl font-bold">FF</span>
          </motion.div>
          
          <div>
            <h1 className="text-2xl font-bold">Final Fusion</h1>
            <p className="text-sm opacity-90">Advanced Language Translator</p>
          </div>
        </div>
        
        <nav className="hidden md:flex items-center space-x-6">
          <Link href="/" className="hover:text-purple-200 transition-colors">
            Text Translation
          </Link>
          <Link href="/voice" className="hover:text-purple-200 transition-colors">
            Voice Translation
          </Link>
          <Link href="/document" className="hover:text-purple-200 transition-colors">
            Document Translation
          </Link>
          <Link href="/image" className="hover:text-purple-200 transition-colors">
            Image Translation
          </Link>
        </nav>
        
        <motion.button
          onClick={toggleDarkMode}
          className={`p-2 rounded-full ${darkMode ? 'bg-gray-800' : 'bg-purple-600'}`}
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.9 }}
          aria-label={darkMode ? 'Switch to light mode' : 'Switch to dark mode'}
        >
          {darkMode ? <FaSun className="text-yellow-300" /> : <FaMoon className="text-yellow-200" />}
        </motion.button>
      </div>
    </header>
  );
};

export default Header;

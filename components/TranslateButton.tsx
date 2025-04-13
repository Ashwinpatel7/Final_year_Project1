import React from 'react';
import { motion } from 'framer-motion';
import { FaSync } from 'react-icons/fa';

interface TranslateButtonProps {
  onClick: () => void;
  isLoading: boolean;
  text?: string;
  icon?: React.ReactNode;
  className?: string;
}

const TranslateButton: React.FC<TranslateButtonProps> = ({
  onClick,
  isLoading,
  text = 'Translate',
  icon = <FaSync />,
  className = ''
}) => {
  return (
    <motion.button
      onClick={onClick}
      disabled={isLoading}
      className={`flex items-center justify-center px-6 py-3 font-bold text-white bg-purple-600 rounded-lg shadow-md hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-opacity-50 disabled:opacity-70 disabled:cursor-not-allowed ${className}`}
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
    >
      <span className={`mr-2 ${isLoading ? 'animate-spin' : ''}`}>
        {icon}
      </span>
      {isLoading ? 'Translating...' : text}
    </motion.button>
  );
};

export default TranslateButton;

import React from 'react';

interface FooterProps {
  darkMode: boolean;
  status: string;
  isError: boolean;
}

const Footer: React.FC<FooterProps> = ({ darkMode, status, isError }) => {
  return (
    <footer className={`w-full py-3 px-6 border-t ${
      darkMode ? 'bg-gray-900 border-gray-800 text-gray-300' : 'bg-white border-gray-200 text-gray-600'
    }`}>
      <div className="container mx-auto flex justify-between items-center">
        <p className={`text-sm ${isError ? 'text-red-500' : ''}`}>
          {status || 'Ready'}
        </p>
        <p className="text-sm">Final Fusion v2.0</p>
      </div>
    </footer>
  );
};

export default Footer;

'use client';

import React from 'react';
import { motion } from 'framer-motion';

export default function Loading() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.5 }}
        className="text-center"
      >
        <div className="mb-6">
          <motion.div
            animate={{ 
              rotate: 360,
              scale: [1, 1.2, 1]
            }}
            transition={{ 
              rotate: { duration: 2, repeat: Infinity, ease: "linear" },
              scale: { duration: 1, repeat: Infinity, repeatType: "reverse" }
            }}
            className="inline-block w-16 h-16 rounded-full border-4 border-purple-600 border-t-transparent"
          />
        </div>
        
        <h2 className="text-2xl font-semibold text-gray-700 mb-2">Loading</h2>
        <p className="text-gray-600">
          Please wait while we prepare your translation experience...
        </p>
      </motion.div>
    </div>
  );
}

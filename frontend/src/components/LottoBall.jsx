import React from 'react';
import { motion } from 'framer-motion';

/** Token for Toto-style pick games (e.g. 6/58). */
export default function NumberToken({ n, idx = 0, size = 'md', variant = 'solid' }) {
  return (
    <motion.div
      initial={{ scale: 0.6, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      transition={{ delay: 0.06 * idx, type: 'spring', stiffness: 220, damping: 16 }}
      className={`num-token ${size === 'sm' ? 'sm' : ''} ${variant === 'outline' ? 'outline' : ''}`}
      data-testid={`result-ball-${idx + 1}`}
    >
      {String(n).padStart(2, '0')}
    </motion.div>
  );
}

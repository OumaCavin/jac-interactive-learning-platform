// JAC Learning Platform - Advanced Card component by Cavin Otieno

import React from 'react';
import { motion, Variants } from 'framer-motion';

/**
 * Advanced Card component with glassmorphism design
 * Supports variant and padding props used throughout the application
 */

interface AdvancedCardProps {
  variant?: 'glass' | 'glass-strong' | 'solid';
  padding?: 'none' | 'sm' | 'md' | 'lg';
  className?: string;
  children: React.ReactNode;
  hover?: boolean;
  onClick?: () => void;
}

const cardVariants: Variants = {
  initial: { y: 0, opacity: 1 },
  hover: { y: -4, opacity: 1 },
};

export const AdvancedCard: React.FC<AdvancedCardProps> = ({
  variant = 'glass',
  padding = 'md',
  className = '',
  children,
  hover = false,
  onClick,
}) => {
  const baseClasses = 'rounded-2xl transition-all duration-300';
  
  const variantClasses = {
    glass: 'glass-card',
    'glass-strong': 'glass-card-strong',
    solid: 'bg-white/10 backdrop-blur-md border border-white/20',
  };

  const paddingClasses = {
    none: '',
    sm: 'p-4',
    md: 'p-6',
    lg: 'p-8',
  };

  const classes = `${baseClasses} ${variantClasses[variant]} ${paddingClasses[padding]} ${className}`;

  if (onClick) {
    return (
      <motion.div
        variants={hover ? cardVariants : undefined}
        initial="initial"
        whileHover="hover"
        className={`${classes} cursor-pointer`}
        onClick={onClick}
      >
        {children}
      </motion.div>
    );
  }

  return (
    <motion.div
      variants={hover ? cardVariants : undefined}
      initial="initial"
      whileHover="hover"
      className={classes}
    >
      {children}
    </motion.div>
  );
};

export default AdvancedCard;
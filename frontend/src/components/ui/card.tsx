// JAC Learning Platform - TypeScript utilities by Cavin Otieno

import React from 'react';

interface CardProps {
  children: React.ReactNode;
  className?: string;
}

const Card: React.FC<CardProps> = ({ children, className = '' }) => (
  <div className={`bg-white rounded-lg shadow-md border ${className}`}>{children}</div>
);

const CardHeader: React.FC<CardProps> = ({ children, className = '' }) => (
  <div className={`px-6 py-4 border-b ${className}`}>{children}</div>
);

const CardTitle: React.FC<CardProps> = ({ children, className = '' }) => (
  <h3 className={`text-lg font-semibold text-gray-900 ${className}`}>{children}</h3>
);

const CardContent: React.FC<CardProps> = ({ children, className = '' }) => (
  <div className={`px-6 py-4 ${className}`}>{children}</div>
);

const CardDescription: React.FC<CardProps> = ({ children, className = '' }) => (
  <p className={`text-sm text-gray-600 mt-1 ${className}`}>{children}</p>
);

export { Card, CardHeader, CardTitle, CardContent, CardDescription };
export default Card;
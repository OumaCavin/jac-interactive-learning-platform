// JAC Learning Platform - TypeScript utilities by Cavin Otieno

import React from 'react';

interface AvatarProps {
  children?: React.ReactNode;
  className?: string;
}

const Avatar: React.FC<AvatarProps> = ({ children, className = '' }) => (
  <div className={`relative inline-flex h-10 w-10 overflow-hidden rounded-full ${className}`}>
    {children}
  </div>
);

interface AvatarFallbackProps {
  children: React.ReactNode;
  className?: string;
}

const AvatarFallback: React.FC<AvatarFallbackProps> = ({ children, className = '' }) => (
  <div className={`flex h-full w-full items-center justify-center rounded-full bg-gray-100 text-gray-600 ${className}`}>
    {children}
  </div>
);

export { Avatar, AvatarFallback };
export default Avatar;
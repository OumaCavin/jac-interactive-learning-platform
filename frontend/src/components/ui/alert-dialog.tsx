import React from 'react';

interface AlertDialogProps {
  children: React.ReactNode;
}

const AlertDialog: React.FC<AlertDialogProps> = ({ children }) => (
  <div className="fixed inset-0 z-50 flex items-center justify-center">
    <div className="bg-black bg-opacity-50 absolute inset-0"></div>
    <div className="relative bg-white rounded-lg shadow-lg max-w-md w-full mx-4">
      {children}
    </div>
  </div>
);

const AlertDialogContent: React.FC<{ children: React.ReactNode; className?: string }> = ({ children, className = '' }) => (
  <div className={`p-6 ${className}`}>{children}</div>
);

const AlertDialogHeader: React.FC<{ children: React.ReactNode; className?: string }> = ({ children, className = '' }) => (
  <div className={`mb-4 ${className}`}>{children}</div>
);

const AlertDialogTitle: React.FC<{ children: React.ReactNode; className?: string }> = ({ children, className = '' }) => (
  <h2 className={`text-lg font-semibold text-gray-900 ${className}`}>{children}</h2>
);

const AlertDialogDescription: React.FC<{ children: React.ReactNode; className?: string }> = ({ children, className = '' }) => (
  <p className={`text-sm text-gray-600 ${className}`}>{children}</p>
);

const AlertDialogFooter: React.FC<{ children: React.ReactNode; className?: string }> = ({ children, className = '' }) => (
  <div className={`flex justify-end space-x-2 mt-6 ${className}`}>{children}</div>
);

const AlertDialogAction: React.FC<{ children: React.ReactNode; onClick?: () => void; className?: string }> = ({ 
  children, 
  onClick, 
  className = '' 
}) => (
  <button 
    onClick={onClick}
    className={`px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 ${className}`}
  >
    {children}
  </button>
);

const AlertDialogCancel: React.FC<{ children: React.ReactNode; onClick?: () => void; className?: string }> = ({ 
  children, 
  onClick, 
  className = '' 
}) => (
  <button 
    onClick={onClick}
    className={`px-4 py-2 bg-gray-200 text-gray-900 rounded-md hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-500 ${className}`}
  >
    {children}
  </button>
);

const AlertDialogTrigger: React.FC<{ children: React.ReactNode; onClick?: () => void; className?: string }> = ({ 
  children, 
  onClick, 
  className = '' 
}) => (
  <button onClick={onClick} className={className}>
    {children}
  </button>
);

export { 
  AlertDialog, 
  AlertDialogContent, 
  AlertDialogHeader, 
  AlertDialogTitle, 
  AlertDialogDescription, 
  AlertDialogFooter, 
  AlertDialogAction, 
  AlertDialogCancel, 
  AlertDialogTrigger 
};
export default AlertDialog;
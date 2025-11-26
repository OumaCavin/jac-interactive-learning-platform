// JAC Learning Platform - TypeScript utilities by Cavin Otieno

import React from 'react';

interface TabsProps {
  children: React.ReactNode;
  defaultValue?: string;
  value?: string;
  onValueChange?: (value: string) => void;
}

const Tabs: React.FC<TabsProps> = ({ children, defaultValue, value, onValueChange }) => {
  const [activeTab, setActiveTab] = React.useState(value || defaultValue || '');
  
  const handleTabChange = (newValue: string) => {
    if (value === undefined) {
      setActiveTab(newValue);
    }
    onValueChange?.(newValue);
  };
  
  return (
    <div data-value={value || activeTab}>
      {React.Children.map(children, child => 
        React.isValidElement(child) 
          ? React.cloneElement(child as React.ReactElement<any>, { 
              activeTab: value || activeTab, 
              onTabChange: handleTabChange 
            })
          : child
      )}
    </div>
  );
};

const TabsList: React.FC<{ children: React.ReactNode; className?: string }> = ({ children, className = '' }) => (
  <div className={`flex space-x-1 rounded-lg bg-gray-100 p-1 ${className}`}>
    {children}
  </div>
);

const TabsTrigger: React.FC<{ 
  children: React.ReactNode; 
  value: string; 
  activeTab?: string; 
  onTabChange?: (value: string) => void; 
  className?: string 
}> = ({ children, value, activeTab, onTabChange, className = '' }) => (
  <button
    className={`px-3 py-2 text-sm font-medium rounded-md transition-colors ${
      activeTab === value 
        ? 'bg-white text-gray-900 shadow' 
        : 'text-gray-600 hover:text-gray-900'
    } ${className}`}
    onClick={() => onTabChange?.(value)}
  >
    {children}
  </button>
);

const TabsContent: React.FC<{ 
  children: React.ReactNode; 
  value: string; 
  activeTab?: string; 
  className?: string 
}> = ({ children, value, activeTab, className = '' }) => (
  activeTab === value ? (
    <div className={`mt-2 ${className}`}>
      {children}
    </div>
  ) : null
);

export { Tabs, TabsList, TabsTrigger, TabsContent };
export default Tabs;
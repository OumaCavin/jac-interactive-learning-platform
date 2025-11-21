import React, { createContext, useContext, useState, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Toaster } from 'react-hot-toast';
// Note: Button import removed to avoid unused import warning

// Notification types
export type NotificationType = 'success' | 'error' | 'warning' | 'info';

export interface Notification {
  id: string;
  type: NotificationType;
  title: string;
  message?: string;
  duration?: number;
  persistent?: boolean;
}

// Notification context
interface NotificationContextType {
  notifications: Notification[];
  addNotification: (notification: Omit<Notification, 'id'>) => void;
  removeNotification: (id: string) => void;
  clearAll: () => void;
}

const NotificationContext = createContext<NotificationContextType | undefined>(undefined);

// Notification item component
interface NotificationItemProps {
  notification: Notification;
  onRemove: (id: string) => void;
}

const NotificationItem: React.FC<NotificationItemProps> = ({ notification, onRemove }) => {
  const { id, type, title, message } = notification;

  const typeStyles = {
    success: 'border-success-500 bg-success-500/10',
    error: 'border-error-500 bg-error-500/10',
    warning: 'border-warning-500 bg-warning-500/10',
    info: 'border-primary-500 bg-primary-500/10',
  };

  const iconStyles = {
    success: '✓',
    error: '✗',
    warning: '⚠',
    info: 'ℹ',
  };

  React.useEffect(() => {
    if (!notification.persistent && notification.duration !== 0) {
      const timer = setTimeout(() => {
        onRemove(id);
      }, notification.duration || 5000);

      return () => clearTimeout(timer);
    }
  }, [id, notification.persistent, notification.duration, onRemove]);

  return (
    <motion.div
      initial={{ opacity: 0, y: -50, scale: 0.8 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      exit={{ opacity: 0, y: -50, scale: 0.8 }}
      className={`
        glass-strong rounded-xl p-4 border-l-4 max-w-sm w-full
        ${typeStyles[type]}
      `}
    >
      <div className="flex items-start justify-between">
        <div className="flex items-start space-x-3">
          <div className={`
            w-6 h-6 rounded-full flex items-center justify-center text-sm font-bold
            ${type === 'success' && 'bg-success-500 text-white'}
            ${type === 'error' && 'bg-error-500 text-white'}
            ${type === 'warning' && 'bg-warning-500 text-white'}
            ${type === 'info' && 'bg-primary-500 text-white'}
          `}>
            {iconStyles[type]}
          </div>
          <div className="flex-1">
            <h4 className="text-white font-medium">{title}</h4>
            {message && (
              <p className="text-white/80 text-sm mt-1">{message}</p>
            )}
          </div>
        </div>
        <button
          onClick={() => onRemove(id)}
          className="text-white/60 hover:text-white transition-colors"
        >
          ✕
        </button>
      </div>
    </motion.div>
  );
};

// Notification provider component
interface NotificationProviderProps {
  children: React.ReactNode;
}

export const NotificationProvider: React.FC<NotificationProviderProps> = ({ children }) => {
  const [notifications, setNotifications] = useState<Notification[]>([]);

  const addNotification = useCallback((notification: Omit<Notification, 'id'>) => {
    const id = Math.random().toString(36).substr(2, 9);
    setNotifications(prev => [...prev, { ...notification, id }]);
  }, []);

  const removeNotification = useCallback((id: string) => {
    setNotifications(prev => prev.filter(n => n.id !== id));
  }, []);

  const clearAll = useCallback(() => {
    setNotifications([]);
  }, []);

  return (
    <NotificationContext.Provider value={{
      notifications,
      addNotification,
      removeNotification,
      clearAll,
    }}>
      {children}
      
      {/* React Hot Toast - Main toast notifications */}
      <Toaster
        position="top-right"
        toastOptions={{
          duration: 4000,
          style: {
            background: '#363636',
            color: '#fff',
          },
          success: {
            duration: 3000,
            iconTheme: {
              primary: '#4ade80',
              secondary: '#fff',
            },
          },
          error: {
            duration: 5000,
            iconTheme: {
              primary: '#ef4444',
              secondary: '#fff',
            },
          },
        }}
      />
      
      {/* Custom notification container (for persistent notifications) */}
      <div className="fixed top-4 right-4 z-50 space-y-2">
        <AnimatePresence>
          {notifications.filter(n => n.persistent).map(notification => (
            <NotificationItem
              key={notification.id}
              notification={notification}
              onRemove={removeNotification}
            />
          ))}
        </AnimatePresence>
      </div>
    </NotificationContext.Provider>
  );
};

// Hook to use notifications
export const useNotifications = () => {
  const context = useContext(NotificationContext);
  if (!context) {
    throw new Error('useNotifications must be used within a NotificationProvider');
  }
  return context;
};

// Convenience hooks for different notification types
export const useSuccessNotification = () => {
  const { addNotification } = useNotifications();
  
  return useCallback((title: string, message?: string, options?: Partial<Notification>) => {
    addNotification({
      type: 'success',
      title,
      message,
      ...options,
    });
  }, [addNotification]);
};

export const useErrorNotification = () => {
  const { addNotification } = useNotifications();
  
  return useCallback((title: string, message?: string, options?: Partial<Notification>) => {
    addNotification({
      type: 'error',
      title,
      message,
      persistent: true, // Errors are persistent by default
      ...options,
    });
  }, [addNotification]);
};

export const useWarningNotification = () => {
  const { addNotification } = useNotifications();
  
  return useCallback((title: string, message?: string, options?: Partial<Notification>) => {
    addNotification({
      type: 'warning',
      title,
      message,
      ...options,
    });
  }, [addNotification]);
};

export const useInfoNotification = () => {
  const { addNotification } = useNotifications();
  
  return useCallback((title: string, message?: string, options?: Partial<Notification>) => {
    addNotification({
      type: 'info',
      title,
      message,
      ...options,
    });
  }, [addNotification]);
};
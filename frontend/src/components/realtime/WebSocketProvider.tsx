/**
 * WebSocket Provider Component
 * 
 * Manages global WebSocket connections for the entire application.
 * Provides real-time updates for dashboard, alerts, metrics, and activities.
 * 
 * Author: MiniMax Agent
 * Created: 2025-11-26
 */

import React, { createContext, useContext, useEffect, useState, ReactNode } from 'react';
import { toast } from 'react-hot-toast';
import { useRealtimeDashboard, useRealtimeAlerts, useRealtimeMetrics } from '@/hooks/useWebSocket';

interface WebSocketContextType {
  // Connection status
  dashboardConnected: boolean;
  alertsConnected: boolean;
  metricsConnected: boolean;
  overallStatus: 'connected' | 'connecting' | 'error' | 'disconnected';
  
  // Real-time data
  dashboardData: any;
  alerts: any[];
  unreadAlertCount: number;
  metrics: any;
  recentActivities: any[];
  
  // Actions
  refreshDashboard: () => void;
  acknowledgeAlert: (alertId: string) => void;
  isConnected: () => boolean;
}

const WebSocketContext = createContext<WebSocketContextType | undefined>(undefined);

interface WebSocketProviderProps {
  children: ReactNode;
  autoConnect?: boolean;
  endpoints?: {
    dashboard?: string;
    alerts?: string;
    metrics?: string;
  };
}

export const WebSocketProvider: React.FC<WebSocketProviderProps> = ({
  children,
  autoConnect = true,
  endpoints = {}
}) => {
  const [connectionAttempts, setConnectionAttempts] = useState(0);
  const [lastConnectionTime, setLastConnectionTime] = useState<Date | null>(null);

  // Default endpoints
  const defaultEndpoints = {
    dashboard: '/ws/dashboard/',
    alerts: '/ws/alerts/',
    metrics: '/ws/metrics/',
    ...endpoints
  };

  // Real-time dashboard hook
  const {
    dashboardData,
    recentActivities,
    metrics: dashboardMetrics,
    connectionStatus: dashboardStatus,
    refreshData: refreshDashboard
  } = useRealtimeDashboard({
    onConnect: () => {
      console.log('Dashboard WebSocket connected');
      toast.success('Dashboard connected to live updates');
      setLastConnectionTime(new Date());
    },
    onDisconnect: () => {
      console.log('Dashboard WebSocket disconnected');
    },
    onError: (error) => {
      console.error('Dashboard WebSocket error:', error);
      toast.error('Dashboard connection error');
    }
  });

  // Real-time alerts hook
  const {
    alerts,
    unreadCount,
    connectionStatus: alertsStatus,
    acknowledgeAlert: ackAlert
  } = useRealtimeAlerts({
    onConnect: () => {
      console.log('Alerts WebSocket connected');
      setLastConnectionTime(new Date());
    },
    onDisconnect: () => {
      console.log('Alerts WebSocket disconnected');
    },
    onError: (error) => {
      console.error('Alerts WebSocket error:', error);
    }
  });

  // Real-time metrics hook
  const {
    metrics,
    historicalData,
    connectionStatus: metricsStatus
  } = useRealtimeMetrics({
    onConnect: () => {
      console.log('Metrics WebSocket connected');
      setLastConnectionTime(new Date());
    },
    onDisconnect: () => {
      console.log('Metrics WebSocket disconnected');
    },
    onError: (error) => {
      console.error('Metrics WebSocket error:', error);
    }
  });

  // Calculate overall connection status
  const getOverallStatus = (): 'connected' | 'connecting' | 'error' | 'disconnected' => {
    const statuses = [dashboardStatus, alertsStatus, metricsStatus];
    
    if (statuses.some(status => status === 'error')) {
      return 'error';
    }
    
    if (statuses.some(status => status === 'connecting')) {
      return 'connecting';
    }
    
    if (statuses.every(status => status === 'connected')) {
      return 'connected';
    }
    
    return 'disconnected';
  };

  // Connection status
  const overallStatus = getOverallStatus();
  const dashboardConnected = dashboardStatus === 'connected';
  const alertsConnected = alertsStatus === 'connected';
  const metricsConnected = metricsStatus === 'connected';

  // Handle reconnection attempts
  useEffect(() => {
    if (overallStatus === 'error' || overallStatus === 'disconnected') {
      setConnectionAttempts(prev => prev + 1);
      
      if (connectionAttempts < 3) {
        // Auto-reconnect after a delay
        const timer = setTimeout(() => {
          console.log(`Attempting to reconnect... (attempt ${connectionAttempts + 1})`);
        }, 5000 * (connectionAttempts + 1)); // Exponential backoff
        
        return () => clearTimeout(timer);
      } else {
        toast.error('Unable to establish real-time connections. Please refresh the page.');
      }
    }
  }, [overallStatus, connectionAttempts]);

  // Connection health monitoring
  useEffect(() => {
    const checkConnectionHealth = () => {
      if (lastConnectionTime) {
        const timeSinceLastConnection = Date.now() - lastConnectionTime.getTime();
        const fiveMinutes = 5 * 60 * 1000;
        
        if (timeSinceLastConnection > fiveMinutes && overallStatus === 'connected') {
          // Connection might be stale, attempt reconnection
          console.log('Connection may be stale, attempting reconnection...');
          refreshDashboard();
        }
      }
    };

    const healthCheck = setInterval(checkConnectionHealth, 60000); // Check every minute
    return () => clearInterval(healthCheck);
  }, [lastConnectionTime, overallStatus, refreshDashboard]);

  // Manual refresh function
  const handleRefreshDashboard = () => {
    if (dashboardConnected) {
      refreshDashboard();
    } else {
      toast.error('Dashboard not connected');
    }
  };

  // Manual acknowledge alert function
  const handleAcknowledgeAlert = (alertId: string) => {
    if (alertsConnected) {
      ackAlert(alertId);
    } else {
      toast.error('Alerts not connected');
    }
  };

  // Connection check function
  const isConnected = () => {
    return dashboardConnected && alertsConnected && metricsConnected;
  };

  const contextValue: WebSocketContextType = {
    // Connection status
    dashboardConnected,
    alertsConnected,
    metricsConnected,
    overallStatus,
    
    // Real-time data
    dashboardData,
    alerts,
    unreadAlertCount: unreadCount,
    metrics: metrics || dashboardMetrics,
    recentActivities,
    
    // Actions
    refreshDashboard: handleRefreshDashboard,
    acknowledgeAlert: handleAcknowledgeAlert,
    isConnected
  };

  return (
    <WebSocketContext.Provider value={contextValue}>
      {children}
    </WebSocketContext.Provider>
  );
};

// Hook to use WebSocket context
export const useWebSocketContext = (): WebSocketContextType => {
  const context = useContext(WebSocketContext);
  if (context === undefined) {
    throw new Error('useWebSocketContext must be used within a WebSocketProvider');
  }
  return context;
};

// Connection status indicator component
export const ConnectionStatus: React.FC<{ className?: string }> = ({ className = '' }) => {
  const { overallStatus, dashboardConnected, alertsConnected, metricsConnected } = useWebSocketContext();
  
  const getStatusConfig = () => {
    switch (overallStatus) {
      case 'connected':
        return {
          icon: '🟢',
          text: 'Live',
          color: 'text-green-600',
          bgColor: 'bg-green-50'
        };
      case 'connecting':
        return {
          icon: '🟡',
          text: 'Connecting',
          color: 'text-yellow-600',
          bgColor: 'bg-yellow-50'
        };
      case 'error':
        return {
          icon: '🔴',
          text: 'Error',
          color: 'text-red-600',
          bgColor: 'bg-red-50'
        };
      default:
        return {
          icon: '⚪',
          text: 'Offline',
          color: 'text-gray-600',
          bgColor: 'bg-gray-50'
        };
    }
  };

  const config = getStatusConfig();

  return (
    <div className={`flex items-center gap-2 ${className}`}>
      <div className={`flex items-center gap-1 px-2 py-1 rounded-full ${config.bgColor}`}>
        <span className="text-xs">{config.icon}</span>
        <span className={`text-xs font-medium ${config.color}`}>
          {config.text}
        </span>
      </div>
      
      {/* Individual connection indicators */}
      <div className="flex items-center gap-1 text-xs text-gray-500">
        <span className={dashboardConnected ? 'text-green-500' : 'text-gray-300'}>●</span>
        <span className={alertsConnected ? 'text-green-500' : 'text-gray-300'}>●</span>
        <span className={metricsConnected ? 'text-green-500' : 'text-gray-300'}>●</span>
      </div>
    </div>
  );
};

// Export default provider
export default WebSocketProvider;
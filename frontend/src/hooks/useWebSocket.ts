// JAC Learning Platform - TypeScript utilities by Cavin Otieno

/**
 * WebSocket Service - Real-time Communication
 * 
 * Handles WebSocket connections for real-time dashboard updates,
 * live alerts, performance metrics, and activity streams.
 * 
 * Author: Cavin Otieno
 * Created: 2025-11-26
 */

import React, { useEffect, useRef, useCallback, useState } from 'react';
import { useDispatch } from 'react-redux';
import { toast } from 'react-hot-toast';

interface WebSocketMessage {
  type: string;
  data?: any;
  message?: string;
  timestamp?: string;
  session_id?: string;
  [key: string]: any;
}

interface WebSocketOptions {
  onMessage?: (message: WebSocketMessage) => void;
  onConnect?: () => void;
  onDisconnect?: () => void;
  onError?: (error: Event) => void;
  reconnectAttempts?: number;
  reconnectInterval?: number;
}

class WebSocketService {
  private connections: Map<string, WebSocket> = new Map();
  private callbacks: Map<string, WebSocketOptions> = new Map();
  private reconnectAttempts: Map<string, number> = new Map();
  private baseUrl: string;

  constructor(baseUrl: string = 'ws://localhost:8000') {
    this.baseUrl = baseUrl;
  }

  /**
   * Connect to a WebSocket endpoint
   */
  connect(endpoint: string, options: WebSocketOptions = {}): Promise<WebSocket> {
    return new Promise((resolve, reject) => {
      try {
        // Close existing connection if any
        this.disconnect(endpoint);

        const wsUrl = `${this.baseUrl}${endpoint}`;
        const ws = new WebSocket(wsUrl);
        
        this.connections.set(endpoint, ws);
        this.callbacks.set(endpoint, options);
        this.reconnectAttempts.set(endpoint, 0);

        ws.onopen = () => {
          console.log(`WebSocket connected to ${endpoint}`);
          this.reconnectAttempts.set(endpoint, 0);
          options.onConnect?.();
          resolve(ws);
        };

        ws.onmessage = (event) => {
          try {
            const message: WebSocketMessage = JSON.parse(event.data);
            
            // Handle different message types
            this.handleMessage(endpoint, message);
            
            // Call custom callback
            options.onMessage?.(message);
            
          } catch (error) {
            console.error('Error parsing WebSocket message:', error);
          }
        };

        ws.onclose = (event) => {
          console.log(`WebSocket disconnected from ${endpoint}`);
          this.connections.delete(endpoint);
          options.onDisconnect?.();
          
          // Attempt reconnection if not a manual close
          if (!event.wasClean && this.shouldReconnect(endpoint, options)) {
            this.scheduleReconnect(endpoint);
          }
        };

        ws.onerror = (error) => {
          console.error(`WebSocket error on ${endpoint}:`, error);
          options.onError?.(error);
          reject(error);
        };

      } catch (error) {
        reject(error);
      }
    });
  }

  /**
   * Disconnect from a WebSocket endpoint
   */
  disconnect(endpoint: string): void {
    const ws = this.connections.get(endpoint);
    if (ws) {
      ws.close(1000, 'Manual disconnect');
      this.connections.delete(endpoint);
      this.callbacks.delete(endpoint);
      this.reconnectAttempts.delete(endpoint);
    }
  }

  /**
   * Send message through WebSocket
   */
  send(endpoint: string, message: any): void {
    const ws = this.connections.get(endpoint);
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify(message));
    } else {
      console.warn(`WebSocket not connected to ${endpoint}`);
    }
  }

  /**
   * Check connection status
   */
  isConnected(endpoint: string): boolean {
    const ws = this.connections.get(endpoint);
    return ws?.readyState === WebSocket.OPEN;
  }

  /**
   * Get connection status
   */
  getConnectionStatus(endpoint: string): string {
    const ws = this.connections.get(endpoint);
    if (!ws) return 'disconnected';
    
    switch (ws.readyState) {
      case WebSocket.CONNECTING: return 'connecting';
      case WebSocket.OPEN: return 'connected';
      case WebSocket.CLOSING: return 'closing';
      case WebSocket.CLOSED: return 'disconnected';
      default: return 'unknown';
    }
  }

  /**
   * Handle different message types
   */
  private handleMessage(endpoint: string, message: WebSocketMessage): void {
    switch (message.type) {
      case 'connection_established':
        console.log('Dashboard connection established');
        break;
        
      case 'dashboard_update':
        // Dispatch to Redux store or call update callback
        this.dispatchUpdate('dashboard', message.data);
        break;
        
      case 'alert_notification':
        // Show toast notification
        if (message.alert) {
          toast(message.alert.message || 'New alert received', {
            icon: this.getAlertIcon(message.alert.type),
            duration: 5000
          });
        }
        this.dispatchUpdate('alerts', message.alert);
        break;
        
      case 'realtime_metrics':
        this.dispatchUpdate('metrics', message.metrics);
        break;
        
      case 'activity_update':
        this.dispatchUpdate('activities', message.activity);
        break;
        
      case 'achievement_unlocked':
        toast.success(`🏆 Achievement Unlocked: ${message.achievement?.title || 'New Achievement'}!`);
        this.dispatchUpdate('achievements', message.achievement);
        break;
        
      case 'pong':
        // Handle ping/pong for connection health
        break;
        
      case 'error':
        console.error('WebSocket error message:', message.message);
        break;
        
      default:
        console.log('Unknown WebSocket message type:', message.type);
    }
  }

  /**
   * Dispatch updates to components
   */
  private dispatchUpdate(type: string, data: any): void {
    // This would typically dispatch to Redux or call component callbacks
    // For now, we'll use a custom event system
    const event = new CustomEvent(`websocket:${type}`, { detail: data });
    window.dispatchEvent(event);
  }

  /**
   * Check if reconnection should be attempted
   */
  private shouldReconnect(endpoint: string, options: WebSocketOptions): boolean {
    const maxAttempts = options.reconnectAttempts || 5;
    const attempts = this.reconnectAttempts.get(endpoint) || 0;
    return attempts < maxAttempts;
  }

  /**
   * Schedule reconnection attempt
   */
  private scheduleReconnect(endpoint: string): void {
    const options = this.callbacks.get(endpoint);
    const interval = options?.reconnectInterval || 5000;
    const attempts = (this.reconnectAttempts.get(endpoint) || 0) + 1;
    
    this.reconnectAttempts.set(endpoint, attempts);
    
    console.log(`Scheduling reconnect to ${endpoint} in ${interval}ms (attempt ${attempts})`);
    
    setTimeout(() => {
      this.connect(endpoint, options);
    }, interval);
  }

  /**
   * Get appropriate icon for alert type
   */
  private getAlertIcon(type: string): string {
    switch (type) {
      case 'performance': return '📊';
      case 'engagement': return '📈';
      case 'achievement': return '🏆';
      case 'system': return '⚙️';
      default: return '💬';
    }
  }

  /**
   * Clean up all connections
   */
  cleanup(): void {
    this.connections.forEach((ws, endpoint) => {
      this.disconnect(endpoint);
    });
  }
}

// Create singleton instance
const webSocketService = new WebSocketService();

// React hook for WebSocket connections
export const useWebSocket = (endpoint: string, options: WebSocketOptions = {}) => {
  const [connectionStatus, setConnectionStatus] = useState<string>('disconnected');
  const dispatch = useDispatch();

  useEffect(() => {
    // Update connection status
    const updateStatus = () => {
      const status = webSocketService.getConnectionStatus(endpoint);
      setConnectionStatus(status);
    };

    // Connect to WebSocket
    webSocketService.connect(endpoint, {
      ...options,
      onConnect: () => {
        updateStatus();
        options.onConnect?.();
      },
      onDisconnect: () => {
        updateStatus();
        options.onDisconnect?.();
      },
      onError: (error) => {
        updateStatus();
        options.onError?.(error);
      }
    }).catch(error => {
      console.error(`Failed to connect to ${endpoint}:`, error);
      setConnectionStatus('error');
    });

    // Set up status checking interval
    const statusInterval = setInterval(updateStatus, 1000);

    return () => {
      clearInterval(statusInterval);
      webSocketService.disconnect(endpoint);
    };
  }, [endpoint, options.onConnect, options.onDisconnect, options.onError]);

  const sendMessage = useCallback((message: any) => {
    webSocketService.send(endpoint, message);
  }, [endpoint]);

  const isConnected = useCallback(() => {
    return webSocketService.isConnected(endpoint);
  }, [endpoint]);

  return {
    connectionStatus,
    sendMessage,
    isConnected
  };
};

// React hook for real-time dashboard updates
export const useRealtimeDashboard = (options: WebSocketOptions = {}) => {
  const [dashboardData, setDashboardData] = useState<any>(null);
  const [recentActivities, setRecentActivities] = useState<any[]>([]);
  const [metrics, setMetrics] = useState<any>(null);

  const handleDashboardUpdate = useCallback((data: any) => {
    setDashboardData(data);
  }, []);

  const handleActivityUpdate = useCallback((activity: any) => {
    setRecentActivities(prev => {
      const updated = [activity, ...prev].slice(0, 20); // Keep last 20 activities
      return updated;
    });
  }, []);

  const handleMetricsUpdate = useCallback((metricsData: any) => {
    setMetrics(metricsData);
  }, []);

  // Set up event listeners for different data types
  useEffect(() => {
    const handleDashboardEvent = (event: CustomEvent) => {
      handleDashboardUpdate(event.detail);
    };

    const handleActivityEvent = (event: CustomEvent) => {
      handleActivityUpdate(event.detail);
    };

    const handleMetricsEvent = (event: CustomEvent) => {
      handleMetricsUpdate(event.detail);
    };

    window.addEventListener('websocket:dashboard', handleDashboardEvent as EventListener);
    window.addEventListener('websocket:activities', handleActivityEvent as EventListener);
    window.addEventListener('websocket:metrics', handleMetricsEvent as EventListener);

    return () => {
      window.removeEventListener('websocket:dashboard', handleDashboardEvent as EventListener);
      window.removeEventListener('websocket:activities', handleActivityEvent as EventListener);
      window.removeEventListener('websocket:metrics', handleMetricsEvent as EventListener);
    };
  }, [handleDashboardUpdate, handleActivityUpdate, handleMetricsUpdate]);

  // Connect to dashboard WebSocket
  const { connectionStatus, sendMessage, isConnected } = useWebSocket('/ws/dashboard/', options);

  return {
    dashboardData,
    recentActivities,
    metrics,
    connectionStatus,
    sendMessage,
    isConnected,
    refreshData: () => sendMessage({ type: 'request_update' })
  };
};

// React hook for real-time alerts
export const useRealtimeAlerts = (options: WebSocketOptions = {}) => {
  const [alerts, setAlerts] = useState<any[]>([]);
  const [unreadCount, setUnreadCount] = useState<number>(0);

  const handleAlertNotification = useCallback((alert: any) => {
    setAlerts(prev => {
      const updated = [alert, ...prev].slice(0, 50); // Keep last 50 alerts
      return updated;
    });
    setUnreadCount(prev => prev + 1);
  }, []);

  // Set up event listener for alerts
  useEffect(() => {
    const handleAlertEvent = (event: CustomEvent) => {
      handleAlertNotification(event.detail);
    };

    window.addEventListener('websocket:alerts', handleAlertEvent as EventListener);

    return () => {
      window.removeEventListener('websocket:alerts', handleAlertEvent as EventListener);
    };
  }, [handleAlertNotification]);

  // Connect to alerts WebSocket
  const { connectionStatus, sendMessage, isConnected } = useWebSocket('/ws/alerts/', {
    ...options,
    onMessage: (message) => {
      if (message.type === 'alert_notification') {
        handleAlertNotification(message.alert);
      }
      options.onMessage?.(message);
    }
  });

  const acknowledgeAlert = useCallback((alertId: string) => {
    sendMessage({
      type: 'acknowledge_alert',
      alert_id: alertId
    });
    
    // Update local state
    setAlerts(prev => prev.map(alert => 
      alert.id === alertId ? { ...alert, acknowledged: true } : alert
    ));
    setUnreadCount(prev => Math.max(0, prev - 1));
  }, [sendMessage]);

  return {
    alerts,
    unreadCount,
    connectionStatus,
    sendMessage,
    isConnected,
    acknowledgeAlert
  };
};

// React hook for real-time metrics
export const useRealtimeMetrics = (options: WebSocketOptions = {}) => {
  const [metrics, setMetrics] = useState<any>(null);
  const [historicalData, setHistoricalData] = useState<any[]>([]);

  const handleMetricsUpdate = useCallback((metricsData: any) => {
    setMetrics(metricsData);
    setHistoricalData(prev => {
      const updated = [...prev, { timestamp: new Date(), ...metricsData }];
      // Keep only last 100 data points
      return updated.slice(-100);
    });
  }, []);

  // Connect to metrics WebSocket
  const { connectionStatus, sendMessage, isConnected } = useWebSocket('/ws/metrics/', {
    ...options,
    onMessage: (message) => {
      if (message.type === 'realtime_metrics') {
        handleMetricsUpdate(message.metrics);
      }
      options.onMessage?.(message);
    }
  });

  return {
    metrics,
    historicalData,
    connectionStatus,
    sendMessage,
    isConnected
  };
};

// Export service instance for direct usage
export default webSocketService;
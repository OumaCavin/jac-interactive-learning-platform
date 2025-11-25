/**
 * WebSocket Service - JAC Learning Platform Frontend
 * 
 * Service for real-time WebSocket connections including agent communications,
 * progress updates, and system notifications.
 * 
 * Author: MiniMax Agent
 * Created: 2025-11-26
 */

import { store } from '../store/store';
import { addMessage, setTyping, setAgentStatus } from '../store/slices/agentSlice';

// Types for WebSocket communications
export interface WebSocketMessage {
  type: string;
  data: any;
  timestamp: string;
  session_id?: string;
  agent_id?: string;
  user_id?: string;
}

export interface AgentWebSocketMessage extends WebSocketMessage {
  type: 'agent_message' | 'agent_response' | 'agent_typing' | 'agent_status' | 'error';
  agent_type: string;
  content?: string;
  metadata?: Record<string, any>;
}

export interface ProgressWebSocketMessage extends WebSocketMessage {
  type: 'progress_update' | 'achievement_unlocked' | 'streak_updated' | 'level_up';
  progress_data?: any;
  achievement_data?: any;
  streak_data?: any;
  level_data?: any;
}

export interface SystemWebSocketMessage extends WebSocketMessage {
  type: 'system_notification' | 'agent_availability' | 'maintenance_alert';
  notification_data?: any;
  agent_list?: any[];
  maintenance_info?: any;
}

class WebSocketService {
  private connections: Map<string, WebSocket> = new Map();
  private reconnectAttempts: Map<string, number> = new Map();
  private maxReconnectAttempts = 5;
  private reconnectDelay = 1000;
  private messageQueue: Map<string, WebSocketMessage[]> = new Map();
  private isAuthenticated = false;
  private authToken: string | null = null;
  private baseURL: string;
  
  // Event listeners
  private listeners: Map<string, Set<(data: any) => void>> = new Map();
  
  constructor() {
    this.baseURL = this.getWebSocketURL();
    this.setupAuthListener();
  }
  
  /**
   * Initialize WebSocket service with authentication
   */
  async initialize(): Promise<void> {
    await this.authenticate();
    
    // Connect to default channels
    this.connect('dashboard');
    this.connect('alerts');
    this.connect('metrics');
  }
  
  /**
   * Authenticate with WebSocket server
   */
  private async authenticate(): Promise<void> {
    try {
      const token = localStorage.getItem('access_token');
      if (token) {
        this.authToken = token;
        this.isAuthenticated = true;
      }
    } catch (error) {
      console.error('WebSocket authentication failed:', error);
    }
  }
  
  /**
   * Listen for authentication changes
   */
  private setupAuthListener(): void {
    // Listen for localStorage changes
    window.addEventListener('storage', (event) => {
      if (event.key === 'access_token') {
        this.handleAuthChange(event.newValue);
      }
    });
    
    // Listen for store auth changes
    store.subscribe(() => {
      const state = store.getState();
      if (state.auth?.token && state.auth.token !== this.authToken) {
        this.handleAuthChange(state.auth.token);
      }
    });
  }
  
  /**
   * Handle authentication token changes
   */
  private handleAuthChange(newToken: string | null): void {
    if (newToken && newToken !== this.authToken) {
      this.authToken = newToken;
      this.isAuthenticated = true;
      this.reconnectAll();
    } else if (!newToken) {
      this.authToken = null;
      this.isAuthenticated = false;
      this.disconnectAll();
    }
  }
  
  /**
   * Get WebSocket URL based on environment
   */
  private getWebSocketURL(): string {
    if (typeof window !== 'undefined') {
      const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
      const host = window.location.host;
      return `${protocol}//${host}/ws/`;
    }
    return 'ws://localhost:8000/ws/';
  }
  
  /**
   * Get WebSocket URL with authentication
   */
  private getAuthenticatedURL(endpoint: string): string {
    let url = `${this.baseURL}${endpoint}/`;
    
    if (this.authToken) {
      const separator = url.includes('?') ? '&' : '?';
      url += `${separator}token=${this.authToken}`;
    }
    
    return url;
  }
  
  /**
   * Connect to a WebSocket endpoint
   */
  connect(endpoint: string, options: {
    onOpen?: (event: Event) => void;
    onMessage?: (event: MessageEvent) => void;
    onClose?: (event: CloseEvent) => void;
    onError?: (event: Event) => void;
  } = {}): void {
    if (this.connections.has(endpoint)) {
      console.warn(`WebSocket connection already exists for ${endpoint}`);
      return;
    }
    
    try {
      const url = this.getAuthenticatedURL(endpoint);
      const ws = new WebSocket(url);
      
      ws.onopen = (event) => {
        console.log(`WebSocket connected: ${endpoint}`);
        this.reconnectAttempts.set(endpoint, 0);
        this.flushMessageQueue(endpoint);
        
        if (options.onOpen) {
          options.onOpen(event);
        }
        
        this.emit('connection_open', { endpoint, event });
      };
      
      ws.onmessage = (event) => {
        try {
          const message: WebSocketMessage = JSON.parse(event.data);
          this.handleMessage(endpoint, message);
          
          if (options.onMessage) {
            options.onMessage(event);
          }
        } catch (error) {
          console.error(`Error parsing WebSocket message from ${endpoint}:`, error);
        }
      };
      
      ws.onclose = (event) => {
        console.log(`WebSocket closed: ${endpoint}`, event.code, event.reason);
        this.connections.delete(endpoint);
        
        if (options.onClose) {
          options.onClose(event);
        }
        
        this.emit('connection_close', { endpoint, event });
        
        // Attempt to reconnect if not a normal closure
        if (event.code !== 1000 && this.isAuthenticated) {
          this.attemptReconnect(endpoint, options);
        }
      };
      
      ws.onerror = (event) => {
        console.error(`WebSocket error for ${endpoint}:`, event);
        
        if (options.onError) {
          options.onError(event);
        }
        
        this.emit('connection_error', { endpoint, event });
      };
      
      this.connections.set(endpoint, ws);
      
    } catch (error) {
      console.error(`Failed to connect WebSocket for ${endpoint}:`, error);
    }
  }
  
  /**
   * Disconnect from a WebSocket endpoint
   */
  disconnect(endpoint: string): void {
    const ws = this.connections.get(endpoint);
    if (ws) {
      ws.close(1000, 'Client disconnect');
      this.connections.delete(endpoint);
    }
  }
  
  /**
   * Disconnect from all WebSocket endpoints
   */
  disconnectAll(): void {
    this.connections.forEach((ws, endpoint) => {
      ws.close(1000, 'Client disconnect all');
    });
    this.connections.clear();
  }
  
  /**
   * Reconnect all WebSocket connections
   */
  reconnectAll(): void {
    const endpoints = Array.from(this.connections.keys());
    endpoints.forEach(endpoint => {
      this.disconnect(endpoint);
      setTimeout(() => this.connect(endpoint), 100);
    });
  }
  
  /**
   * Attempt to reconnect a failed connection
   */
  private attemptReconnect(endpoint: string, options: any): void {
    const attempts = this.reconnectAttempts.get(endpoint) || 0;
    
    if (attempts < this.maxReconnectAttempts) {
      const delay = this.reconnectDelay * Math.pow(2, attempts);
      console.log(`Reconnecting to ${endpoint} in ${delay}ms (attempt ${attempts + 1})`);
      
      setTimeout(() => {
        this.reconnectAttempts.set(endpoint, attempts + 1);
        this.connect(endpoint, options);
      }, delay);
    } else {
      console.error(`Max reconnection attempts reached for ${endpoint}`);
      this.emit('connection_failed', { endpoint, attempts });
    }
  }
  
  /**
   * Send message to a WebSocket endpoint
   */
  send(endpoint: string, message: WebSocketMessage): void {
    const ws = this.connections.get(endpoint);
    
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify(message));
    } else {
      // Queue message for later sending
      if (!this.messageQueue.has(endpoint)) {
        this.messageQueue.set(endpoint, []);
      }
      this.messageQueue.get(endpoint)!.push(message);
    }
  }
  
  /**
   * Flush queued messages for an endpoint
   */
  private flushMessageQueue(endpoint: string): void {
    const queue = this.messageQueue.get(endpoint);
    if (queue && queue.length > 0) {
      const ws = this.connections.get(endpoint);
      if (ws && ws.readyState === WebSocket.OPEN) {
        while (queue.length > 0) {
          const message = queue.shift()!;
          ws.send(JSON.stringify(message));
        }
        this.messageQueue.delete(endpoint);
      }
    }
  }
  
  /**
   * Handle incoming WebSocket messages
   */
  private handleMessage(endpoint: string, message: WebSocketMessage): void {
    this.emit('message', { endpoint, message });
    
    // Route message based on type and endpoint
    switch (endpoint) {
      case 'ai-interaction':
        this.handleAgentMessage(message);
        break;
      case 'dashboard':
      case 'metrics':
        this.handleProgressMessage(message);
        break;
      case 'alerts':
        this.handleSystemMessage(message);
        break;
      default:
        this.emit(endpoint, message);
    }
  }
  
  /**
   * Handle agent-related WebSocket messages
   */
  private handleAgentMessage(message: WebSocketMessage): void {
    if (message.type === 'agent_response') {
      const agentMessage = message as AgentWebSocketMessage;
      
      // Add message to store
      if (agentMessage.content && agentMessage.agent_id) {
        store.dispatch(addMessage({
          id: `agent-${message.timestamp}-${Math.random().toString(36).substr(2, 9)}`,
          agent_id: agentMessage.agent_id,
          user_id: 'current-user',
          content: agentMessage.content,
          type: 'text',
          timestamp: message.timestamp,
          is_read: true
        }));
        
        // Stop typing indicator
        store.dispatch(setTyping({ agentId: agentMessage.agent_id, isTyping: false }));
      }
    } else if (message.type === 'agent_typing') {
      const agentMessage = message as AgentWebSocketMessage;
      
      // Set typing indicator
      if (agentMessage.agent_id) {
        store.dispatch(setTyping({ agentId: agentMessage.agent_id, isTyping: true }));
        
        // Auto-stop typing after 5 seconds
        setTimeout(() => {
          store.dispatch(setTyping({ agentId: agentMessage.agent_id, isTyping: false }));
        }, 5000);
      }
    } else if (message.type === 'agent_status') {
      const agentMessage = message as AgentWebSocketMessage;
      
      // Update agent status
      if (agentMessage.agent_id && agentMessage.metadata?.status) {
        store.dispatch(setAgentStatus({
          agentId: agentMessage.agent_id,
          status: agentMessage.metadata.status
        }));
      }
    }
  }
  
  /**
   * Handle progress-related WebSocket messages
   */
  private handleProgressMessage(message: WebSocketMessage): void {
    const progressMessage = message as ProgressWebSocketMessage;
    
    switch (message.type) {
      case 'achievement_unlocked':
        this.emit('achievement_unlocked', progressMessage.achievement_data);
        break;
      case 'streak_updated':
        this.emit('streak_updated', progressMessage.streak_data);
        break;
      case 'level_up':
        this.emit('level_up', progressMessage.level_data);
        break;
      case 'progress_update':
        this.emit('progress_updated', progressMessage.progress_data);
        break;
    }
  }
  
  /**
   * Handle system WebSocket messages
   */
  private handleSystemMessage(message: WebSocketMessage): void {
    const systemMessage = message as SystemWebSocketMessage;
    
    switch (message.type) {
      case 'system_notification':
        this.emit('system_notification', systemMessage.notification_data);
        break;
      case 'agent_availability':
        this.emit('agent_availability_changed', systemMessage.agent_list);
        break;
      case 'maintenance_alert':
        this.emit('maintenance_alert', systemMessage.maintenance_info);
        break;
    }
  }
  
  /**
   * Event listener management
   */
  on(event: string, callback: (data: any) => void): void {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, new Set());
    }
    this.listeners.get(event)!.add(callback);
  }
  
  off(event: string, callback: (data: any) => void): void {
    const eventListeners = this.listeners.get(event);
    if (eventListeners) {
      eventListeners.delete(callback);
      if (eventListeners.size === 0) {
        this.listeners.delete(event);
      }
    }
  }
  
  private emit(event: string, data: any): void {
    const eventListeners = this.listeners.get(event);
    if (eventListeners) {
      eventListeners.forEach(callback => {
        try {
          callback(data);
        } catch (error) {
          console.error(`Error in WebSocket event listener for ${event}:`, error);
        }
      });
    }
  }
  
  /**
   * Check if connected to an endpoint
   */
  isConnected(endpoint: string): boolean {
    const ws = this.connections.get(endpoint);
    return ws?.readyState === WebSocket.OPEN;
  }
  
  /**
   * Get connection status for all endpoints
   */
  getConnectionStatus(): Record<string, boolean> {
    const status: Record<string, boolean> = {};
    this.connections.forEach((ws, endpoint) => {
      status[endpoint] = ws.readyState === WebSocket.OPEN;
    });
    return status;
  }
  
  /**
   * Agent-specific methods
   */
  
  /**
   * Send message to a specific agent
   */
  sendAgentMessage(agentId: string, agentType: string, content: string, sessionId?: string): void {
    const message: AgentWebSocketMessage = {
      type: 'agent_message',
      agent_type: agentType,
      agent_id: agentId,
      content,
      session_id: sessionId,
      timestamp: new Date().toISOString(),
      data: {
        user_message: content,
        agent_id: agentId,
        session_id: sessionId
      }
    };
    
    this.send('ai-interaction', message);
  }
  
  /**
   * Connect to agent chat for a specific agent
   */
  connectAgentChat(agentId: string, agentType: string, sessionId: string): void {
    this.connect('ai-interaction');
    
    // Join agent-specific room
    const joinMessage: WebSocketMessage = {
      type: 'join_room',
      data: {
        agent_id: agentId,
        agent_type: agentType,
        session_id: sessionId
      },
      timestamp: new Date().toISOString()
    };
    
    this.send('ai-interaction', joinMessage);
  }
  
  /**
   * Leave agent chat room
   */
  leaveAgentChat(agentId: string, agentType: string, sessionId: string): void {
    const leaveMessage: WebSocketMessage = {
      type: 'leave_room',
      data: {
        agent_id: agentId,
        agent_type: agentType,
        session_id: sessionId
      },
      timestamp: new Date().toISOString()
    };
    
    this.send('ai-interaction', leaveMessage);
  }
  
  /**
   * Get agent typing status
   */
  isAgentTyping(agentId: string): boolean {
    const state = store.getState();
    const agent = state.agents?.agents?.find(a => a.id === agentId);
    return agent?.isTyping || false;
  }
  
  /**
   * Subscribe to specific agent events
   */
  subscribeToAgent(agentId: string, event: string, callback: (data: any) => void): void {
    this.on(`agent_${agentId}_${event}`, callback);
  }
  
  /**
   * Unsubscribe from agent events
   */
  unsubscribeFromAgent(agentId: string, event: string, callback: (data: any) => void): void {
    this.off(`agent_${agentId}_${event}`, callback);
  }
}

// Create singleton instance
export const webSocketService = new WebSocketService();

// Auto-initialize when module loads
if (typeof window !== 'undefined') {
  webSocketService.initialize().catch(error => {
    console.error('Failed to initialize WebSocket service:', error);
  });
}

export default webSocketService;
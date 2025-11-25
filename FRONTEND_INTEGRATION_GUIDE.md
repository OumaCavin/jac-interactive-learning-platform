
# Frontend Integration Guide - Real-time Analytics & AI

## WebSocket Connections

### 1. Predictive Analytics WebSocket
```javascript
const predictiveSocket = new WebSocket('ws://localhost:8000/ws/predictive/');

// Listen for predictive updates
predictiveSocket.onmessage = function(event) {
    const data = JSON.parse(event.data);
    
    if (data.type === 'predictive_analytics_update') {
        // Update UI with predictive insights
        updatePredictiveDisplay(data.data);
    }
    
    if (data.type === 'ai_recommendation') {
        // Display AI-generated recommendations
        displayAIRecommendations(data.recommendations);
    }
};

// Request manual update
predictiveSocket.send(JSON.stringify({
    type: 'request_predictive_update'
}));
```

### 2. AI Interaction WebSocket
```javascript
const aiSocket = new WebSocket('ws://localhost:8000/ws/ai-interaction/');

// Send AI chat message
aiSocket.send(JSON.stringify({
    type: 'ai_chat',
    message: 'Help me understand JAC walkers',
    agent_type: 'learning_assistant',
    context: { current_module: 'JAC Basics' }
}));

// Listen for AI responses
aiSocket.onmessage = function(event) {
    const data = JSON.parse(event.data);
    
    if (data.type === 'ai_response') {
        // Display AI response
        displayAIResponse(data.response);
    }
};
```

## API Endpoints

### 1. Predictive Streaming API
```javascript
// Get comprehensive predictive analytics
const response = await fetch('/api/predictive/streaming/?type=comprehensive&ai_enhanced=true');
const data = await response.json();

// Use the predictive data
data.predictive_insights.learning_velocity
data.ai_enhanced_insights.ai_insights
```

### 2. AI Interaction API
```javascript
// Get available AI agents
const agentsResponse = await fetch('/api/ai/agents/');
const agents = await agentsResponse.json();

// Chat with specific agent
const chatResponse = await fetch('/api/ai/interaction/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        agent_type: 'mentor_coach',
        message: 'What should I learn next?',
        context: { current_progress: 65 }
    })
});
const aiResponse = await chatResponse.json();
```

## Real-time Dashboard Integration

### 1. Dashboard Data Updates
```javascript
// Subscribe to dashboard updates
const dashboardSocket = new WebSocket('ws://localhost:8000/ws/dashboard/');

dashboardSocket.onmessage = function(event) {
    const data = JSON.parse(event.data);
    
    if (data.type === 'dashboard_initial_data') {
        initializeDashboard(data);
    }
    
    if (data.type === 'new_activities') {
        updateActivityFeed(data.activities);
    }
    
    if (data.type === 'alert_notification') {
        showAlertNotification(data.alerts);
    }
    
    if (data.type === 'predictive_analytics_update') {
        updatePredictiveSection(data.data);
    }
};
```

### 2. Performance Monitoring
```javascript
// Monitor performance in real-time
const metricsSocket = new WebSocket('ws://localhost:8000/ws/metrics/');

metricsSocket.onmessage = function(event) {
    const data = JSON.parse(event.data);
    
    if (data.type === 'realtime_metrics') {
        updatePerformanceCharts(data.metrics);
    }
};
```

## AI Agent Integration

### 1. Agent Selection
```javascript
// Get available agents
const agents = [
    {
        type: 'learning_assistant',
        name: 'Alex',
        role: 'JAC Programming Learning Assistant',
        specializations: ['JAC basics', 'OSP concepts', 'problem solving']
    },
    {
        type: 'code_reviewer', 
        name: 'Blake',
        role: 'JAC Code Reviewer',
        specializations: ['code review', 'debugging', 'optimization']
    }
    // ... more agents
];

// Render agent selection UI
function renderAgentSelection() {
    const container = document.getElementById('agent-selection');
    agents.forEach(agent => {
        const agentCard = createAgentCard(agent);
        container.appendChild(agentCard);
    });
}
```

### 2. AI Chat Interface
```javascript
class AIChatInterface {
    constructor(agentType = 'learning_assistant') {
        this.agentType = agentType;
        this.chatHistory = [];
        this.setupWebSocket();
    }
    
    setupWebSocket() {
        this.socket = new WebSocket('ws://localhost:8000/ws/ai-interaction/');
        
        this.socket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.handleAIResponse(data);
        };
    }
    
    sendMessage(message, context = {}) {
        this.socket.send(JSON.stringify({
            type: 'ai_chat',
            message: message,
            agent_type: this.agentType,
            context: context
        }));
        
        // Add to local history
        this.chatHistory.push({ role: 'user', content: message });
    }
    
    handleAIResponse(data) {
        if (data.type === 'ai_response') {
            this.displayResponse(data.response);
            this.chatHistory.push({ role: 'assistant', content: data.response });
        }
    }
    
    switchAgent(newAgentType) {
        this.agentType = newAgentType;
        this.socket.send(JSON.stringify({
            type: 'agent_switch',
            agent_type: newAgentType
        }));
    }
}
```

## Real-time Predictive Analytics UI

### 1. Predictive Insights Display
```javascript
class PredictiveAnalyticsUI {
    constructor() {
        this.sections = {
            velocity: document.getElementById('learning-velocity'),
            engagement: document.getElementById('engagement-patterns'),
            success: document.getElementById('success-probability'),
            completion: document.getElementById('time-to-completion'),
            retention: document.getElementById('retention-risk'),
            gaps: document.getElementById('knowledge-gaps'),
            clusters: document.getElementById('learning-clusters')
        };
    }
    
    updatePredictiveData(predictiveData) {
        // Update each section with new data
        Object.keys(predictiveData).forEach(section => {
            if (this.sections[section]) {
                this.renderSection(this.sections[section], predictiveData[section]);
            }
        });
    }
    
    renderSection(element, data) {
        if (data.error) {
            element.innerHTML = `<div class="error">Error: ${data.error}</div>`;
            return;
        }
        
        // Render predictive data based on section type
        switch(element.id) {
            case 'learning-velocity':
                this.renderVelocityChart(element, data);
                break;
            case 'engagement-patterns':
                this.renderEngagementPattern(element, data);
                break;
            // ... other sections
        }
    }
    
    renderVelocityChart(element, data) {
        // Implementation for velocity chart
        element.innerHTML = `
            <div class="metric-card">
                <h3>Learning Velocity</h3>
                <div class="metric-value">${data.velocity_score || 'N/A'}</div>
                <div class="metric-trend">${data.trend || 'Calculating...'}</div>
                <div class="chart-container">
                    <canvas id="velocity-chart"></canvas>
                </div>
            </div>
        `;
        
        // Initialize chart
        this.createChart('velocity-chart', data.chart_data);
    }
}
```

## Error Handling and Fallbacks

### 1. WebSocket Error Handling
```javascript
function setupWebSocketWithFallback(url, fallbackEndpoints) {
    const socket = new WebSocket(url);
    
    socket.onerror = function(error) {
        console.error('WebSocket error:', error);
        
        // Fallback to HTTP polling
        startHTTPPolling(fallbackEndpoints);
    };
    
    socket.onclose = function(event) {
        if (event.code !== 1000) { // Not normal closure
            console.log('WebSocket closed unexpectedly, attempting reconnect...');
            setTimeout(() => setupWebSocketWithFallback(url, fallbackEndpoints), 5000);
        }
    };
    
    return socket;
}
```

### 2. AI Service Fallbacks
```javascript
class AIServiceWithFallback {
    async getResponse(message, agentType) {
        try {
            // Try WebSocket first
            return await this.getWebSocketResponse(message, agentType);
        } catch (error) {
            console.log('WebSocket failed, trying HTTP API');
            try {
                return await this.getHttpResponse(message, agentType);
            } catch (httpError) {
                console.log('HTTP API failed, using local responses');
                return this.getLocalResponse(message, agentType);
            }
        }
    }
    
    getLocalResponse(message, agentType) {
        // Return pre-defined responses for offline mode
        const localResponses = {
            'learning_assistant': 'I\'m currently offline, but I recommend practicing JAC basics!',
            'code_reviewer': 'I\'m offline, but make sure to check your JAC syntax!',
            // ... more local responses
        };
        
        return {
            response: localResponses[agentType] || 'I\'m here to help when online!',
            agent_type: agentType,
            offline: true
        };
    }
}
```

## Performance Optimization

### 1. Data Caching
```javascript
class PredictiveDataCache {
    constructor() {
        this.cache = new Map();
        this.cacheTimeout = 60000; // 1 minute
    }
    
    get(key) {
        const item = this.cache.get(key);
        if (item && (Date.now() - item.timestamp) < this.cacheTimeout) {
            return item.data;
        }
        return null;
    }
    
    set(key, data) {
        this.cache.set(key, {
            data: data,
            timestamp: Date.now()
        });
    }
    
    clear() {
        this.cache.clear();
    }
}
```

### 2. Debounced Updates
```javascript
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Usage for updating predictive analytics
const updatePredictiveUI = debounce((data) => {
    predictiveAnalyticsUI.updatePredictiveData(data);
}, 1000);
```

## Testing and Debugging

### 1. WebSocket Testing
```javascript
class WebSocketTester {
    constructor(url) {
        this.url = url;
        this.logs = [];
    }
    
    connectAndTest() {
        const socket = new WebSocket(this.url);
        
        socket.onopen = () => {
            this.log('WebSocket connected successfully');
            this.testMessages(socket);
        };
        
        socket.onmessage = (event) => {
            this.log('Received:', event.data);
        };
        
        socket.onerror = (error) => {
            this.log('WebSocket error:', error);
        };
        
        socket.onclose = () => {
            this.log('WebSocket closed');
        };
    }
    
    testMessages(socket) {
        // Test different message types
        socket.send(JSON.stringify({ type: 'ping' }));
        socket.send(JSON.stringify({ type: 'request_predictive_update' }));
    }
    
    log(...args) {
        console.log('[WebSocket Tester]', ...args);
        this.logs.push({ timestamp: new Date(), args });
    }
}
```

This frontend integration guide provides all the necessary components for implementing the real-time analytics and AI features in the React frontend.

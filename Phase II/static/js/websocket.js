/**
 * WebSocket Client Module
 * Roman Urdu: Real-time updates ke liye WebSocket connection
 * 
 * Features:
 * - WebSocketClient class: Connection manage karna
 * - Auto-reconnection with exponential backoff
 * - Message handlers: connected, task.created, task.updated, task.deleted
 * - localStorage multi-tab sync
 * 
 * Message Types:
 * - connected: Connection established
 * - task.created: New task created
 * - task.updated: Task updated
 * - task.deleted: Task deleted
 * - analytics.updated: Analytics data changed
 */

class WebSocketClient {
    /**
     * Create WebSocket client
     * Roman Urdu: WebSocket client initialize karna
     * 
     * @param {string} url - WebSocket URL (e.g., ws://localhost:8000/api/ws)
     */
    constructor(url) {
        this.url = url;
        this.ws = null;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 10;
        this.baseReconnectDelay = 1000; // 1 second
        this.maxReconnectDelay = 30000; // 30 seconds
        this.messageHandlers = new Map();
        this.isConnected = false;
        this.lastMessageTimestamp = null;
        
        // Auto-connect
        this.connect();
    }
    
    /**
     * Connect to WebSocket server
     * Roman Urdu: WebSocket server se connect karna
     */
    connect() {
        try {
            // Get auth token
            const token = this.getAuthToken();
            if (!token) {
                console.warn('No auth token, WebSocket connection skipped');
                return;
            }
            
            // Create WebSocket connection with token
            const wsUrl = `${this.url}?token=${token}`;
            this.ws = new WebSocket(wsUrl);
            
            // Connection opened
            this.ws.onopen = () => {
                console.log('WebSocket connected');
                this.isConnected = true;
                this.reconnectAttempts = 0;
                
                // Send connected message
                this.emit('connected', { type: 'connected', timestamp: new Date().toISOString() });
            };
            
            // Message received
            this.ws.onmessage = (event) => {
                try {
                    const message = JSON.parse(event.data);
                    console.log('WebSocket message received:', message);
                    
                    this.lastMessageTimestamp = Date.now();
                    
                    // Handle message based on type
                    this.handleMessage(message);
                } catch (error) {
                    console.error('Error parsing WebSocket message:', error);
                }
            };
            
            // Connection closed
            this.ws.onclose = (event) => {
                console.log('WebSocket closed:', event.code, event.reason);
                this.isConnected = false;
                
                // Attempt to reconnect
                this.scheduleReconnect();
            };
            
            // Connection error
            this.ws.onerror = (error) => {
                console.error('WebSocket error:', error);
            };
            
        } catch (error) {
            console.error('Error creating WebSocket connection:', error);
            this.scheduleReconnect();
        }
    }
    
    /**
     * Schedule reconnection with exponential backoff
     * Roman Urdu: Exponential backoff ke saath reconnect schedule karna
     */
    scheduleReconnect() {
        if (this.reconnectAttempts >= this.maxReconnectAttempts) {
            console.error('Max WebSocket reconnect attempts reached');
            if (typeof showToast === 'function') {
                showToast('Real-time updates disconnected. Refresh page to reconnect.', 'warning');
            }
            return;
        }
        
        // Calculate delay with exponential backoff
        const delay = Math.min(
            this.baseReconnectDelay * Math.pow(2, this.reconnectAttempts),
            this.maxReconnectDelay
        );
        
        this.reconnectAttempts++;
        console.log(`WebSocket reconnect attempt ${this.reconnectAttempts} in ${delay}ms`);
        
        setTimeout(() => {
            console.log('Attempting WebSocket reconnect...');
            this.connect();
        }, delay);
    }
    
    /**
     * Handle incoming message
     * Roman Urdu: Incoming message handle karna
     * 
     * @param {Object} message - Message object
     */
    handleMessage(message) {
        const { type, data } = message;
        
        switch (type) {
            case 'connected':
                console.log('WebSocket connected successfully');
                break;
                
            case 'task.created':
                this.handleTaskCreated(data);
                break;
                
            case 'task.updated':
                this.handleTaskUpdated(data);
                break;
                
            case 'task.deleted':
                this.handleTaskDeleted(data);
                break;
                
            case 'analytics.updated':
                this.handleAnalyticsUpdated(data);
                break;
                
            case 'echo':
                // Echo response, ignore
                break;
                
            default:
                console.warn('Unknown WebSocket message type:', type);
        }
        
        // Emit to custom handlers
        this.emit(type, data);
    }
    
    /**
     * Handle task.created message
     * Roman Urdu: task.created message handle karna
     * 
     * @param {Object} data - Task data
     */
    handleTaskCreated(data) {
        console.log('Task created via WebSocket:', data);
        
        // Broadcast to localStorage for multi-tab sync
        this.broadcastToLocalStorage('task.created', data);
        
        // Reload todos if function exists
        if (typeof loadTodos === 'function') {
            loadTodos();
        }
        
        // Show notification
        if (typeof showToast === 'function' && data.title) {
            showToast(`Task created: ${data.title}`, 'success', 3000);
        }
    }
    
    /**
     * Handle task.updated message
     * Roman Urdu: task.updated message handle karna
     * 
     * @param {Object} data - Updated task data
     */
    handleTaskUpdated(data) {
        console.log('Task updated via WebSocket:', data);
        
        // Broadcast to localStorage for multi-tab sync
        this.broadcastToLocalStorage('task.updated', data);
        
        // Reload todos if function exists
        if (typeof loadTodos === 'function') {
            loadTodos();
        }
        
        // Show notification
        if (typeof showToast === 'function') {
            showToast(`Task updated: ${data.title || 'Task'}`, 'info', 2000);
        }
    }
    
    /**
     * Handle task.deleted message
     * Roman Urdu: task.deleted message handle karna
     * 
     * @param {Object} data - Deleted task ID
     */
    handleTaskDeleted(data) {
        console.log('Task deleted via WebSocket:', data);
        
        // Broadcast to localStorage for multi-tab sync
        this.broadcastToLocalStorage('task.deleted', data);
        
        // Reload todos if function exists
        if (typeof loadTodos === 'function') {
            loadTodos();
        }
        
        // Show notification
        if (typeof showToast === 'function') {
            showToast('Task deleted', 'info', 2000);
        }
    }
    
    /**
     * Handle analytics.updated message
     * Roman Urdu: analytics.updated message handle karna
     * 
     * @param {Object} data - Analytics data
     */
    handleAnalyticsUpdated(data) {
        console.log('Analytics updated via WebSocket');
        
        // Reload analytics if function exists
        if (typeof loadAnalyticsStats === 'function') {
            loadAnalyticsStats();
        }
    }
    
    /**
     * Broadcast message to localStorage for multi-tab sync
     * Roman Urdu: Multi-tab sync ke liye localStorage mein message bhejna
     * 
     * @param {string} type - Message type
     * @param {Object} data - Message data
     */
    broadcastToLocalStorage(type, data) {
        try {
            const event = {
                type,
                data,
                timestamp: Date.now(),
                source: 'websocket'
            };
            
            localStorage.setItem('websocket_broadcast', JSON.stringify(event));
            
            // Clear after a short delay to allow re-triggering
            setTimeout(() => {
                localStorage.removeItem('websocket_broadcast');
            }, 100);
        } catch (error) {
            console.error('Error broadcasting to localStorage:', error);
        }
    }
    
    /**
     * Send message to WebSocket server
     * Roman Urdu: WebSocket server ko message bhejna
     * 
     * @param {Object} message - Message object
     */
    send(message) {
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
            this.ws.send(JSON.stringify(message));
        } else {
            console.warn('WebSocket not connected, message not sent:', message);
        }
    }
    
    /**
     * Register message handler
     * Roman Urdu: Message handler register karna
     * 
     * @param {string} type - Message type
     * @param {Function} handler - Handler function
     */
    on(type, handler) {
        this.messageHandlers.set(type, handler);
    }
    
    /**
     * Emit message to handlers
     * Roman Urdu: Handlers ko message emit karna
     * 
     * @param {string} type - Message type
     * @param {Object} data - Message data
     */
    emit(type, data) {
        const handler = this.messageHandlers.get(type);
        if (handler) {
            handler(data);
        }
    }
    
    /**
     * Get auth token from localStorage
     * Roman Urdu: localStorage se auth token obtain karna
     * 
     * @returns {string|null} Auth token
     */
    getAuthToken() {
        // Try different possible token locations
        const token = localStorage.getItem('access_token') ||
                     localStorage.getItem('token') ||
                     localStorage.getItem('auth_token');
        
        if (!token) {
            // Try to get from cookie
            const cookies = document.cookie.split(';');
            for (const cookie of cookies) {
                const [name, value] = cookie.trim().split('=');
                if (name === 'access_token' || name === 'token') {
                    return value;
                }
            }
        }
        
        return token;
    }
    
    /**
     * Disconnect from WebSocket server
     * Roman Urdu: WebSocket server se disconnect karna
     */
    disconnect() {
        if (this.ws) {
            this.ws.close();
            this.ws = null;
            this.isConnected = false;
        }
    }
}

/**
 * Setup localStorage listener for multi-tab sync
 * Roman Urdu: Multi-tab sync ke liye localStorage listener setup karna
 */
function setupLocalStorageSync() {
    window.addEventListener('storage', (event) => {
        // Only handle our broadcast events
        if (event.key !== 'websocket_broadcast') return;
        
        // Ignore self-originated events (check timestamp)
        if (!event.newValue) return;
        
        try {
            const broadcast = JSON.parse(event.newValue);
            const now = Date.now();
            const maxAge = 5000; // 5 seconds
            
            // Ignore old events
            if (now - broadcast.timestamp > maxAge) return;
            
            console.log('Received broadcast from localStorage:', broadcast);
            
            // Handle based on type
            switch (broadcast.type) {
                case 'task.created':
                    if (typeof loadTodos === 'function') {
                        loadTodos();
                    }
                    break;
                    
                case 'task.updated':
                    if (typeof loadTodos === 'function') {
                        loadTodos();
                    }
                    break;
                    
                case 'task.deleted':
                    if (typeof loadTodos === 'function') {
                        loadTodos();
                    }
                    break;
                    
                case 'analytics.updated':
                    if (typeof loadAnalyticsStats === 'function') {
                        loadAnalyticsStats();
                    }
                    break;
            }
        } catch (error) {
            console.error('Error handling localStorage sync:', error);
        }
    });
}

/**
 * Broadcast to localStorage (for manual triggers)
 * Roman Urdu: localStorage mein manual broadcast bhejna
 * 
 * @param {string} type - Message type
 * @param {Object} data - Message data
 */
function broadcastToLocalStorage(type, data) {
    try {
        const event = {
            type,
            data,
            timestamp: Date.now(),
            source: 'manual'
        };
        
        localStorage.setItem('websocket_broadcast', JSON.stringify(event));
        
        // Clear after a short delay
        setTimeout(() => {
            localStorage.removeItem('websocket_broadcast');
        }, 100);
    } catch (error) {
        console.error('Error broadcasting to localStorage:', error);
    }
}

// Global WebSocket client instance
let websocketClient = null;

/**
 * Initialize WebSocket connection
 * Roman Urdu: WebSocket connection initialize karna
 * 
 * @param {string} baseUrl - Base WebSocket URL (optional)
 */
function initWebSocket(baseUrl = null) {
    // Determine WebSocket URL
    let wsUrl = baseUrl || `ws://${window.location.host}/api/ws`;
    
    // Use wss:// for production (HTTPS)
    if (window.location.protocol === 'https:') {
        wsUrl = wsUrl.replace('ws://', 'wss://');
    }
    
    // Create WebSocket client
    websocketClient = new WebSocketClient(wsUrl);
    
    // Setup localStorage sync
    setupLocalStorageSync();
    
    console.log('WebSocket client initialized:', wsUrl);
    
    return websocketClient;
}

/**
 * Get WebSocket client instance
 * Roman Urdu: WebSocket client instance obtain karna
 * 
 * @returns {WebSocketClient|null} WebSocket client
 */
function getWebSocketClient() {
    return websocketClient;
}

/**
 * Disconnect WebSocket
 * Roman Urdu: WebSocket disconnect karna
 */
function disconnectWebSocket() {
    if (websocketClient) {
        websocketClient.disconnect();
        websocketClient = null;
    }
}

// Export functions
window.WebSocketModule = {
    WebSocketClient,
    initWebSocket,
    getWebSocketClient,
    disconnectWebSocket,
    broadcastToLocalStorage
};

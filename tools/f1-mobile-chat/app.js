/**
 * F1 Designer Mobile Chat
 * A PWA for chatting with the f1-designer agent from anywhere
 */

// ============================================================================
// Configuration
// ============================================================================

const CONFIG = {
    STORAGE_KEYS: {
        SERVER_URL: 'f1-designer-server-url',
        CURRENT_SESSION: 'f1-designer-current-session'
    },
    AGENT: 'f1-designer',
    RECONNECT_DELAY: 3000,
    TOAST_DURATION: 3000
};

// ============================================================================
// State
// ============================================================================

const state = {
    serverUrl: null,
    currentSession: null,
    sessions: [],
    messages: [],
    isConnected: false,
    isSending: false,
    eventSource: null
};

// ============================================================================
// DOM Elements
// ============================================================================

const elements = {
    // Screens
    settingsScreen: document.getElementById('settings-screen'),
    sessionsScreen: document.getElementById('sessions-screen'),
    chatScreen: document.getElementById('chat-screen'),
    
    // Settings
    serverUrlInput: document.getElementById('server-url'),
    connectBtn: document.getElementById('connect-btn'),
    connectionStatus: document.getElementById('connection-status'),
    
    // Sessions
    settingsBtn: document.getElementById('settings-btn'),
    newSessionBtn: document.getElementById('new-session-btn'),
    sessionsList: document.getElementById('sessions-list'),
    
    // Chat
    backBtn: document.getElementById('back-btn'),
    saveBacklogBtn: document.getElementById('save-backlog-btn'),
    sessionStatus: document.getElementById('session-status'),
    messagesContainer: document.getElementById('messages'),
    messageInput: document.getElementById('message-input'),
    sendBtn: document.getElementById('send-btn'),
    
    // UI
    toast: document.getElementById('toast'),
    loading: document.getElementById('loading')
};

// ============================================================================
// API Client
// ============================================================================

const api = {
    async request(endpoint, options = {}) {
        const url = `${state.serverUrl}${endpoint}`;
        
        // Use AbortController for timeout (5 min for AI responses)
        const controller = new AbortController();
        const timeoutMs = options.timeout || 300000; // 5 minutes default
        const timeoutId = setTimeout(() => controller.abort(), timeoutMs);
        
        try {
            const response = await fetch(url, {
                ...options,
                signal: controller.signal,
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                }
            });
            
            clearTimeout(timeoutId);
            
            if (!response.ok) {
                throw new Error(`API Error: ${response.status} ${response.statusText}`);
            }
            
            const text = await response.text();
            return text ? JSON.parse(text) : null;
        } catch (error) {
            clearTimeout(timeoutId);
            if (error.name === 'AbortError') {
                throw new Error('Request timed out');
            }
            throw error;
        }
    },
    
    async checkHealth() {
        return this.request('/global/health');
    },
    
    async listSessions() {
        const result = await this.request('/session');
        // Filter to only show sessions that used f1-designer
        return result || [];
    },
    
    async createSession() {
        return this.request('/session', {
            method: 'POST',
            body: JSON.stringify({
                title: `F1 Ideas - ${new Date().toLocaleDateString()}`
            })
        });
    },
    
    async getSession(id) {
        return this.request(`/session/${id}`);
    },
    
    async getMessages(sessionId) {
        return this.request(`/session/${sessionId}/message`);
    },
    
    async sendMessage(sessionId, text) {
        return this.request(`/session/${sessionId}/message`, {
            method: 'POST',
            body: JSON.stringify({
                agent: CONFIG.AGENT,
                parts: [{ type: 'text', text }]
            })
        });
    },
    
    async sendMessageAsync(sessionId, text) {
        // Use async endpoint - doesn't wait for response
        await this.request(`/session/${sessionId}/prompt_async`, {
            method: 'POST',
            body: JSON.stringify({
                agent: CONFIG.AGENT,
                parts: [{ type: 'text', text }]
            })
        });
    },
    
    async saveToBacklog(idea) {
        // Use shell command to append to context file
        // This runs a shell command through OpenCode
        const command = `echo "\n\n## Idea from Mobile - ${new Date().toISOString()}\n${idea.replace(/"/g, '\\"')}" >> .opencode/context/f1-designer-context.md`;
        
        return this.request(`/session/${state.currentSession.id}/shell`, {
            method: 'POST',
            body: JSON.stringify({
                agent: CONFIG.AGENT,
                command: command
            })
        });
    }
};

// ============================================================================
// Event Stream (SSE)
// ============================================================================

function connectEventStream() {
    if (state.eventSource) {
        state.eventSource.close();
    }
    
    state.eventSource = new EventSource(`${state.serverUrl}/event`);
    
    state.eventSource.onopen = () => {
        console.log('SSE connected');
    };
    
    state.eventSource.onmessage = (event) => {
        try {
            const data = JSON.parse(event.data);
            handleServerEvent(data);
        } catch (e) {
            console.error('SSE parse error:', e);
        }
    };
    
    state.eventSource.onerror = (error) => {
        console.error('SSE error:', error);
        state.eventSource.close();
        
        // Attempt reconnect
        setTimeout(() => {
            if (state.isConnected) {
                connectEventStream();
            }
        }, CONFIG.RECONNECT_DELAY);
    };
}

function handleServerEvent(event) {
    // Handle different event types from OpenCode
    const { type, properties } = event;
    
    if (!state.currentSession) return;
    
    switch (type) {
        case 'message.created':
        case 'message.updated':
            if (properties?.sessionID === state.currentSession.id) {
                refreshMessages();
            }
            break;
            
        case 'part.created':
        case 'part.updated':
            if (properties?.sessionID === state.currentSession.id) {
                refreshMessages();
            }
            break;
            
        case 'session.status':
            if (properties?.sessionID === state.currentSession.id) {
                updateSessionStatus(properties.status);
            }
            break;
    }
}

function updateSessionStatus(status) {
    const indicator = elements.sessionStatus;
    if (status === 'busy' || status === 'running') {
        indicator.classList.add('busy');
        state.isSending = true;
    } else {
        indicator.classList.remove('busy');
        state.isSending = false;
    }
    updateSendButton();
}

// ============================================================================
// UI Helpers
// ============================================================================

function showScreen(screen) {
    elements.settingsScreen.classList.add('hidden');
    elements.sessionsScreen.classList.add('hidden');
    elements.chatScreen.classList.add('hidden');
    screen.classList.remove('hidden');
}

function showLoading(show = true) {
    elements.loading.classList.toggle('hidden', !show);
}

function showToast(message, type = 'info') {
    elements.toast.textContent = message;
    elements.toast.className = `toast ${type}`;
    elements.toast.classList.remove('hidden');
    
    setTimeout(() => {
        elements.toast.classList.add('hidden');
    }, CONFIG.TOAST_DURATION);
}

function updateSendButton() {
    elements.sendBtn.disabled = state.isSending || !elements.messageInput.value.trim();
}

function formatTime(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const diffDays = Math.floor((now - date) / (1000 * 60 * 60 * 24));
    
    if (diffDays === 0) {
        return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    } else if (diffDays === 1) {
        return 'Yesterday';
    } else if (diffDays < 7) {
        return date.toLocaleDateString([], { weekday: 'short' });
    } else {
        return date.toLocaleDateString([], { month: 'short', day: 'numeric' });
    }
}

function renderMarkdown(text) {
    // Check for swarm status and render it specially
    const swarmContent = parseSwarmStatus(text);
    if (swarmContent.hasSwarm) {
        return swarmContent.html;
    }
    
    // Simple markdown rendering
    return text
        // Code blocks
        .replace(/```(\w*)\n([\s\S]*?)```/g, '<pre><code>$2</code></pre>')
        // Inline code
        .replace(/`([^`]+)`/g, '<code>$1</code>')
        // Bold
        .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
        // Italic
        .replace(/\*([^*]+)\*/g, '<em>$1</em>')
        // Line breaks
        .replace(/\n/g, '<br>');
}

function parseSwarmStatus(text) {
    // Look for ASCII box swarm panel (╔═══...╚═══)
    const boxMatch = text.match(/╔[═]+╗[\s\S]*?╚[═]+╝/);
    
    if (boxMatch) {
        const boxContent = boxMatch[0];
        const agents = [];
        
        // Parse each line looking for agent status
        const lines = boxContent.split('\n');
        for (const line of lines) {
            // Match: ║  ✅ Agent Name          done        ║
            // Or:    ║  ⏳ Agent Name          working...  ║
            const agentMatch = line.match(/║\s*(✅|⏳|❌)\s+([^║]+?)\s+(done|working\.\.\.|error)\s*║/);
            if (agentMatch) {
                agents.push({
                    name: agentMatch[2].trim(),
                    status: agentMatch[3] === 'working...' ? 'pending' : agentMatch[3]
                });
            }
        }
        
        if (agents.length > 0) {
            const done = agents.filter(a => a.status === 'done').length;
            const total = agents.length;
            
            // Get content after the box
            let cleanText = text.replace(/╔[═]+╗[\s\S]*?╚[═]+╝/, '').trim();
            
            const swarmHtml = renderSwarmPanel(agents, done, total);
            const contentHtml = cleanText ? renderBasicMarkdown(cleanText) : '';
            
            return { 
                hasSwarm: true, 
                html: swarmHtml + contentHtml 
            };
        }
    }
    
    // Fallback: Look for [SWARM_STATUS] markers
    const swarmMatch = text.match(/\[SWARM_STATUS\]([\s\S]*?)\[\/SWARM_STATUS\]/);
    
    if (!swarmMatch) {
        // Check for simple swarm indicators
        const agentMatches = text.matchAll(/\[AGENT:([^\]:]+):([^\]]+)\]/g);
        const agents = [...agentMatches];
        
        if (agents.length === 0) {
            return { hasSwarm: false, html: '' };
        }
        
        // Build swarm panel from individual markers
        const agentList = agents.map(m => ({
            name: m[1],
            status: m[2].toLowerCase()
        }));
        
        const done = agentList.filter(a => a.status === 'done').length;
        const total = agentList.length;
        
        // Remove agent markers from text
        let cleanText = text.replace(/\[AGENT:[^\]]+\]/g, '').trim();
        
        const swarmHtml = renderSwarmPanel(agentList, done, total);
        const contentHtml = cleanText ? renderBasicMarkdown(cleanText) : '';
        
        return { 
            hasSwarm: true, 
            html: swarmHtml + contentHtml 
        };
    }
    
    // Parse structured swarm status
    const statusBlock = swarmMatch[1];
    const lines = statusBlock.trim().split('\n');
    const agents = [];
    
    for (const line of lines) {
        const match = line.match(/^([^:]+):(.+)$/);
        if (match) {
            agents.push({
                name: match[1].trim(),
                status: match[2].trim().toLowerCase()
            });
        }
    }
    
    const done = agents.filter(a => a.status === 'done').length;
    const total = agents.length;
    
    // Get content after swarm status
    let cleanText = text.replace(/\[SWARM_STATUS\][\s\S]*?\[\/SWARM_STATUS\]/, '').trim();
    
    const swarmHtml = renderSwarmPanel(agents, done, total);
    const contentHtml = cleanText ? renderBasicMarkdown(cleanText) : '';
    
    return { 
        hasSwarm: true, 
        html: swarmHtml + contentHtml 
    };
}

function renderSwarmPanel(agents, done, total) {
    const agentRows = agents.map(agent => {
        const icon = agent.status === 'done' ? '✅' : 
                     agent.status === 'error' ? '❌' : '⏳';
        const statusClass = agent.status === 'done' ? 'done' : 
                           agent.status === 'error' ? 'error' : 'pending';
        return `<div class="swarm-agent ${statusClass}">
            <span class="swarm-icon">${icon}</span>
            <span class="swarm-name">${agent.name}</span>
            <span class="swarm-status">${agent.status}</span>
        </div>`;
    }).join('');
    
    const progress = total > 0 ? Math.round((done / total) * 100) : 0;
    
    return `
        <div class="swarm-panel">
            <div class="swarm-header">
                <span class="swarm-title">🚀 Swarm Status</span>
                <span class="swarm-count">${done}/${total}</span>
            </div>
            <div class="swarm-progress">
                <div class="swarm-progress-bar" style="width: ${progress}%"></div>
            </div>
            <div class="swarm-agents">
                ${agentRows}
            </div>
        </div>
    `;
}

function renderBasicMarkdown(text) {
    return text
        .replace(/```(\w*)\n([\s\S]*?)```/g, '<pre><code>$2</code></pre>')
        .replace(/`([^`]+)`/g, '<code>$1</code>')
        .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
        .replace(/\*([^*]+)\*/g, '<em>$1</em>')
        .replace(/\n/g, '<br>');
}

// ============================================================================
// Sessions
// ============================================================================

async function loadSessions() {
    try {
        showLoading(true);
        state.sessions = await api.listSessions();
        renderSessions();
    } catch (error) {
        console.error('Failed to load sessions:', error);
        showToast('Failed to load sessions', 'error');
    } finally {
        showLoading(false);
    }
}

function renderSessions() {
    if (state.sessions.length === 0) {
        elements.sessionsList.innerHTML = `
            <div class="empty-state">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
                </svg>
                <p>No brainstorms yet.<br>Tap + to start one!</p>
            </div>
        `;
        return;
    }
    
    // Sort by most recent
    const sorted = [...state.sessions].sort((a, b) => 
        new Date(b.updatedAt || b.createdAt) - new Date(a.updatedAt || a.createdAt)
    );
    
    elements.sessionsList.innerHTML = sorted.map(session => `
        <div class="session-item" data-id="${session.id}">
            <div class="icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
                </svg>
            </div>
            <div class="details">
                <div class="title">${session.title || 'Untitled Session'}</div>
                <div class="meta">${formatTime(session.updatedAt || session.createdAt)}</div>
            </div>
        </div>
    `).join('');
    
    // Add click handlers
    elements.sessionsList.querySelectorAll('.session-item').forEach(item => {
        item.addEventListener('click', () => openSession(item.dataset.id));
    });
}

async function createNewSession() {
    try {
        showLoading(true);
        const session = await api.createSession();
        state.currentSession = session;
        localStorage.setItem(CONFIG.STORAGE_KEYS.CURRENT_SESSION, session.id);
        await loadSessions();
        openChat();
    } catch (error) {
        console.error('Failed to create session:', error);
        showToast('Failed to create session', 'error');
    } finally {
        showLoading(false);
    }
}

async function openSession(sessionId) {
    try {
        showLoading(true);
        state.currentSession = await api.getSession(sessionId);
        localStorage.setItem(CONFIG.STORAGE_KEYS.CURRENT_SESSION, sessionId);
        openChat();
    } catch (error) {
        console.error('Failed to open session:', error);
        showToast('Failed to open session', 'error');
    } finally {
        showLoading(false);
    }
}

// ============================================================================
// Chat
// ============================================================================

function openChat() {
    showScreen(elements.chatScreen);
    refreshMessages();
}

async function refreshMessages() {
    if (!state.currentSession) return;
    
    try {
        const result = await api.getMessages(state.currentSession.id);
        state.messages = result || [];
        renderMessages();
    } catch (error) {
        console.error('Failed to load messages:', error);
    }
}

function renderMessages() {
    if (state.messages.length === 0) {
        elements.messagesContainer.innerHTML = `
            <div class="empty-state">
                <p>Start brainstorming with f1-designer!</p>
            </div>
        `;
        return;
    }
    
    const html = state.messages.map(msg => {
        const { info, parts } = msg;
        const isUser = info.role === 'user';
        
        // Extract text content from parts
        const textParts = parts
            .filter(p => p.type === 'text')
            .map(p => p.text)
            .join('\n');
        
        if (!textParts) return '';
        
        return `
            <div class="message ${isUser ? 'user' : 'assistant'}">
                ${!isUser ? '<div class="agent-label">f1-designer</div>' : ''}
                ${renderMarkdown(textParts)}
            </div>
        `;
    }).join('');
    
    elements.messagesContainer.innerHTML = html;
    
    // Scroll to bottom
    elements.messagesContainer.scrollTop = elements.messagesContainer.scrollHeight;
}

async function sendMessage() {
    const text = elements.messageInput.value.trim();
    if (!text || state.isSending || !state.currentSession) return;
    
    state.isSending = true;
    updateSendButton();
    elements.messageInput.value = '';
    autoResizeInput();
    
    // Add user message immediately for responsiveness
    const userMsg = {
        info: { role: 'user', id: 'temp-' + Date.now() },
        parts: [{ type: 'text', text }]
    };
    state.messages.push(userMsg);
    renderMessages();
    
    // Create streaming response container
    const streamDiv = document.createElement('div');
    streamDiv.className = 'message assistant streaming';
    streamDiv.id = 'streaming-response';
    streamDiv.innerHTML = '<div class="agent-label">f1-designer</div><div class="stream-content"><span class="thinking-dots">Thinking</span></div>';
    elements.messagesContainer.appendChild(streamDiv);
    elements.messagesContainer.scrollTop = elements.messagesContainer.scrollHeight;
    
    try {
        // Send message async (returns immediately)
        await api.sendMessageAsync(state.currentSession.id, text);
        
        // Start polling for response updates
        await pollForResponse();
        
    } catch (error) {
        console.error('Failed to send message:', error);
        showToast('Failed to send message', 'error');
        // Remove the temp message on error
        state.messages = state.messages.filter(m => m.info.id !== userMsg.info.id);
        const streamEl = document.getElementById('streaming-response');
        if (streamEl) streamEl.remove();
        renderMessages();
    } finally {
        state.isSending = false;
        updateSendButton();
    }
}

async function pollForResponse() {
    const streamContent = document.querySelector('#streaming-response .stream-content');
    let lastContent = '';
    let stableCount = 0;
    const maxPolls = 300; // 5 minutes max (1 second intervals)
    let polls = 0;
    
    while (polls < maxPolls) {
        await sleep(1000); // Poll every second
        polls++;
        
        try {
            const messages = await api.getMessages(state.currentSession.id);
            if (!messages || messages.length === 0) continue;
            
            // Find the latest assistant message
            const assistantMsgs = messages.filter(m => m.info.role === 'assistant');
            if (assistantMsgs.length === 0) continue;
            
            const latest = assistantMsgs[assistantMsgs.length - 1];
            const textParts = latest.parts
                .filter(p => p.type === 'text')
                .map(p => p.text)
                .join('\n');
            
            if (textParts && textParts !== lastContent) {
                // Update the streaming display
                streamContent.innerHTML = renderMarkdown(textParts);
                elements.messagesContainer.scrollTop = elements.messagesContainer.scrollHeight;
                lastContent = textParts;
                stableCount = 0;
            } else if (textParts) {
                stableCount++;
                // If content hasn't changed for 3 seconds, assume done
                if (stableCount >= 3) {
                    break;
                }
            }
        } catch (error) {
            console.error('Poll error:', error);
        }
    }
    
    // Remove streaming div and do final refresh
    const streamEl = document.getElementById('streaming-response');
    if (streamEl) streamEl.remove();
    await refreshMessages();
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// ============================================================================
// Save to Backlog
// ============================================================================

async function saveToBacklog() {
    if (!state.currentSession || state.messages.length === 0) {
        showToast('No ideas to save', 'error');
        return;
    }
    
    // Get the last assistant message as the idea
    const assistantMessages = state.messages
        .filter(m => m.info.role === 'assistant')
        .map(m => m.parts.filter(p => p.type === 'text').map(p => p.text).join('\n'));
    
    if (assistantMessages.length === 0) {
        showToast('No ideas to save', 'error');
        return;
    }
    
    const lastIdea = assistantMessages[assistantMessages.length - 1];
    
    try {
        showLoading(true);
        await api.saveToBacklog(lastIdea);
        showToast('Saved to backlog!', 'success');
    } catch (error) {
        console.error('Failed to save to backlog:', error);
        showToast('Failed to save', 'error');
    } finally {
        showLoading(false);
    }
}

// ============================================================================
// Connection
// ============================================================================

async function connect() {
    const url = elements.serverUrlInput.value.trim();
    if (!url) {
        elements.connectionStatus.textContent = 'Please enter a server URL';
        elements.connectionStatus.className = 'status error';
        return;
    }
    
    // Normalize URL
    let serverUrl = url;
    if (!serverUrl.startsWith('http')) {
        serverUrl = 'http://' + serverUrl;
    }
    serverUrl = serverUrl.replace(/\/$/, ''); // Remove trailing slash
    
    elements.connectBtn.disabled = true;
    elements.connectionStatus.textContent = 'Connecting...';
    elements.connectionStatus.className = 'status';
    
    try {
        state.serverUrl = serverUrl;
        const health = await api.checkHealth();
        
        if (health.healthy) {
            state.isConnected = true;
            localStorage.setItem(CONFIG.STORAGE_KEYS.SERVER_URL, serverUrl);
            
            elements.connectionStatus.textContent = `Connected (v${health.version})`;
            elements.connectionStatus.className = 'status success';
            
            // Connect SSE
            connectEventStream();
            
            // Load sessions
            await loadSessions();
            showScreen(elements.sessionsScreen);
        } else {
            throw new Error('Server unhealthy');
        }
    } catch (error) {
        console.error('Connection failed:', error);
        elements.connectionStatus.textContent = 'Connection failed. Check URL and server.';
        elements.connectionStatus.className = 'status error';
        state.isConnected = false;
    } finally {
        elements.connectBtn.disabled = false;
    }
}

function disconnect() {
    state.isConnected = false;
    if (state.eventSource) {
        state.eventSource.close();
        state.eventSource = null;
    }
    showScreen(elements.settingsScreen);
}

// ============================================================================
// Input Handling
// ============================================================================

function autoResizeInput() {
    const input = elements.messageInput;
    input.style.height = 'auto';
    input.style.height = Math.min(input.scrollHeight, 120) + 'px';
}

// ============================================================================
// Event Listeners
// ============================================================================

function initEventListeners() {
    // Settings
    elements.connectBtn.addEventListener('click', connect);
    elements.serverUrlInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') connect();
    });
    
    // Sessions
    elements.settingsBtn.addEventListener('click', disconnect);
    elements.newSessionBtn.addEventListener('click', createNewSession);
    
    // Chat
    elements.backBtn.addEventListener('click', () => {
        showScreen(elements.sessionsScreen);
        loadSessions();
    });
    elements.saveBacklogBtn.addEventListener('click', saveToBacklog);
    elements.sendBtn.addEventListener('click', sendMessage);
    elements.messageInput.addEventListener('input', () => {
        autoResizeInput();
        updateSendButton();
    });
    elements.messageInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
}

// ============================================================================
// Initialization
// ============================================================================

function init() {
    initEventListeners();
    
    // Restore saved server URL
    const savedUrl = localStorage.getItem(CONFIG.STORAGE_KEYS.SERVER_URL);
    if (savedUrl) {
        elements.serverUrlInput.value = savedUrl;
    }
    
    // Register service worker for PWA
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('service-worker.js')
            .then(() => console.log('Service worker registered'))
            .catch(err => console.error('SW registration failed:', err));
    }
}

// Start the app
init();

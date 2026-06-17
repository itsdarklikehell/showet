/**
 * Showet Collaborative Client
 * WebSocket-based real-time demo collaboration
 */

class ShowetCollaborative {
    constructor(sessionId) {
        this.sessionId = sessionId;
        this.ws = null;
        this.playbackState = 'idle';
        this.onMessageCallback = null;
    }

    connect() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const host = window.location.host || 'localhost:8765';
        
        this.ws = new WebSocket(`${protocol}//${host}/ws/${this.sessionId}`);
        
        this.ws.onopen = () => {
            console.log('🤝 Connected to Showet session');
            this.send({ type: 'join', session_id: this.sessionId, client_id: this.getClientId() });
        };
        
        this.ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.handleMessage(data);
        };
        
        this.ws.onclose = () => {
            console.log('❌ Disconnected from session');
        };
    }

    handleMessage(data) {
        switch(data.type) {
            case 'session_info':
                if (data.session) {
                    this.updateUI(data.session);
                }
                break;
            case 'playback_state':
                this.syncPlayback(data.state, data.time);
                break;
            case 'chat':
                this.displayChatMessage(data.message, data.sender);
                break;
        }
        
        if (this.onMessageCallback) {
            this.onMessageCallback(data);
        }
    }

    send(data) {
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
            this.ws.send(JSON.stringify(data));
        }
    }

    updatePlayback(state, time) {
        this.playbackState = state;
        this.send({ type: 'playback_state', state, time });
    }

    sendChat(message) {
        if (message.trim()) {
            this.send({ type: 'chat', message, sender: this.getClientId() });
            this.addChatInput(message);
        }
    }

    syncPlayback(state, time) {
        // Override this to handle playback synchronization
        console.log(`Sync playback: ${state} at ${time}s`);
    }

    updateUI(session) {
        console.log('Session info:', session);
    }

    displayChatMessage(message, sender) {
        const chatContainer = document.getElementById('chat-messages');
        if (!chatContainer) return;
        
        const msgDiv = document.createElement('div');
        msgDiv.className = 'chat-message';
        msgDiv.innerHTML = `<strong>${sender}:</strong> ${message}`;
        chatContainer.appendChild(msgDiv);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    addChatInput(message) {
        const input = document.getElementById('chat-input');
        if (input) {
            input.value = '';
            input.focus();
        }
    }

    getClientId() {
        return 'user_' + Math.random().toString(36).substr(2, 9);
    }

    disconnect() {
        if (this.ws) {
            this.ws.close();
        }
    }
}

// Global instance
window.ShowetCollaborative = ShowetCollaborative;
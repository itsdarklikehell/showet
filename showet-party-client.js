/**
 * Showet Party Mode Client Extension
 * Adds synchronized demo playback controls for collaborative viewing
 */

class ShowetPartyMode extends ShowetCollaborative {
    constructor(sessionId) {
        super(sessionId);
        this.isHost = false;
        this.currentDemo = null;
    }

    addHostControls() {
        if (!this.isHost) return;
        
        const controls = document.querySelector('.controls');
        if (!controls) return;
        
        // Check if controls already added
        if (document.getElementById('party-start-btn')) return;
        
        const partyDiv = document.createElement('div');
        partyDiv.className = 'control-group';
        partyDiv.innerHTML = `
            <label>Party Mode (Host)</label>
            <button id="party-start-btn" style="background:#ff6b00;color:white;border:none;padding:6px 10px;border-radius:4px;cursor:pointer;">
                Start Party Session
            </button>
        `;
        controls.appendChild(partyDiv);
        
        document.getElementById('party-start-btn').onclick = () => this.startPartySession();
    }

    startPartySession() {
        const sessionId = prompt('Enter/create party session ID:', 'showet-party-' + Date.now());
        if (sessionId) {
            this.isHost = true;
            this.sessionId = sessionId;
            this.connect();
        }
    }

    handleMessage(data) {
        super.handleMessage(data);
        
        switch(data.type) {
            case 'demo_launch':
                this.syncDemoLaunch(data.demo_id, data.demo_name);
                break;
            case 'playback_state':
                this.syncPlayback(data.state, data.time, data.demo_id);
                break;
        }
    }

    syncDemoLaunch(demoId, demoName) {
        // Auto-load demo on all clients when host launches
        console.log(`[Party] Host launched demo: ${demoName} (${demoId})`);
        
        // Show notification
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed; top: 20px; right: 20px; 
            background: #ff6b00; color: white; padding: 10px 15px;
            border-radius: 4px; z-index: 1000; animation: slideIn 0.3s;
        `;
        notification.textContent = `🎉 Party Demo: ${demoName}`;
        document.body.appendChild(notification);
        
        setTimeout(() => notification.remove(), 3000);
        
        // Trigger demo launch
        if (demoName) {
            this.launchDemoByName(demoName);
        }
    }

    launchDemoByName(name) {
        // Find and click the platform item
        const items = document.querySelectorAll('.platform-item');
        items.forEach(item => {
            if (item.textContent.toLowerCase().includes(name.toLowerCase())) {
                item.click();
            }
        });
    }

    syncPlayback(state, time, demoId) {
        // Sync emulator playback state
        console.log(`[Party] Syncing playback: ${state} at ${time}s`);
        
        // This would integrate with nostalgist.js playback controls
        if (demoId && !this.currentDemo) {
            this.currentDemo = demoId;
        }
    }
}

// Extend global ShowetCollaborative
window.ShowetPartyMode = ShowetPartyMode;
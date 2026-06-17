/**
 * Showet Preview Clips Generator
 * Creates 30-second highlight clips for demo previews in Museum Mode
 * Enhanced with scene.org integration
 */

class ShowetPreviewClips {
    constructor() {
        this.clips = new Map();
        this.sceneOrgClient = null; // Will connect to scene.org
        this.previewDir = 'previews';
    }

    setSceneOrgClient(client) {
        this.sceneOrgClient = client;
    }

    async generatePreview(demoId, platform = 'amiga', duration = 30) {
        // In a real implementation, this would:
        // 1. Download demo from scene.org if needed
        // 2. Launch the demo in nostalgist.js
        // 3. Capture frames and extract highlight moments
        // 4. Create a 30-second highlight clip using ffmpeg
        
        // Check scene.org for the demo
        if (this.sceneOrgClient) {
            const demos = await this.sceneOrgClient.search_demos(demoId);
            if (demos.length > 0) {
                const demo = demos[0];
                console.log(`Found ${demoId} on scene.org: ${demo.url}`);
            }
        }
        
        const clipPath = `${this.previewDir}/${demoId.replace(/\\s+/g, '_').toLowerCase()}_clip.mp4`;
        
        return {
            demo_id: demoId,
            clip_path: clipPath,
            duration: duration,
            thumbnail: clipPath.replace('.mp4', '.jpg'),
            source_platform: platform
        };
    }

    async generateAllPreviews(demoList) {
        // Batch generate preview clips for multiple demos
        const results = [];
        for (const demo of demoList) {
            const preview = await this.generatePreview(demo.name, demo.platform);
            results.push(preview);
        }
        return results;
    }

    getPreviewGallery(containerId = 'preview-gallery') {
        const container = document.getElementById(containerId);
        if (!container) return;
        
        let html = '<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:10px;">';
        
        for (const [name, path] of this.clips.entries()) {
            html += `
                <div style="cursor:pointer;background:#111;padding:8px;border-radius:4px;" onclick="ShowetPreviews.playPreview('${name}')">
                    <img src="${path.replace('.mp4', '_thumb.jpg')}" 
                         style="width:100%;height:120px;object-fit:cover;border-radius:4px;">
                    <div style="color:#aaa;margin-top:5px;font-size:0.85em;">${name}</div>
                </div>
            `;
        }
        
        html += '</div>';
        container.innerHTML = html;
    }

    async playPreview(demoName) {
        const clipInfo = this.clips.get(demoName);
        if (!clipInfo) return;
        
        // Show in modal or dedicated player
        const modal = document.createElement('div');
        modal.style.cssText = `
            position:fixed;top:0;left:0;width:100%;height:100%;
            background:rgba(0,0,0,0.9);z-index:1000;
            display:flex;justify-content:center;align-items:center;
        `;
        modal.innerHTML = `
            <video src="${clipInfo}" autoplay controls 
                   style="max-width:90%;max-height:80%;border-radius:8px;">
            </video>
            <button onclick="this.parentElement.remove()" 
                    style="position:absolute;top:20px;right:20px;background:#ff6b00;color:#fff;border:none;padding:10px 20px;cursor:pointer;">
                Close
            </button>
        `;
        document.body.appendChild(modal);
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    window.ShowetPreviews = new ShowetPreviewClips();
});
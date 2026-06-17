/**
 * Showet Preview Clips Generator
 * Creates 30-second highlight clips for demo previews in Museum Mode
 */

class ShowetPreviewClips {
    constructor() {
        this.clips = {
            "Second Reality": "previews/second_reality_clip.mp4",
            "Heaven Seven": "previews/heaven_seven_clip.mp4",
            "Elevated": "previews/elevated_clip.mp4",
            "Arte": "previews/arte_clip.mp4"
        };
    }

    async generatePreview(demoId, duration = 30) {
        // In a real implementation, this would:
        // 1. Launch the demo in nostalgist.js
        // 2. Capture frames using MediaRecorder
        // 3. Create a 30-second highlight clip
        
        const clipPath = this.clips[demoId] || `previews/${demoId}_clip.mp4`;
        
        return {
            demo_id: demoId,
            clip_path: clipPath,
            duration: duration,
            thumbnail: clipPath.replace('.mp4', '.jpg')
        };
    }

    getClipForDemo(demoName) {
        const clipPath = this.clips[demoName];
        if (!clipPath) return null;
        
        return {
            source: clipPath,
            thumbnail: clipPath.replace('.mp4', '_thumb.jpg'),
            duration: 30
        };
    }

    async showPreview(demoName, containerId = 'preview-container') {
        const clipInfo = this.getClipForDemo(demoName);
        if (!clipInfo) return;
        
        const container = document.getElementById(containerId);
        if (!container) return;
        
        container.innerHTML = `
            <video src="${clipInfo.source}" 
                   poster="${clipInfo.thumbnail}"
                   autoplay muted loop
                   style="width:100%;max-width:400px;border-radius:8px;">
            </video>
            <div style="margin-top:10px;color:#aaa;font-size:0.9em;">
                30-second highlight preview
            </div>
        `;
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    window.ShowetPreviews = new ShowetPreviewClips();
});
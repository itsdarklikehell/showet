/**
 * Showet + nostalgist.js Integration
 * 
 * This script demonstrates how to use the generated nostalgist configs
 * to launch demos in the browser using Television Simulator '99.
 * 
 * Usage: Include this after nostalgist.js in your HTML
 * <script src="https://cdn.jsdelivr.net/npm/nostalgist@latest/dist/nostalgist.min.js"></script>
 * <script src="showet-nostalgist-loader.js"></script>
 */

class ShowetNostalgistLoader {
    constructor(configDir = '/nostalgist_configs') {
        this.configDir = configDir;
        this.currentEmulator = null;
    }

    /**
     * Load a demo for a specific platform
     * @param {string} platformSlug - The showet platform slug (e.g., 'nintendo_famicom')
     * @param {string} romUrl - URL to the ROM file to launch
     */
    async launchDemo(platformSlug, romUrl) {
        const config = await this._loadPlatformConfig(platformSlug);
        
        if (config.error) {
            console.error('Platform not found:', config.error);
            return null;
        }

        // Override the ROM URL with the actual demo
        config.rom = romUrl;

        try {
            this.currentEmulator = await Nostalgist.launch(config);
            return this.currentEmulator;
        } catch (err) {
            console.error('Failed to launch emulator:', err);
            return null;
        }
    }

    /**
     * Load platform configuration from JSON
     * @private
     */
    async _loadPlatformConfig(platformSlug) {
        const response = await fetch(`${this.configDir}/${platformSlug}.json`);
        if (!response.ok) {
            return { error: `Configuration not found for ${platformSlug}` };
        }
        return await response.json();
    }

    /**
     * Get list of available platforms
     * @returns {Promise<string[]>} Array of platform slugs
     */
    async getAvailablePlatforms() {
        // In a real implementation, this would fetch from a manifest
        // For now, we'll use the known platforms
        return [
            'nintendo_famicom', 'sega_megadrive', 'commodore_64',
            'atari_2600', 'superfamicom', 'playstation',
            // ... more platforms as generated
        ];
    }

    /**
     * Exit current emulator
     */
    exit() {
        if (this.currentEmulator) {
            this.currentEmulator.exit();
            this.currentEmulator = null;
        }
    }
}

// Global instance
window.showetNostalgist = new ShowetNostalgistLoader();

// Example usage:
// await showetNostalgist.launchDemo('nintendo_famicom', 'https://example.com/demo.nes');
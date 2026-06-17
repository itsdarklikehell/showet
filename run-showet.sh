#!/bin/bash
# Showet Ultimate Launcher - One command to demo paradise
# Usage: ./run-showet.sh [platform] [demo_id] [--tour|--hall-of-fame|--random]

set -e

PLATFORM="${1:-commodore_64}"
DEMO_ID="${2:-12345}"
MODE="${3:-}"

echo "🚀 SHOWET DEMO RUNNER v2.0 - Launching..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Start the web server in background
python3 -m http.server 8000 &
SERVER_PID=$!

# Wait for server
sleep 2

# Open browser with appropriate mode
case "$MODE" in
    --tour)
        URL="http://localhost:8000/showet-showcase.html?mode=tour"
        echo "🎞️  Starting Demoscene Tour Mode..."
        ;;
    --hall-of-fame)
        URL="http://localhost:8000/showet-showcase.html?mode=hof"
        echo "🏆 Launching Hall of Fame..."
        ;;
    --random)
        URL="http://localhost:8000/showet-showcase.html?mode=random&platform=$PLATFORM"
        echo "🎲 Selecting random demo on $PLATFORM..."
        ;;
    *)
        URL="http://localhost:8000/showet-showcase.html?platform=$PLATFORM&demo=$DEMO_ID"
        echo "🕹️  Loading demo #$DEMO_ID on $PLATFORM..."
        ;;
esac

# Open browser
if command -v xdg-open &> /dev/null; then
    xdg-open "$URL"
elif command -v open &> /dev/null; then
    open "$URL"
else
    echo "🌐 Open your browser to: $URL"
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Showet running! Press Ctrl+C to stop."
echo ""
echo "Features available:"
echo "  🎨 Shader editor - customize CRT effects in real-time"
echo "  🎞️  Tour mode - journey through demoscene history"
echo "  📅 Timeline - explore demo releases by era"
echo "  🎵 Spectrum - visual audio analysis"
echo "  🤝 Collaboration - real-time multi-user sessions"
echo ""

# Cleanup on exit
trap 'kill $SERVER_PID 2>/dev/null; echo "🛑 Showet stopped."' INT TERM EXIT

# Keep script running
wait $SERVER_PID
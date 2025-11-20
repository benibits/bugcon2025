#!/bin/bash
################################################################################
# BugCon 2025 - Simple Injection Demo Startup Script (Linux/macOS)
################################################################################
# This script:
#   1. Starts Chrome with remote debugging on port 9222
#   2. Starts the presentation server on port 8000
#   3. Opens the presentation in the debugging-enabled Chrome
################################################################################

set -e  # Exit on error

echo ""
echo "========================================"
echo " BugCon 2025 - Injection Demo Startup"
echo "========================================"
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Create temp directory if it doesn't exist
CHROME_DEBUG_DIR="${TMPDIR:-/tmp}/chrome-debug"
mkdir -p "$CHROME_DEBUG_DIR"

echo "[1/4] Starting Chrome with debugging on port 9222..."
echo ""

# Find Chrome executable based on OS
CHROME_BIN=""
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    if [ -f "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" ]; then
        CHROME_BIN="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    elif [ -f "/Applications/Chromium.app/Contents/MacOS/Chromium" ]; then
        CHROME_BIN="/Applications/Chromium.app/Contents/MacOS/Chromium"
    fi
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    if command -v google-chrome &> /dev/null; then
        CHROME_BIN="google-chrome"
    elif command -v chromium-browser &> /dev/null; then
        CHROME_BIN="chromium-browser"
    elif command -v chromium &> /dev/null; then
        CHROME_BIN="chromium"
    fi
fi

if [ -z "$CHROME_BIN" ]; then
    echo "ERROR: Chrome/Chromium not found!"
    echo "Please install Chrome or Chromium, or update the path in this script."
    exit 1
fi

# Start Chrome with debugging in background
"$CHROME_BIN" \
    --remote-debugging-port=9222 \
    --user-data-dir="$CHROME_DEBUG_DIR" \
    --remote-allow-origins=* \
    &> /dev/null &

CHROME_PID=$!
echo "Chrome started with PID: $CHROME_PID"

echo "[2/4] Waiting for Chrome to initialize (5 seconds)..."
sleep 5

# Verify Chrome is listening
if lsof -Pi :9222 -sTCP:LISTEN -t >/dev/null 2>&1 || netstat -an 2>/dev/null | grep -q "\.9222.*LISTEN"; then
    echo "SUCCESS: Chrome is listening on port 9222"
else
    echo "WARNING: Chrome debugging port not detected!"
    echo "Continuing anyway, but injection may fail..."
fi

echo ""
echo "[3/4] Starting presentation server on port 8000..."

# Navigate to slides directory
SLIDES_DIR="$SCRIPT_DIR/../../slides"
cd "$SLIDES_DIR"

# Start server in background
python3 serve_slides.py --no-browser &> /dev/null &
SERVER_PID=$!
echo "Server started with PID: $SERVER_PID"

sleep 2

# Verify server is running
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1 || netstat -an 2>/dev/null | grep -q "\.8000.*LISTEN"; then
    echo "SUCCESS: Presentation server is running"
else
    echo "ERROR: Presentation server failed to start!"
    exit 1
fi

echo ""
echo "[4/4] Opening presentation in debugging Chrome..."
sleep 3

# Open presentation using CDP API
cd "$SCRIPT_DIR"
python3 open_in_debug_chrome.py http://localhost:8000/slides/

if [ $? -ne 0 ]; then
    echo "WARNING: Failed to open in debug Chrome"
    echo "You can manually open: http://localhost:8000/slides/ in the debug Chrome window"
fi

echo ""
echo "========================================"
echo " DEMO ENVIRONMENT READY!"
echo "========================================"
echo ""
echo "Chrome Debug Port: http://localhost:9222/json"
echo "Presentation:      http://localhost:8000"
echo ""
echo "To run the injection:"
echo "  python3 inject_cat_opening.py"
echo ""
echo "To clean up when done:"
echo "  ./cleanup_demo.sh"
echo ""


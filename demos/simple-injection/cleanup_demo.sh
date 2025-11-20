#!/bin/bash
################################################################################
# BugCon 2025 - Clean Up Demo Processes (Linux/macOS)
################################################################################

echo ""
echo "Cleaning up demo processes..."
echo ""

# Kill presentation server (Python on port 8000)
echo "Stopping presentation server..."
SERVER_PIDS=$(lsof -ti :8000 2>/dev/null || netstat -anp 2>/dev/null | grep ":8000" | awk '{print $7}' | cut -d'/' -f1)
if [ ! -z "$SERVER_PIDS" ]; then
    for pid in $SERVER_PIDS; do
        if [ ! -z "$pid" ] && [ "$pid" != "-" ]; then
            echo "  Killing process $pid"
            kill -9 "$pid" 2>/dev/null || sudo kill -9 "$pid" 2>/dev/null
        fi
    done
    echo "  Server stopped"
else
    echo "  No server process found"
fi

# Kill Chrome debug instances
echo "Stopping debugging Chrome instances..."

# Get Chrome debug directory
CHROME_DEBUG_DIR="${TMPDIR:-/tmp}/chrome-debug"

# Find and kill Chrome processes using the debug directory
CHROME_PIDS=$(ps aux | grep -E "chrome.*--remote-debugging-port=9222|chromium.*--remote-debugging-port=9222" | grep -v grep | awk '{print $2}')

if [ ! -z "$CHROME_PIDS" ]; then
    for pid in $CHROME_PIDS; do
        if [ ! -z "$pid" ]; then
            echo "  Killing Chrome process $pid"
            kill -9 "$pid" 2>/dev/null || sudo kill -9 "$pid" 2>/dev/null
        fi
    done
    echo "  Chrome stopped"
else
    echo "  No debug Chrome process found"
fi

# Alternative: Kill anything listening on port 9222
DEBUG_PIDS=$(lsof -ti :9222 2>/dev/null || netstat -anp 2>/dev/null | grep ":9222" | awk '{print $7}' | cut -d'/' -f1)
if [ ! -z "$DEBUG_PIDS" ]; then
    for pid in $DEBUG_PIDS; do
        if [ ! -z "$pid" ] && [ "$pid" != "-" ]; then
            echo "  Killing process $pid on port 9222"
            kill -9 "$pid" 2>/dev/null || sudo kill -9 "$pid" 2>/dev/null
        fi
    done
fi

echo ""
echo "Cleanup complete!"
echo ""
echo "Verify with:"
if command -v lsof &> /dev/null; then
    echo "  lsof -i :9222,8000"
elif command -v netstat &> /dev/null; then
    echo "  netstat -an | grep -E ':(9222|8000)'"
fi
echo ""


#!/usr/bin/env python3
"""
Helper: Open URL in Debugging Chrome
Opens a URL in the Chrome instance with debugging enabled (port 9222)
"""

import json
import requests
import sys

DEBUG_PORT = 9222
DEBUG_HOST = "127.0.0.1"

def open_url_in_debug_chrome(url: str) -> bool:
    """Open URL in a new tab in the debugging Chrome instance"""
    try:
        # Use Chrome DevTools Protocol to open new tab
        # PUT method for /json/new with URL parameter
        response = requests.put(
            f"http://{DEBUG_HOST}:{DEBUG_PORT}/json/new?{url}",
            timeout=3
        )
        
        if response.status_code == 200:
            print(f"[+] Opened in debugging Chrome: {url}")
            return True
        else:
            print(f"[-] Failed to open URL (status: {response.status_code})")
            return False
            
    except requests.Timeout:
        print("[-] Connection timeout - is Chrome running with --remote-debugging-port=9222?")
        return False
    except requests.RequestException as e:
        print(f"[-] Connection failed - is Chrome running with debugging enabled?")
        return False
    except Exception:
        print("[-] Unexpected error")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python open_in_debug_chrome.py <URL>")
        print("Example: python open_in_debug_chrome.py http://localhost:8000")
        sys.exit(1)
    
    url = sys.argv[1]
    success = open_url_in_debug_chrome(url)
    sys.exit(0 if success else 1)


#!/usr/bin/env python3
"""
One-Click Bold Opening: Inject Cat Into Presentation
BugCon 2025

Dead simple script for the opening moment.
Just run it, cat appears, audience gasps.

Usage:
    python inject_cat_opening.py
    
    (That's it!)
"""

import json
import requests
import websocket
import logging
import sys

# Configure secure logging
logging.basicConfig(level=logging.WARNING, format='%(message)s')

DEBUG_PORT = 9222
DEBUG_HOST = "127.0.0.1"  # Localhost only - secure default
WS_TIMEOUT = 5  # WebSocket timeout in seconds

def validate_port(port: int) -> bool:
    """Validate port number is in valid range"""
    return isinstance(port, int) and 1 <= port <= 65535

def validate_ws_url(url: str) -> bool:
    """Validate WebSocket URL is localhost only"""
    if not url or not isinstance(url, str):
        return False
    # Must be localhost/127.0.0.1 only
    return url.startswith('ws://127.0.0.1:') or url.startswith('ws://localhost:')

def inject_cat():
    """One function, one purpose: INJECT THAT CAT! 🐱"""
    
    # Input validation
    if not validate_port(DEBUG_PORT):
        print("[-] Invalid port configuration")
        return False
    
    ws = None
    try:
        print("[*] Finding presentation tab...")
        
        # Get presentation tab with timeout
        response = requests.get(
            f"http://{DEBUG_HOST}:{DEBUG_PORT}/json/list", 
            timeout=3
        )
        
        if response.status_code != 200:
            print("[-] Failed to connect to Chrome")
            return False
        
        # Validate JSON response
        try:
            targets = response.json()
            if not isinstance(targets, list):
                print("[-] Unexpected response format")
                return False
        except (json.JSONDecodeError, ValueError):
            print("[-] Invalid response from Chrome")
            return False
        
        # Find first page (should be your presentation)
        target = None
        for t in targets:
            if not isinstance(t, dict):
                continue
            if t.get('type') == 'page':
                target = t
                break
        
        if not target:
            print("[-] No presentation found!")
            return False
        
        print(f"[+] Found: {target.get('title', 'Unknown')}")
        
        # Validate and connect to WebSocket
        ws_url = target.get('webSocketDebuggerUrl')
        if not ws_url or not validate_ws_url(ws_url):
            print("[-] Invalid WebSocket URL")
            return False
        
        ws = websocket.create_connection(ws_url, timeout=WS_TIMEOUT)
        ws.settimeout(1)  # Short timeout for draining events
        
        # Enable Runtime
        ws.send(json.dumps({"id": 1, "method": "Runtime.enable", "params": {}}))
        # Drain any event messages until we get our command response
        for _ in range(10):  # Max 10 messages to avoid infinite loop
            try:
                msg = ws.recv()
                data = json.loads(msg)
                if 'id' in data and data['id'] == 1:
                    break  # Got our response
            except (websocket.WebSocketTimeoutException, json.JSONDecodeError):
                break
        
        # Reset timeout for actual command
        ws.settimeout(WS_TIMEOUT)
    
        # INJECT THE CAT!
        cat_injection = """
        (function() {
            const cat = document.createElement('img');
            cat.src = 'https://media.giphy.com/media/JIX9t2j0ZTN9S/giphy.gif';
            cat.style.position = 'fixed';
            cat.style.bottom = '20px';
            cat.style.right = '20px';
            cat.style.width = '250px';
            cat.style.height = '250px';
            cat.style.zIndex = '9999';
            cat.style.borderRadius = '15px';
            cat.style.boxShadow = '0 0 40px rgba(0, 255, 65, 1)';
            cat.style.border = '4px solid #00ff41';
            cat.style.opacity = '0';
            cat.style.transform = 'scale(0) rotate(-360deg)';
            cat.style.transition = 'all 0.8s cubic-bezier(0.68, -0.55, 0.265, 1.55)';
            cat.id = 'injected-cat';
            
            document.body.appendChild(cat);
            
            setTimeout(() => {
                cat.style.opacity = '1';
                cat.style.transform = 'scale(1) rotate(0deg)';
            }, 100);
            
            return '🐱 CAT DEPLOYED!';
        })();
        """
        
        print("[*] Injecting typing cat...")
        
        ws.send(json.dumps({
            "id": 2,
            "method": "Runtime.evaluate",
            "params": {
                "expression": cat_injection,
                "returnByValue": True
            }
        }))
        
        # Receive response, filtering out events
        result = None
        for _ in range(10):  # Max 10 messages
            try:
                response_str = ws.recv()
                data = json.loads(response_str)
                
                # We want the response with our command ID
                if 'id' in data and data['id'] == 2:
                    result = data
                    break
            except websocket.WebSocketTimeoutException:
                print("[-] Response timeout")
                return False
            except (json.JSONDecodeError, ValueError):
                print("[-] Invalid JSON from Chrome")
                logging.debug("JSON decode failed")
                continue  # Try next message
        
        if not result or not isinstance(result, dict):
            print("[-] No valid response received")
            return False
        
        # Check for successful injection
        if result.get('result', {}).get('result', {}).get('value'):
            print("\n" + "=" * 50)
            print("CAT SUCCESSFULLY INJECTED!")
            print("=" * 50)
            print('"I just injected that cat into my presentation."')
            print('"From outside the browser."')
            print('"Using the attack I\'m about to explain."')
            print('"Zero authentication."')
            print("")
            print('"Now imagine I\'m an attacker... and this isn\'t a cat."')
            print("=" * 50)
            return True
        else:
            print("[-] Injection failed!")
            # Debug: Show what we got back
            if result.get('error'):
                logging.warning(f"CDP Error: {result.get('error')}")
            if result.get('exceptionDetails'):
                logging.warning(f"JS Exception occurred")
            logging.debug(f"Response: {result}")
            return False
    
    except requests.Timeout:
        print("[-] Connection timeout")
        logging.debug("HTTP request timed out")
        return False
    except requests.RequestException:
        print("[-] Connection failed")
        logging.debug("HTTP request failed")
        return False
    except websocket.WebSocketTimeoutException:
        print("[-] WebSocket timeout")
        logging.debug("WebSocket operation timed out")
        return False
    except websocket.WebSocketException:
        print("[-] WebSocket error")
        logging.debug("WebSocket operation failed")
        return False
    except Exception:
        print("[-] Unexpected error occurred")
        logging.debug("Unexpected error in inject_cat")
        return False
    finally:
        # Ensure WebSocket cleanup
        if ws:
            try:
                ws.close()
            except Exception:
                pass  # Ignore cleanup errors


if __name__ == "__main__":
    try:
        success = inject_cat()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n[!] Interrupted by user")
        sys.exit(130)
    except Exception:
        # Generic error - no stack trace to user
        print("[-] Error occurred")
        print("\nMake sure:")
        print("  1. Chrome is running with --remote-debugging-port=9222")
        print("  2. Your presentation is open in that Chrome window")
        logging.debug("Fatal error in main", exc_info=True)
        sys.exit(1)

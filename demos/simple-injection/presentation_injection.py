#!/usr/bin/env python3
"""
CDP Meta-Demo: Inject Content Into Your Own Presentation
BugCon 2025 - Bold Opening Script

This script demonstrates CDP's power by injecting a cat GIF into the 
presentation slides WHILE YOU'RE PRESENTING. Meta-level demonstration
of arbitrary JavaScript execution via Chrome Remote Debugging.

Usage:
    1. Start presentation in Chrome with debugging
    2. Navigate to title slide
    3. Run: python presentation_injection.py
    4. Watch the magic happen!

Author: Your Name
Conference: BugCon 2025
"""

import json
import requests
import websocket
import time
import sys
import logging
import re
from typing import Optional, Dict

# Terminal colors
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    HAS_COLOR = True
except ImportError:
    # Fallback if colorama not installed
    class Fore:
        RED = YELLOW = GREEN = CYAN = BLUE = MAGENTA = WHITE = ""
    class Style:
        BRIGHT = RESET_ALL = ""
    HAS_COLOR = False

# Configure secure logging
logging.basicConfig(level=logging.WARNING, format='%(message)s')

DEBUG_PORT = 9222
DEBUG_HOST = "127.0.0.1"  # Localhost only - secure default
WS_TIMEOUT = 5  # WebSocket timeout in seconds
MAX_JS_LENGTH = 50000  # Max length for custom JavaScript input


def validate_port(port: int) -> bool:
    """Validate port number is in valid range"""
    return isinstance(port, int) and 1 <= port <= 65535


def validate_ws_url(url: str) -> bool:
    """Validate WebSocket URL is localhost only"""
    if not url or not isinstance(url, str):
        return False
    # Must be localhost/127.0.0.1 only
    return url.startswith('ws://127.0.0.1:') or url.startswith('ws://localhost:')


def validate_method_name(method: str) -> bool:
    """Validate CDP method name format"""
    if not method or not isinstance(method, str):
        return False
    # CDP methods are like "Runtime.enable" - alphanumeric with dots
    return bool(re.match(r'^[A-Za-z][A-Za-z0-9.]*$', method))


def escape_js_string(text: str) -> str:
    """Escape user input for safe inclusion in JavaScript strings"""
    if not isinstance(text, str):
        return ""
    # Escape quotes, backslashes, and control characters
    replacements = {
        '\\': '\\\\',
        "'": "\\'",
        '"': '\\"',
        '\n': '\\n',
        '\r': '\\r',
        '\t': '\\t',
        '\b': '\\b',
        '\f': '\\f'
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    # Remove any remaining control characters
    text = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', text)
    return text


class PresentationInjector:
    """Inject content into presentation slides via CDP"""
    
    def __init__(self, host: str = DEBUG_HOST, port: int = DEBUG_PORT):
        # Validate inputs
        if not validate_port(port):
            raise ValueError(f"Invalid port number: {port}")
        if host not in ("127.0.0.1", "localhost"):
            raise ValueError(f"Only localhost connections allowed, got: {host}")
        
        self.host = host
        self.port = port
        self.base_url = f"http://{host}:{port}"
        self.ws = None
        self.message_id = 0
        
    def find_presentation_tab(self) -> Optional[Dict]:
        """Find the tab with the presentation (index.html)"""
        try:
            response = requests.get(f"{self.base_url}/json/list", timeout=3)
            
            if response.status_code != 200:
                print(f"{Fore.RED}[-] Failed to connect to Chrome")
                logging.debug(f"HTTP status: {response.status_code}")
                return None
            
            # Validate JSON response
            try:
                targets = response.json()
                if not isinstance(targets, list):
                    print(f"{Fore.RED}[-] Unexpected response format")
                    return None
            except (json.JSONDecodeError, ValueError):
                print(f"{Fore.RED}[-] Invalid response from Chrome")
                return None
            
            # Look for presentation tab
            for target in targets:
                if not isinstance(target, dict):
                    continue
                if target.get('type') == 'page':
                    url = target.get('url', '')
                    title = target.get('title', '')
                    
                    # Match presentation tab
                    if ('index.html' in url or 
                        'Abusing Chrome' in title or
                        'BugCon' in title):
                        print(f"{Fore.GREEN}[+] Found presentation tab: {title}")
                        return target
            
            # Fallback: Return first page if no match
            for target in targets:
                if not isinstance(target, dict):
                    continue
                if target.get('type') == 'page':
                    print(f"{Fore.GREEN}[+] Using first available tab: {target.get('title')}")
                    return target
        
        except requests.Timeout:
            print(f"{Fore.RED}[-] Connection timeout")
            logging.debug("HTTP request timed out")
        except requests.RequestException:
            print(f"{Fore.RED}[-] Connection failed")
            logging.debug("HTTP request failed")
        except Exception:
            print(f"{Fore.RED}[-] Error finding presentation")
            logging.debug("Unexpected error in find_presentation_tab")
        
        return None
    
    def connect(self, target: Dict) -> bool:
        """Connect to the presentation tab via WebSocket"""
        ws_url = target.get('webSocketDebuggerUrl')
        if not ws_url:
            print(f"{Fore.RED}[-] No WebSocket URL available")
            return False
        
        # Validate WebSocket URL
        if not validate_ws_url(ws_url):
            print(f"{Fore.RED}[-] Invalid WebSocket URL")
            logging.debug(f"URL validation failed")
            return False
        
        try:
            print(f"{Fore.CYAN}[*] Connecting to WebSocket...")
            self.ws = websocket.create_connection(ws_url, timeout=WS_TIMEOUT)
            print(f"{Fore.GREEN}[+] Connected!")
            return True
        except websocket.WebSocketTimeoutException:
            print(f"{Fore.RED}[-] Connection timeout")
            logging.debug("WebSocket connection timed out")
            return False
        except websocket.WebSocketException:
            print(f"{Fore.RED}[-] WebSocket error")
            logging.debug("WebSocket connection failed")
            return False
        except Exception:
            print(f"{Fore.RED}[-] Connection failed")
            logging.debug("Unexpected error in connect")
            return False
    
    def send_command(self, method: str, params: Optional[Dict] = None) -> Optional[Dict]:
        """Send CDP command and get response with security validation"""
        if not self.ws:
            return None
        
        # Validate method name
        if not validate_method_name(method):
            print(f"{Fore.RED}[-] Invalid method name")
            logging.debug(f"Method validation failed")
            return None
        
        # Validate params
        if params is not None and not isinstance(params, dict):
            print(f"{Fore.RED}[-] Invalid parameters")
            return None
        
        self.message_id += 1
        command = {
            "id": self.message_id,
            "method": method,
            "params": params or {}
        }
        
        try:
            self.ws.send(json.dumps(command))
            response_str = self.ws.recv()
            
            # Validate JSON response
            try:
                response = json.loads(response_str)
                if not isinstance(response, dict):
                    print(f"{Fore.RED}[-] Unexpected response format")
                    return None
                return response
            except (json.JSONDecodeError, ValueError):
                print(f"{Fore.RED}[-] Invalid response format")
                logging.debug("JSON decode failed")
                return None
                
        except websocket.WebSocketTimeoutException:
            print(f"{Fore.RED}[-] Command timeout")
            logging.debug(f"Timeout for method: {method}")
            return None
        except websocket.WebSocketException:
            print(f"{Fore.RED}[-] WebSocket error")
            logging.debug(f"WebSocket error for method: {method}")
            return None
        except Exception:
            print(f"{Fore.RED}[-] Command failed")
            logging.debug(f"Unexpected error for method: {method}")
            return None
    
    def inject_dancing_cat(self) -> bool:
        """Inject an animated dancing cat GIF"""
        print(f"\n{Fore.CYAN}[*] Injecting dancing cat...")
        
        js_code = """
        (function() {
            // Create cat image element
            const cat = document.createElement('img');
            cat.src = 'https://media.giphy.com/media/JIX9t2j0ZTN9S/giphy.gif'; // Dancing cat
            cat.style.position = 'fixed';
            cat.style.bottom = '20px';
            cat.style.right = '20px';
            cat.style.width = '200px';
            cat.style.height = '200px';
            cat.style.zIndex = '9999';
            cat.style.borderRadius = '10px';
            cat.style.boxShadow = '0 0 30px rgba(0, 255, 65, 0.8)';
            cat.style.border = '3px solid #00ff41';
            cat.style.opacity = '0';
            cat.style.transform = 'scale(0) rotate(-180deg)';
            cat.style.transition = 'all 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55)';
            cat.id = 'injected-cat';
            
            // Add to page
            document.body.appendChild(cat);
            
            // Animate in
            setTimeout(() => {
                cat.style.opacity = '1';
                cat.style.transform = 'scale(1) rotate(0deg)';
            }, 100);
            
            return 'Cat injected successfully! 🐱';
        })();
        """
        
        response = self.send_command("Runtime.evaluate", {
            "expression": js_code,
            "returnByValue": True
        })
        
        if response:
            # Check for errors
            if "error" in response:
                print(f"{Fore.RED}[-] Injection failed: {response['error'].get('message', 'Unknown error')}")
                return False
            
            # Success - extract result if available
            result = response.get("result", {}).get("result", {})
            message = result.get('value', 'Injection complete!')
            print(f"{Fore.GREEN}[+] {message}")
            return True
        else:
            print(f"{Fore.RED}[-] Injection failed - no response")
            return False
    
    def inject_matrix_rain(self) -> bool:
        """Inject Matrix-style falling code effect (alternative demo)"""
        print(f"\n{Fore.CYAN}[*] Injecting Matrix rain effect...")
        
        js_code = """
        (function() {
            // Create canvas for Matrix effect
            const canvas = document.createElement('canvas');
            canvas.id = 'matrix-rain';
            canvas.style.position = 'fixed';
            canvas.style.top = '0';
            canvas.style.left = '0';
            canvas.style.width = '100%';
            canvas.style.height = '100%';
            canvas.style.zIndex = '9998';
            canvas.style.pointerEvents = 'none';
            canvas.style.opacity = '0.3';
            
            document.body.appendChild(canvas);
            
            const ctx = canvas.getContext('2d');
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
            
            const chars = 'CDP1010110CHROME01DEBUG01PORT922201';
            const fontSize = 14;
            const columns = canvas.width / fontSize;
            const drops = Array(Math.floor(columns)).fill(1);
            
            function draw() {
                ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                
                ctx.fillStyle = '#00ff41';
                ctx.font = fontSize + 'px monospace';
                
                for (let i = 0; i < drops.length; i++) {
                    const text = chars[Math.floor(Math.random() * chars.length)];
                    ctx.fillText(text, i * fontSize, drops[i] * fontSize);
                    
                    if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
                        drops[i] = 0;
                    }
                    drops[i]++;
                }
            }
            
            const interval = setInterval(draw, 33);
            
            // Auto-remove after 5 seconds
            setTimeout(() => {
                clearInterval(interval);
                canvas.remove();
            }, 5000);
            
            return 'Matrix effect activated! 💚';
        })();
        """
        
        response = self.send_command("Runtime.evaluate", {
            "expression": js_code,
            "returnByValue": True
        })
        
        if response:
            # Check for errors
            if "error" in response:
                print(f"{Fore.RED}[-] Injection failed: {response['error'].get('message', 'Unknown error')}")
                return False
            
            # Success - extract result if available
            result = response.get("result", {}).get("result", {})
            message = result.get('value', 'Effect complete!')
            print(f"{Fore.GREEN}[+] {message}")
            return True
        else:
            print(f"{Fore.RED}[-] Injection failed - no response")
            return False
    
    def inject_text_overlay(self, text: str = "🚨 INJECTED VIA CDP 🚨") -> bool:
        """Inject a text overlay banner"""
        # Validate and sanitize input
        if not isinstance(text, str):
            print(f"{Fore.RED}[-] Invalid text input")
            return False
        
        if len(text) > 200:
            print(f"{Fore.RED}[-] Text too long (max 200 chars)")
            return False
        
        # Escape user input to prevent code injection
        safe_text = escape_js_string(text)
        
        print(f"\n{Fore.CYAN}[*] Injecting text overlay...")
        
        js_code = f"""
        (function() {{
            const banner = document.createElement('div');
            banner.textContent = '{safe_text}';
            banner.style.position = 'fixed';
            banner.style.top = '50%';
            banner.style.left = '50%';
            banner.style.transform = 'translate(-50%, -50%) scale(0)';
            banner.style.fontSize = '48px';
            banner.style.fontWeight = 'bold';
            banner.style.color = '#ff4444';
            banner.style.textShadow = '0 0 20px rgba(255, 68, 68, 0.8)';
            banner.style.zIndex = '10000';
            banner.style.padding = '20px 40px';
            banner.style.background = 'rgba(0, 0, 0, 0.9)';
            banner.style.border = '3px solid #ff4444';
            banner.style.borderRadius = '10px';
            banner.style.transition = 'all 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55)';
            banner.id = 'injected-banner';
            
            document.body.appendChild(banner);
            
            setTimeout(() => {{
                banner.style.transform = 'translate(-50%, -50%) scale(1)';
            }}, 100);
            
            setTimeout(() => {{
                banner.style.transform = 'translate(-50%, -50%) scale(0)';
                setTimeout(() => banner.remove(), 500);
            }}, 3000);
            
            return 'Banner injected!';
        }})();
        """
        
        response = self.send_command("Runtime.evaluate", {
            "expression": js_code,
            "returnByValue": True
        })
        
        if response:
            # Check for errors
            if "error" in response:
                print(f"{Fore.RED}[-] Injection failed: {response['error'].get('message', 'Unknown error')}")
                return False
            
            # Success
            print(f"{Fore.GREEN}[+] Text overlay complete!")
            return True
        else:
            print(f"{Fore.RED}[-] Injection failed - no response")
            return False
    
    def remove_injected_content(self) -> bool:
        """Clean up injected elements"""
        print(f"\n{Fore.CYAN}[*] Removing injected content...")
        
        js_code = """
        (function() {
            const injected = document.querySelectorAll('[id^="injected-"]');
            injected.forEach(el => el.remove());
            return `Removed ${injected.length} elements`;
        })();
        """
        
        response = self.send_command("Runtime.evaluate", {
            "expression": js_code,
            "returnByValue": True
        })
        
        if response:
            # Check for errors
            if "error" in response:
                print(f"{Fore.RED}[-] Cleanup failed: {response['error'].get('message', 'Unknown error')}")
                return False
            
            # Success - show how many elements were removed
            result = response.get("result", {}).get("result", {})
            message = result.get('value', 'Cleanup complete')
            print(f"{Fore.GREEN}[+] {message}")
            return True
        else:
            print(f"{Fore.RED}[-] Cleanup failed - no response")
            return False
    
    def disconnect(self):
        """Close WebSocket connection"""
        if self.ws:
            try:
                self.ws.close()
                print(f"\n{Fore.GREEN}[+] Disconnected")
            except Exception:
                # Ignore errors during cleanup
                pass


def main():
    """Main demonstration flow"""
    print(f"{Fore.CYAN}{Style.BRIGHT}{'=' * 70}")
    print(f"{Fore.CYAN}{Style.BRIGHT}CDP Meta-Demo: Inject Content Into Presentation")
    print(f"{Fore.CYAN}{Style.BRIGHT}BugCon 2025 - Bold Opening")
    print(f"{Fore.CYAN}{Style.BRIGHT}{'=' * 70}")
    
    try:
        injector = PresentationInjector()
    except ValueError as e:
        print(f"{Fore.RED}[-] Configuration error: {e}")
        sys.exit(1)
    
    # Find and connect to presentation
    target = injector.find_presentation_tab()
    if not target:
        print(f"\n{Fore.RED}[-] Could not find presentation tab!")
        print(f"\n{Fore.YELLOW}Make sure:")
        print(f"{Fore.YELLOW}  1. Chrome is running with --remote-debugging-port=9222")
        print(f"{Fore.YELLOW}  2. Your presentation (index.html) is open")
        sys.exit(1)
    
    if not injector.connect(target):
        sys.exit(1)
    
    try:
        # Enable Runtime domain
        injector.send_command("Runtime.enable")
        
        # Show menu
        print(f"\n{Fore.CYAN}{Style.BRIGHT}{'=' * 70}")
        print(f"{Fore.CYAN}{Style.BRIGHT}Choose your injection:")
        print(f"{Fore.CYAN}{Style.BRIGHT}{'=' * 70}")
        print(f"{Fore.WHITE}1. Dancing Cat GIF")
        print(f"{Fore.WHITE}2. Matrix Rain Effect")
        print(f"{Fore.WHITE}3. Text Banner ('INJECTED VIA CDP')")
        print(f"{Fore.WHITE}4. Custom JavaScript (advanced)")
        print(f"{Fore.WHITE}5. Remove injected content")
        print(f"{Fore.WHITE}0. Exit")
        
        while True:
            choice = input("\nSelect option (0-5): ").strip()
            
            if choice == '1':
                injector.inject_dancing_cat()
            
            elif choice == '2':
                injector.inject_matrix_rain()
            
            elif choice == '3':
                custom_text = input("Enter text to display (or press Enter for default): ").strip()
                if custom_text:
                    injector.inject_text_overlay(custom_text)
                else:
                    injector.inject_text_overlay()
            
            elif choice == '4':
                print(f"\n{Fore.YELLOW}[!] WARNING: Custom JavaScript execution")
                print(f"{Fore.YELLOW}[!] This will execute arbitrary code in the browser")
                confirm = input(f"{Fore.YELLOW}Are you sure? (yes/no): ").strip().lower()
                
                if confirm != 'yes':
                    print(f"{Fore.CYAN}[*] Cancelled")
                    continue
                
                print(f"\n{Fore.CYAN}Enter JavaScript (end with empty line):")
                lines = []
                while True:
                    try:
                        line = input()
                        if not line:
                            break
                        lines.append(line)
                    except EOFError:
                        break
                
                js_code = '\n'.join(lines)
                
                # Basic validation
                if not js_code.strip():
                    print(f"{Fore.RED}[-] Empty input")
                    continue
                
                if len(js_code) > MAX_JS_LENGTH:
                    print(f"{Fore.RED}[-] Code too long (max {MAX_JS_LENGTH} chars)")
                    continue
                
                # Check for obviously dangerous patterns
                dangerous_patterns = [
                    r'eval\s*\(',
                    r'Function\s*\(',
                    r'<script',
                    r'javascript:',
                ]
                
                is_dangerous = False
                for pattern in dangerous_patterns:
                    if re.search(pattern, js_code, re.IGNORECASE):
                        print(f"{Fore.YELLOW}[!] WARNING: Detected potentially dangerous pattern: {pattern}")
                        confirm2 = input(f"{Fore.YELLOW}Continue anyway? (yes/no): ").strip().lower()
                        if confirm2 != 'yes':
                            print(f"{Fore.CYAN}[*] Cancelled")
                            is_dangerous = True
                            break
                
                if is_dangerous:
                    continue
                
                response = injector.send_command("Runtime.evaluate", {
                    "expression": js_code,
                    "returnByValue": True
                })
                
                if response:
                    # Check for errors
                    if "error" in response:
                        print(f"{Fore.RED}[-] Command failed: {response['error'].get('message', 'Unknown error')}")
                        continue
                    
                    # Check for JavaScript exceptions
                    result = response.get("result", {})
                    if "exceptionDetails" in result:
                        exception = result.get("exceptionDetails", {})
                        error_msg = exception.get("exception", {}).get("description", "JavaScript error")
                        print(f"{Fore.RED}[-] JavaScript error: {error_msg}")
                    elif "result" in result:
                        value = result.get('result', {}).get('value', 'Success')
                        print(f"{Fore.GREEN}[+] Result: {value}")
                    else:
                        print(f"{Fore.GREEN}[+] Command executed")
                else:
                    print(f"{Fore.RED}[-] Command failed - no response")
            
            elif choice == '5':
                injector.remove_injected_content()
            
            elif choice == '0':
                break
            
            else:
                print(f"{Fore.RED}[-] Invalid choice!")
    
    finally:
        # Ensure cleanup
        injector.disconnect()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}[!] Interrupted by user")
        sys.exit(130)
    except Exception:
        # Generic error - no stack trace to user
        print(f"\n{Fore.RED}[-] Unexpected error occurred")
        print(f"\n{Fore.YELLOW}Make sure:")
        print(f"{Fore.YELLOW}  1. Chrome is running with --remote-debugging-port=9222")
        print(f"{Fore.YELLOW}  2. Your presentation (index.html) is open")
        logging.debug("Fatal error in main", exc_info=True)
        sys.exit(1)

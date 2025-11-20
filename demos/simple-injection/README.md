# Simple Injection Demo - BugCon 2025

**Dramatic opening for your presentation: Inject a dancing cat into your own slides!**

## What This Does

This demo injects content (a dancing cat GIF) into your live presentation slides using Chrome DevTools Protocol (CDP). It's designed for the bold opening moment where you demonstrate the attack in real-time.

---

## 🚀 Quick Start (Recommended)

### Option 1: Automated Setup

**Windows:**
```cmd
start_demo.bat
```

**Linux/macOS:**
```bash
chmod +x start_demo.sh cleanup_demo.sh  # First time only
./start_demo.sh
```

This will:
- Start Chrome with debugging on port 9222
- Start the presentation server on port 8000
- Open the presentation in Chrome

**Run the injection:**
```bash
# Windows
python inject_cat_opening.py

# Linux/macOS
python3 inject_cat_opening.py
```

**Watch the magic happen!** 🎉

**Clean up when done:**
```bash
# Windows
cleanup_demo.bat

# Linux/macOS
./cleanup_demo.sh
```

---

## 📋 Manual Setup (Cross-Platform)

### Step 1: Start Chrome with Debugging

**Windows:**
```cmd
cd ..\chrome-debugging-exploit\red-team
start_chrome_debug.bat
```

**Linux/Mac:**
```bash
cd ../chrome-debugging-exploit/red-team
./start_chrome_debug.sh
```

### Step 2: Start Presentation Server

```bash
cd ../../slides
python serve_slides.py
```

Leave this running in a separate terminal.

### Step 3: Open Presentation

Open **Chrome** (the debugging-enabled instance) and navigate to:
```
http://localhost:8000
```

**IMPORTANT:** Make sure it opens in the debugging-enabled Chrome, not your default browser!

### Step 4: Run the Injection

```bash
cd ../demos/simple-injection
python inject_cat_opening.py
```

---

## 🎭 Using the Advanced Injector

For more control and multiple injection options:

```bash
python presentation_injection.py
```

This provides a menu with:
1. **Dancing Cat GIF** - The classic opening
2. **Matrix Rain Effect** - Dramatic code rain overlay
3. **Text Banner** - Custom text overlay
4. **Custom JavaScript** - Advanced: Execute arbitrary JS
5. **Remove Injected Content** - Clean up

---

## 🛡️ Security Features

Both scripts have been hardened with:

✅ **Input Validation** - All inputs validated before use  
✅ **Localhost-Only** - Binds to 127.0.0.1 only  
✅ **Timeouts** - Network operations have 5-second timeouts  
✅ **No Stack Traces** - Generic errors to users, detailed to logs  
✅ **Resource Cleanup** - Proper WebSocket/connection cleanup  
✅ **XSS Prevention** - User input is escaped in `inject_text_overlay()`  

---

## 🐛 Troubleshooting

### "No presentation found!"

**Problem:** Chrome isn't running with debugging enabled.

**Solution:** 
- Make sure you ran `start_demo.bat` or `start_chrome_debug.bat`
- Verify: Visit http://localhost:9222/json in any browser
- You should see a JSON list of tabs

### "Connection failed"

**Problem:** Presentation not open in debugging Chrome.

**Solution:**
- Make sure http://localhost:8000 is open in the **debugging-enabled Chrome**
- Not Brave, not Edge, not regular Chrome - the one with `--remote-debugging-port=9222`

### Found "GitHub" instead of presentation

**Problem:** Script connected to wrong tab.

**Solution:**
- Close unnecessary tabs in the debugging Chrome
- Make sure the presentation tab is the first/only page open
- Refresh the presentation

### Injection runs but nothing happens

**Problem:** JavaScript error or timing issue.

**Solution:**
- Open Chrome DevTools (F12) on the presentation tab
- Check Console for errors
- Try again - GIF might still be loading

---

## 📦 Requirements

```bash
pip install -r requirements.txt
```

Dependencies:
- `websocket-client==1.6.4`
- `requests==2.31.0`

---

## 🎯 Files

- `inject_cat_opening.py` - Simple one-click cat injection
- `presentation_injection.py` - Advanced multi-option injector
- `start_demo.bat` - Automated Windows setup script
- `cleanup_demo.bat` - Clean up processes
- `requirements.txt` - Python dependencies

---

## ⚠️ Disclaimer

This is a security demonstration tool for educational purposes. Only use on systems you own or have explicit permission to test.

---

**Now go blow some minds at BugCon 2025!** 🚀🐱



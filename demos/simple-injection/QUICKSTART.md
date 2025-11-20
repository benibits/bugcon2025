# 🚀 Quick Start - Cat Injection Demo

## ✅ TESTED & WORKING!

### One-Click Setup

**Windows:**
```cmd
cd demos\simple-injection
start_demo.bat
```

**Linux/macOS:**
```bash
cd demos/simple-injection
chmod +x start_demo.sh cleanup_demo.sh  # First time only
./start_demo.sh
```

Wait for all services to start (~10 seconds), then:

### Run the Injection

1. **Navigate to any slide** using arrow keys
2. **Run the injection:**
   
   **Windows:**
   ```cmd
   python inject_cat_opening.py
   ```
   
   **Linux/macOS:**
   ```bash
   python3 inject_cat_opening.py
   ```
   
3. **Watch the cat appear!** 🐱

### Clean Up

**Windows:**
```cmd
cleanup_demo.bat
```

**Linux/macOS:**
```bash
./cleanup_demo.sh
```

---

## Manual Setup (Linux/Mac)

```bash
# Terminal 1: Start Chrome with debugging
cd ../chrome-debugging-exploit/red-team
./start_chrome_debug.sh

# Terminal 2: Start slide server
cd ../../slides
python3 serve_slides.py

# Terminal 3: Open presentation in debug Chrome
cd ../demos/simple-injection
python3 open_in_debug_chrome.py http://localhost:8000

# Navigate to slide 2, then inject
python3 inject_cat_opening.py
```

---

## Troubleshooting

**"No presentation found!"**
- Make sure presentation opened in debug Chrome (check http://localhost:9222/json)

**"Connection failed"**

Windows:
```cmd
netstat -ano | findstr :9222
netstat -ano | findstr :8000
```

Linux/macOS:
```bash
lsof -i :9222,8000
# or
netstat -an | grep -E ':(9222|8000)'
```

---

**Full documentation:** See [README.md](README.md)


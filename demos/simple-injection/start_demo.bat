@echo off
REM ============================================================================
REM BugCon 2025 - Simple Injection Demo Startup Script
REM ============================================================================
REM This script:
REM   1. Starts Chrome with remote debugging on port 9222
REM   2. Waits for Chrome to be ready
REM   3. Starts the presentation server on port 8000
REM   4. Opens the presentation in the debugging-enabled Chrome
REM ============================================================================

echo.
echo ========================================
echo  BugCon 2025 - Injection Demo Startup
echo ========================================
echo.

REM Change to script directory
cd /d "%~dp0"

REM Create temp directory if it doesn't exist
if not exist "C:\temp\chrome-debug" mkdir "C:\temp\chrome-debug"

echo [1/4] Starting Chrome with debugging on port 9222...
echo.

REM Start Chrome with debugging
if exist "C:\Program Files\Google\Chrome\Application\chrome.exe" (
    start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\temp\chrome-debug" --remote-allow-origins=*
) else if exist "%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe" (
    start "" "%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\temp\chrome-debug" --remote-allow-origins=*
) else (
    echo ERROR: Chrome not found in standard installation paths!
    echo Please install Chrome or update the path in this script.
    pause
    exit /b 1
)

echo [2/4] Waiting for Chrome to initialize (5 seconds)...
timeout /t 5 /nobreak >nul

REM Verify Chrome is listening
netstat -ano | findstr :9222 >nul
if errorlevel 1 (
    echo WARNING: Chrome debugging port not detected!
    echo Continuing anyway, but injection may fail...
) else (
    echo SUCCESS: Chrome is listening on port 9222
)

echo.
echo [3/4] Starting presentation server on port 8000...
cd ..\..\slides
start /B python serve_slides.py --no-browser
timeout /t 2 /nobreak >nul

REM Verify server is running
netstat -ano | findstr :8000 >nul
if errorlevel 1 (
    echo ERROR: Presentation server failed to start!
    pause
    exit /b 1
) else (
    echo SUCCESS: Presentation server is running
)

echo.
echo [4/4] Opening presentation in debugging Chrome...
REM Wait a bit longer for slide server to be fully ready
timeout /t 3 /nobreak >nul

REM Open presentation DIRECTLY in debugging Chrome using CDP API
REM This ensures it opens in the debug Chrome, not the default browser (Brave)
cd /d "%~dp0"
python open_in_debug_chrome.py http://localhost:8000/slides/

if errorlevel 1 (
    echo WARNING: Failed to open in debug Chrome
    echo You can manually open: http://localhost:8000/slides/ in the debug Chrome window
)

echo.
echo ========================================
echo  DEMO ENVIRONMENT READY!
echo ========================================
echo.
echo Chrome Debug Port: http://localhost:9222/json
echo Presentation:      http://localhost:8000
echo.
echo Navigate to slide 2 (Quick Poll slide), then run:
echo   python inject_cat_opening.py
echo.
echo Press any key to exit this window...
pause >nul



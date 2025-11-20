@echo off
REM ============================================================================
REM BugCon 2025 - Clean Up Demo Processes
REM ============================================================================

echo.
echo Cleaning up demo processes...
echo.

REM Kill presentation server (Python on port 8000)
echo Stopping presentation server...
for /f "tokens=5" %%a in ('netstat -ano 2^>nul ^| findstr :8000 ^| findstr LISTENING') do (
    taskkill /F /PID %%a >nul 2>&1
)

REM Kill Chrome processes with debug profile
echo Stopping debugging Chrome instances...
REM Kill Chrome instances using the debug user data directory
wmic process where "name='chrome.exe' and commandline like '%%chrome-debug%%'" delete >nul 2>&1

echo.
echo Cleanup complete!
echo You can verify with: netstat -ano ^| findstr ":9222 :8000"
echo.
pause



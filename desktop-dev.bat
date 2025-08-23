@echo off
echo Starting StockCeramique Desktop Development...

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo Error: Node.js is not installed or not in PATH
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

REM Check if dependencies are installed
if not exist "node_modules" (
    echo Installing dependencies...
    npm install
)

REM Install desktop dependencies if needed
if not exist "node_modules\electron" (
    echo Installing desktop dependencies...
    npm install --save-dev electron@26.0.0 electron-builder@26.0.12 cross-env@7.0.3
)

REM Start the desktop server in background
echo Starting desktop server on port 3001...
start /b cmd /c "set DESKTOP_PORT=3001 && tsx server/index-desktop.ts"

REM Wait for server to start
echo Waiting for server to start...
timeout /t 3 /nobreak >nul

REM Start Electron
echo Starting Electron desktop app...
electron electron/main.js

echo Desktop app closed.
pause
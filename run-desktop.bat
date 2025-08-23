@echo off
echo Starting StockCeramique Desktop (Production Mode)...

REM Start the desktop server
echo Starting local server...
start /b cmd /c "set NODE_ENV=production && set DESKTOP_PORT=3001 && node dist-desktop/index-desktop.js"

REM Wait a moment for server to start
timeout /t 2 /nobreak >nul

REM Start Electron
echo Starting desktop application...
electron electron/main.js

echo Application closed.
pause
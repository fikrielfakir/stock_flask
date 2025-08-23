@echo off
echo Quick Desktop Test - StockCeramique

REM Check if tsx is available globally
tsx --version >nul 2>&1
if errorlevel 1 (
    echo Installing tsx globally...
    call npm install -g tsx
)

REM Check if electron is available locally
if not exist "node_modules\.bin\electron.cmd" (
    echo Installing Electron locally...
    call npm install --save-dev electron@26.0.0
)

REM Start desktop server in background
echo Starting desktop server on port 3001...
start /b cmd /c "set NODE_ENV=development && set DESKTOP_PORT=3001 && tsx server/index-desktop.ts"

REM Wait for server
echo Waiting for server to start...
timeout /t 3 /nobreak >nul

REM Test server
curl http://127.0.0.1:3001/api/health >nul 2>&1
if errorlevel 1 (
    echo Server failed to start. Check console for errors.
    pause
    exit /b 1
)

echo Server running! Starting Electron app...
set NODE_ENV=development
.\node_modules\.bin\electron.cmd electron/main.js

echo Desktop app closed.
pause
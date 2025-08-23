@echo off
echo Testing Desktop App in Development Mode...

REM Kill any existing processes
taskkill /f /im node.exe 2>nul
taskkill /f /im electron.exe 2>nul

REM Start the desktop server
echo Starting desktop server...
start /b cmd /c "set NODE_ENV=development && set DESKTOP_PORT=3001 && tsx server/index-desktop.ts"

REM Wait for server to start
echo Waiting for server to start...
timeout /t 5 /nobreak >nul

REM Test if server is running
curl -f http://127.0.0.1:3001/api/health
if errorlevel 1 (
    echo Server not responding. Check if tsx is installed: npm install -g tsx
    pause
    exit /b 1
)

echo Server is running! Starting Electron...

REM Install electron locally if needed
if not exist "node_modules\.bin\electron.cmd" (
    echo Installing electron locally...
    npm install --save-dev electron@26.0.0
)

REM Start Electron
set NODE_ENV=development
.\node_modules\.bin\electron.cmd electron/main.js

echo Desktop app closed.
pause
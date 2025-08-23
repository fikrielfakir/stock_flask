@echo off
echo Building StockCeramique Desktop - Fixed Version

REM Install dependencies if needed
if not exist "node_modules\electron" (
    echo Installing Electron...
    call npm install --save-dev electron@26.0.0 electron-builder@26.0.12
)

REM Build React frontend
echo Step 1: Building React frontend...
call npm run build
if errorlevel 1 (
    echo Frontend build failed
    pause
    exit /b 1
)

REM Build desktop server (without external packages flag that was causing issues)
echo Step 2: Building desktop server...
if not exist "dist-desktop" mkdir dist-desktop
call npx esbuild server/index-desktop.ts --platform=node --bundle --format=cjs --outdir=dist-desktop --target=node18
if errorlevel 1 (
    echo Desktop server build failed
    pause
    exit /b 1
)

REM Fix the CommonJS compatibility issue
echo Step 3: Fixing import.meta in CommonJS build...
powershell -Command "(Get-Content 'dist-desktop\index-desktop.js') -replace 'import\.meta\.url', '__filename' | Set-Content 'dist-desktop\index-desktop.js'"

REM Build the desktop app
echo Step 4: Building Electron app...
call npx electron-builder --config package-desktop.json --win --publish=never
if errorlevel 1 (
    echo Electron build failed
    pause
    exit /b 1
)

echo.
echo ======================================
echo SUCCESS! Desktop app built
echo ======================================
echo.
echo Installer location: dist-electron\StockCeramique Setup.exe
echo.
echo You can now:
echo 1. Install the app on this computer
echo 2. Share the installer with others
echo 3. The app runs completely offline
echo.
pause
@echo off
echo Fixing dependencies and building StockCeramique Desktop...

REM Step 1: Install Electron locally first
echo Step 1: Installing Electron locally...
call npm install --save-dev electron@26.0.0
if errorlevel 1 (
    echo Failed to install Electron
    pause
    exit /b 1
)

REM Step 2: Install electron-builder
echo Step 2: Installing electron-builder...
call npm install --save-dev electron-builder@26.0.12
if errorlevel 1 (
    echo Failed to install electron-builder
    pause
    exit /b 1
)

REM Step 3: Build frontend (if not already built)
echo Step 3: Building frontend...
if not exist "dist\index.html" (
    call npm run build
    if errorlevel 1 (
        echo Failed to build frontend
        pause
        exit /b 1
    )
) else (
    echo Frontend already built, skipping...
)

REM Step 4: Build desktop server
echo Step 4: Building desktop server...
if not exist "dist-desktop" mkdir dist-desktop
call npx esbuild server/index-desktop.ts --platform=node --bundle --format=esm --outdir=dist-desktop --external:better-sqlite3 --external:ws --external:express
if errorlevel 1 (
    echo Failed to build desktop server
    pause
    exit /b 1
)

REM Step 5: Use the correct package.json with all required fields
echo Step 5: Building with correct configuration...
call npx electron-builder --config package-desktop.json --win
if errorlevel 1 (
    echo Failed to build Electron app
    pause
    exit /b 1
)

echo.
echo ======================================
echo BUILD SUCCESSFUL!
echo ======================================
echo.
echo Your Windows installer is ready at:
echo dist-electron\StockCeramique Setup.exe
echo.
echo You can now distribute this file to any Windows computer.
echo.
pause
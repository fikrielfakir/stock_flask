@echo off
echo Quick Desktop Build for StockCeramique...

REM Install desktop tools only
echo Installing Electron and builder tools...
call npm install --save-dev electron@26.0.0 electron-builder@26.0.12 cross-env@7.0.3

REM Build frontend first
echo Building React frontend...
call npm run build
if errorlevel 1 (
    echo Error building frontend
    pause
    exit /b 1
)

REM Build desktop server with correct esbuild options
echo Building desktop server...
if not exist "dist-desktop" mkdir dist-desktop
call npx esbuild server/index-desktop.ts --platform=node --bundle --format=esm --outdir=dist-desktop --external:better-sqlite3 --external:ws --external:express

REM Copy required files to project root for electron-builder
copy package-desktop.json package-desktop-temp.json
copy electron-builder.json electron-builder-temp.json

REM Create the Windows executable from project root
echo Creating Windows executable...
call npx electron-builder --config package-desktop-temp.json --win --publish=never

REM Clean up temp files
del package-desktop-temp.json 2>nul
del electron-builder-temp.json 2>nul

echo.
echo ======================================
echo DESKTOP BUILD COMPLETE!
echo ======================================
echo.
echo Find your installer at: dist-electron\StockCeramique Setup.exe
echo.
pause
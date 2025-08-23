@echo off
echo Building StockCeramique Desktop Application

REM Install dependencies
if not exist "node_modules\electron" (
    echo Installing desktop dependencies...
    call npm install --save-dev electron@26.0.0 electron-builder@26.0.12
)

REM Build frontend
echo Step 1: Building React frontend...
call npm run build
if errorlevel 1 (
    echo Frontend build failed
    pause
    exit /b 1
)

REM Build desktop server
echo Step 2: Building desktop server...
if not exist "dist-desktop" mkdir dist-desktop
call npx esbuild server/index-desktop.ts --platform=node --bundle --format=cjs --outdir=dist-desktop --target=node18 --external:better-sqlite3
if errorlevel 1 (
    echo Desktop server build failed
    pause
    exit /b 1
)

REM Create a clean electron-builder config without devDependencies
echo Step 3: Creating build configuration...
echo { > build-config.json
echo   "appId": "com.stockceramique.desktop", >> build-config.json
echo   "productName": "StockCeramique", >> build-config.json
echo   "directories": { >> build-config.json
echo     "output": "dist-electron" >> build-config.json
echo   }, >> build-config.json
echo   "files": [ >> build-config.json
echo     "dist/**/*", >> build-config.json
echo     "electron/**/*", >> build-config.json
echo     "dist-desktop/**/*" >> build-config.json
echo   ], >> build-config.json
echo   "win": { >> build-config.json
echo     "target": "nsis", >> build-config.json
echo     "requestedExecutionLevel": "asInvoker" >> build-config.json
echo   }, >> build-config.json
echo   "nsis": { >> build-config.json
echo     "oneClick": false, >> build-config.json
echo     "allowToChangeInstallationDirectory": true, >> build-config.json
echo     "createDesktopShortcut": true, >> build-config.json
echo     "createStartMenuShortcut": true >> build-config.json
echo   } >> build-config.json
echo } >> build-config.json

REM Build the electron app
echo Step 4: Building Windows executable...
call npx electron-builder --config build-config.json --win --publish=never
if errorlevel 1 (
    echo Electron build failed
    pause
    exit /b 1
)

REM Clean up
del build-config.json 2>nul

echo.
echo ======================================
echo SUCCESS! Desktop app built successfully
echo ======================================
echo.
echo Your Windows installer is ready at:
echo dist-electron\StockCeramique Setup.exe
echo.
echo The installer includes:
echo - Complete offline application
echo - Local SQLite database
echo - Desktop and Start Menu shortcuts
echo.
echo You can now distribute this .exe file to any Windows computer
echo.
pause
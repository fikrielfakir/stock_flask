@echo off
echo.
echo StockCeramique Windows Desktop App Builder
echo ==========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.11 or later from https://python.org
    pause
    exit /b 1
)

echo [1/4] Installing Windows-specific requirements...
pip install -r requirements-windows.txt
if errorlevel 1 (
    echo ERROR: Failed to install requirements
    pause
    exit /b 1
)

echo.
echo [2/4] Cleaning previous build...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"

echo.
echo [3/4] Building Windows executable with PyInstaller...
pyinstaller StockCeramique.spec --clean --noconfirm
if errorlevel 1 (
    echo ERROR: PyInstaller build failed
    pause
    exit /b 1
)

echo.
echo [4/4] Build completed successfully!
echo.
echo Executable location: dist\StockCeramique.exe
echo.
echo Installation Notes for Windows 10:
echo - Requires Windows 10 version 1803 or later
echo - May need Visual C++ Redistributable
echo - Database will be created in: %%USERPROFILE%%\StockCeramique\
echo.
pause
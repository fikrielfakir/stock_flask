# StockCéramique Desktop Setup Guide

## For End Users (Simple Installation)

### 1. Download and Install
1. Download the `StockCeramique Setup.exe` file
2. Double-click to run the installer
3. Follow the installation wizard
4. The app will be installed and a desktop shortcut created

### 2. First Run
- The app will create a local database automatically
- All your data stays on your computer
- No internet connection required

## For Developers (Building from Source)

### Prerequisites
- Windows 10/11
- Node.js 18+ installed from https://nodejs.org/
- Git (optional, for cloning)

### Quick Start
1. Download or clone the project files
2. Open Command Prompt or PowerShell in the project folder
3. Run: `desktop-dev.bat` (for development)
4. Or run: `desktop-build.bat` (to build installer)

### Available Commands

**Development Mode** (for testing):
```cmd
desktop-dev.bat
```
This starts the development server and opens the app for testing.

**Build Installer** (for distribution):
```cmd
desktop-build.bat
```
This creates the Windows installer (.exe file) in the `dist-electron` folder.

**Run Built App** (after building):
```cmd
run-desktop.bat
```
This runs the production version without rebuilding.

### Manual Commands (if batch files don't work)

**Start Development Server:**
```cmd
set DESKTOP_PORT=3001
tsx server/index-desktop.ts
```

**Start Electron (in another terminal):**
```cmd
electron electron/main.js
```

**Build Everything:**
```cmd
npm run build
npx esbuild server/index-desktop.ts --platform=node --packages=external --bundle --format=esm --outdir=dist-desktop
npx electron-builder --config electron-builder.json --win
```

## Database Location
- **Development**: `./data/stockceramique.db`
- **Installed App**: `%APPDATA%/StockCeramique/stockceramique.db`

## Troubleshooting

### "tsx is not recognized"
Install TypeScript executor globally:
```cmd
npm install -g tsx
```

### "electron is not recognized"
Install Electron globally:
```cmd
npm install -g electron
```

### Port Already in Use
Change the port in the batch files:
```cmd
set DESKTOP_PORT=3002
```

### Database Issues
Delete the database file to reset:
- Development: Delete `./data/stockceramique.db`
- Production: Delete `%APPDATA%/StockCeramique/stockceramique.db`

## Features
- Complete offline operation
- Local SQLite database
- Same interface as web version
- Windows-native application
- Automatic database backup
- Fast startup and performance

## Distribution
The built installer (`StockCeramique Setup.exe`) can be distributed to any Windows computer without requiring Node.js or any other dependencies.
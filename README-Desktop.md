# StockCéramique Desktop Edition

## Overview
StockCéramique Desktop is a Windows .exe application that runs your inventory management system completely offline with a local SQLite database.

## Key Features
- **Complete Offline Operation**: No internet required after installation
- **Local SQLite Database**: All data stored securely on your computer
- **Windows .exe Application**: Easy to install and distribute
- **Same Great Interface**: Identical web interface in a desktop app
- **Cross-Platform Ready**: Can build for Windows, Mac, and Linux

## Development and Building

### Prerequisites
- Node.js 18+
- All npm dependencies installed (`npm install`)

### Development Mode
```bash
# Start desktop development server
DESKTOP_PORT=3001 tsx server/index-desktop.ts

# In another terminal, start Electron
electron electron/main.js
```

### Building for Distribution
```bash
# Build complete desktop application
./desktop-build.sh
```

The build process:
1. Builds the React frontend (`npm run build`)
2. Bundles the desktop server with esbuild
3. Creates the Electron application package
4. Generates Windows installer (.exe)

### Output Files
After building, you'll find:
- **Windows**: `dist-electron/StockCéramique Setup.exe` - Installer for Windows
- **Portable**: `dist-electron/win-unpacked/` - Portable application folder

## Database Storage
- **Development**: `./data/stockceramique.db`
- **Production**: User's AppData directory (Windows) or equivalent
- **Automatic**: Database schema creates automatically on first run

## Distribution
The generated .exe file is a complete installer that:
- Installs the application to Program Files
- Creates desktop and start menu shortcuts
- Sets up the local database automatically
- Requires no additional dependencies

## Architecture
- **Frontend**: Same React/TypeScript application
- **Backend**: Express server with SQLite instead of PostgreSQL
- **Desktop**: Electron wrapper with native OS integration
- **Database**: SQLite with same schema as web version

## API Endpoints (Local)
All endpoints run on `http://127.0.0.1:3001`:
- `GET /api/health` - Server health check
- `GET /api/articles` - List all articles
- `POST /api/articles` - Create new article  
- `GET /api/dashboard/stats` - Dashboard statistics

## Security
- Local-only server (127.0.0.1)
- No external network dependencies
- All data remains on user's computer
- Standard Electron security practices

## Future Enhancements
- Data import/export features
- Backup/restore functionality
- Network sync capabilities (optional)
- Multi-user support for shared databases
const { app, BrowserWindow, Menu, shell } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

// Keep a global reference of the window object
let mainWindow = null;
let serverProcess = null;

const isDevelopment = process.env.NODE_ENV === 'development';
const serverPort = 3001;
const frontendUrl = `http://127.0.0.1:${serverPort}`;

function createWindow() {
  // Create the browser window
  mainWindow = new BrowserWindow({
    width: 1400,
    height: 900,
    minWidth: 800,
    minHeight: 600,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      webSecurity: true,
      allowRunningInsecureContent: false,
    },
    show: false, // Don't show until ready-to-show
    titleBarStyle: 'default',
    autoHideMenuBar: true, // Hide menu bar but allow Alt to show it
  });

  // Remove default menu bar completely
  Menu.setApplicationMenu(null);

  // Load the app
  mainWindow.loadURL(frontendUrl);

  // Show window when ready
  mainWindow.once('ready-to-show', () => {
    if (mainWindow) {
      mainWindow.show();
      
      // Focus the window
      if (isDevelopment) {
        mainWindow.webContents.openDevTools();
      }
    }
  });

  // Handle external links
  mainWindow.webContents.setWindowOpenHandler(({ url }) => {
    shell.openExternal(url);
    return { action: 'deny' };
  });

  // Handle page navigation
  mainWindow.webContents.on('will-navigate', (event, url) => {
    if (url !== frontendUrl && !url.startsWith(frontendUrl)) {
      event.preventDefault();
      shell.openExternal(url);
    }
  });

  // Emitted when the window is closed
  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

function startServer() {
  return new Promise((resolve, reject) => {
    // Path to your desktop server
    const serverPath = path.join(__dirname, '../dist-desktop/index-desktop.js');
    
    console.log('Starting desktop server from:', serverPath);
    
    serverProcess = spawn('node', [serverPath], {
      env: { 
        ...process.env, 
        NODE_ENV: 'production', 
        DESKTOP_PORT: serverPort.toString() 
      },
      stdio: ['ignore', 'pipe', 'pipe'],
    });

    let serverStarted = false;

    if (serverProcess.stdout) {
      serverProcess.stdout.on('data', (data) => {
        const output = data.toString();
        console.log('Server:', output);
        
        // Look for server ready message
        if (output.includes('Desktop server running') && !serverStarted) {
          serverStarted = true;
          resolve();
        }
      });
    }

    if (serverProcess.stderr) {
      serverProcess.stderr.on('data', (data) => {
        console.error('Server Error:', data.toString());
      });
    }

    serverProcess.on('error', (error) => {
      console.error('Failed to start server process:', error);
      reject(error);
    });

    serverProcess.on('exit', (code) => {
      console.log(`Server process exited with code ${code}`);
      if (!serverStarted) {
        reject(new Error(`Server failed to start (exit code: ${code})`));
      }
    });

    // Timeout after 15 seconds
    setTimeout(() => {
      if (!serverStarted) {
        console.log('Server start timeout - proceeding anyway');
        resolve();
      }
    }, 15000);
  });
}

// This method will be called when Electron has finished initialization
app.whenReady().then(async () => {
  try {
    console.log('Electron app ready, starting server...');
    
    // Start the server first
    await startServer();
    
    console.log('Server started, creating window...');
    
    // Then create the window
    createWindow();

    app.on('activate', () => {
      // On macOS, re-create window when dock icon is clicked
      if (BrowserWindow.getAllWindows().length === 0) {
        createWindow();
      }
    });
  } catch (error) {
    console.error('Failed to start application:', error);
    app.quit();
  }
});

// Quit when all windows are closed
app.on('window-all-closed', () => {
  // Kill server process if it exists
  if (serverProcess && !serverProcess.killed) {
    console.log('Terminating server process...');
    serverProcess.kill('SIGTERM');
  }
  
  // On macOS, keep app running even when all windows are closed
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('before-quit', () => {
  // Kill server process when app is quitting
  if (serverProcess && !serverProcess.killed) {
    console.log('Killing server process before quit...');
    serverProcess.kill('SIGKILL');
  }
});

// Security: Prevent new window creation
app.on('web-contents-created', (event, contents) => {
  contents.on('new-window', (navigationEvent, url) => {
    navigationEvent.preventDefault();
    shell.openExternal(url);
  });
});
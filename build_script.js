import { execSync } from 'child_process';
import fs from 'fs';
import path from 'path';

console.log('Building StockCeramique Desktop Application');

try {
  // Step 1: Clean previous builds
  console.log('Step 1: Cleaning previous builds...');
  if (fs.existsSync('dist')) {
    fs.rmSync('dist', { recursive: true });
  }
  if (fs.existsSync('dist-desktop')) {
    fs.rmSync('dist-desktop', { recursive: true });
  }
  if (fs.existsSync('dist-electron-main')) {
    fs.rmSync('dist-electron-main', { recursive: true });
  }

  // Step 2: Build React frontend
  console.log('Step 2: Building React frontend...');
  execSync('vite build', { stdio: 'inherit' });

  // Step 3: Build backend server
  console.log('Step 3: Building backend server...');
  execSync('esbuild server/index.ts --platform=node --packages=external --bundle --format=esm --outdir=dist', { stdio: 'inherit' });

  // Step 4: Build desktop server
  console.log('Step 4: Building desktop server...');
  execSync('esbuild server/index-desktop.ts --platform=node --packages=external --bundle --format=esm --outdir=dist-desktop', { stdio: 'inherit' });

  // Step 5: Build Electron main process
  console.log('Step 5: Building Electron main process...');
  execSync('esbuild electron/main.ts --platform=node --packages=external --bundle --format=esm --outdir=dist-electron-main', { stdio: 'inherit' });

  // Step 6: Copy necessary files
  console.log('Step 5: Copying files...');
  
  // Copy package.json to dist-desktop
  const packageJson = JSON.parse(fs.readFileSync('package.json', 'utf8'));
  // Remove devDependencies to reduce bundle size
  delete packageJson.devDependencies;
  fs.writeFileSync(path.join('dist-desktop', 'package.json'), JSON.stringify(packageJson, null, 2));

  // Step 7: Build Electron app
  console.log('Step 6: Building Electron application...');
  execSync('electron-builder --config build-config.json', { stdio: 'inherit' });

  console.log('✅ Build completed successfully!');
  console.log('📦 Electron app built in: dist-electron/');

} catch (error) {
  console.error('❌ Build failed:', error.message);
  process.exit(1);
}

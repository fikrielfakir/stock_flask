#!/bin/bash

echo "🏗️  Building StockCéramique Desktop Application..."

# Step 1: Build frontend
echo "📦 Building frontend..."
npm run build

# Step 2: Build desktop server
echo "🖥️  Building desktop server..."
mkdir -p dist-desktop
esbuild server/index-desktop.ts --platform=node --packages=external --bundle --format=esm --outdir=dist-desktop

# Step 3: Copy necessary files
echo "📋 Copying files..."
cp -r electron dist-desktop/
cp electron-builder.json dist-desktop/
cp -r data dist-desktop/ || mkdir -p dist-desktop/data

# Step 4: Build Electron app
echo "⚡ Building Electron app..."
electron-builder --config dist-desktop/electron-builder.json

echo "✅ Desktop build complete! Check dist-electron folder for the .exe file."
echo "💾 Database will be stored locally in the user's AppData folder"
echo "🚀 You can now distribute the .exe file to users"

# Desktop Scripts
desktop-dev: concurrently "tsx server/index-desktop.ts" "wait-on http://127.0.0.1:3001 && electron electron/main.js"
desktop-build: vite build && esbuild server/index-desktop.ts --platform=node --packages=external --bundle --format=esm --outdir=dist-desktop && electron-builder --config electron-builder.json
desktop-start: electron electron/main.js


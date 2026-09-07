import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const rootDir = path.dirname(fileURLToPath(import.meta.url))

export default defineConfig({
  plugins: [react()],
  cacheDir: '.vite-cache',
  resolve: { alias: { '@': path.resolve(rootDir, './src') } },
  server: { host: '127.0.0.1', port: 8090, strictPort: true },
  preview: { host: '127.0.0.1', port: 8090, strictPort: true },
  build: { sourcemap: false, chunkSizeWarningLimit: 600 },
})

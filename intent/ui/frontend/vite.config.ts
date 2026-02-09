import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// In prod-ish mode the FastAPI backend serves the SPA under /ui.
// Setting base to /ui/ ensures assets are requested from /ui/assets/*.
export default defineConfig(({ mode }: { mode: string }) => ({
  plugins: [react()],
  base: mode === 'production' ? '/ui/' : '/',
  server: {
    port: 5173,
    strictPort: true,
  },
}))


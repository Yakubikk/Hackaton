import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  server: {
    host: '192.168.1.5',
    port: 4000,
  },
  plugins: [react()],
})

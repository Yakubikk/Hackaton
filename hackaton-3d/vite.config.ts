import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  server: {
    host: '192.168.126.209',
    port: 4000,
  },
  plugins: [react()],
})

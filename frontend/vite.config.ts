import path from "path"
import tailwindcss from "@tailwindcss/vite"
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { version } from "./package.json";

export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  server: {
    allowedHosts: [
      "myprettyai.local" // DEV
    ],
    proxy: {
      "/api": "http://localhost:8000",
      "/llm": "http://localhost:8001",
      "/tts": "http://localhost:8002",
      "/stt": "http://localhost:8003"
    },
  },
  define: {
    __APP_VERSION__: JSON.stringify(version),
  },
})

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],

  test: {
    environment: 'jsdom',         // simulate browser DOM
    globals:     true,
    coverage: {
      reporter: ['text', 'html'],
    },
  },

  server: {
    proxy: {
      // Proxy all /api and /static requests to FastAPI
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/static': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },

  build: {
    rollupOptions: {
      output: {
        // Content-hash filenames for long-term browser caching
        entryFileNames:  'assets/[name].[hash].js',
        chunkFileNames:  'assets/[name].[hash].js',
        assetFileNames:  'assets/[name].[hash].[ext]',
      },
    },
  },
})
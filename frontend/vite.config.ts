import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
    },
  },
  build: {
    rollupOptions: {
      output: {
        manualChunks(id) {
          if (id.includes("node_modules/element-plus")) return "vendor-element-plus";
          if (id.includes("node_modules/vue") || id.includes("node_modules/vue-router") || id.includes("node_modules/pinia")) {
            return "vendor-vue";
          }
          if (id.includes("node_modules/axios")) return "vendor-axios";
        },
      },
    },
  },
})

import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
      // 可以添加其他的路径别名
    },
  },
  // define: {
  //   "$": 'window.jQuery',        // 把 $ 替换为 jQuery
  //   "jQuery": 'window.jQuery',   // 全局暴露 jQuery
  //   'window.$': 'window.jQuery',  // 显式将 jQuery 绑定到 window 对象
  // },
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        ws: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  },
  optimizeDeps: {
    include: ['echarts']
  },
  // build: {
  //   rollupOptions: {
  //     external: ['jquery'],  // 将 jQuery 作为外部依赖，避免被打包
  //   },
  // },
  assetsInclude: ['**/*.glb'],

  // Vite 配置中没有类似 `lintOnSave` 的配置，默认使用 VLS、ESLint 或者其他工具，可以在 `vite.config.js` 或项目根目录配置 ESLint。
})

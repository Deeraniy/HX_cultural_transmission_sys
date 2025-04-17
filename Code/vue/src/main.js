import './assets/main.css'
import './assets/font/font.css'  // 引入汇文明朝体字体
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import App from '@/App.vue'
import router from "@/router.js";
import * as echarts from 'echarts'
import 'swiper/css'
import 'swiper/css/effect-cards'
import './utils/echartConfig.js'  // 引入 ECharts 配置
import { createI18n } from 'vue-i18n'
import en from './locales/en.json'
import zh from './locales/zh.json'

// 创建 i18n 实例
const i18n = createI18n({
  legacy: false, // 使用 Composition API 模式
  globalInjection: true, // 全局注入 $t 函数
  locale: localStorage.getItem('language') || 'zh', // 从本地存储获取语言设置，默认中文
  messages: {
    zh,
    en
  }
})

const app = createApp(App)
const pinia = createPinia()

app.config.globalProperties.$echarts = echarts

// 使用 Vue 插件
app.use(pinia)
   .use(ElementPlus)
   .use(router)
   .use(i18n)
   .mount('#app')
// 11

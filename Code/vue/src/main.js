import './assets/main.css'
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

const app = createApp(App)
const pinia = createPinia()

app.config.globalProperties.$echarts = echarts

// 使用 Vue 插件
app.use(pinia)
   .use(ElementPlus)
   .use(router)
   .mount('#app')

import './assets/main.css'
import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import App from '@/App.vue'
import router from "@/router.js";



const app = createApp(App)

// 使用 Vue 插件
app.use(ElementPlus).use(router).mount('#app')

import './assets/main.css'
// main.ts
import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import App from '@/App.vue'
import router from "@/router.js";
const app = createApp(App)

app.use(ElementPlus).use(router).mount('#app')

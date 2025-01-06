//import './jquery.js'; // 先引入 jQuery
//import * as jQuery from 'jquery';  // 使用这种方式来导入 jQuery
// console.log('jQuery:', jQuery);
// window.$ = window.jQuery = jQuery; // 将 jQuery 绑定到 window 对象
// console.log('window.$', window.$)
// console.log('window.jQuery', window.jQuery)
import './assets/main.css'
import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import App from '@/App.vue'
import router from "@/router.js";

const app = createApp(App)

// 使用 Vue 插件
app.use(ElementPlus).use(router).mount('#app')

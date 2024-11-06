import './assets/main.css'
// main.ts
import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import App from './components/InterestPlace/PlaceDetail.vue'

const app = createApp(App)

app.use(ElementPlus).mount('#app')

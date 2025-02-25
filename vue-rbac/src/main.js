import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import ElementPlus from 'element-plus'
import '@/router/permission.js'
import 'element-plus/dist/index.css'
import '@/assets/styles/border.css'
import '@/assets/styles/reset.css'

import SvgIcon from '@/icons'

// 国际化中文
import zhCn from 'element-plus/es/locale/lang/zh-cn'

const app=createApp(App)

app.use(ElementPlus, {
    locale: zhCn,
})

SvgIcon(app);
app.use(store)
app.use(router)
app.use(ElementPlus)
app.mount('#app')

import { createRouter, createWebHashHistory } from 'vue-router'




const routes = [
  {
    path: '/',
    name: '首页',
    component: () => import('../layout'),
    redirect:'/index',
    children:[
      {
        path: '/index',
        name: '首页',
        component: () => import('../views/index/index.vue')
      },
      {
        path: '/userCenter',
        name: '个人中心',
        component: () => import('../views/userCenter/index.vue')
      }
    ]
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('../views/Login.vue')
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})



export default router

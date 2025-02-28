// 路由守卫实现
import store from "@/store";
import router from "@/router/index";
import {ref} from "vue";

router.beforeEach((to, from, next)=>{
    let token=sessionStorage.getItem("token")
    // let token=ref(sessionStorage.getItem("token"))
    // console.log("token="+token);
    let hasRoutes=store.state.hasRoutes;
    // let menuList=ref(sessionStorage.getItem("menuList"))
    let menuList=JSON.parse(sessionStorage.getItem("menuList"))
    // console.log("to.path="+to.path);
    // console.log("menuList="+menuList)
    // console.log("hasRoutes="+hasRoutes)
    const whiteList=['/login'] // 白名单
    if(token){
        if(!hasRoutes){
            bindRoute(menuList);
            store.commit("SET_ROUTES_STATE",true)
        }
        next();
    }else{
        if(whiteList.includes(to.path)){
            next(); // 放行
        }else{
            next("/login") // 跳转登录页面
        }
    }
})

// 动态绑定路由
const bindRoute=(menuList)=>{
    let newRoutes=router.options.routes;
    menuList.forEach(menu=>{
        if(menu.children){
            menu.children.forEach(m=>{
                // 菜单转成路由
                let route=menuToRoute(m,menu.name);
                if(route){
                    newRoutes[0].children.push(route); // 添加到路由管理
                }
            })
        }
    })
    // 重新添加到路由
    newRoutes.forEach(route=>{
        router.addRoute(route);
    })
}

// 菜单转成路由
const menuToRoute = (menu,parentName) => {

    if (!menu.component) {
        return null
    }else{
        let route = {
            name: menu.name,
            path: menu.path,
            meta:{
                parentName:parentName
            }
        }
        route.component = () => import('@/views/' + menu.component +'.vue')

        return route
    }
}

// const menuList=JSON.parse(sessionStorage.getItem("menuList"))
// const token=sessionStorage.getItem("token")
//
// console.log(typeof menuList);
// if(token){
//     console.log("动态绑定路由")
//     bindRoute(menuList); // 动态绑定路由
// }

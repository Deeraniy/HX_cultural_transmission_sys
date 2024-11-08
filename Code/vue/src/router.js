import {createRouter, createWebHashHistory} from 'vue-router';

// 定义路由
const routes = [
    {
        path: '/',
        component:() => import('./components/InterestPlace/PlaceOfInterestMain.vue'),
    },
    {
        path: '/placeDetail',
        component:() => import('./components/InterestPlace/PlaceDetail.vue'),
    },
    {
        path: '/3d',
        component:() => import('./components/Three.vue')
    }
];

// 创建路由器实例
const router =createRouter({
    history:createWebHashHistory(),
    routes
});

export default router;

import {createRouter, createWebHashHistory} from 'vue-router';

// 定义路由
const routes = [
    {
        path: '/',
        component:() => import('./components/IndexHeader.vue'),
    },
    {
        path: '/placeOfInterest',
        component:() => import('./components/InterestPlace/PlaceOfInterestMain.vue'),
    },
    {
        path: '/index',
        component:() => import('./components/IndexHeader.vue'),
    },
    {
        path: '/placeDetail',
        component:() => import('./components/InterestPlace/PlaceDetail.vue'),
    },
    {
        path: '/detail',
        component:() => import('./components/DetailPage.vue'),
    },
    {
        path: '/3d',
        component:() => import('./components/Three.vue')
    },
    {
        path: '/walk/:title',
        name: 'Walk',
        component:() => import('./components/RedCulture/Walk.vue'),
        props: true // 使得路由参数自动作为 prop 传递给组件
    },
    {
        path: '/filmLiterature',
        component:() => import('./components/FilmLiterature/FilmLiteratureMain.vue')
    },
    {
        path: '/model',
        component:() => import('./components/MaoZedongSeries.vue')
    },
    {
        path: '/red',
        component:() => import('./components/RedCulture/RedCultureHeader.vue')
    },
    {
        path: '/folkCustom',
        component:() => import('./components/FolkCustom/FolkCustomMain.vue')
    },
    {
        path: '/folkCustomInfluence',
        component:() => import('./components/FolkCustom/FolkCustomInfluence.vue')
    }
    ,{
        path: '/folkSentimentAnalyze',
        component:() => import('./components/FolkCustom/FolkSentimentAnalyze.vue')
    },
    {
        path: '/card',
        component:() => import('./components/FolkCustom/LunBo.vue')
    },
    {
        path:'/page',
        component:() => import('./components/FilmLiterature/Literature/PageFlip.vue')
    },
    {
        path: '/food',
        redirect: '/food/home',
        name: 'FoodShow',
        component:()=>import('./components/Food/FoodShow.vue'), // 美食文化主页组件 foodshow里面有router-view,用子路由实现
        children: [
            {
                path: 'home',
                name: 'FoodHome',
                component: () => import('./components/Food/HomePageMain.vue')
            },
            {
                path: 'detail',
                name: 'FoodPage',
                component: () => import('./components/Food/FoodPage.vue'),
            },
            {
                path: 'detail/:foodName',
                name: 'FoodDetailPage',
                component: () => import('./components/Food/FoodDetailPage.vue'),
                props: true,
            },
            {
                path: 'propagation',
                name: 'PropagationPage',
                component: () => import('./components/Food/PropagationPage.vue'),
            },
        ],
    },
    {
        path: '/header',
        name: 'header',
        component:()=>import('./components/FolkCustom/header.vue'), // 美食详情页面

    },

];

// 创建路由器实例
const router =createRouter({
    history:createWebHashHistory(),
    routes
});

export default router;

import {createRouter, createWebHashHistory} from 'vue-router';

// 定义路由
const routes = [
    {
        path: '/',
        component:() => import('./components/InterestPlace/PlaceOfInterestMain.vue'),
    },
    {
        path: '/index',
        component:() => import('./components/index.vue'),
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
        path: '/filmLiterature',
        component:() => import('./components/FilmLiterature/FilmLiteratureMain.vue')
    },
    {
        path: '/model',
        component:() => import('./components/MaoZedongSeries.vue')
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
        name: 'FoodShow',
        component:()=>import('./components/Food/FoodShow.vue'), // 美食文化主页组件
    },
    {
        path: '/food/propagation',
        name: 'PropagationPage',
        component:()=>import('./components/Food/PropagationPage.vue'), // 传播效果分析页面
    },
    {
        path: '/food/detail',
        name: 'FoodPage',
        component:()=>import('./components/Food/FoodPage.vue'), // 美食专区页面
    },
    {
        path: '/food/detail/:foodName',
        name: 'FoodDetailPage',
        component:()=>import('./components/Food/FoodDetailPage.vue'), // 美食详情页面
        props: true, // Pass the `foodName` as a prop to the component
    }
];

// 创建路由器实例
const router =createRouter({
    history:createWebHashHistory(),
    routes
});

export default router;

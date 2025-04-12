import {createRouter, createWebHashHistory} from 'vue-router';
import { useUserStore } from '@/stores/user';
import { createPinia } from 'pinia';

import UserHome from "@/components/User/UserHome.vue";
import UserHomeMain from "@/components/User/components/main/UserHomeMain.vue";
import UserTags from "@/components/User/components/left/UserTags.vue";
import UserProfile from "@/components/User/components/left/UserProfile.vue";
import UserArticle from "@/components/User/components/left/UserArticle.vue";
import UserStar from "@/components/User/components/left/UserStar.vue"
import UserUpload from "@/components/User/components/left/UserUpload.vue"
import UserActivity from "@/components/User/components/left/UserActivity.vue";
import Login from "@/components/login.vue"
import RecommendMap from "@/components/Recommend/WorldMapChart.vue"
// 创建 Pinia 实例
const pinia = createPinia();

// 定义路由
const routes = [
    {
        path: '/index',
        component:() => import('./components/IndexHeader.vue'),
        children: [{
            path: 'background',
            component:()=> import('./components/Background/BackgroundIntro.vue'),
        },
            {
                path: 'about',
                component:() => import('./components/About/AboutUs.vue'),
            }]
    },
    {
        path: '/login',
        component:() => import('./components/login.vue'),
    },
    {
        path: '/',
        component:() => import('./components/login.vue'),
    },
    {
        path: '/userHome',
        component: UserHome,
        children: [{
            path: '',
            component: UserArticle
        },
            {
                path: 'tags',
                component: UserTags
            },
            {
              path: 'activity',
                component: UserActivity
            },
            {
                path: 'upload',
                component: UserUpload
            },
            {
                path: 'profile',
                component: UserProfile
            },
            {
                path: 'article',
                component: UserArticle
            },
            {
                path: 'star',
                component: UserStar
            },
        ]
    },
    {
        path: '/recommend',
        component:() => import('./components/Recommend/RecommendPage.vue'),
    },
    {
        path: '/recommendMap',
        component:() => import('./components/Recommend/WorldMapChart.vue'),
    },
    {
        path: '/placeOfInterest',
        component:() => import('./components/InterestPlace/PlaceOfInterestMain.vue'),
    },

    {
        path: '/report',
        component:() => import('./components/ReportGeneration/ReportMain.vue'),
    },
    {
        path: '/globe',
        name: 'Globe3D',
        component: () => import('@/components/Spread/Globe3D.vue')
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
        path: '/platform',
        component:() => import('./components/EntireAnalysis/PlatformAnalysisHeader.vue'),
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
    {
        path:'/background',//背景介绍
        name: 'background',
        component:()=>import('./components/Background/BackgroundIntro.vue'),
    }
    ,
    {
        path:'/about',//关于我们
        name: 'about',
        component:()=>import('./components/About/AboutUs.vue'),
    }
];

// 创建路由器实例
const router = createRouter({
    history: createWebHashHistory(),
    routes
});

// 添加全局导航守卫
const scrollPositions = {};

router.beforeEach((to, from, next) => {
    // 需要认证的路由
    const authRoutes = [
        '/userHome',
        '/recommend',
        '/placeOfInterest',
        '/placeDetail',
        '/detail',
        '/platform'
    ];

    // 从 localStorage 直接检查登录状态
    const isLoggedIn = !!localStorage.getItem('userId');

    if (authRoutes.includes(to.path) && !isLoggedIn) {
        next('/login');
    } else {
        // 保存离开页面的滚动位置
        if (from.path === '/recommend') {
            scrollPositions[from.path] = window.scrollY;
        }
        next();
    }
});

router.afterEach((to, from) => {
    // 恢复页面的滚动位置
    if (to.path === '/recommend' && scrollPositions[to.path]) {
        nextTick(() => {
            window.scrollTo(0, scrollPositions[to.path]);
        });
    }
});

export default router;

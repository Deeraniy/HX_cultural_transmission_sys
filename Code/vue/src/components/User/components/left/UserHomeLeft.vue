<!-- 用户主页左栏 -->
<script setup>
import { useRouter } from 'vue-router';
import { ref } from 'vue'
import UserHome from '@/components/User/UserHome.vue'

// 导入图标
import {
  Document,
  Menu as IconMenu,
  Location,
  Setting,
  ChatLineSquare,
  Flag,
  DataAnalysis, Star, Upload
} from '@element-plus/icons-vue'
// 使用路由
const router = useRouter();
// 监听按钮状态
const createArticle=()=>{
    router.push({
        path: '/editor'
    })
}
// 修改资料
const jumpEmpty = () => {
    router.push({
        path: '/empty'
    })
}
// 用户主页
const jumpUserHome = () => {
    router.push({
        path: '/userHome'
    })
}

// 跳转标签
const jumpTags = () => {
    router.push({
        path: '/userHome/tags'
    })
}
const jumpSet = () => {
  router.push({
    path: '/userHome/profile'
  })
}

// 跳转修改资料
const jumpProfile = () => {
    router.push({
        path: '/userHome/profile'
    })
}

// 全部文章
const jumpArticle = () => {
    router.push({
        path: '/userHome/article'
    })
}
const jumpUpload = () =>{
  router.push({
    path: '/userHome/upload'
  })
}
const jumpStar = () => {
  router.push({
    path: '/userHome/star'
  })
}

const jumpActivity = () => {
  router.push({
    path: '/userHome/activity'
  })
}
</script>

<template>
    <div>
      <div>

      </div>
        <!-- 菜单组件 -->
        <el-menu class="card">
            <!-- 菜单3 -->
            <el-menu-item index="3" @click="jumpArticle">
                <el-icon>
                    <document />
                </el-icon>
                <template #title>浏览记录</template>
            </el-menu-item>
            <!--  -->
            <el-menu-item index="4" @click="jumpStar">
              <el-icon><Star/></el-icon>
                <template #title>收藏</template>
            </el-menu-item>
          <el-menu-item index="5" @click="jumpActivity">
            <el-icon><DataAnalysis /></el-icon>
            <template #title>用户画像</template>
          </el-menu-item>
          <el-menu-item index="6" @click="jumpUpload">
            <el-icon><Upload /></el-icon>
            <template #title>关系上传</template>
          </el-menu-item>
            <!-- 菜单4 -->
            <el-menu-item index="7" @click="jumpSet">
                <el-icon>
                    <setting />
                </el-icon>
                <template #title>设置</template>
            </el-menu-item>
        </el-menu>
    </div>
</template>


<style scoped>
/* 样式 */
.card{
    width: 200px;
    min-height: 400px;
    border-radius: 10px;
}
</style>

<template>
  <div class="whole">
    <div class="total">
      <!-- 左侧大标题 -->
      <div :class="['menu-title', { 'right-position1': locale === 'en' }]">
        <h2>{{ $t('mei-shi-wen-hua-fen-xi') }}</h2>
        <!-- 返回按钮 -->
        <el-button :class="['back-btn', { 'right-position': locale === 'en' }]" @click="goBack">{{ $t('fan-hui') }}</el-button>
      </div>

      <!-- 菜单区域 -->
      <el-menu
          class="el-menu-demo"
          mode="horizontal"
          :ellipsis="false"
          :router="true"
      >
        <!-- 首页菜单项 -->
        <el-menu-item index="/food/home">{{ $t('menu.home') }}</el-menu-item>
        <!-- 美食专区菜单项 -->
        <el-menu-item index="/food/detail">{{ $t('mei-shi-zhuan-qu') }}</el-menu-item>
        <!-- 传播效果分析菜单项 -->
        <el-menu-item index="/food/propagation">{{ $t('chuan-bo-xiao-guo-fen-xi') }}</el-menu-item>
      </el-menu>
    </div>

    <el-main>
      <router-view />
    </el-main>
  </div>
</template>


<script lang="ts" setup>
// 引入 vue-router
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n';
const { t, locale } = useI18n();
const router = useRouter()



// 返回上一页的方法
const goBack = () => {
  router.push('/index')  // 返回到index页面
}
</script>

<style scoped>
@import '@/assets/font/font.css';

.total {
  display: flex;
  align-items: flex-end;
  background-image: url('@/assets/img_4.png');
  background-size: cover;
  background-position: center;
  padding-left: 20px;
}

.whole {
  margin-top: -55px;
  background-image: url('@/assets/img2.png');
  background-color: #fff8f0;
  background-size: cover;
  background-position: center;
}


.el-main {
  padding: 0;
}

.menu-title {
  transform: translateY(25px);
  font-family: 'HelveticaNeue', serif;
  font-size: 24px;
  color: #fff8f0;
  margin-right: 700px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  margin-bottom: 10px;
}

.el-menu-demo {
  margin-right: 0px;
  display: flex;
  justify-content: flex-end;
  background-color: transparent !important;
  box-shadow: none;
  padding-top: 0;
  padding-bottom: 0;
  border-bottom: none;
  border-radius: 0;
}

.el-menu-item {
  margin-right: 0px;
  background-color: #B71C1C64 !important;
  color: #fff8f0 !important;
  font-size: 20px;
  font-family: 'HelveticaNeue', serif !important;
  border-bottom: none !important;
}

.el-menu-item.is-active,
.el-menu-item:hover {
  color: #ffd700 !important;
  background-color: #B71C1C64 !important;
}

:deep(.el-sub-menu__title) {
  color: #fff8f0 !important;
  background-color: #B71C1C64 !important;
  font-family: 'HelveticaNeue', serif !important;
  font-size: 20px;
  padding: 0 10px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  cursor: pointer;
}

:deep(.el-sub-menu__icon-arrow) {
  display: none !important;
}

:deep(.el-sub-menu__title:hover),
:deep(.el-sub-menu__title.is-active) {
  color: #ffd700 !important;
  background-color: #B71C1C64 !important;
}

:deep(.el-sub-menu) {
  background-color: transparent !important;
}

/* 返回按钮样式 */
.back-btn {
  font-family: 'HelveticaNeue', serif;
  background-color: transparent !important;
  color: #fff8f0 !important;
  border: none;
  font-size: 20px;
  margin-bottom: 0px;

  cursor: pointer;
  transition: background-color 0.3s ease;
}
/* 英文模式下的右对齐 */
.right-position {
  margin-left: 0px; /* 右边距，保证按钮离右边有一定间距 */
  margin-right: 400px;
}
.right-position1 {
  margin-right: 0px; /* 右边距，保证按钮离右边有一定间距 */

}

</style>

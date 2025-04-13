<script setup>
import {ref} from "vue";
import {useRouter} from "vue-router";
defineProps(
    {
      activeIndex: String,
    }
)
const router = useRouter()
const handleSelect = (key) => {
  if (key === '1') {
    router.push('/folkCustom')
  } else if (key === '2') {
    router.push('/folkCustomInfluence')
  } else if (key === '3') {
    router.push('/folkSentimentAnalyze')
  }
}
</script>

<template>
  <div>
  <el-menu
      :default-active="activeIndex"
      class="el-menu-demo"
      mode="horizontal"
      :ellipsis="false"
      @select="handleSelect"
  >
    <el-menu-item index="1" >{{ $t('menu.home') }}</el-menu-item>
    <el-menu-item index="2">{{ $t('chuan-bo-xiao-guo') }}</el-menu-item>
    <!-- <el-menu-item index="3">情感分析</el-menu-item> -->
  </el-menu>
  </div>
</template>

<style scoped>

/* 菜单样式 */
.el-menu-demo {
  display: flex; /* 使用 flex 布局 */
  justify-content: flex-end;   /* 菜单项靠右对齐 */
  background-color: transparent !important; /* 将菜单背景设为透明 */
  box-shadow: none; /* 移除默认阴影（如果有的话） */
  padding-right: 20px;
  border-bottom-left-radius: 30px; /* 左下圆角 */
  border-bottom-right-radius: 30px; /* 右下圆角 */
  box-shadow: none;
}

/* 覆盖菜单项文字样式 */
.el-menu-item {
  color: #fff8f0 !important;
  font-size: 20px;
  font-family: 'HelveticaNeue', serif !important;
}

/* 选中和悬停菜单项的颜色和背景 */
.el-menu-item.is-active,
.el-menu-item:hover {
  color: #ffd700 !important; /* 设置选中和悬停状态的文字颜色为金色 */
  background-color: rgba(255, 255, 255, 0.2) !important; /* 透明度为20%的淡色背景 */
  border-bottom: 2px solid #ffd700; /* 添加选中和悬停菜单项的下边框 */
}

/* 覆盖“工作台”标题样式 */
.el-sub-menu >>> .el-sub-menu__title {
  color: #fff8f0 !important;
  font-family: 'HelveticaNeue', serif !important;
}

/* 子菜单的悬停和选中样式 */
.el-sub-menu__title:hover,
.el-sub-menu__title.is-active {
  color: #ffd700 !important;
  background-color: rgba(255, 255, 255, 0.2) !important;
}
</style>

<template>
  <div class="button-container">
    <!-- 返回按钮和标题 -->
    <el-page-header @back="onBack" class="header">
      <template #content>
        <span class="title" style="font-size: 30px">{{title}}</span>
      </template>
    </el-page-header>

    <!-- 用户信息和头像 -->
    <div class="user-info">
      <img src="@/assets/cat.gif" style="width: 100px" @click="drawer = true">
      <div class="block">
        <el-avatar :size="50" :src="circleUrl" />
      </div>
      <div class="toolbar">
        <el-dropdown>
          <el-icon style="margin-right: 0px; font-size: 25px; margin-top: 5px">
            <Setting />
          </el-icon>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item>退出登录</el-dropdown-item>
              <el-dropdown-item>个人信息</el-dropdown-item>
              <el-dropdown-item>修改密码</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </div>
    <el-drawer v-model="drawer" title="I am the title" :with-header="false">
      <span>Hi there!</span>
    </el-drawer>
  </div>
</template>

<script setup>
import { ArrowLeft, Setting } from "@element-plus/icons-vue";
import { ref } from "vue";
import router from "@/router.js";
const drawer = ref(false)

const circleUrl = ref("https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png");
const props = defineProps({title:String})
const onBack = () => {
  router.go(-1);
  console.log("返回按钮被点击");
};
</script>

<style scoped>
@import '@/assets/font/font.css';

/* 主容器的样式，与 tab 样式一致 */
.button-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 20px;
  background-image: url('@/assets/img_4.png'); /* 设置与标签栏一致的背景 */
  background-size: cover;
  background-position: center;
  border-bottom-left-radius: 30px;
  border-bottom-right-radius: 30px;
}

/* 返回按钮样式 */
.header {
  width: 100%;
  display: flex;
  align-items: center;
  cursor: pointer;
}

.back-icon {
  color: #fff8f0;
  font-size: 25px;
  margin-right: 8px;
}

/* 标题样式 */
.title {
  color: #fff8f0;
  font-family: 'HelveticaNeue', serif;
  font-size: 20px;
  font-weight: bold;
}

/* 用户信息区域 */
.user-info {
  display: flex;
  align-items: center;
  color: #fff8f0;
}

.sub-title {
  font-family: 'HelveticaNeue', serif;
  font-size: 18px;
  color: #fff8f0;
  margin-right: 15px;
}

.block {
  margin-right: 15px;
}
.header .el-page-header__content::before,
.header .el-page-header__content::after {
  content: none; /* 隐藏多余的分隔符 */
}
/* 工具栏图标样式 */
.toolbar .el-icon {
  color: #fff8f0;
}
</style>

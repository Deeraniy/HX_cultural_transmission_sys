<template>
  <el-main>
      <div class="iframe-container">
    <iframe src="http://127.0.0.1:7860" class="custom-iframe"></iframe>
  </div>
  </el-main>

</template>

<script lang="ts" setup>
import { ref } from 'vue'
</script>

<style>
/* 使用 flexbox 实现居中 */
.iframe-container {
  padding-top: 30px; /* 让 iframe 距离顶部有一定的间距 */
  display: flex;
  justify-content: center; /* 水平居中 */
  align-items: flex-start; /* 让内容靠上而非完全垂直居中 */
  height: 100vh; /* 设置容器高度为视口高度 */
  margin: 0;
}

/* 自定义 iframe 样式 */
.custom-iframe {
  width: 1000px;
  height: 900px;
  border: none; /* 移除边框 */
  overflow: hidden; /* 禁用滚动条 */
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1); /* 可选：添加阴影效果 */
  border-radius: 10px; /* 可选：添加圆角 */
}
:deep(.el-main.el-main) {
overflow: hidden !important;
padding: 0 !important;
height: 100% !important;
}

/* 或者使用属性选择器增加优先级 */
:deep([class*="el-main"]) {
overflow: hidden !important;
padding: 0 !important;
height: 100% !important;
}

/* 如果还不行，可以尝试使用多重选择器 */
:deep(.el-container .el-main) {
overflow: hidden !important;
padding: 0 !important;
height: 100% !important;
}

/* 隐藏滚动条 */
:deep(.el-main::-webkit-scrollbar) {
width: 8px; /* 定义滚动条宽度 */
height: 8px;
background-color: transparent; /* 滚动条背景颜色 */
}

:deep(.el-main::-webkit-scrollbar-thumb) {
background-color: transparent; /* 滚动条滑块颜色 */
border-radius: 4px; /* 滚动条滑块圆角 */
}

:deep(.el-main::-webkit-scrollbar-thumb:hover) {
background-color: rgba(0, 0, 0, 0.2); /* 鼠标悬停时滚动条滑块颜色 */
}


.main-container {
width: 100%;
display: flex;
overflow: hidden; /* 禁止滚动 */
flex-direction: column;
}
</style>

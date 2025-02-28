<!-- 用户主页界面 -->
<script setup>
import UserHomeLeft from '@/components/User/components/left/UserHomeLeft.vue';
import UserHomeMain from "@/components/User/components/main/UserHomeMain.vue";
// import LayoutFooter from '@/components/User/components/LayoutFooter.vue';
</script>

<template>
  <div class="HomeMain" >
    <div class="content-wrapper">
      <div style="display: flex; justify-content: center;">
        <UserHomeMain/>
      </div>

      <div class="borderMain" style="
  margin: 0 auto;  /* 使用 auto 边距实现水平居中 */
  max-width: 1100px;  /* 设置最大宽度，防止在大屏幕上过宽 */
  padding: 0 50px;  /* 替换原来的左右 margin，使用 padding */
">
        <div style="
    display: flex;
    margin-bottom: 50px;
    justify-content: center;
    align-items: flex-start;  /* 确保子元素从顶部对齐 */
  ">
          <!-- 用户主页面 -->
          <UserHomeLeft style="margin-left: 20px"/>  <!-- 移除固定的左边距 -->
          <!-- RouterView 放在 Card 中 -->
          <el-card style="
      width: 60%;
      margin-left: 20px;
      margin-right: 20px;
      min-height: 500px;
      padding-left: 20px;
      padding-top: 20px;
      box-shadow: 0 2px 12px 0 rgba(0,0,0,0.1);
      border-radius: 12px;
    ">
            <RouterView/>
          </el-card>
        </div>
      </div>
    </div>
  </div>
<!--    <LayoutFooter />-->
</template>
<style scoped>
.HomeMain {
  background-image: url('@/assets/userhomeBACK.jpg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  background-attachment: fixed;
  min-height: 100vh;
  margin: 0;
  padding: 0;
}


/* 如果需要添加一个半透明遮罩让内容更容易阅读 */
.content-wrapper {
  background-color: rgba(255, 255, 255, 0.7);
  min-height: 100vh;
  padding: 20px;
}
</style>

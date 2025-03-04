<!-- 用户主页界面 -->
<script setup>
import UserHomeLeft from '@/components/User/components/left/UserHomeLeft.vue';
import UserHomeMain from "@/components/User/components/main/UserHomeMain.vue";
// import LayoutFooter from '@/components/User/components/LayoutFooter.vue';
</script>

<template>
  <div style="margin-left: 400px">
    <UserHomeMain/>
  </div>

    <div class="borderMain">
        <div style="display: flex;margin-bottom: 50px;justify-content: center;">
            <!-- 用户主页面 -->
            <UserHomeLeft style="margin-left: 200px"/>
<!--            &lt;!&ndash; 三级路由出组件 &ndash;&gt;-->
            <RouterView style="width: 100%"/>
        </div>
    </div>
<!--    <LayoutFooter />-->
</template>
<style scoped>
.borderMain {
    margin-top: 20px;
}
</style>

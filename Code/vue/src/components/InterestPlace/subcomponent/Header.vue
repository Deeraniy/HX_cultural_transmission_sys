<template>
  <div class="button-container">
    <el-page-header :icon="ArrowLeft" title="返回"   @click="$router.go(-1)" >
      <template #content>
        <span class="text-large font-600 mr-3" style="font-size: larger"> Title </span>
      </template>
    </el-page-header>

    <div>
      <div class="sub-title">用户名</div>
        <div class="block">
          <el-avatar :size="50" :src="circleUrl" />
        </div>
      <div class="toolbar">
        <el-dropdown>
          <el-icon style="margin-right: 0px;font-size:25px;margin-top: 5px">
            <setting />
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
    </div>

</template>

<script setup>

import { ArrowRight, ArrowLeft, Setting} from "@element-plus/icons-vue";
import {ref} from "vue";
const circleUrl = ref('https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png')
</script>

<style scoped>
.button-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 10px;
}
</style>

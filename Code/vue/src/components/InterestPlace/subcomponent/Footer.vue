<template>
  <el-button-group>
    <el-button type="default" :icon="ArrowLeft">上一页</el-button>
    <el-button type="default">
      下一页<el-icon class="el-icon--right"><ArrowRight /></el-icon>
    </el-button>
  </el-button-group>

  <el-button-group class="ml-4">
    <el-button type="default" :icon="Share" />
    <el-button type="default" :icon="CirclePlusFilled" />
    <el-button type="default" :icon="RemoveFilled" />
  </el-button-group>
</template>

<script setup lang="ts">

import {ArrowLeft, CirclePlusFilled, RemoveFilled, Share,ArrowRight} from "@element-plus/icons-vue";
</script>

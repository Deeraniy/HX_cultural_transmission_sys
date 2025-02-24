<script lang="ts" setup>
import type { FormInstance, FormRules } from 'element-plus'
import { ElButton } from 'element-plus'
</script>

<template>
  <div>
    <!-- 标题 -->
    <div>
      <el-text class="mainTitle">我的活动</el-text>
    </div>
    <div style="display: flex;">
      <el-card shadow="hover" class="box-card">

      </el-card>

    </div>
  </div>
</template>

<style scoped>
.img{
  height: 40px;
  width: 40px;
  border-radius: 50%;
  object-fit: cover;
  margin-right: 10px;
}
.box-card {
  margin-top: 21px;
  margin-left: 20px;
  border-radius: 7px;
  width: 750px;
  padding-right: 30px;
}

.card {
  margin-top: 21px;
  margin-left: 20px;
  border-radius: 5px;
  width: 300px;
  height: 300px;
}

.input {
  width: 500px;
  height: 40px;
}

.input-mini {
  width: 250px;
  height: 40px;
}

.mainTitle {
  margin-left: 30px;
  font-size: 18px;
  color: #000;
  font-weight: bolder;
}

.profile {
  margin-left: 30px;
  margin-top: 20px;
}
</style>

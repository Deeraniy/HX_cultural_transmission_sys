<template>
  <div class="whole">
    <div class="total">
      <!-- 固定显示的标题，不作为菜单项 -->
      <h2 class="fixed-title">非遗民俗分析界面</h2>

      <!-- 菜单区域 -->
      <Header :activeIndex="activeIndex"/>
    </div>
          <FolkCustom/>
  </div>


</template>

<script lang="ts" setup>
import { ref,onMounted } from 'vue'
import FolkCustom from './FolkCustom.vue'
import {useRouter} from "vue-router";
import Header from './header.vue'
const router = useRouter()
const activeIndex = ref('1')

</script>

<style scoped>
@import '@/assets/font/font.css';

.total{
  background-image: url('@/assets/img_4.png');
  background-size: cover;
  background-position: center;
  border-bottom-left-radius: 30px; /* 左下圆角 */
  border-bottom-right-radius: 30px; /* 右下圆角 */
}
.whole{
  background-image: url('@/assets/img2.png');
  background-color: #fff8f0;
  background-size: cover;
  background-position: center;
}
.el-main {
  padding: 0;
}
/* 固定标题样式 */
.fixed-title {
  color: #fff8f0;
  font-family: 'HelveticaNeue', serif;
  font-size: 45px;
  margin: 0 16px;
}

</style>

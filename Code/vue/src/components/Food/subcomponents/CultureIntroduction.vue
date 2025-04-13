<template>
  <div class="culture-box">
    <el-card class="content-container" :body-style="{ padding: '0' }">
      <el-row>
        <!-- 图片列 -->
        <el-col :span="8">
          <img src="@/assets/foodImg/food5.jpg" alt="food5" class="food-image" />
        </el-col>

        <!-- 文字内容列 -->
        <el-col :span="16">
          <div class="text-container">
            <div class="title">{{ $t('hu-xiang-yin-shi-wen-hua') }}</div>
            <p :style="textStyle">
              {{ $t('hu-xiang-yin-shi-wen-hua-yuan-yuan-liu-chang-ke-yi-zhui-su-dao-xian-qin-shi-qi-hu-nan-di-chu-zhong-guo-nan-bu-qi-hou-shi-run-wu-chan-feng-fu-wei-hu-xiang-yin-shi-ti-gong-le-feng-fu-de-yuan-cai-liao-hu-xiang-yin-shi-wen-hua-shen-shou-chu-wen-hua-de-ying-xiang-ju-you-nong-yu-de-di-fang-te-se') }} 
            </p>
          </div>
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>


<script setup>
import { computed } from 'vue';
import { useI18n } from 'vue-i18n';

const { locale } = useI18n();

// 动态设置文本样式
const textStyle = computed(() => {
  return locale.value === 'en' ? { fontSize: '24px' } : { fontSize: '30px' };
});
</script>


<style scoped>
@import '@/assets/font/font.css';
.culture-box {
  width: 95%;
  margin: 30px auto;
}

.content-container {
  display: flex;
  justify-content: space-between;
  padding: 0;
}

.food-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.text-container {
  padding: 20px 30px;
  background-color: #f9f9f9;
  border-radius: 12px;
  height: 100%;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.title {
  font-family: 'HelveticaNeue', serif;
  font-size: 40px;
  color: #b71c1c;
  font-weight: bold;
  line-height: 45px;
  margin-bottom: 10px;
  position: relative;
  left: 270px;  /* 向右移动 50px，数字根据需要调整 */
}


.text-container p {
  font-family: 'HelveticaNeue', serif;
  margin-top: 10px;
  font-size: 30px;
  line-height: 1.8;
  color: #333;
}
</style>

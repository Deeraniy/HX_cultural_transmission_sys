<template>
  <div class="main">
    <!-- 卡片容器 -->
    <el-card class="content-card" :body-style="{ padding: '20px' }">
      <div class="section-title">
        {{ $t('xiang-cai-yun-wei') }}<br />
        <span>{{ $t('the-essence-of-hunan-cuisine') }}</span>
      </div>

      <!-- 使用 el-row 和 el-col 布局 -->
      <el-row gutter={30}>
        <!-- 第一列 -->
        <el-col :span="8" :xs="24" :sm="12" :md="8">
          <el-card class="food-item">
            <el-image
                class="image-container"
                :src="food3"
                alt="$t('chou-dou-fu')"
                fit="contain"
            />
            <div class="description-container">
              <div class="item-title">{{ $t('chou-dou-fu-0') }}</div>
              <p :style="descriptionStyle">{{ $t('chou-dou-fu-shi-hu-nan-de-chuan-tong-xiao-chi-wai-pi-su-cui-nei-li-ruan-nen-wei-dao-du-te-ju-you-kai-wei-xiao-shi-zeng-jin-shi-yu-de-gong-xiao-tong-shi-han-you-feng-fu-de-dan-bai-zhi-he-wei-sheng-su') }}</p>
            </div>
          </el-card>
        </el-col>

        <!-- 第二列 -->
        <el-col :span="8" :xs="24" :sm="12" :md="8">
          <el-card class="food-item">
            <el-image
                class="image-container"
                :src="food4"
                alt="$t('you-xian-xiang-gan')"
                fit="contain"
            />
            <div class="description-container">
              <div class="item-title item-title-secondary">{{ $t('you-xian-xiang-gan-0') }}</div>
              <p :style="descriptionStyle">{{ $t('you-xian-xiang-gan-shi-hu-nan-sheng-you-xian-de-chuan-tong-shi-pin-kou-gan-xiang-cui-wei-dao-xian-mei-ju-you-jian-pi-kai-wei-qing-re-jie-du-de-gong-xiao-shi-he-duo-zhong-peng-ren-fang-shi') }}</p>
            </div>
          </el-card>
        </el-col>

        <!-- 第三列 -->
        <el-col :span="8" :xs="24" :sm="12" :md="8">
          <el-card class="food-item">
            <el-image
                class="image-container"
                :src="food1"
                alt="$t('tang-you-ba-ba')"
                fit="contain"
            />
            <div class="description-container">
              <div class="item-title item-title-secondary">{{ $t('tang-you-ba-ba-0') }}</div>
              <p :style="descriptionStyle">{{ $t('tang-you-ba-ba-shi-hu-nan-de-chuan-tong-xiao-chi-wai-pi-su-cui-nei-li-ruan-nuo-tian-er-bu-ni-ju-you-zi-bu-yang-yan-jian-pi-kai-wei-de-gong-xiao-shi-dong-ji-de-jia-pin') }}</p>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>


<script setup>
import food1 from "@/assets/foodImg/food1.jpg";
import food4 from "@/assets/foodImg/food4.jpg";
import food3 from "@/assets/foodImg/food3.jpg";
import { computed } from 'vue';
import { useI18n } from 'vue-i18n';

const { locale } = useI18n();

// 动态设置文本样式
const descriptionStyle = computed(() => {
  return locale.value === 'en' ? { fontSize: '12px' } : { fontSize: '20px' };
});
</script>

<style scoped>
@import '@/assets/font/font.css';
.main {
  width: 96.5%;
  display: flex;
  margin-left: 25px;
}

.section-title {
  margin-top: 10px;
  font-family: 'HelveticaNeue', serif;
  font-size: 50px;
  font-weight: bolder;
  width: 100%;
  text-align: center;
  line-height: 50px;
}

.section-title span {
  color: #8aaa3d;
  font-size: 16px;
  font-family: 'HelveticaNeue', serif;
  line-height: 50px;
}

/* 卡片容器 */
.content-card {
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

/* 图片容器样式 */
.image-container {
  width: 100%;
  height: 210px;
  overflow: hidden;
  border-radius: 8px;
}

.description-container {
  height: 180px;
  background: #eeeeee;
  padding: 20px 30px;
  margin-top: 15px;
  text-align: center;
}

.description-container .item-title {
  color: #80b50f;
  font-size: 40px;
  font-weight: bold;
  height: 60px;
  font-family: 'HelveticaNeue', serif;
  border-bottom: #b9b9b9 1px solid;
  margin-bottom: 10px;
}

.description-container .item-title-secondary {
  color: #80b50f;
  font-size: 40px;
  font-family: 'HelveticaNeue', serif;
  font-weight: bold;
  height: 60px;
  border-bottom: #b9b9b9 1px solid;
  margin-bottom: 10px;
}

.description-container p {
  font-family: 'HelveticaNeue', serif;
  font-size: 20px;
  line-height: 25px;
}

/* 自适应布局 */
.food-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 30px;
}

.el-card {
  margin: 10px;
}

/* 响应式设计 */
@media (max-width: 700px) {
  .section-title {
    font-size: 40px;
  }
  .description-container {
    height: 200px;
  }
  .food-item {
    margin-bottom: 20px;
  }
}
</style>

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
            <div class="title">湖湘饮食文化</div>
            <p>
              湖湘饮食文化源远流长，可以追溯到先秦时期。湖南地处中国南部，气候湿润，物产丰富，为湖湘饮食提供了丰富的原材料。湖湘饮食文化深受楚文化的影响，具有浓郁的地方特色
            </p>
          </div>
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>

<script setup>
// 这里可以加入其他逻辑
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

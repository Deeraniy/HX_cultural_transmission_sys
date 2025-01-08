<template>
  <div class="food-trait-box">
    <!-- 卡片容器 -->
    <el-card class="content-card" :body-style="{ padding: '20px' }">
      <el-row>
        <!-- 文本容器 -->
        <el-col :span="12">
          <div class="text-container">
            <p>
              湖南的饮食文化具有以下几个显著特点：
            </p>
            <ul>
              <li><strong>重口味与辣味</strong>：湖南菜以其独特的辣味著称，辣椒是湖湘菜的灵魂，能够开胃消食，增进食欲。</li>
              <li><strong>丰富的食材</strong>：湖南地处亚热带，四季分明，盛产各种山珍野味、水产品和蔬菜，如竹笋、蕨菜、鱼、虾等。</li>
              <li><strong>多样化的烹饪技法</strong>：湖湘菜的烹饪技法多样，包括炒、炖、蒸、烧等，每种技法都有其独特的风味。</li>
              <li><strong>地方特色鲜明</strong>：每个地区都有其独特的美食，如攸县香干、糖油粑粑等，体现了湖湘文化的多样性。</li>
            </ul>
          </div>
        </el-col>

        <!-- 图片容器 -->
        <el-col :span="6">
          <div class="image-box">
            <img :src="food6" alt="food6" class="food-img" />
          </div>
        </el-col>

        <el-col :span="6">
          <div class="image-box">
            <img :src="food7" alt="food7" class="food-img" />
          </div>
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>

<script setup>
import food6 from '@/assets/foodImg/food6.jpg';
import food7 from '@/assets/foodImg/food7.jpg';
</script>

<style scoped>
.food-trait-box {
  width: 100%;
  margin: 30px auto;
}

.content-card {
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

/* 文本容器样式 */
.text-container {
  padding: 20px;
  font-size: 18px;
}

.text-container p {
  line-height: 1.8;
  font-size: 22px;
}

.text-container ul {
  font-size: 16px;
  padding-left: 20px;
}

.text-container ul li {
  line-height: 1.8;
  margin-bottom: 8px;
}

.text-container strong {
  color: #da251c; /* 强调文字颜色 */
}

.image-box {
  width: 100%;
  height: 0;
  margin-top: 30%;
  padding-bottom: 100%; /* 创建正方形容器 */
  position: relative;
  overflow: hidden;
}

.food-img {
  position: absolute;
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 8px;
}
</style>

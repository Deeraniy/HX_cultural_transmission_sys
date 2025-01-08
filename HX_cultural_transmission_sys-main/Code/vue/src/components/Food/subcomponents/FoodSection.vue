<template>
  <div>
    <!-- 卡片容器 -->
    <el-card class="content-card" :body-style="{ padding: '20px' }">
      <div class="section-title">
        湘菜韵味<br />
        <span>—— The Essence of Hunan Cuisine ——</span>
      </div>

      <!-- 使用 el-row 和 el-col 布局 -->
      <el-row gutter={30}>
        <!-- 第一列 -->
        <el-col :span="8">
          <el-card class="food-item">
            <el-image
                class="image-container"
                :src=food3
                alt="臭豆腐"
                fit="contain"
            />
            <div class="description-container">
              <div class="item-title">臭豆腐</div>
              <p>臭豆腐是湖南的传统小吃，外皮酥脆，内里软嫩，味道独特。具有开胃消食、增进食欲的功效，同时含有丰富的蛋白质和维生素。</p>
            </div>
          </el-card>
        </el-col>

        <!-- 第二列 -->
        <el-col :span="8">
          <el-card class="food-item">
            <el-image
                class="image-container"
                :src=food4
                alt="攸县香干"
                fit="contain"
            />
            <div class="description-container">
              <div class="item-title item-title-secondary">攸县香干</div>
              <p>攸县香干是湖南省攸县的传统食品，口感香脆，味道鲜美。具有健脾开胃、清热解毒的功效，适合多种烹饪方式。</p>
            </div>
          </el-card>
        </el-col>

        <!-- 第三列 -->
        <el-col :span="8">
          <el-card class="food-item">
            <el-image
                class="image-container"
                :src=food1
                alt="糖油粑粑"
                fit="contain"
            />
            <div class="description-container">
              <div class="item-title item-title-secondary">糖油粑粑</div>
              <p>糖油粑粑是湖南的传统小吃，外皮酥脆，内里软糯，甜而不腻。具有滋补养颜、健脾开胃的功效，是冬季的佳品。</p>
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
</script>

<style scoped>

.section-title {
  font-size: 50px;
  font-weight: bolder;
  width: 100%;
  text-align: center;
  line-height: 60px;
  font-family: Verdana, Geneva, sans-serif;
}

.section-title span {
  color: #8aaa3d;
  font-size: 16px;
  font-family: Arial, Helvetica, sans-serif;
  line-height: 60px;
}

/* 卡片容器 */
.content-card {
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

/* 图片容器样式 */
.image-container {
  width: 100%;
  height: 200px;
  overflow: hidden;
  border-radius: 8px;
}

.description-container {
  height: 250px;
  background: #eeeeee;
  padding: 20px 30px;
  margin-top: 15px;
  text-align: center;
}

.description-container .item-title {
  color: #80b50f;
  font-size: 18px;
  font-weight: bold;
  height: 60px;
  border-bottom: #b9b9b9 1px solid;
  margin-bottom: 10px;
}

.description-container .item-title-secondary {
  color: #80b50f;
  font-size: 18px;
  font-weight: bold;
  height: 60px;
  border-bottom: #b9b9b9 1px solid;
  margin-bottom: 10px;
}

.description-container p {
  font-size: 16px;
  line-height: 25px;
}

/* 自适应布局 */
.food-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.el-card {
  margin-bottom: 30px;
}
</style>

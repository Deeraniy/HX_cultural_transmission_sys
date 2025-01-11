<template>
  <div class="whole">
    <div class="total">
      <!-- 固定显示的标题，不作为菜单项 -->
      <h2 class="fixed-title">非遗民俗分析界面</h2>

      <!-- 菜单区域 -->
      <el-menu
          :default-active="activeIndex"
          class="el-menu-demo"
          mode="horizontal"
          :ellipsis="false"
          @select="handleSelect"
      >
        <el-menu-item index="2">情感分析与预测</el-menu-item>
        <el-menu-item index="3">传播策略生成</el-menu-item>
        <el-menu-item index="4">风景名胜3D展示</el-menu-item>
        <el-menu-item index="5">社交分享信息展示</el-menu-item>
        <el-menu-item index="6">沉浸式故事叙述</el-menu-item>
        <el-sub-menu index="1">
          <template #title>
            <span class="work">工作台</span>
          </template>
          <el-menu-item index="1-1">item one</el-menu-item>
          <el-menu-item index="1-2">item two</el-menu-item>
          <el-menu-item index="1-3">item three</el-menu-item>
          <el-sub-menu index="1-4">
            <template #title>item four</template>
            <el-menu-item index="1-4-1">item one</el-menu-item>
            <el-menu-item index="1-4-2">item two</el-menu-item>
            <el-menu-item index="1-4-3">item three</el-menu-item>
          </el-sub-menu>
        </el-sub-menu>
      </el-menu>
    </div>
    <el-main>
      <div style="display: flex;height: 100% ">
        <div style="flex-grow: 1; justify-content: center; align-items: center;width: 100%">
          <div>
            我是文化作品名称
          </div>

          <div v-show="activeIndex === '2'" class="评分图" id="scoreChart" ></div>
          <div v-show="activeIndex === '1'" class="词云图" id="wordCloudChart" ></div>
          <div v-show="activeIndex === '3'" class="情感占比图" id="emotionRatioChart" ></div>
          <div v-show="activeIndex === '4'" class="情感变化趋势图" id="emotionTrendChart" ></div>

          <div v-show="activeIndex === '5'" class="热门评论">
            <h3>热门评论</h3>
            <el-card v-for="(comment, index) in hotComments" :key="index" class="comment-card">
              <div>{{ comment.user }}</div>
              <p>{{ comment.content }}</p>
            </el-card>
          </div>

          <!-- 智能分析区 -->
          <div v-show="activeIndex === '6'" class="智能分析">
            <h3>智能分析</h3>
            <div class="analysis-container">
              <p>大模型分析结果将在这里展示。</p>
            </div>
          </div>









        </div>
        <div style="flex-grow: 1; display: flex; justify-content: flex-end; align-items: center;width: 500px">
<!--          轮盘菜单-->
          <div style="border-top-left-radius: 1000px; border-bottom-left-radius: 1000px; position: relative; display: flex; flex-direction: column; align-items: flex-end; margin-top: 10px; width: 300px; background-image: url(src/assets/folkCustom/纹理6.jpg);">
            <div style="margin-bottom: 15px; text-align: right; margin-right: 5px;" @click="activeIndex = '2'">
              <img src="@/assets/folkCustom/用户趋势.png" alt="" style="width: 40px; height: 40px;"/>
              <p style="margin: 5px 0 0; font-size: 14px; color: #333;">情感趋势图</p>
            </div>
            <div style="margin-bottom: 15px; text-align: right; margin-right: 100px;" @click="activeIndex = '3'">
              <img src="@/assets/folkCustom/服务评分模板.png" alt="" style="width: 40px; height: 40px;"/>
              <p style="margin: 5px 0 0; font-size: 14px; color: #333;">评分图</p>
            </div>
            <div style="margin-bottom: 15px; text-align: right; margin-right: 200px;" @click="activeIndex = '4'">
              <img src="@/assets/folkCustom/智能分析＊.png" alt="" style="width: 40px; height: 40px;"/>
              <p style="margin: 5px 0 0; font-size: 14px; color: #333;">智能分析</p>
            </div>
            <div style="margin-bottom: 15px; text-align: right; margin-right: 200px; margin-top: 30px;" @click="activeIndex = '5'">
              <img src="@/assets/folkCustom/词云图.png" alt="" style="width: 40px; height: 40px;"/>
              <p style="margin: 5px 0 0; font-size: 14px; color: #333;">词云图</p>
            </div>
            <div style="margin-bottom: 15px; text-align: right; margin-right: 100px; margin-top: 20px;" @click="activeIndex = '6'">
              <img src="@/assets/folkCustom/饼图.png" alt="" style="width: 40px; height: 40px;"/>
              <p style="margin: 5px 0 0; font-size: 14px; color: #333;">情感占比图</p>
            </div>
            <div style="margin-bottom: 15px; text-align: right; margin-right: 5px;" @click="activeIndex = '1'">
              <img src="@/assets/folkCustom/评论.png" alt="" style="width: 40px; height: 40px;"/>
              <p style="margin: 5px 0 0; font-size: 14px; color: #333;">评论区</p>
            </div>
          </div>
        </div>
      </div>
    </el-main>
  </div>


</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue';
import * as echarts from 'echarts';

const hotComments = ref([
  { user: '用户A', content: '这部作品让我印象深刻！' },
  { user: '用户B', content: '文化与现代的结合非常新颖！' },
  { user: '用户C', content: '希望看到更多类似的内容。' },
]);
// 初始化图表函数
const initChart = (id: string, options: echarts.EChartsOption) => {
  const chartDom = document.getElementById(id);
  if (chartDom) {
    const chart = echarts.init(chartDom);
    chart.setOption(options);
    return chart;
  }
};

const activeIndex = ref('2');
const handleSelect = (key: string, keyPath: string[]) => {
  console.log(key, keyPath);
};

onMounted(() => {
  // 评分图
  initChart('scoreChart', {
    title: { text: '评分图' },
    tooltip: {},
    xAxis: { data: ['A', 'B', 'C', 'D'] },
    yAxis: {},
    series: [{ type: 'bar', data: [5, 20, 36, 10] }],
  });

  // 词云图
  initChart('wordCloudChart', {
    title: { text: '词云图' },
    tooltip: {},
    series: [
      {
        type: 'wordCloud',
        shape: 'circle',
        data: [
          { name: '文化', value: 100 },
          { name: '民俗', value: 80 },
          { name: '分析', value: 60 },
          { name: '非遗', value: 50 },
        ],
      },
    ],
  });

  // 情感占比图
  initChart('emotionRatioChart', {
    title: { text: '情感占比图' },
    tooltip: {},
    series: [
      {
        type: 'pie',
        data: [
          { value: 40, name: '积极' },
          { value: 30, name: '中立' },
          { value: 30, name: '消极' },
        ],
      },
    ],
  });

  // 情感变化趋势图
  initChart('emotionTrendChart', {
    title: { text: '情感变化趋势图' },
    tooltip: {},
    xAxis: { data: ['1月', '2月', '3月', '4月'] },
    yAxis: {},
    series: [{ type: 'line', data: [10, 22, 30, 40] }],
  });
});
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
#scoreChart,
#wordCloudChart,
#emotionRatioChart,
#emotionTrendChart {
  width: 800px;
  height: 600px;
  margin-left: 50px;
}

/* 固定标题样式 */
.fixed-title {
  color: #fff8f0;
  font-family: 'HelveticaNeue', serif;
  font-size: 45px;
  margin: 0 16px;
}

/* 菜单样式 */
.el-menu-demo {
  display: flex; /* 使用 flex 布局 */
  justify-content: flex-end;   /* 菜单项靠右对齐 */
  background-color: transparent !important; /* 将菜单背景设为透明 */
  box-shadow: none; /* 移除默认阴影（如果有的话） */
  padding-right: 20px;
  border-bottom-left-radius: 30px; /* 左下圆角 */
  border-bottom-right-radius: 30px; /* 右下圆角 */
  box-shadow: none;
}

/* 覆盖菜单项文字样式 */
.el-menu-item {
  color: #fff8f0 !important;
  font-size: 20px;
  font-family: 'HelveticaNeue', serif !important;
}

/* 选中和悬停菜单项的颜色和背景 */
.el-menu-item.is-active,
.el-menu-item:hover {
  color: #ffd700 !important; /* 设置选中和悬停状态的文字颜色为金色 */
  background-color: rgba(255, 255, 255, 0.2) !important; /* 透明度为20%的淡色背景 */
  border-bottom: 2px solid #ffd700; /* 添加选中和悬停菜单项的下边框 */
}

/* 覆盖“工作台”标题样式 */
.el-sub-menu >>> .el-sub-menu__title {
  color: #fff8f0 !important;
  font-family: 'HelveticaNeue', serif !important;
}

/* 子菜单的悬停和选中样式 */
.el-sub-menu__title:hover,
.el-sub-menu__title.is-active {
  color: #ffd700 !important;
  background-color: rgba(255, 255, 255, 0.2) !important;
}
</style>

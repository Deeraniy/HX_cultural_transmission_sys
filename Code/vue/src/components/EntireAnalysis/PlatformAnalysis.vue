<template>
  <div class="whole">
    <el-main>
      <div style="display: flex;height: 100%">
        <div style="flex-grow: 1; justify-content: center; align-items: center;width: 100%">
          <div>
            我是文化作品名称
          </div>

          <!-- 使用 LineRace 组件替代情感趋势图 -->
          <div v-if="activeIndex === '2'" class="评分图">
            <LineRace :timeData="timeData" />
          </div>
          <div v-show="activeIndex === '1'" class="词云图" id="wordCloudChart"></div>
          <div v-show="activeIndex === '3'" class="情感占比图" id="emotionRatioChart"></div>
          <div v-show="activeIndex === '4'" class="情感变化趋势图" id="emotionTrendChart"></div>

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
          <!-- 轮盘菜单 -->
          <div style="border-top-left-radius: 1000px; border-bottom-left-radius: 1000px; position: relative; display: flex; flex-direction: column; align-items: flex-end; margin-top: 10px; width: 300px; background-image: url(src/assets/folkCustom/纹理6.jpg);">
            <div style="margin-bottom: 15px; text-align: right; margin-right: 5px;" @click="activeIndex = '2'">
              <img src="@/assets/folkCustom/用户趋势.png" alt="" style="width: 40px; height: 40px;"/>
              <p style="margin: 5px 0 0; font-size: 14px; color: #333;">情感趋势图</p>
            </div>
            <div style="margin-bottom: 18px; text-align: right; margin-right: 130px;" @click="activeIndex = '3'">
              <img src="@/assets/folkCustom/服务评分模板.png" alt="" style="width: 40px; height: 40px;"/>
              <p style="margin: 5px 0 0; font-size: 14px; color: #333;">评分图</p>
            </div>
            <div style="margin-bottom: 15px; text-align: right; margin-right: 200px;" @click="activeIndex = '4'">
              <img src="@/assets/folkCustom/智能分析＊.png" alt="" style="width: 40px; height: 40px;"/>
              <p style="margin: 5px 0 0; font-size: 14px; color: #333;">智能分析</p>
            </div>
            <div style="margin-bottom: 15px; text-align: right; margin-right: 200px; margin-top: 60px;" @click="activeIndex = '5'">
              <img src="@/assets/folkCustom/词云图.png" alt="" style="width: 40px; height: 40px;"/>
              <p style="margin: 5px 0 0; font-size: 14px; color: #333;">词云图</p>
            </div>
            <div style="margin-bottom: 5px; text-align: right; margin-right: 130px; margin-top: 30px;" @click="activeIndex = '6'">
              <img src="@/assets/folkCustom/饼图.png" alt="" style="width: 40px; height: 40px;"/>
              <p style="margin: 5px 0 0; font-size: 14px; color: #333;">情感占比图</p>
            </div>
            <div style="margin-bottom: 0px; text-align: right; margin-right: 15px;" @click="activeIndex = '1'">
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
import { ref, onMounted, nextTick } from 'vue';
import LineRace from '@/components/EntireAnalysis/subcomponent/LineRace.vue'; // 引入 LineRace 组件
import * as echarts from 'echarts';

const activeIndex = ref('2');
const hotComments = ref([
  { user: '用户A', content: '这部作品让我印象深刻！' },
  { user: '用户B', content: '文化与现代的结合非常新颖！' },
  { user: '用户C', content: '希望看到更多类似的内容。' },
]);

// 模拟 timeData 数据
const timeData = [
  { date: '2024-01-01', xiaohongshuSentimentScore: 0.8, douyinSentimentScore: 0.7, weiboSentimentScore: 0.9, bilibiliSentimentScore: 0.85 },
  { date: '2024-01-02', xiaohongshuSentimentScore: 0.75, douyinSentimentScore: 0.65, weiboSentimentScore: 0.88, bilibiliSentimentScore: 0.80 },
  { date: '2024-01-03', xiaohongshuSentimentScore: 0.72, douyinSentimentScore: 0.68, weiboSentimentScore: 0.85, bilibiliSentimentScore: 0.78 },
  { date: '2024-01-04', xiaohongshuSentimentScore: 0.78, douyinSentimentScore: 0.74, weiboSentimentScore: 0.90, bilibiliSentimentScore: 0.82 },
  { date: '2024-01-05', xiaohongshuSentimentScore: 0.80, douyinSentimentScore: 0.76, weiboSentimentScore: 0.92, bilibiliSentimentScore: 0.84 },
  { date: '2024-01-06', xiaohongshuSentimentScore: 0.85, douyinSentimentScore: 0.79, weiboSentimentScore: 0.94, bilibiliSentimentScore: 0.88 },
  { date: '2024-01-07', xiaohongshuSentimentScore: 0.82, douyinSentimentScore: 0.77, weiboSentimentScore: 0.93, bilibiliSentimentScore: 0.86 },
];



// 初始化图表函数
function initChart(id: string, options: any) {
  const chartContainer = document.getElementById(id);
  if (chartContainer) {
    const chart = echarts.init(chartContainer as HTMLElement);
    chart.setOption(options);
  } else {
    console.warn(`Chart container with id ${id} not found.`);
  }
}

onMounted(() => {
  nextTick(() => {
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


<style scoped lang="scss">
@import '@/assets/font/font.css';
#app {
  height: 100vh;
  margin: 0;
}

.el-main {
  margin-top: 80px;
  --el-main-padding: 0;
}

.hunan-tourist-attractions {
  background-size: cover;
  background-repeat: no-repeat;
  background-position: center;
}

.attraction-container {
  height: 600px;
  position: relative;
  display: flex; /* 使用 flex 布局 */
  flex-direction: row; /* 保证图片和文字并排显示 */
  width: 100%;
  //height: 100%; /* 保证容器占满屏幕 */
  background-image: url('@/assets/BookB.png');
}

.attraction-container::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(255, 255, 255, 0.2); /* 半透明白色，透明度可调 */
  z-index: -1; /* 确保覆盖层在背景图和文本下面 */
}

.scroll-bar {
  width: 100%;
  height: 40px; /* 增加滚动条高度 */
  background-color: #B71C1C64; /* 淡红色 */
  position: absolute;
  top: 0; /* 确保它固定在容器顶部 */
  z-index: 10; /* 保证滚动条位于最上层 */
  display: flex;
  justify-content: center;
  align-items: center;
  color: #fff;
  font-size: 18px; /* 调整字体大小 */
  overflow: hidden; /* 超出部分隐藏 */
}

.scroll-bar-text {
  font-family: 'HelveticaNeue', serif;
  white-space: nowrap; /* 防止文本换行 */
  display: inline-block;
  padding-right: 100%; /* 保证文本宽度足够 */
  animation: scroll-text 20s linear infinite; /* 文字滚动动画 */
}

/* 滚动条的动画效果 */
@keyframes scroll-text {
  0% {
    transform: translateX(100%); /* 初始时，文本在右侧外面 */
  }
  100% {
    transform: translateX(-100%); /* 最终，文本滚动到左侧外面 */
  }
}


.location-box {
  margin-top: 60px;
  font-family: 'HelveticaNeue', serif;
  margin-left: 40px;
  margin-right: 20px;
  width: 650px;
  height: 320px; /* 设置固定高度 */
  border-radius: 8px;

  /* 去掉背景色 */
  background-color: transparent; /* 完全透明的背景 */

  /* 去掉边框和阴影 */
  border: none; /* 去除边框 */
  box-shadow: none; /* 去除阴影 */

  /* 设置右下角背景图片 */
  //background-image: url('@/assets/水墨小人.png');
  background-position: right 10px bottom -10px; /* 向下偏移一点 */
  background-repeat: no-repeat; /* 不重复显示背景 */
  background-size: 200px 250px; /* 将背景图大小调整为 100px */

  /* 保证卡片的内容不受影响，保持完全不透明 */
  opacity: 1; /* 保证内容不透明 */
}

.carousel-image-container {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.carousel-image-container img {
  max-height: 100%;
  width: auto;
  object-fit: contain; /* 保证图片完整显示，避免裁剪 */
}

.pic img {
  width: 100%; /* 让图片填满容器的宽度 */
  height: 100%; /* 让图片填满容器的高度 */
  object-fit: cover; /* 保证图片不变形，填充整个容器 */
}

.s-title {
  margin-left: 10px;
  margin-top: 8px;
  font-size: 34px;
  font-weight: bold;
  color: #fff8f0;
}

.p {
  margin-left: 10px;
  font-size: 26px;
  color: #fff8f0;
  margin-top: 10px;
}

.ts {
  margin-left: 10px;
  font-size: 18px;
  color: #fff8f0;
}

/* 使用 :deep() 来深度修改 el-carousel 的垂直指示器样式 */
.hunan-tourist-attractions :deep(.el-carousel__indicators--vertical li button) {
  width: 10px;          /* 设置指示器的宽度 */
  height: 10px;         /* 设置指示器的高度 */
  border-radius: 50%;   /* 使按钮变圆 */
  background-color: #ccc; /* 设置默认颜色 */
  margin: 4px 0;        /* 上下间距 */
  transition: background-color 0.3s ease; /* 平滑过渡 */
}

/* 修改当前激活状态指示器的样式 */
.hunan-tourist-attractions :deep(.el-carousel__indicators--vertical li.is-active button) {
  background-color: #b71c1c; /* 激活时的颜色 */
}

.el-carousel {
  margin-top: 60px;
  margin-bottom: 20px;
  margin-left: 20px;
  width: 500px;
  height: auto;
}

</style>

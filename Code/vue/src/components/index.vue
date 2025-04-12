<template>
  <el-main>
    <div style="height: 100%">
      <!-- 轮播图 -->
      <el-carousel
          v-model:active-index="activeIndex"
          :autoplay="shouldAutoplay"
          :interval="3000"
          arrow="always"
          style="height: 100%; width: 100%; position: relative;"
      >
        <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; position: relative;">
          <img src="@/assets/index-back3.jpg" alt="Image 3" style="width: 100%; height: 100%; object-fit: cover;" />
          <!-- 添加蒙版和文字 -->
          <div class="carousel-overlay">
            <span class="overlay-text">{{ t('index.title.main') }}</span>
            <span class="overlay-text">{{ t('index.title.sub') }}</span>
          </div>
        </div>
        <!-- 第一个视频项 -->
        <el-carousel-item>
          <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0;">
            <video
                ref="videoElement"
                :src="videoUrl"
                width="100%"
                height="100%"

                autoplay
                muted
                @ended="onVideoEnded"
                style="object-fit: cover; width: 100%; height: 100%;"
            ></video>
          </div>
        </el-carousel-item>

        <!-- 后续图片项 -->
        <el-carousel-item>
          <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0;">
            <img src="@/assets/index-back.jpg" alt="Image 1" style="width: 100%; height: 100%; object-fit: cover;" />
          </div>
        </el-carousel-item>
        <el-carousel-item>
          <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0;">
            <img src="@/assets/index-back2.png" alt="Image 2" style="width: 100%; height: 100%; object-fit: cover;" />
          </div>
        </el-carousel-item>
        <el-carousel-item>
          <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0;">
            <img src="@/assets/index-back3.jpg" alt="Image 3" style="width: 100%; height: 100%; object-fit: cover;" />
          </div>
        </el-carousel-item>
      </el-carousel>

      <!-- 添加我们的功能区块 -->
      <FeaturesSection />

<!--      这里是知识图谱-->
      <div class="knowledge-graph">
        <div ref="chart" style="height: 800px; width: 100%;"></div>
        <div>
          <el-input
              v-model="searchTerm"
              placeholder="输入节点名称搜索"
              clearable
              @input="handleSearch"
          >
            <template #prefix>
              <el-icon><search /></el-icon>
            </template>
          </el-input>
        </div>
      </div>
<!--      这里显示节点详情-->
      <div class="node-detail" v-if="selectedNode">
        <div class="detail-header">
          <h3>{{ selectedNode.name }}</h3>

        </div>
        <div class="detail-content">
          <div v-if="selectedNode.properties">
            <div v-for="key in filteredPropertyKeys" :key="key">
              <strong>{{ propertyMap[key] || key }}：</strong>
              <template v-if="key === 'image_url' || key === 'img_url'">
                <img
                    :src="selectedNode.properties[key]"
                    :alt="propertyMap[key]"
                    style="max-width: 200px; height: auto; margin-top: 8px; border-radius: 4px;"
                >
              </template>
              <!-- 其他属性处理 -->
              <template v-else>
                <span>{{ selectedNode.properties[key] || '暂无数据' }}</span>
              </template>
            </div>

          </div>
          <div v-else>
            该节点暂无更多详细信息
          </div>
        </div>
        <el-button class="close-btn" @click="selectedNode = null" circle>×</el-button>
        <el-button @click="handleViewDetail">查看详情</el-button>
      </div>

      <!-- 替换原有block4跳转 -->
      <footer class="site-footer">
        <div class="footer-container">
          <div class="footer-section about">
            <h3>{{ t('index.footer.about.title') }}</h3>
            <p>{{ t('index.footer.about.content') }}</p>
          </div>

          <div class="footer-section links">
            <h3>{{ t('index.footer.quickLinks.title') }}</h3>
            <ul>
              <li><a href="#/folkCustom">{{ t('index.footer.quickLinks.folkCustom') }}</a></li>
              <li><a href="#/placeOfInterest">{{ t('index.footer.quickLinks.placeOfInterest') }}</a></li>
              <li><a href="#/red">{{ t('index.footer.quickLinks.redCulture') }}</a></li>
              <li><a href="#/filmLiterature">{{ t('index.footer.quickLinks.filmLiterature') }}</a></li>
              <li><a href="#/food">{{ t('index.footer.quickLinks.food') }}</a></li>
              <li><a href="#/globe">{{ t('index.footer.quickLinks.globalAnalysis') }}</a></li>
              <li><a href="#/detail">{{ t('index.footer.quickLinks.sentimentAnalysis') }}</a></li>
              <li><a href="#/report">{{ t('index.footer.quickLinks.strategy') }}</a></li>
            </ul>
          </div>

          <div class="footer-section data-support">
            <h3>{{ t('index.footer.dataSupport.title') }}</h3>
            <p>{{ t('index.footer.dataSupport.culture') }}</p>
            <p>{{ t('index.footer.dataSupport.cultural') }}</p>
            <p>{{ t('index.footer.dataSupport.heritage') }}</p>
            <p>{{ t('index.footer.dataSupport.museum') }}</p>
          </div>

          <div class="footer-section contact">
            <h3>{{ t('index.footer.contact.title') }}</h3>
            <p><i class="el-icon-location"></i> {{ t('index.footer.contact.address') }}</p>
            <p><i class="el-icon-phone"></i> {{ t('index.footer.contact.phone') }}</p>
            <p><i class="el-icon-message"></i> {{ t('index.footer.contact.email') }}</p>
          </div>
        </div>

        <div class="footer-bottom">
          <p>{{ t('index.footer.copyright.text') }}</p>
          <p>{{ t('index.footer.copyright.support') }}</p>
        </div>
      </footer>

    </div>
  </el-main>

</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, computed } from 'vue';
import { useI18n } from 'vue-i18n';
import {ref, onMounted, onBeforeUnmount, computed} from 'vue';
import IndexMain from "@/components/IndexMain.vue";
import FeaturesSection from "@/components/Home/FeaturesSection.vue";
import HuXiangCuisine from "@/components/Home/HuXiangCuisine.vue";
// 使用 import 语法加载视频文件
import videoFile from '@/assets/湖南形象宣传片国际版《This is Hunan》.mp4';
import data from '../../static/data.json'
import { useRouter } from 'vue-router'
const router = useRouter()
const activeIndex = ref(0); // 当前轮播项的索引
const videoUrl = ref(videoFile); // 将视频路径赋值给变量
const shouldAutoplay = ref(false); // 控制是否自动播放轮播图
let carouselTimer = null; // 用于存储定时器
// 视频播放结束后的回调
// 视频播放结束后的处理
import { Search } from '@element-plus/icons-vue'
import * as echarts from 'echarts';
const chart = ref(null);
const selectedNode = ref(null);
const searchTerm = ref('');
const propertyMap = {
  food_name: '菜品名称',
  folk_name: '民俗名称',
  spot_name: '景点名称',
  city_id: '所属城市',
  folk_type: '民俗类型',
  address: '详细地址',
  image_url: '图片',
  opening_hours: '开放时间',
  cuisine_type: '菜系类型',
  author: '作者',
  img_url: '图片',
  text: '简要描述',
  publish_year: '出版年份'
};
const filterMap = {

const { t, locale } = useI18n();

// 根据语言环境返回不同的字体大小
const titleFontSize = computed(() => {
  return locale.value === 'en' ? '8rem' : '14rem';
});

  folk_id: true,
  food_id: true,
  literature_id: true,
  spot_id: true,    // 过滤图片URL
  city_id: true,      // 过滤城市ID
  description_url: true,
};
let myChart = null;

const filteredPropertyKeys = computed(() => {
  if (!selectedNode.value?.properties) return [];
  return Object.keys(selectedNode.value.properties)
      .filter(key => !filterMap[key]);
});
const onVideoEnded = () => {
  console.log('视频播放结束');
  shouldAutoplay.value = true; // 启用轮播
  activeIndex.value = 1; // 切换到第二项
  startCarousel(); // 开始轮播
};
const processData = (rawData, searchTerm = '') => {
  const categories = [
    { name: t('index.knowledgeGraph.categories.core') },
    { name: t('index.knowledgeGraph.categories.theme') },
    { name: t('index.knowledgeGraph.categories.spot') },
    { name: t('index.knowledgeGraph.categories.literature') },
    { name: t('index.knowledgeGraph.categories.food') },
    { name: t('index.knowledgeGraph.categories.folk') }
    { name: '核心文化' },
    {name: '主题分类'},
    {name: '景点'},
    {name: '文学'},
    {name: '饮食'},
    {name: '民俗'}
  ];

  let nodes = [];
  const coreNode = rawData.data.find(item => item.type === "Core");

  // 核心节点始终显示
  nodes.push({
    id: coreNode.id,
    name: coreNode.name,
    category: 0,
    symbolSize: 50,
    isMatched: true
  });

  rawData.data.forEach(item => {
    if (item.type !== "Core") {
      const isMatched = item.name.toLowerCase().includes(searchTerm.toLowerCase());
      let categoryIndex = 1;
      switch (item.categories || item.type) {
        case 'Theme': categoryIndex = 1; break;
        case 'Spot': categoryIndex = 2; break;
        case 'Literature': categoryIndex = 3; break;
        case 'Food': categoryIndex = 4; break;
        case 'Folk': categoryIndex = 5; break;
      }

      nodes.push({
        id: item.id,
        name: item.name,
        category: categoryIndex,
        isMatched,
        symbolSize: categoryIndex === 1 ? (isMatched ? 45 : 35) : (isMatched ? 35 : 25)
      });

      // 处理景点时生成对应的城市节点

    }
  });

  // 过滤出isMatched为true的节点
  const filteredNodes = nodes.filter(node => node.isMatched);

  // 生成所有可能的链接
  let links = [];
  if (rawData.links) {
    rawData.links.forEach(link => {
      links.push({
        source: link.source,
        target: link.target,
        name: link.name // 直接使用JSON中的name
      });
    });
  }
  rawData.data.forEach(item => {
    if (item.type === 'Theme') {
      links.push({ source: coreNode.id, target: item.id });
    }
    if (item.categories === 'Spot' && item.properties?.city_id) {
      const cityId = `city_${item.properties.city_id}`;
      links.push({ source: cityId, target: item.id });
    }
  });

  // 过滤链接，确保source和target都存在
  const filteredLinks = links.filter(link => {
    const sourceExists = filteredNodes.some(n => n.id === link.source);
    const targetExists = filteredNodes.some(n => n.id === link.target);
    return sourceExists && targetExists;
  });

  return { nodes: filteredNodes, links: filteredLinks, categories };
};

const initChart = () => {
  myChart = echarts.init(chart.value);
  const graphData = processData(data);

  // 颜色映射数组（索引对应分类）
  const colorPalette = [
    '#5470c6', // 0:核心文化
    '#91cc75', // 1:主题分类
    '#fac858', // 2:景点
    '#73c0de', // 3:文学
    '#ee6666', // 4:饮食
    '#3ba272'  // 5:民俗
  ];
  const option = {
    title: {
      text: t('index.knowledgeGraph.title'),
      top: 20,
      left: 'center'
    },
    tooltip: {},
    legend: {
      data: graphData.categories.map(c => c.name),
      selected: {
        '核心文化': true,
        '主题分类': false,
        '景点': false,
        '文学': false,
        '饮食': false,
        '民俗': false
      },
      top: 50
    },
    series: [{
      type: 'graph',
      layout: 'force',
      force: {
        repulsion: 200,
        edgeLength: 100,
        gravity: 0.1
      },
      draggable: true,
      data: graphData.nodes.map(node => ({
        ...node,
        itemStyle: {
          color: colorPalette[node.category] // 根据节点分类设置颜色
        }
      })),
      links: graphData.links.map(link => ({
        source: link.source,
        target: link.target,
        label: {
          show: true,
          formatter: link.name,  // 显示连接名称
          fontSize: 12,
          color: '#666',
          position: 'middle'     // 标签显示在线条中间
        }
      })),
      categories: graphData.categories,
      edgeSymbol: ['none', 'arrow'],
      edgeSymbolSize: [0, 10],
      label: {
        show: true,
        position: 'right',
        fontSize: 12
      },
      lineStyle: {
        color: '#aaa',
        curveness: 0.2
      },
      emphasis: {
        focus: 'adjacency',
        label: {
          show: true,
          fontSize: 14
        }
      },
      itemStyle: {
        color:"#333",

      }
    }]
  };

  myChart.setOption(option);
  myChart.on('click', params => {
    if (params.dataType === 'node') {
      const rawNode = data.data.find(item => item.id === params.data.id);
      selectedNode.value = {
        ...params.data,
        properties: rawNode?.properties || {},
        type: rawNode?.type || determineNodeType(rawNode)
      };
    }
  });
  const determineNodeType = (rawNode) => {
    if (rawNode.properties.spot_id) return 'spot'
    if (rawNode.properties.food_id) return 'food'
    if (rawNode.properties.folk_id) return 'folk'
    if (rawNode.properties.literature_id) return 'literature'
    return 'other'
  }
  window.addEventListener('resize', () => myChart.resize());
};
const handleSearch = () => {

  updateChart(searchTerm.value);
};
const handleViewDetail = () => {
  if (!selectedNode.value) return

  const node = selectedNode.value
  let routeParams = {
    name: node.name,
    value: 1,  // 默认值
    theme: 1    // 默认主题
  }

  // 根据节点类型设置参数
  switch(node.type) {
    case 'spot':
      routeParams.value = 1
      break
    case 'food':
      routeParams.value = 3
      break
    case 'folk':
      routeParams.value = 4
      break
    case 'literature':
      routeParams.value = 2
      // 文学类型需要子主题，这里假设数据中有subTheme属性
      routeParams.theme = node.properties.subThemeId || 1
      break
    default:
      routeParams.value = 1
  }
    if(node.type === 'spot' || node.type === 'food' || node.type === 'folk' || node.type === 'literature'){
      router.push({
        path: '/detail',
        query: routeParams
      })
    }

}
const updateChart = () => {
  console.log("搜索词：", searchTerm.value)
  const graphData = processData(data, searchTerm.value)
  console.log("更新后的数据：", graphData)
  const colorPalette = [
    '#5470c6', // 0:核心文化
    '#91cc75', // 1:主题分类
    '#fac858', // 2:景点
    '#73c0de', // 3:文学
    '#ee6666', // 4:饮食
    '#3ba272'  // 5:民俗
  ];
  const option = {
    title: {
      text: '湖湘文化知识图谱',
      top: 20,
      left: 'center'
    },
    tooltip: {},
    legend: {
      data: graphData.categories.map(c => c.name),
      selected: {
        '核心文化': true,
        '主题分类': false,
        '景点': false,
        '文学': false,
        '饮食': false,
        '民俗': false
      },
      top: 50
    },
    series: [{
      type: 'graph',
      layout: 'force',
      force: {
        repulsion: 200,
        edgeLength: 100,
        gravity: 0.1
      },
      draggable: true,
      data: graphData.nodes.map(node => ({
        ...node,
        itemStyle: {
          color: colorPalette[node.category] // 根据节点分类设置颜色
        }
      })),
      links: graphData.links.map(link => ({
        source: link.source,
        target: link.target,
        label: {
          show: true,
          formatter: link.name,  // 显示连接名称
          fontSize: 12,
          color: '#666',
          position: 'middle'     // 标签显示在线条中间
        }
      })),
      categories: graphData.categories,
      edgeSymbol: ['none', 'arrow'],
      edgeSymbolSize: [0, 10],
      label: {
        show: true,
        position: 'right',
        fontSize: 12
      },
      lineStyle: {
        color: '#aaa',
        curveness: 0.2
      },
      emphasis: {
        focus: 'adjacency',
        label: {
          show: true,
          fontSize: 14
        }
      },
      itemStyle: {
        color:"#333",

      }
    }]
  };

  myChart.setOption(option);
};

// 修改后的搜索处理

// 开始轮播的函数
const startCarousel = () => {
  if (carouselTimer) clearInterval(carouselTimer);

  carouselTimer = setInterval(() => {
    if (activeIndex.value === 0) {
      // 如果回到视频项，停止轮播
      clearInterval(carouselTimer);
      shouldAutoplay.value = false;
      return;
    }
    activeIndex.value = (activeIndex.value + 1) % 4;
  }, 3000);
};

// 组件卸载前清理定时器
onBeforeUnmount(() => {
  if (carouselTimer) {
    clearInterval(carouselTimer);
  }
});
// 手动切换到下一个项
// 组件挂载时初始化
const iframeRef = ref(null);

// 动态设置 iframe 高度
onMounted(() => {
  initChart();
  shouldAutoplay.value = false;


  // 窗口大小变化时自适应

  // 监听 iframe 加载完成
  if (iframeRef.value) {
    iframeRef.value.onload = () => {
      try {
        // 获取 iframe 内容的实际高度
        const height = iframeRef.value.contentWindow.document.documentElement.scrollHeight;
        iframeRef.value.style.height = `1800px`;
      } catch (e) {
        console.error('设置 iframe 高度失败:', e);
      }
    };
  }
});

</script>

<style scoped>
@import '@/assets/font/font.css';
.carousel-overlay {
  position: absolute;
  top: -30px;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5); /* 半透明黑色蒙版 */
  display: flex;
  flex-direction: column; /* 改为纵向排列 */
  justify-content: center;
  align-items: center;
  z-index: 2;
}

.node-detail {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 400px;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.15);
  z-index: 9999;
  padding: 20px;
}
.overlay-text {
  font-family: 'HelveticaNeue', serif;
  color: white;
  font-size: v-bind(titleFontSize);
  font-weight: bold;
  text-align: center;
  padding: 0px;
  line-height: 1.2; /* 控制行间距 */
  display: block; /* 确保每个文本块独占一行 */
  margin-top: -30px; /* 调整上边距，使两行文字更紧凑 */
}

/* 为第一行文字添加特殊样式 */
.overlay-text:first-child {
  margin-top: -250px; /* 保持原来的上边距 */
}

html, body {
  margin: 0;
  padding: 0;
  overflow: hidden !important; /* 强制禁止滚动 */
  height: 100% !important;
  width: 100% !important;
}

* {
  -ms-overflow-style: none;  /* IE 和 Edge */
  scrollbar-width: none;  /* Firefox */
}
.main-container {
  width: 100%;
  display: flex;
  overflow: hidden; /* 禁止滚动 */
  flex-direction: column;
}
/* 覆盖 element-plus 的默认样式 */

:deep(.el-main.el-main) {
  overflow: hidden !important;
  padding: 0 !important;
  height: 100% !important;
}

/* 或者使用属性选择器增加优先级 */
:deep([class*="el-main"]) {
  overflow: hidden !important;
  padding: 0 !important;
  height: 100% !important;
}

/* 如果还不行，可以尝试使用多重选择器 */
:deep(.el-container .el-main) {
  overflow: hidden !important;
  padding: 0 !important;
  height: 100% !important;
}

/* 隐藏滚动条 */
:deep(.el-main::-webkit-scrollbar) {
  width: 8px; /* 定义滚动条宽度 */
  height: 8px;
  background-color: transparent; /* 滚动条背景颜色 */
}

:deep(.el-main::-webkit-scrollbar-thumb) {
  background-color: transparent; /* 滚动条滑块颜色 */
  border-radius: 4px; /* 滚动条滑块圆角 */
}

:deep(.el-main::-webkit-scrollbar-thumb:hover) {
  background-color: rgba(0, 0, 0, 0.2); /* 鼠标悬停时滚动条滑块颜色 */
}
/* 确保轮播图的容器填满整个屏幕 */
.el-carousel {
  position: relative;
  width: 100%;
  height: 705px !important; /* 强制应用高度 */
  margin: 0 auto;
  overflow: hidden;
}

/* 使用 :deep 强制修改 el-carousel__container 的高度 */
:deep(.el-carousel__container) {
  height: 705px !important; /* 强制设置容器的高度 */
}

/* 每个轮播项的样式 */
.el-carousel-item {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden; /* 确保内容溢出时不会显示 */
}

/* 确保图片和视频填充并覆盖整个容器 */
video, img {
  object-fit: cover; /* 使内容填充容器并裁剪 */
  width: 100%;
  height: 100%;
}
video {
  object-fit: cover; /* 使视频填充容器并裁剪 */
  width: 100%;
  height: 100%;
  transform: scale(1.2); /* 稍微放大视频 */
  transform-origin: center center; /* 保持视频从中心放大 */
}

.iframe-section {
  width: 100%;
  height: 2000px; /* 或其他适当的高度 */
}

iframe {
  width: 100%;
  min-height: 100%; /* 至少保持一个视口高度 */
  border: none;
  overflow: hidden; /* 禁止滚动 */
}
html, body {
  margin: 0;
  padding: 0;
  overflow: hidden !important; /* 强制禁止滚动 */
  height: 100% !important;
  width: 100% !important;
}

/* 禁用滚动条 */
::-webkit-scrollbar {
  display: none;
}

* {
  -ms-overflow-style: none;  /* IE 和 Edge */
  scrollbar-width: none;  /* Firefox */
}
.cont{
  color: white;
  max-width: 100px;
  max-height: 100px;
}
.sHoverItem:hover .cont p {
  color: purple;
}

/* 网站页脚样式 */
.site-footer {
  background: linear-gradient(to top,
    rgba(101, 30, 20, 1) 0%,
    rgba(101, 30, 20, 0.9) 30%,
    rgba(101, 30, 20, 0.7) 60%,
    rgba(101, 30, 20, 0.3) 90%,
    rgba(101, 30, 20, 0.0) 100%);
  color: #fff;
  padding: 20px 0 0 0;
  margin-top: 20px;
  position: relative;
}

.footer-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 50px 10px 40px;
  position: relative;
  z-index: 2;
}

.footer-section {
  flex: 1;
  min-width: 200px;
  margin-bottom: 15px;
  padding: 0 10px;
}

.footer-section h3 {
  font-family: 'HelveticaNeue', '汇文明朝体', serif;
  font-size: 18px;
  margin-bottom: 10px;
  padding-bottom: 5px;
  position: relative;
}

.footer-section h3::after {
  content: '';
  position: absolute;
  left: 0;
  bottom: 0;
  width: 40px;
  height: 2px;
  background-color: #f0e8d5;
}

.footer-section p {
  line-height: 1.5;
  margin-bottom: 6px;
  font-size: 13px;
  color: rgba(255, 255, 255, 0.9);
}

.footer-section.links {
  flex: 1.5;
  min-width: 280px;
}

.footer-section.links ul {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 5px 25px;
}

.footer-section.about {
  flex: 1.2;
}

.footer-section.data-support,
.footer-section.contact {
  flex: 1;
}

.footer-section.links a {
  color: rgba(255, 255, 255, 0.9);
  text-decoration: none;
  transition: color 0.3s ease;
  display: inline-block;
  padding: 2px 0;
  font-size: 13px;
}

.footer-section.contact p {
  margin-bottom: 5px;
}

.footer-section.contact i {
  margin-right: 10px;
  color: #f0e8d5;
}

.footer-section.links a:hover {
  color: #fff;
  text-decoration: underline;
}

.footer-section.data-support p {
  margin-bottom: 5px;
}

.footer-bottom {
  background-color: rgba(101, 30, 20, 1);
  text-align: center;
  padding: 10px 0;
  position: relative;
  z-index: 2;
}

.footer-bottom p {
  margin: 3px 0;
  color: rgba(255, 255, 255, 0.8);
  font-size: 12px;
}

/* 增加响应式设计 */
@media (max-width: 992px) {
  .footer-container {
    flex-wrap: wrap;
    padding: 30px 40px 10px 30px;
  }

  .footer-section {
    flex: 0 0 calc(50% - 20px);
    min-width: initial;
    margin-bottom: 20px;
  }

  .site-footer {
    background: linear-gradient(to top,
      rgba(101, 30, 20, 1) 0%,
      rgba(101, 30, 20, 0.9) 40%,
      rgba(101, 30, 20, 0.7) 70%,
      rgba(101, 30, 20, 0.3) 90%,
      rgba(101, 30, 20, 0.0) 100%);
    margin-top: 15px;
  }

  .footer-section.links {
    flex: 0 0 calc(60% - 20px);
  }

  .footer-section.about {
    flex: 0 0 calc(40% - 20px);
  }

  .footer-section.data-support,
  .footer-section.contact {
    flex: 0 0 calc(50% - 20px);
  }
}

@media (max-width: 768px) {
  .footer-container {
    padding: 25px 30px 10px 25px;
  }

  .footer-section h3 {
    font-size: 16px;
    margin-bottom: 8px;
  }
}

@media (max-width: 600px) {
  .footer-section {
    flex: 0 0 100%;
  }

  .footer-container {
    padding: 20px 20px 10px 20px;
  }

  .footer-section p,
  .footer-section.links a {
    font-size: 12px;
    line-height: 1.4;
  }

  .footer-section.links li {
    margin-bottom: 4px;
  }

  .footer-section.links {
    flex: 0 0 100%;
  }

  .footer-section.links ul {
    gap: 4px 10px;
  }
}
</style>


<template>
  <div class="analysis-container">
    <!-- 标题区域 -->
    <div class="header-section">
      <div class="title-wrapper">
        <el-icon><DataAnalysis /></el-icon>
        <span class="main-title">{{ t('user.activity.title') }}</span>
      </div>
      <div class="subtitle">{{ t('user.activity.subtitle') }}</div>
    </div>

    <!-- 图表区域 -->
    <el-card class="chart-card">
      <div class="chart-header">
        <div class="chart-title">
          <h3>{{ t('user.activity.interestChart.title') }}</h3>
          <p class="chart-desc">{{ t('user.activity.interestChart.description') }}</p>
        </div>
        <!-- <div class="chart-actions">
          <el-radio-group v-model="timeRange" size="small">
            <el-radio-button label="week">{{ t('user.activity.interestChart.timeRange.week') }}</el-radio-button>
            <el-radio-button label="month">{{ t('user.activity.interestChart.timeRange.month') }}</el-radio-button>
            <el-radio-button label="year">{{ t('user.activity.interestChart.timeRange.year') }}</el-radio-button>
          </el-radio-group>
        </div> -->
      </div>
      <div id="main" class="chart-container"></div>
    </el-card>
  </div>
</template>

<script setup>
import {onMounted, ref, watchEffect} from 'vue';
import { DataAnalysis } from "@element-plus/icons-vue";
import * as echarts from 'echarts';
import UserAPI from "@/api/user";
import {useUserStore} from "@/stores/user.ts";
import { useI18n } from 'vue-i18n';

const { t } = useI18n();

const SingleHistoryList = ref([]);
const AllHistoryList = ref([]);
const userStore = useUserStore();
const timeRange = ref('month');
const TYPE_MAPPING = {
  placeOfInterest: t('user.activity.chart.categories.placeOfInterest'),
  food: t('user.activity.chart.categories.food'),
  literature: t('user.activity.chart.categories.literature'),
  folk: t('user.activity.chart.categories.folk')
};
const processData = () => {
  // 确保有有效数据
  if (SingleHistoryList.value.length === 0 || AllHistoryList.value.length === 0)
    return null;

  // 处理当前用户数据（优化计算逻辑）
  const currentCounts = Object.fromEntries(
      Object.keys(TYPE_MAPPING).map(type => [
        type,
        SingleHistoryList.value.filter(item => item.type === type).length
      ])
  );

  // 处理所有用户数据（优化性能）
  const userStats = AllHistoryList.value.reduce((acc, item) => {
    const uid = item.uid;
    if (!acc.has(uid)) acc.set(uid, { placeOfInterest:0, food:0, literature:0, folk:0 });
    acc.get(uid)[item.type] += 1;
    return acc;
  }, new Map());

  // 计算平均值（添加容错处理）
  const userCount = userStats.size || 1;
  const averageCounts = Object.fromEntries(
      Object.keys(TYPE_MAPPING).map(type => [
        type,
        Array.from(userStats.values()).reduce((sum, user) => sum + (user[type] || 0), 0) / userCount
      ])
  );

  // 构建动态指标
  const indicator = [];
  const currentData = [];
  const averageData = [];

  Object.entries(TYPE_MAPPING).forEach(([type, name]) => {
    const currentVal = currentCounts[type] || 0;
    const averageVal = averageCounts[type] || 0;
    const maxVal = Math.max(currentVal, averageVal) * 1.5; // 动态调整最大值

    indicator.push({
      name: `${name}\n（当前:${currentVal} 平均:${averageVal.toFixed(1)}）`,
      max: Math.ceil(maxVal) || 1 // 确保最小值
    });

    currentData.push(currentVal);
    averageData.push(averageVal);
  });

  return { indicator, currentData, averageData };
};
// 新增响应式图表更新
let myChart = null;
const updateChart = () => {
  const chartData = processData();
  if (!chartData || !myChart) return;

  // 计算每个指标的最大值，确保数据点不会超出雷达图
  const indicatorMaxValues = [];
  for (let i = 0; i < chartData.currentData.length; i++) {
    // 找出当前值和平均值中的最大值
    const maxVal = Math.max(chartData.currentData[i], chartData.averageData[i]);
    // 为最大值增加20%的余量，并向上取整
    const safeMax = Math.ceil(maxVal * 1.2);
    indicatorMaxValues.push(safeMax === 0 ? 1 : safeMax); // 确保最小值为1
  }

  const option = {
    title: {
      text: t('user.activity.chart.mainTitle'),
      textStyle: {
        fontFamily: 'HelveticaNeue, "Helvetica Neue", Helvetica, Arial, sans-serif',
        fontSize: 16
      }
    },
    legend: {
      data: [t('user.activity.chart.currentPublish'), t('user.activity.chart.averageLevel')],
      textStyle: {
        fontFamily: 'HelveticaNeue, "Helvetica Neue", Helvetica, Arial, sans-serif'
      },
      bottom: 0
    },
    radar: {
      radius: '65%',
      center: ['50%', '50%'],
      splitNumber: 4,
      axisName: {
        show: true,
        fontFamily: 'HelveticaNeue, "Helvetica Neue", Helvetica, Arial, sans-serif'
      },
      splitArea: {
        areaStyle: {
          color: ['rgba(250,250,250,0.1)', 'rgba(240,240,240,0.2)']
        }
      },
      indicator: [
        { name: t('user.activity.chart.categories.placeOfInterest'), max: indicatorMaxValues[0] },
        { name: t('user.activity.chart.categories.food'), max: indicatorMaxValues[1] },
        { name: t('user.activity.chart.categories.literature'), max: indicatorMaxValues[2] },
        { name: t('user.activity.chart.categories.folk'), max: indicatorMaxValues[3] },
      ]
    },
    series: [
      {
        name: t('user.activity.chart.comparisonTitle'),
        type: 'radar',
        symbolSize: 6,
        lineStyle: {
          width: 2
        },
        data: [
          {
            value: chartData.currentData,
            name: t('user.activity.chart.currentPublish'),
            itemStyle: {
              color: '#5470c6'
            },
            areaStyle: {
              color: 'rgba(84,112,198,0.3)'
            }
          },
          {
            value: chartData.averageData,
            name: t('user.activity.chart.averageLevel'),
            itemStyle: {
              color: '#91cc75'
            },
            areaStyle: {
              color: 'rgba(145,204,117,0.3)'
            }
          }
        ]
      }
    ],
    textStyle: {
      fontFamily: 'HelveticaNeue, "Helvetica Neue", Helvetica, Arial, sans-serif'
    }
  };

  myChart.setOption(option);
};
const getHistory = () => {
  // 获取后端文章数据
  const userId = getUserId();
  UserAPI.GetUserHistory(userId).then(res => {
    SingleHistoryList.value = res;
    console.log(t('user.activity.messages.getHistorySuccess'))
    console.log(SingleHistoryList.value)
  });
  UserAPI.GetAllHistory().then(res => {
    AllHistoryList.value = res;
    console.log(t('user.activity.messages.getAllHistorySuccess'))
    console.log(AllHistoryList.value)
  })
}
const getUserId = () => {
  // 首先从 userStore 中获取
  if (userStore.userId) {
    return userStore.userId;
  }

  // 如果 userStore 中没有，尝试从 localStorage 获取
  const userId = localStorage.getItem('userId');
  if (userId) {
    return userId;
  }

  // 如果都没有，返回 null
  console.warn(t('user.activity.messages.userIdMissing'));
  return null;
};
onMounted(async () => {
  const chartDom = document.getElementById('main');
  myChart = echarts.init(chartDom);

  // 初始化加载数据
  await getHistory();

  // 设置响应式更新
  watchEffect(updateChart);

  // 优化resize处理
  let resizeTimer;
  window.addEventListener('resize', () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(() => {
      myChart?.resize();
    }, 200);
  });
});
</script>

<style scoped>
.analysis-container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
  font-family: 'HelveticaNeue', 'Helvetica Neue', Helvetica, Arial, sans-serif;
}

.header-section {
  margin-bottom: 30px;
}

.title-wrapper {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.main-title {
  margin-left: 10px;
  font-size: 24px;
  font-weight: 600;
  color: #303133;
}

.subtitle {
  color: #909399;
  font-size: 14px;
  margin-left: 34px;
}

.chart-card {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  margin-bottom: 30px;
  overflow: hidden;
}

.chart-header {
  padding: 20px 20px 0;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.chart-title h3 {
  margin: 0;
  font-size: 18px;
  color: #303133;
}

.chart-desc {
  margin: 5px 0 0;
  font-size: 13px;
  color: #909399;
}

.chart-container {
  height: 550px;
  padding: 30px;
  font-family: 'HelveticaNeue', 'Helvetica Neue', Helvetica, Arial, sans-serif;
  position: relative;
}

.chart-actions {
  margin-top: 5px;
}

/* 深度选择器修改 element-plus 组件样式 */
:deep(.el-card__body) {
  padding: 0;
  overflow: hidden; /* 防止内容溢出 */
}

:deep(.el-radio-button__inner) {
  padding: 8px 15px;
  font-family: 'HelveticaNeue', 'Helvetica Neue', Helvetica, Arial, sans-serif;
}

/* 响应式布局 */
@media screen and (max-width: 768px) {
  .analysis-container {
    padding: 10px;
  }

  .chart-header {
    flex-direction: column;
    gap: 15px;
  }

  .chart-container {
    height: 400px;
  }
}
</style>

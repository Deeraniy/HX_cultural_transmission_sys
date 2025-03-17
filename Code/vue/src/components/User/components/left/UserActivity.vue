<template>
  <div class="analysis-container">
    <!-- 标题区域 -->
    <div class="header-section">
      <div class="title-wrapper">
        <el-icon><DataAnalysis /></el-icon>
        <span class="main-title">用户画像分析</span>
      </div>
      <div class="subtitle">基于用户行为数据的多维度分析</div>
    </div>

    <!-- 图表区域 -->
    <el-card class="chart-card">
      <div class="chart-header">
        <div class="chart-title">
          <h3>兴趣偏好分布</h3>
          <p class="chart-desc">展示用户在不同领域的活跃度和参与度</p>
        </div>
        <div class="chart-actions">
          <el-radio-group v-model="timeRange" size="small">
            <el-radio-button label="week">周</el-radio-button>
            <el-radio-button label="month">月</el-radio-button>
            <el-radio-button label="year">年</el-radio-button>
          </el-radio-group>
        </div>
      </div>
      <div id="main" class="chart-container"></div>
    </el-card>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { DataAnalysis } from "@element-plus/icons-vue";
import * as echarts from 'echarts';

const timeRange = ref('month');

onMounted(() => {
  const chartDom = document.getElementById('main');
  const myChart = echarts.init(chartDom);

  const option = {
    title: {
      show: false
    },
    legend: {
      data: ['当前分布', '平均水平'],
      bottom: 0
    },
    radar: {
      shape: 'circle',
      splitNumber: 5,
      axisName: {
        color: '#666',
        fontSize: 14
      },
      splitLine: {
        lineStyle: {
          color: ['#ddd']
        }
      },
      splitArea: {
        show: true,
        areaStyle: {
          color: ['#f8f9fa', '#fff']
        }
      },
      indicator: [
        { name: '文学创作', max: 100 },
        { name: '美食探索', max: 100 },
        { name: '艺术鉴赏', max: 100 },
        { name: '文化传承', max: 100 },
        { name: '社区互动', max: 100 },
        { name: '知识分享', max: 100 }
      ]
    },
    series: [
      {
        name: '用户画像分析',
        type: 'radar',
        data: [
          {
            value: [85, 70, 90, 65, 88, 75],
            name: '当前分布',
            lineStyle: {
              color: '#409EFF'
            },
            areaStyle: {
              color: 'rgba(64, 158, 255, 0.2)'
            }
          },
          {
            value: [70, 75, 65, 60, 70, 65],
            name: '平均水平',
            lineStyle: {
              color: '#67C23A'
            },
            areaStyle: {
              color: 'rgba(103, 194, 58, 0.2)'
            }
          }
        ]
      }
    ]
  };

  myChart.setOption(option);

  // 响应窗口大小变化
  window.addEventListener('resize', () => {
    myChart.resize();
  });
});
</script>

<style scoped>
.analysis-container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
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
  height: 500px;
  padding: 20px;
}

.chart-actions {
  margin-top: 5px;
}

/* 深度选择器修改 element-plus 组件样式 */
:deep(.el-card__body) {
  padding: 0;
}

:deep(.el-radio-button__inner) {
  padding: 8px 15px;
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

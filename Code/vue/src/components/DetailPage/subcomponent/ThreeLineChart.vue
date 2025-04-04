<script setup>
import { ref, onMounted, nextTick, onUnmounted, watch } from 'vue';
import * as echarts from 'echarts';
import {
  TitleComponent,
  ToolboxComponent,
  TooltipComponent,
  GridComponent,
  VisualMapComponent,
  MarkAreaComponent
} from 'echarts/components';
import { LineChart } from 'echarts/charts';
import { UniversalTransition } from 'echarts/features';
import { CanvasRenderer } from 'echarts/renderers';

echarts.use([
  TitleComponent,
  ToolboxComponent,
  TooltipComponent,
  GridComponent,
  VisualMapComponent,
  MarkAreaComponent,
  LineChart,
  CanvasRenderer,
  UniversalTransition
]);

const props = defineProps({
  timeData: {
    type: Object,
    required: true,
  }
});

const showReport = ref(false);
const chartRef = ref(null);
let chart = null;

const renderChart = () => {
  if (!chartRef.value || !props.timeData) return;

  // 销毁现有实例
  if (chart) {
    chart.dispose();
  }

  // 创建新实例
  chart = echarts.init(chartRef.value);

  try {
    // 准备数据
    const economicData = [...props.timeData.economic_data].sort((a, b) => 
      a.year - b.year || a.month - b.month
    );
    const sentimentData = [...props.timeData.sentiment_data].sort((a, b) => 
      a.year - b.year || a.month - b.month
    );

    // 生成x轴标签（年-月）
    const xData = economicData.map(item =>
        `${item.year}-${item.month.toString().padStart(2, '0')}`
    );
    const allDates = Array.from(new Set([
      ...economicData.map(d => `${d.year}-${d.month.toString().padStart(2, '0')}`),
      ...sentimentData.map(d => `${d.year}-${d.month.toString().padStart(2, '0')}`),
      ...props.timeData.casual_impact_analysis.counterfactual_predictions.dates
          .map(d => `${d.year}-${d.month.toString().padStart(2, '0')}`)
    ])).sort();

    // 数据对齐
    const alignData = (source, key, scale = 1) => {
      return allDates.map(date => {
        const item = source.find(d =>
            `${d.year}-${d.month.toString().padStart(2, '0')}` === date
        );
        return item ? (item[key] !== null ? item[key] * scale : null) : null;
      });
    };

    // 突变点信息
    const changePoint = props.timeData.casual_impact_analysis.change_point_info.date;
    const changePointIndex = allDates.findIndex(d =>
        d === `${changePoint.year}-${changePoint.month.toString().padStart(2, '0')}`
    );

    var option;
    const seriesData = [
      {
        name: '居民消费价格指数',
        data: economicData.map(item => item.cpi),
        color: '#5470C6' // 蓝色
      },
      {
        name: 'Investment',
        data: economicData.map(item => item.investment),
        color: '#91CC75' // 绿色
      },
      {
        name: 'Sales Rate',
        data: economicData.map(item => item.sales_rate),
        color: '#FAC858' // 黄色
      },
      {
        name: 'sentiment',
        data: sentimentData.map(item => item.sentiment_score * 100),
        color: '#FFB7C5' // 粉色
      }
    ];
    option =  {
      tooltip: {
        trigger: 'axis',
        axisPointer: { type: 'cross' },
        textStyle: {
          fontFamily: 'HelveticaNeue, serif'
        }
      },
      legend: {
        data: ['居民消费价格指数', '固定资产投资额累计增长', '工业产品销售率', '实际情感', '预测情感', '置信区间'],
        textStyle: {
          fontFamily: 'HelveticaNeue, serif'
        }
      },
      toolbox: {
        show: true,
        feature: { saveAsImage: {} },
        right: '40px',     // 设置右侧距离
        top: '10px',       // 设置顶部距离
        itemSize: 20,      // 设置图标大小
        itemGap: 10        // 设置图标间距
      },
      xAxis: {
        type: 'category',
        data: allDates,
        axisLabel: {
          rotate: 45,
          fontFamily: 'HelveticaNeue, serif'
        }
      },
      yAxis: [ // 双Y轴配置
        {
          type: 'value',
          name: '居民消费价格指数/工业产品销售率',
          position: 'left',
          scale: true,
          nameLocation: 'middle',
          nameGap: 50,
          nameRotate: 90,
          splitNumber: 5,
          nameTextStyle: {
            fontFamily: 'HelveticaNeue, serif'
          },
          axisLabel: {
            fontFamily: 'HelveticaNeue, serif',
            fontSize: 14
          }
        },
        {
          type: 'value',
          name: '固定资产投资额累计增长/情感',
          position: 'right',
          axisLabel: {
            formatter: '{value}%',
            fontFamily: 'HelveticaNeue, serif',
            fontSize: 14
          },
          nameLocation: 'middle',
          nameGap: 50,
          nameRotate: -90,
          splitNumber: 5,
          offset: 20,
          nameTextStyle: {
            fontFamily: 'HelveticaNeue, serif'
          },
          axisLabel: {
            fontFamily: 'HelveticaNeue, serif'
          }
        }
      ],
      series: [
        {
          name: '居民消费价格指数',
          type: 'line',
          yAxisIndex: 1, // 指定左轴
          data: alignData(economicData, 'cpi'),
          smooth: true,
          itemStyle: { color: '#5470C6' },
          label: {
            fontFamily: 'HelveticaNeue, serif'
          }
        },
        {
          name: '固定资产投资额累计增长',
          type: 'line',
          yAxisIndex: 1, // 指定右轴
          data: alignData(economicData, 'investment'),
          smooth: true,
          itemStyle: { color: '#91CC75' },
          label: {
            fontFamily: 'HelveticaNeue, serif'
          }
        },
        {
          name: '工业产品销售率',
          type: 'line',
          yAxisIndex: 1,
          data: alignData(economicData, 'sales_rate'),
          smooth: true,
          itemStyle: { color: '#FAC858' },
          label: {
            fontFamily: 'HelveticaNeue, serif'
          }
        },
        {
          name: '实际情感',
          type: 'line',
          data: alignData(sentimentData, 'sentiment_score', 100),
          smooth: true,
          itemStyle: { color: '#FF6B6B' },
          markLine: {
            triggerEvent: true,
            data: [{ xAxis: changePointIndex }],
            symbol: 'circle',
            lineStyle: { color: '#FF6B6B', type: 'dashed' },
            label: {
              position: 'end',
              formatter: '突变点\n{@score}',
              backgroundColor: 'rgba(255,107,107,0.3)',
              fontFamily: 'HelveticaNeue, serif'
            }
          },
          label: {
            fontFamily: 'HelveticaNeue, serif'
          }
        },
        {
          name: '预测情感',
          type: 'line',
          data: alignData(
              props.timeData.casual_impact_analysis.counterfactual_predictions.dates
                  .map((d, i) => ({
                    year: d.year,
                    month: d.month,
                    sentiment_score: props.timeData.casual_impact_analysis
                        .counterfactual_predictions.predicted_sentiment[i]
                  })),
              'sentiment_score',
              100
          ),
          smooth: true,
          itemStyle: { color: '#A685E2' },
          label: {
            fontFamily: 'HelveticaNeue, serif',
            fontSize: 14
          }
        },
        {
          name: '置信区间',
          type: 'line',
          data: alignData(
              props.timeData.casual_impact_analysis.counterfactual_predictions.dates
                  .map((d, i) => ({
                    year: d.year,
                    month: d.month,
                    value: props.timeData.casual_impact_analysis
                        .counterfactual_predictions.ci_upper[i] * 100
                  })),
              'value'
          ),
          itemStyle: { color: 'transparent' },
          areaStyle: {
            color: 'rgba(166,133,226,0.2)',
            origin: 'start'
          },
          lineStyle: { opacity: 0 },
          stack: 'confidence',
          symbol: 'none',
          label: {
            fontFamily: 'HelveticaNeue, serif'
          }
        },
        {
          name: '置信区间',
          type: 'line',
          data: alignData(
              props.timeData.casual_impact_analysis.counterfactual_predictions.dates
                  .map((d, i) => ({
                    year: d.year,
                    month: d.month,
                    value: props.timeData.casual_impact_analysis
                        .counterfactual_predictions.ci_lower[i] * 100
                  })),
              'value'
          ),
          itemStyle: { color: 'transparent' },
          areaStyle: { color: 'rgba(166,133,226,0.2)' },
          lineStyle: { opacity: 0 },
          stack: 'confidence',
          symbol: 'none',
          label: {
            fontFamily: 'HelveticaNeue, serif',
            fontSize: 14
          }
        }
      ],
      dataZoom: [
        {
          type: 'slider',  // 使用滑动条类型
          show: true,
          xAxisIndex: [0],
          bottom: 10,      // 距离底部的距离
          height: 20,      // 滑动条高度
          start: 0,        // 初始显示全部数据
          end: 100,
          handleSize: '110%',  // 两侧手柄大小
          handleStyle: {
            color: '#fff',
            shadowBlur: 3,
            shadowColor: 'rgba(0,0,0,0.3)',
            shadowOffsetX: 2,
            shadowOffsetY: 2
          }
        }
      ],
      grid: {
        top: '20%',
        left: '0%',
        right: '8%',
        bottom: '15%',
        containLabel: true
      }
    };

    chart.setOption(option);
  } catch (error) {
    console.error('Error rendering chart:', error);
  }
};

const initChart = () => {
  if (!chartRef.value) return;
  
  // 强制设置容器的高度
  chartRef.value.style.height = '400px';
  
  // 销毁现有实例
  if (chart) {
    chart.dispose();
  }

  // 创建新实例
  chart = echarts.init(chartRef.value);
  renderChart();
};

// 修改监听逻辑
watch(() => props.timeData, () => {
  if (props.timeData) {
    nextTick(() => {
      initChart();
    });
  }
}, { deep: true });

onMounted(() => {
  // 等待父组件完全渲染
  nextTick(() => {
    // 强制等待一帧
    requestAnimationFrame(() => {
      initChart();
      
      // 监听窗口大小变化
      window.addEventListener('resize', () => {
        if (chart) {
          chart.resize();
        }
      });
    });
  });
});

onUnmounted(() => {
  // 清理
  if (chart) {
    chart.dispose();
  }
  window.removeEventListener('resize', () => {
    if (chart) {
      chart.resize();
    }
  });
});
</script>

<template>
  <div class="three-line-container">
    <div class="chart-wrapper">
      <div class="report-button">
        <el-button type="primary" @click="showReport = true" size="small">
          查看分析报告
        </el-button>
      </div>
      <div ref="chartRef" class="chart-container"></div>
    </div>
    
    <el-dialog
      v-model="showReport"
      title="因果推理分析报告"
      width="50%"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      :show-close="true"
      class="report-dialog"
    >
      <div class="analysis-report">
        <div class="report-text">
          {{ props.timeData?.casual_impact_analysis?.impact_report || '暂无报告' }}
        </div>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button type="primary" @click="showReport = false">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
.three-line-container {
  width: 100%;
  height: 100%;
  min-height: 400px;
}

.chart-wrapper {
  width: 100%;
  height: 100%;
  position: relative;
  border-radius: 8px;
  padding: 20px 40px;
}

.chart-container {
  width: 100%;
  height: 400px !important; /* 强制固定高度 */
}

.report-button {
  position: absolute;
  top: -10px;
  left: 0px;
  z-index: 10;
}

.analysis-report {
  max-height: 60vh;
  overflow-y: auto;
  padding: 20px 30px;
}

.report-text {
  color: #606266;
  font-size: 14px;
  white-space: pre-wrap;
  word-break: break-word;
  line-height: 1.8;
  font-family: 'Microsoft YaHei', sans-serif;
}

/* Dialog 样式 */
:deep(.el-dialog) {
  border-radius: 8px;
  overflow: hidden;
}

:deep(.el-dialog__header) {
  padding: 20px 30px;
  margin-right: 0;
  border-bottom: 1px solid #fff;
  background-color: #fff;
}

:deep(.el-dialog__title) {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

:deep(.el-dialog__body) {
  padding: 0;
  background-color: #ffffff;
}

:deep(.el-dialog__footer) {
  padding: 15px 30px;
  border-top: 1px solid #fff;
  background-color: #fff;
}

/* 滚动条样式 */
.analysis-report::-webkit-scrollbar {
  width: 6px;
  display: block;
}

.analysis-report::-webkit-scrollbar-thumb {
  background-color: #C0C4CC;
  border-radius: 3px;
  &:hover {
    background-color: #909399;
  }
}

.analysis-report::-webkit-scrollbar-track {
  background-color: #F4F4F5;
  border-radius: 3px;
}

/* 确保滚动条始终显示 */
.analysis-report {
  &:hover::-webkit-scrollbar-thumb {
    background-color: #909399;
  }
}
</style>

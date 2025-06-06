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
import { useI18n } from 'vue-i18n';

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

const { t,locale } = useI18n();

const showReport = ref(false);
const chartRef = ref(null);
let chart = null;
// formatReport 方法
const getReport = (report) => {
  // 这里可以处理或格式化报告内容
  if (locale.value === 'zh') {
    return formatReport(report.impact_report);
  } else {
    return report.impact_report_en;
  }
};
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
        name: t('detail.economic.cpi'),
        data: economicData.map(item => item.cpi),
        color: '#5470C6' // 蓝色
      },
      {
        name: t('detail.economic.investment'),
        data: economicData.map(item => item.investment),
        color: '#91CC75' // 绿色
      },
      {
        name: t('detail.economic.salesRate'),
        data: economicData.map(item => item.sales_rate),
        color: '#FAC858' // 黄色
      },
      {
        name: t('detail.sentiment.actual'),
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
        data: [
          t('detail.economic.cpi'),
          t('detail.economic.investment'),
          t('detail.economic.salesRate'),
          t('detail.sentiment.actual'),
          t('detail.sentiment.predicted'),
          t('detail.sentiment.confidenceInterval')
        ],
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
          name: t('detail.economic.yAxisLabel1'),
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
          name: t('detail.economic.yAxisLabel2'),
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
          name: t('detail.economic.cpi'),
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
          name: t('detail.economic.investment'),
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
          name: t('detail.economic.salesRate'),
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
          name: t('detail.sentiment.actual'),
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
              formatter: `${t('detail.sentiment.changePoint')}\n{@score}`,
              backgroundColor: 'rgba(255,107,107,0.3)',
              fontFamily: 'HelveticaNeue, serif'
            }
          },
          label: {
            fontFamily: 'HelveticaNeue, serif'
          }
        },
        {
          name: t('detail.sentiment.predicted'),
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
          name: t('detail.sentiment.confidenceInterval'),
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
          name: t('detail.sentiment.confidenceInterval'),
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

// 添加格式化报告的函数
const formatReport = (report) => {
  if (!report) return '';
  
  // 替换数字编号为加粗样式
  let formatted = report.replace(/(\d+\.\s*[\u4e00-\u9fa5]+.*?[:：])/g, '<strong>$1</strong>');
  
  // 替换破折号为HTML实体
  formatted = formatted.replace(/[-－]/g, '&mdash;');
  
  // 为所有段落添加缩进
  return formatted;
};
</script>

<template>
  <div class="three-line-container">
    <div class="chart-wrapper">
      <div class="report-button">
        <el-button type="danger" @click="showReport = true" size="small" class="custom-btn">
          {{ t('detail.report.viewAnalysis') }}
        </el-button>
      </div>
      <div ref="chartRef" class="chart-container"></div>
    </div>
    
    <el-dialog
      v-model="showReport"
      :title="t('detail.report.causalAnalysis')"
      width="60%"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      :show-close="true"
      class="report-dialog"
      :modal-append-to-body="true"
      :append-to-body="true"
      :lock-scroll="true"
      destroy-on-close
      center
      :top="'10vh'"
    >
      <div class="analysis-report">
        <div class="report-text">
          <div class="report-section" v-if="props.timeData?.casual_impact_analysis">
            <div v-html="getReport(props.timeData.casual_impact_analysis)"></div>
          </div>
          <div v-else>{{ t('detail.report.noReport') }}</div>
        </div>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button type="primary" @click="showReport = false">{{ t('common.confirm') }}</el-button>
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
  max-height: calc(80vh - 140px); /* 设置最大高度 */
  overflow-y: auto;
  overflow-x: hidden;
  padding: 30px;
}

.report-text {
  color: #333;
  font-size: 16px;
  white-space: pre-wrap;
  word-break: break-word;
  line-height: 1.8;
  font-family: 'HelveticaNeue', serif;
}

.report-section {
  margin-bottom: 20px;
}

.report-section strong {
  color: #b71c1c;
  font-weight: 600;
  font-size: 18px;
  display: block;
  margin-bottom: 10px;
}

.report-section p {
  text-indent: 2em;
  margin: 10px 0;
}

/* Dialog 样式 */
:deep(.el-dialog) {
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  max-height: 80vh;
  position: fixed !important;
  top: 10vh !important;
  margin: 0 auto !important;
  left: 0;
  right: 0;
}

:deep(.el-dialog__header) {
  padding: 20px 30px;
  margin-right: 0;
  border-bottom: 1px solid #eee;
  background-color: #b71c1c;
}

:deep(.el-dialog__title) {
  font-size: 18px;
  font-weight: 600;
  color: white;
  font-family: 'HelveticaNeue', serif;
}

:deep(.el-dialog__headerbtn .el-dialog__close) {
  color: white;
}

:deep(.el-dialog__headerbtn:hover .el-dialog__close) {
  color: #f0f0f0;
}

:deep(.el-dialog__body) {
  padding: 0;
  background-color: #ffffff;
  max-height: calc(80vh - 120px); /* 减去header和footer的高度 */
  overflow: hidden;
}

:deep(.el-dialog__footer) {
  padding: 15px 30px;
  border-top: 1px solid #eee;
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

/* 自定义按钮样式 */
.custom-btn {
  background-color: #b71c1c !important;
  border-color: #b71c1c !important;
  color: white;
}

.custom-btn:hover, .custom-btn:focus {
  background-color: #d32f2f !important;
  border-color: #d32f2f !important;
}

/* Dialog样式 - 修改确定按钮 */
:deep(.el-button--primary) {
  background-color: #b71c1c !important;
  border-color: #b71c1c !important;
}

:deep(.el-button--primary:hover), :deep(.el-button--primary:focus) {
  background-color: #d32f2f !important;
  border-color: #d32f2f !important;
}
</style>

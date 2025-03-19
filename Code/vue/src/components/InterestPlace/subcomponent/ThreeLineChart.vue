<script setup>
import {onMounted, ref} from 'vue';
import * as echarts from 'echarts/core';
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

// const props = defineProps({
//   timeData: {
//     type: Object,
//     required: true,
//   }
// })
const timeData ={
  "status": "success",
  "sentiment_data": [
    {
      "year": 2021,
      "month": 2,
      "sentiment_score": -0.569,
      "sentiment": "negative",
      "comment_count": 2
    },
    {
      "year": 2021,
      "month": 3,
      "sentiment_score": 1.0,
      "sentiment": "positive",
      "comment_count": 1
    },
    {
      "year": 2021,
      "month": 5,
      "sentiment_score": -0.296,
      "sentiment": "negative",
      "comment_count": 4
    },
    {
      "year": 2021,
      "month": 8,
      "sentiment_score": -1.0,
      "sentiment": "negative",
      "comment_count": 1
    },
    {
      "year": 2021,
      "month": 10,
      "sentiment_score": 0.0,
      "sentiment": "neutral",
      "comment_count": 2
    },
    {
      "year": 2021,
      "month": 11,
      "sentiment_score": -1.0,
      "sentiment": "negative",
      "comment_count": 1
    },
    {
      "year": 2021,
      "month": 12,
      "sentiment_score": -1.0,
      "sentiment": "negative",
      "comment_count": 1
    },
    {
      "year": 2022,
      "month": 3,
      "sentiment_score": 0.631,
      "sentiment": "positive",
      "comment_count": 2
    },
    {
      "year": 2022,
      "month": 4,
      "sentiment_score": 1.0,
      "sentiment": "positive",
      "comment_count": 1
    },
    {
      "year": 2022,
      "month": 5,
      "sentiment_score": -0.467,
      "sentiment": "negative",
      "comment_count": 2
    },
    {
      "year": 2022,
      "month": 6,
      "sentiment_score": -0.501,
      "sentiment": "negative",
      "comment_count": 4
    },
    {
      "year": 2022,
      "month": 7,
      "sentiment_score": -0.418,
      "sentiment": "negative",
      "comment_count": 2
    },
    {
      "year": 2022,
      "month": 9,
      "sentiment_score": 1.0,
      "sentiment": "positive",
      "comment_count": 1
    },
    {
      "year": 2022,
      "month": 11,
      "sentiment_score": -1.0,
      "sentiment": "negative",
      "comment_count": 1
    },
    {
      "year": 2023,
      "month": 1,
      "sentiment_score": 1.0,
      "sentiment": "positive",
      "comment_count": 1
    },
    {
      "year": 2023,
      "month": 2,
      "sentiment_score": -0.128,
      "sentiment": "negative",
      "comment_count": 3
    },
    {
      "year": 2023,
      "month": 3,
      "sentiment_score": -1.0,
      "sentiment": "negative",
      "comment_count": 1
    },
    {
      "year": 2023,
      "month": 4,
      "sentiment_score": -0.48,
      "sentiment": "negative",
      "comment_count": 2
    },
    {
      "year": 2023,
      "month": 6,
      "sentiment_score": 0.0,
      "sentiment": "neutral",
      "comment_count": 1
    },
    {
      "year": 2023,
      "month": 7,
      "sentiment_score": -0.572,
      "sentiment": "negative",
      "comment_count": 2
    },
    {
      "year": 2023,
      "month": 8,
      "sentiment_score": -0.487,
      "sentiment": "negative",
      "comment_count": 2
    },
    {
      "year": 2023,
      "month": 9,
      "sentiment_score": -0.637,
      "sentiment": "negative",
      "comment_count": 3
    },
    {
      "year": 2023,
      "month": 11,
      "sentiment_score": 0.0,
      "sentiment": "neutral",
      "comment_count": 2
    },
    {
      "year": 2024,
      "month": 3,
      "sentiment_score": 0.0,
      "sentiment": "neutral",
      "comment_count": 1
    },
    {
      "year": 2024,
      "month": 6,
      "sentiment_score": 0.0,
      "sentiment": "neutral",
      "comment_count": 2
    },
    {
      "year": 2024,
      "month": 7,
      "sentiment_score": -1.0,
      "sentiment": "negative",
      "comment_count": 3
    },
    {
      "year": 2024,
      "month": 8,
      "sentiment_score": 0.471,
      "sentiment": "positive",
      "comment_count": 2
    },
    {
      "year": 2024,
      "month": 9,
      "sentiment_score": 0.531,
      "sentiment": "positive",
      "comment_count": 2
    },
    {
      "year": 2024,
      "month": 10,
      "sentiment_score": 1.0,
      "sentiment": "positive",
      "comment_count": 1
    },
    {
      "year": 2024,
      "month": 11,
      "sentiment_score": -1.0,
      "sentiment": "negative",
      "comment_count": 2
    },
    {
      "year": 2024,
      "month": 12,
      "sentiment_score": -1.0,
      "sentiment": "negative",
      "comment_count": 1
    }
  ],
  "economic_data": [
    {
      "year": 2021,
      "month": 1,
      "cpi": 100.9,
      "investment": 6.5,
      "sales_rate": null
    },
    {
      "year": 2021,
      "month": 2,
      "cpi": 100.3,
      "investment": 7.1,
      "sales_rate": null
    },
    {
      "year": 2021,
      "month": 3,
      "cpi": 99.5,
      "investment": 7.3,
      "sales_rate": 98.1
    },
    {
      "year": 2021,
      "month": 4,
      "cpi": 99.6,
      "investment": 7.6,
      "sales_rate": 97.9
    },
    {
      "year": 2021,
      "month": 5,
      "cpi": 99.8,
      "investment": 20.8,
      "sales_rate": 97.8
    },
    {
      "year": 2021,
      "month": 6,
      "cpi": 99.6,
      "investment": 20.7,
      "sales_rate": 97.5
    },
    {
      "year": 2021,
      "month": 7,
      "cpi": 100.2,
      "investment": 15.6,
      "sales_rate": 97.8
    },
    {
      "year": 2021,
      "month": 8,
      "cpi": 100.3,
      "investment": 13.5,
      "sales_rate": 98.0
    },
    {
      "year": 2021,
      "month": 9,
      "cpi": 100.2,
      "investment": 12.9,
      "sales_rate": 97.4
    },
    {
      "year": 2021,
      "month": 10,
      "cpi": 100.6,
      "investment": 11.2,
      "sales_rate": 96.2
    },
    {
      "year": 2021,
      "month": 11,
      "cpi": 100.4,
      "investment": 9.6,
      "sales_rate": 97.8
    },
    {
      "year": 2021,
      "month": 12,
      "cpi": 99.6,
      "investment": 9.1,
      "sales_rate": 97.9
    },
    {
      "year": 2022,
      "month": 1,
      "cpi": 100.1,
      "investment": 8.7,
      "sales_rate": null
    },
    {
      "year": 2022,
      "month": 2,
      "cpi": 100.6,
      "investment": 8.4,
      "sales_rate": null
    },
    {
      "year": 2022,
      "month": 3,
      "cpi": 100.0,
      "investment": 8.0,
      "sales_rate": 96.7
    },
    {
      "year": 2022,
      "month": 4,
      "cpi": 100.1,
      "investment": 10.4,
      "sales_rate": 96.3
    },
    {
      "year": 2022,
      "month": 5,
      "cpi": 100.0,
      "investment": 10.4,
      "sales_rate": 96.9
    },
    {
      "year": 2022,
      "month": 6,
      "cpi": 100.3,
      "investment": 9.4,
      "sales_rate": 96.2
    },
    {
      "year": 2022,
      "month": 7,
      "cpi": 100.5,
      "investment": 8.8,
      "sales_rate": 97.7
    },
    {
      "year": 2022,
      "month": 8,
      "cpi": 100.0,
      "investment": 8.7,
      "sales_rate": 98.2
    },
    {
      "year": 2022,
      "month": 9,
      "cpi": 100.4,
      "investment": 8.4,
      "sales_rate": 97.1
    },
    {
      "year": 2022,
      "month": 10,
      "cpi": 100.1,
      "investment": 8.0,
      "sales_rate": 96.3
    },
    {
      "year": 2022,
      "month": 11,
      "cpi": 99.8,
      "investment": 8.0,
      "sales_rate": 96.6
    },
    {
      "year": 2022,
      "month": 12,
      "cpi": 99.5,
      "investment": 7.9,
      "sales_rate": 97.8
    },
    {
      "year": 2023,
      "month": 1,
      "cpi": 100.4,
      "investment": 7.8,
      "sales_rate": null
    },
    {
      "year": 2023,
      "month": 2,
      "cpi": 99.6,
      "investment": 6.6,
      "sales_rate": null
    },
    {
      "year": 2023,
      "month": 3,
      "cpi": 99.7,
      "investment": 7.1,
      "sales_rate": 96.6
    },
    {
      "year": 2023,
      "month": 4,
      "cpi": 100.0,
      "investment": 0.8,
      "sales_rate": 97.1
    },
    {
      "year": 2023,
      "month": 5,
      "cpi": 100.0,
      "investment": 0.2,
      "sales_rate": 97.5
    },
    {
      "year": 2023,
      "month": 6,
      "cpi": 99.8,
      "investment": -0.1,
      "sales_rate": 96.3
    },
    {
      "year": 2023,
      "month": 7,
      "cpi": 100.1,
      "investment": -1.4,
      "sales_rate": 97.1
    },
    {
      "year": 2023,
      "month": 8,
      "cpi": 100.4,
      "investment": -6.3,
      "sales_rate": 97.3
    },
    {
      "year": 2023,
      "month": 9,
      "cpi": 100.3,
      "investment": -6.1,
      "sales_rate": 95.8
    },
    {
      "year": 2023,
      "month": 10,
      "cpi": 100.0,
      "investment": -4.9,
      "sales_rate": 96.5
    },
    {
      "year": 2023,
      "month": 11,
      "cpi": 99.6,
      "investment": -3.4,
      "sales_rate": 96.3
    },
    {
      "year": 2023,
      "month": 12,
      "cpi": 99.9,
      "investment": -3.2,
      "sales_rate": 97.0
    },
    {
      "year": 2024,
      "month": 1,
      "cpi": 100.1,
      "investment": -3.1,
      "sales_rate": null
    },
    {
      "year": 2024,
      "month": 2,
      "cpi": 101.1,
      "investment": 3.4,
      "sales_rate": null
    },
    {
      "year": 2024,
      "month": 3,
      "cpi": 99.3,
      "investment": 4.1,
      "sales_rate": 95.7
    },
    {
      "year": 2024,
      "month": 4,
      "cpi": 100.1,
      "investment": 1.7,
      "sales_rate": 96.0
    },
    {
      "year": 2024,
      "month": 5,
      "cpi": 100.0,
      "investment": 1.5,
      "sales_rate": 97.1
    },
    {
      "year": 2024,
      "month": 6,
      "cpi": 99.8,
      "investment": 0.4,
      "sales_rate": 95.9
    },
    {
      "year": 2024,
      "month": 7,
      "cpi": 100.4,
      "investment": 3.2,
      "sales_rate": 96.3
    },
    {
      "year": 2024,
      "month": 8,
      "cpi": 100.3,
      "investment": 3.4,
      "sales_rate": 95.9
    },
    {
      "year": 2024,
      "month": 9,
      "cpi": 99.8,
      "investment": 2.3,
      "sales_rate": 95.8
    },
    {
      "year": 2024,
      "month": 10,
      "cpi": 99.9,
      "investment": 2.5,
      "sales_rate": 95.6
    },
    {
      "year": 2024,
      "month": 11,
      "cpi": 99.4,
      "investment": 2.7,
      "sales_rate": 95.8
    },
    {
      "year": 2024,
      "month": 12,
      "cpi": 99.8,
      "investment": 2.8,
      "sales_rate": 97.9
    },
    {
      "year": 2025,
      "month": 1,
      "cpi": 100.6,
      "investment": null,
      "sales_rate": null
    }
  ],
  "casual_impact_analysis": {
    "change_point_info": {
      "index": 7,
      "date": {
        "year": 2021,
        "month": 8
      },
      "value": 1.0546666666666666
    },
    "impact_summary": {
      "average": {
        "actual": -0.19103225806451613,
        "predicted": 0.5991143132699397,
        "effect": -0.7901465713344558,
        "ci_lower": 46.913201068053645,
        "ci_upper": -48.493494210722545
      },
      "cumulative": {
        "actual": -5.922,
        "predicted": 18.57254371136813,
        "effect": -23.616120580161624,
        "ci_lower": 29.849677791701716,
        "ci_upper": -77.08191895202496
      }
    },
    "impact_report": "\n情感分析因果推理报告\n\n1. 变化点信息:\n   - 变化点位置: 第7个月\n   - 变化点日期: 2021年8月\n   - 变化幅度: 1.055\n\n2. 平均效应分析:\n   - 实际情感得分平均值: -0.191\n   - 预测情感得分平均值: 0.599\n   - 平均因果效应: -0.790\n   - 95%置信区间: [46.913, -48.493]\n\n3. 累积效应分析:\n   - 实际累积情感得分: -5.922\n   - 预测累积情感得分: 18.573\n   - 累积因果效应: -23.616\n   - 95%置信区间: [29.850, -77.082]\n\n4. 相对效应:\n   - 相对变化: 398.8%\n\n5. 结论:\n   在经济指标变化后的期间，情感得分的实际值与预测值之间存在0.790的差异。\n   这表明经济变化产生了显著影响。\n",
    "counterfactual_predictions": {
      "dates": [
        {
          "year": 2021,
          "month": 9
        },
        {
          "year": 2021,
          "month": 10
        },
        {
          "year": 2021,
          "month": 11
        },
        {
          "year": 2021,
          "month": 12
        },
        {
          "year": 2022,
          "month": 1
        },
        {
          "year": 2022,
          "month": 2
        },
        {
          "year": 2022,
          "month": 3
        },
        {
          "year": 2022,
          "month": 4
        },
        {
          "year": 2022,
          "month": 5
        },
        {
          "year": 2022,
          "month": 6
        },
        {
          "year": 2022,
          "month": 7
        },
        {
          "year": 2022,
          "month": 8
        },
        {
          "year": 2022,
          "month": 9
        },
        {
          "year": 2022,
          "month": 10
        },
        {
          "year": 2022,
          "month": 11
        },
        {
          "year": 2022,
          "month": 12
        },
        {
          "year": 2023,
          "month": 1
        },
        {
          "year": 2023,
          "month": 2
        },
        {
          "year": 2023,
          "month": 3
        },
        {
          "year": 2023,
          "month": 4
        },
        {
          "year": 2023,
          "month": 5
        },
        {
          "year": 2023,
          "month": 6
        },
        {
          "year": 2023,
          "month": 7
        }
      ],
      "actual_sentiment": [
        1.0,
        -0.467,
        -0.501,
        -0.418,
        1.0,
        -1.0,
        1.0,
        -0.128,
        -1.0,
        -0.48,
        0.0,
        -0.572,
        -0.487,
        -0.637,
        0.0,
        0.0,
        0.0,
        -1.0,
        0.471,
        0.531,
        1.0,
        -1.0,
        -1.0
      ],
      "predicted_sentiment": [
        0.5272639314984093,
        0.08841343282208375,
        0.4150272734764574,
        -1.2392271261167167,
        -0.5160584721867106,
        0.7678474583573707,
        -0.008025157413202366,
        1.1072240778900162,
        0.9485474609794733,
        0.4269753954175223,
        1.4988199607405164,
        0.4169566320601531,
        0.10330165823134035,
        1.6484320587650416,
        1.9428076624031598,
        2.493309218071597,
        1.8512893175659475,
        0.5302427199936319,
        1.0303770008738162,
        1.841677882677186,
        1.8895180995327865,
        2.3442440360498304,
        -0.1808439415280847
      ],
      "ci_lower": [
        -0.549104769959545,
        -1.1686538223492593,
        -0.9998460730000908,
        -2.7959914271961948,
        -2.202819745058841,
        -1.0395850007422611,
        -1.9285616961837286,
        -0.920116322560388,
        -1.1802450610489503,
        -1.7986494841140368,
        -0.8195964399381017,
        -1.9906777067631931,
        -2.3903606308581553,
        -0.9283877088114172,
        -0.714568603223996,
        -0.2422523549265796,
        -0.9602841960043437,
        -2.355341124699798,
        -1.927365825556746,
        -1.1865049271688752,
        -1.2075029905460202,
        -0.8201181642898605,
        -3.411143716701339
      ],
      "ci_upper": [
        1.6036326329563637,
        1.3454806879934267,
        1.8299006199530055,
        0.317537174962762,
        1.1707028006854199,
        2.575279917457003,
        1.9125113813573245,
        3.13456447834042,
        3.0773399830078967,
        2.652600274949082,
        3.817236361419134,
        2.8245909708834995,
        2.5969639473208357,
        4.2252518263415,
        4.600183928030315,
        5.228870791069774,
        4.662862831136239,
        3.4158265646870625,
        3.988119827304379,
        4.869860692523247,
        4.986539189611593,
        5.508606236389521,
        3.0494558336451707
      ]
    }
  },
  "tag_info": {
    "name": "土家族竹雕",
    "id": 6
  }
}
const showReport = ref(false);
onMounted(() => {
  // const economicData = [...props.timeData.economic_data]
  //     .sort((a, b) => a.year - b.year || a.month - b.month); // 按时间排序
  // const sentimentData = [...props.timeData.sentiment_data]
  //     .sort((a, b) => a.year - b.year || a.month - b.month); // 按时间排序
  const economicData = [...timeData.economic_data]
      .sort((a, b) => a.year - b.year || a.month - b.month);

  const sentimentData = [...timeData.sentiment_data]
      .sort((a, b) => a.year - b.year || a.month - b.month);// 按时间排序
  // 生成x轴标签（年-月）
  const xData = economicData.map(item =>
      `${item.year}-${item.month.toString().padStart(2, '0')}`
  );
  const allDates = Array.from(new Set([
    ...economicData.map(d => `${d.year}-${d.month.toString().padStart(2, '0')}`),
    ...sentimentData.map(d => `${d.year}-${d.month.toString().padStart(2, '0')}`),
    ...timeData.casual_impact_analysis.counterfactual_predictions.dates
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
  const changePoint = timeData.casual_impact_analysis.change_point_info.date;
  const changePointIndex = allDates.findIndex(d =>
      d === `${changePoint.year}-${changePoint.month.toString().padStart(2, '0')}`
  );
  var chartDom = document.getElementById('main');
  var myChart = echarts.init(chartDom);
  myChart.on('click', (params) => {
    if (params.componentType === 'markLine') {
      showReport.value = true;
    }
  });

  var option;
  const seriesData = [
    {
      name: 'CPI',
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
    title: {
      text: '综合经济与情感分析',
      subtext: '实际数据 vs 预测分析'
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'cross' }
    },
    legend: {
      data: ['CPI', '投资', '销售率', '实际情感', '预测情感', '置信区间']
    },
    toolbox: {
      show: true,
      feature: { saveAsImage: {} }
    },
    xAxis: {
      type: 'category',
      data: allDates,
      axisLabel: { rotate: 45 }
    },
    yAxis: [ // 双Y轴配置
      {
        type: 'value',
        name: 'CPI/销售率',
        position: 'left',
        scale: true
      },
      {
        type: 'value',
        name: '投资/情感',
        position: 'right',
        axisLabel: {
          formatter: '{value}%'
        },
        offset: 0
      }
    ],
    series: [
      {
        name: 'CPI',
        type: 'line',
        yAxisIndex: 1, // 指定左轴
        data: alignData(economicData, 'cpi'),
        smooth: true,
        itemStyle: { color: '#5470C6' }
      },
      {
        name: '投资',
        type: 'line',
        yAxisIndex: 1, // 指定右轴
        data: alignData(economicData, 'investment'),
        smooth: true,
        itemStyle: { color: '#91CC75' }
      },
      {
        name: '销售率',
        type: 'line',
        yAxisIndex: 1,
        data: alignData(economicData, 'sales_rate'),
        smooth: true,
        itemStyle: { color: '#FAC858' }
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
            backgroundColor: 'rgba(255,107,107,0.3)'
          }
        }
      },
      {
        name: '预测情感',
        type: 'line',
        data: alignData(
            timeData.casual_impact_analysis.counterfactual_predictions.dates
                .map((d, i) => ({
                  year: d.year,
                  month: d.month,
                  sentiment_score: timeData.casual_impact_analysis
                      .counterfactual_predictions.predicted_sentiment[i]
                })),
            'sentiment_score',
            100
        ),
        smooth: true,
        itemStyle: { color: '#A685E2' }
      },
      {
        name: '置信区间',
        type: 'line',
        data: alignData(
            timeData.casual_impact_analysis.counterfactual_predictions.dates
                .map((d, i) => ({
                  year: d.year,
                  month: d.month,
                  value: timeData.casual_impact_analysis
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
        symbol: 'none'
      },
      {
        name: '置信区间',
        type: 'line',
        data: alignData(
            timeData.casual_impact_analysis.counterfactual_predictions.dates
                .map((d, i) => ({
                  year: d.year,
                  month: d.month,
                  value: timeData.casual_impact_analysis
                      .counterfactual_predictions.ci_lower[i] * 100
                })),
            'value'
        ),
        itemStyle: { color: 'transparent' },
        areaStyle: { color: 'rgba(166,133,226,0.2)' },
        lineStyle: { opacity: 0 },
        stack: 'confidence',
        symbol: 'none'
      }
    ],
    dataZoom: [{
      type: 'inside',
      start: 50,
      end: 100
    }]
  };

  option && myChart.setOption(option);
});
</script>

<template>

  <div id="main" style="width: 100%; height: 400px;"></div>
  <!-- 因果推理报告 Drawer -->
  <el-drawer
      v-model="showReport"
      title="因果推理报告"
      direction="rtl"
      size="40%"
      :before-close="handleClose"
  >
    <template #default>
      <pre style="white-space: pre-wrap; padding: 20px">{{ timeData.casual_impact_analysis.impact_report }}</pre>
    </template>
    <template #footer>
      <div style="flex: auto">
        <el-button @click="showReport = false">关闭报告</el-button>
      </div>
    </template>
  </el-drawer>
</template>

<style scoped>
:deep(.el-drawer__body) {
  overflow: auto;
  padding: 0 20px;
}

pre {
  font-family: 'Microsoft YaHei', sans-serif;
  line-height: 1.6;
  background: #f8f9fa;
  border-radius: 4px;
  padding: 15px !important;
}

:deep(.el-drawer__header) {
  margin-bottom: 10px;
  padding: 20px;
  border-bottom: 1px solid #ebeef5;
}
</style>

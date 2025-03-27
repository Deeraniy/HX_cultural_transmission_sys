import * as echarts from 'echarts';

// 创建自定义主题
const theme = {
  textStyle: {
    fontFamily: 'HelveticaNeue, serif',
    fontSize: 16,
  },
  title: {
    textStyle: {
      fontFamily: 'HelveticaNeue, serif',
      fontSize: 20,
    }
  },
  legend: {
    textStyle: {
      fontFamily: 'HelveticaNeue, serif',
      fontSize: 16,
    }
  },
  tooltip: {
    textStyle: {
      fontFamily: 'HelveticaNeue, serif',
      fontSize: 16,
    }
  },
  axisLabel: {
    fontFamily: 'HelveticaNeue, serif',
    fontSize: 16,
  },
  label: {
    fontFamily: 'HelveticaNeue, serif',
    fontSize: 16,
  }
};

// 注册主题
echarts.registerTheme('hunanTheme', theme);

// 导出配置
export const initChart = (dom) => {
  return echarts.init(dom, 'hunanTheme');
};

export default theme;
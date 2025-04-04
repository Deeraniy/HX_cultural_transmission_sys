<template>
  <div class="world-map-container">
    <div ref="chartContainer" class="chart-container"></div>
    <div class="zoom-controls">
      <button @click="handleZoom('in')" class="zoom-btn">+</button>
      <button @click="handleZoom('out')" class="zoom-btn">-</button>
      <button @click="resetZoom" class="zoom-btn">
        <i class="el-icon-refresh"></i>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import * as echarts from 'echarts';
import worldJson from '@/json/world.json';
import UserAPI from '@/api/user';

const chartContainer = ref(null);
let chart = null;

const hoveredRegion = ref(null);

const currentZoom = ref(1.2);
const ZOOM_STEP = 0.2;
const MIN_ZOOM = 0.8;
const MAX_ZOOM = 2.5;

const showLabels = ref(true);

// 修改 shouldShowLabel 函数，增加更严格的面积判断
const shouldShowLabel = (params, zoom) => {
  // 定义国家大小等级
  const countryLevels = {
    large: ['Russia', 'China', 'United States', 'Canada', 'Brazil', 'Australia', 'India'],
    medium: ['Kazakhstan', 'Argentina', 'Mexico', 'Indonesia', 'Saudi Arabia', 'Iran', 
             'Mongolia', 'Libya', 'Egypt', 'Sudan', 'Algeria', 'France', 'Spain', 'Turkey']
  };

  // 获取国家的地理特征以计算面积
  const feature = worldJson.features.find(f => f.properties.name === params.name);
  if (!feature) return false;

  // 计算近似面积（使用坐标点数量作为面积参考）
  let area = 0;
  if (feature.geometry.type === 'Polygon') {
    area = feature.geometry.coordinates[0].length;
  } else if (feature.geometry.type === 'MultiPolygon') {
    area = feature.geometry.coordinates.reduce((sum, poly) => sum + poly[0].length, 0);
  }

  // 根据缩放级别和面积决定是否显示
  if (zoom <= 1.2) {
    // 最小缩放时只显示大国
    return countryLevels.large.includes(params.name);
  } else if (zoom <= 1.8) {
    // 中等缩放时显示大国和中等国家
    return countryLevels.large.includes(params.name) || 
           countryLevels.medium.includes(params.name);
  } else if (zoom <= 2.5) {
    // 较大缩放时显示大中小国家，但要求小国面积达到一定值
    return countryLevels.large.includes(params.name) || 
           countryLevels.medium.includes(params.name) ||
           area > 20; // 面积阈值，可以调整
  }
  // 最大缩放时显示所有国家
  return true;
};

const handleZoom = (type) => {
  if (!chart) return;

  const option = chart.getOption();
  if (type === 'in' && currentZoom.value < MAX_ZOOM) {
    currentZoom.value += ZOOM_STEP;
  } else if (type === 'out' && currentZoom.value > MIN_ZOOM) {
    currentZoom.value -= ZOOM_STEP;
  }

  // 更新缩放
  option.geo[0].zoom = currentZoom.value;
  
  // 更新标签显示
  option.geo[0].label.show = (params) => 
    showLabels.value && shouldShowLabel(params, currentZoom.value);
  
  chart.setOption(option);
};

const resetZoom = () => {
  if (!chart) return;

  // 恢复到初始状态
  currentZoom.value = 1.2;
  const option = chart.getOption();
  option.geo[0].zoom = currentZoom.value;
  option.geo[0].center = [5, 15];  // 恢复到初始视角
  
  // 更新标签显示
  option.geo[0].label.show = (params) => shouldShowLabel(params, currentZoom.value);
    
  chart.setOption(option);
};

// 修改 toggleLabels 函数，确保切换时也考虑缩放级别
const toggleLabels = () => {
  showLabels.value = !showLabels.value;
  if (chart) {
    const option = chart.getOption();
    option.geo[0].label.show = (params) => 
      showLabels.value && shouldShowLabel(params, currentZoom.value);
    chart.setOption(option);
  }
};

// 创建饼图数据
const createPieData = (themeData) => {
  const result = Object.entries(themeData).map(([name, value]) => ({
    name,
    value: value || 0
  }));
  return result;
};

// 创建饼图系列
const createPieSeries = (center, radius, regionName, themeData) => {
  // 转换主题数据为数组格式
  const pieData = Object.entries(themeData).map(([name, value]) => ({
    name,
    value: parseInt(value) || 0
  })).filter(item => item.value > 0);

  // 如果是中国或者有数据才显示
  if (regionName !== 'China' && pieData.length === 0) {
    return null;
  }

  console.log(`${regionName} 的饼图数据:`, pieData);

  return {
    type: 'pie',
    coordinateSystem: 'geo',
    name: '主题分布',
    tooltip: {
      formatter: (params) => {
        return `${regionName}<br/>${params.name}: ${params.value}`;
      }
    },
    label: {
      show: false
    },
    labelLine: {
      show: false
    },
    animationDuration: 0,
    radius,
    center,
    data: pieData
  };
};

// 添加一个函数来计算标签大小
const getLabelSize = (params) => {
  // 一些大国使用稍大的字号
  const largeCountries = ['Russia', 'China', 'USA', 'Canada', 'Brazil', 'Australia'];
  if (largeCountries.includes(params.name)) {
    return 10;  // 大国使用较大字号
  }
  return 8;  // 其他国家使用标准字号
};

const initChart = async () => {
  if (!chartContainer.value) return;

  // 用于统计未找到坐标的国家
  const missingCoordinates = new Set();

  // 创建 ECharts 实例
  chart = echarts.init(chartContainer.value);
  chart.showLoading();

  // 标准化地区名称的函数
  const normalizeRegionName = (name) => {
    if (!name) return '';
    return name.trim()
        .replace(/\s+/g, ' ')
        .replace(/\([^)]*\)/g, '')
        .trim();
  };

  // 地区名称映射表
  const regionNameMap = {
    'United States': 'USA',
    'United States of America': 'USA',
    'Democratic Republic of the Congo': 'Dem. Rep. Congo',
    'Congo': 'Dem. Rep. Congo',
    'Republic of the Congo': 'Congo',
    'Russian Federation': 'Russia',
    'United Republic of Tanzania': 'Tanzania',
    'United Kingdom': 'UK',
    'Korea': 'South Korea',
    'Republic of Korea': 'South Korea',
    'Democratic People\'s Republic of Korea': 'North Korea',
  };

  try {
    const response = await UserAPI.getUserDistribution();
    if (response.status !== 'success') {
      throw new Error(response.message || '获取数据失败');
    }
    const distributionData = response.data;

    // 创建标准化的数据映射
    const normalizedData = {};
    Object.entries(distributionData).forEach(([region, data]) => {
      let normalizedRegion = normalizeRegionName(region);
      // 使用映射表转换地区名称
      normalizedRegion = regionNameMap[normalizedRegion] || normalizedRegion;
      normalizedData[normalizedRegion] = data;
      console.log(`地区数据: ${normalizedRegion}`, data);
    });

    // 注册世界地图
    echarts.registerMap('world', worldJson);

    // 基础配置
    const baseGeoConfig = {
      map: 'world',
      roam: 'move',
      zoom: 1.2,
      center: [5, 15],  // 使用初始视角
      itemStyle: {
        areaColor: '#e7e8ea',
        borderColor: '#ccc'
      },
      label: {
        show: (params) => showLabels.value && shouldShowLabel(params, currentZoom.value),
        fontSize: (params) => {
          // 根据缩放级别和国家大小动态调整字体大小
          const baseSize = getLabelSize(params);
          const zoomFactor = Math.max(1, currentZoom.value / 1.2);
          return Math.min(baseSize * zoomFactor, 14); // 限制最大字号
        },
        color: '#333',
        backgroundColor: 'rgba(255, 255, 255, 0.7)',
        padding: [2, 4],
        borderRadius: 2,
        position: 'center',
        formatter: (params) => {
          const nameMap = {
            'United States of America': 'USA',
            'United Kingdom': 'UK',
            'Russian Federation': 'Russia',
            'Democratic Republic of the Congo': 'DR Congo',
            'Republic of Korea': 'S.Korea',
            "Democratic People's Republic of Korea": 'N.Korea',
            'United Arab Emirates': 'UAE',
            'Saudi Arabia': 'S.Arabia',
            'New Zealand': 'N.Zealand'
          };
          return nameMap[params.name] || params.name;
        }
      },
      emphasis: {
        itemStyle: {
          areaColor: '#b71c1c',
          borderColor: '#fff',
          borderWidth: 1,
          shadowBlur: 10,
          shadowColor: 'rgba(183, 28, 28, 0.3)'
        },
        label: {
          show: true,
          color: '#fff',
          fontSize: 10,
          fontWeight: 'bold',
          backgroundColor: 'rgba(183, 28, 28, 0.7)',
          padding: [3, 5],
          borderRadius: 2
        }
      }
    };

    const option = {
      backgroundColor: '#fff',
      geo: baseGeoConfig,
      tooltip: {
        show: true,
        trigger: 'item',
        enterable: true,
        confine: true,
        triggerOn: 'mousemove',
        position: 'right',
        backgroundColor: 'rgba(255, 255, 255, 0.95)',
        borderColor: '#fff',
        borderWidth: 1,
        padding: [0,0],
        textStyle: {
          color: '#333',
          fontSize: 14
        }
      },
      series: [
        ...Object.entries(normalizedData)
            .map(([region, data]) => {
              const coordinates = getRegionCoordinates(region, missingCoordinates);
              return {
                name: region,
                type: 'pie',
                coordinateSystem: 'geo',
                center: coordinates,
                radius: 15,
                data: Object.entries(data.themes).map(([name, value]) => ({
                  name,
                  value: value || 0
                })).filter(item => item.value > 0),
                label: { show: false },
                labelLine: { show: false },
                tooltip: {
                  formatter: (params) => {
                    const regionData = normalizedData[region];
                    if (!regionData) return '';

                    let html = `
                    <div style="min-width: 200px;padding: 10px">
                      <div style="font-size: 16px; font-weight: bold; margin-bottom: 10px;
                                 padding-bottom: 8px; border-bottom: 1px solid #eee">
                        ${region}
                      </div>
                      <div style="color: #666; margin-bottom: 8px">
                        <span style="color: #b71c1c; font-weight: bold">
                          ${regionData.total}
                        </span> 位用户
                      </div>
                      <div style="margin-top: 5px">
                        <div style="font-weight: bold; margin-bottom: 5px">主题偏好：</div>
                    `;

                    Object.entries(regionData.themes).forEach(([theme, count]) => {
                      if (count > 0) {
                        const percentage = ((count / regionData.total) * 100).toFixed(1);
                        html += `
                        <div style="display: flex; justify-content: space-between;
                                    margin: 4px 0; align-items: center">
                          <span style="color: #666">${theme}</span>
                          <span style="color: #b71c1c">
                            ${count} (${percentage}%)
                          </span>
                        </div>
                      `;
                      }
                    });

                    html += `
                      </div>
                    </div>
                  `;

                    return html;
                  }
                }
              };
            })
            .filter(Boolean)
      ]
    };

    console.log('最终的图表配置:', option);
    chart.hideLoading();
    chart.setOption(option);

    // 在所有处理完成后，输出统计信息
    if (missingCoordinates.size > 0) {
      console.log('\n=== 坐标获取统计 ===');
      console.log(`共有 ${missingCoordinates.size} 个国家未找到坐标:`);
      console.log(Array.from(missingCoordinates).sort().join(', '));
      console.log('=====================\n');
    }

  } catch (error) {
    console.error('加载世界地图数据失败:', error);
    console.error('详细错误信息:', error.stack);
    chart.hideLoading();
  }
};

// 获取地区坐标
const getRegionCoordinates = (region, missingCoordinates) => {
  // 从 world.json 中获取国家中心点坐标
  const getCountryCentroid = (countryName) => {
    // 添加国家名称映射
    const countryNameMap = {
      'Bolivia ': 'Bolivia',
      // 可以添加其他需要映射的国家名称
    };

    // 尝试获取标准名称
    const standardName = countryNameMap[countryName] || countryName;

    const feature = worldJson.features.find(f =>
        f.properties.name === standardName ||
        f.properties.name.toLowerCase() === standardName.toLowerCase()
    );

    // 如果找到了对应的国家
    if (feature) {
      // 从 geometry 中计算中心点
      if (feature.geometry && feature.geometry.coordinates) {
        if (feature.geometry.type === 'Polygon') {
          // 对于单个多边形，取第一个环的坐标平均值
          const coords = feature.geometry.coordinates[0];
          const center = coords.reduce((acc, curr) => {
            return [acc[0] + curr[0], acc[1] + curr[1]];
          }, [0, 0]);
          return [center[0] / coords.length, center[1] / coords.length];
        } else if (feature.geometry.type === 'MultiPolygon') {
          // 对于多个多边形，取第一个多边形的中心点
          const coords = feature.geometry.coordinates[0][0];
          const center = coords.reduce((acc, curr) => {
            return [acc[0] + curr[0], acc[1] + curr[1]];
          }, [0, 0]);
          return [center[0] / coords.length, center[1] / coords.length];
        }
      }
    }
    return null;
  };

  // 预定义的坐标映射（用于常用国家，确保位置准确）
  const coordinates = {
    'China': [116.4, 39.9],
    'USA': [-95, 39.8],
    'Russia': [37, 55],
    'Japan': [139, 35],
    'UK': [0, 51],
    'South Africa': [25, -29],
    'New Zealand': [174, -41],
    'Bahrain': [50.5, 26],
    'Montenegro': [19.2, 42.8],
    'Sierra Leone': [-11.8, 8.5],
    'Guinea-Bissau': [-15.2, 11.8],
    // 添加缺失的国家坐标
    'Antigua and Barbuda': [-61.8, 17.1],
    'Bolivia (Plurinational State of)': [-65.2, -19.0],
    'Bosnia and Herzegovina': [17.8, 44.0],
    'Brunei Darussalam': [114.7, 4.5],
    'Cabo Verde': [-23.5, 15.1],
    'Central African Republic': [20.9, 6.6],
    'Czech Republic': [15.5, 49.8],
    'Democratic People\'s Republic of Korea': [127.5, 40.0],
    'Democratic Republic of the Congo': [23.7, -2.9],
    'Dominican Republic': [-70.2, 18.7],
    'Equatorial Guinea': [10.3, 1.7],
    'Eswatini': [31.5, -26.5],
    'Iran (Islamic Republic of)': [53.7, 32.4],
    'Lao People\'s Democratic Republic': [102.5, 19.9],
    'Maldives': [73.5, 4.2],
    'Marshall Islands': [171.2, 7.1],
    'Micronesia (Federated States of)': [150.6, 7.4],
    'Monaco': [7.4, 43.7],
    'Nauru': [166.9, -0.5],
    'North Macedonia': [21.7, 41.6],
    'Republic of Korea': [127.8, 36.0],
    'Republic of Moldova': [28.4, 47.2],
    'Russian Federation': [37.6, 55.8],
    'San Marino': [12.4, 43.9],
    'Solomon Islands': [160.2, -9.6],
    'South Sudan': [31.6, 4.9],
    'St. Kitts and Nevis': [-62.7, 17.3],
    'St. Lucia': [-61.0, 13.9],
    'St. Vincent and the Grenadines': [-61.2, 13.2],
    'Syrian Arab Republic': [38.3, 35.0],
    'São Tomé and Príncipe': [6.6, 0.3],
    'Tuvalu': [179.2, -8.5],
    'United Republic of Tanzania': [34.9, -6.4],
    'Venezuela (Bolivarian Republic of)': [-66.6, 6.4],
    'Viet Nam': [108.3, 14.1]
  };

  // 先尝试从预定义映射获取
  let result = coordinates[region];

  // 如果没有预定义坐标，尝试从 world.json 获取
  if (!result) {
    const centroid = getCountryCentroid(region);
    if (centroid) {
      // 确保经度在 -180 到 180 之间
      centroid[0] = ((centroid[0] + 180) % 360) - 180;
      result = centroid;
    } else {
      console.warn(`警告: 未找到地区 ${region} 的坐标配置`);
      missingCoordinates.add(region);
      result = [0, 0];
    }
  }

  console.log(`地区 ${region} 的最终坐标:`, result);
  return result;
};

onMounted(() => {
  initChart();

  // 添加窗口大小变化的监听
  window.addEventListener('resize', () => {
    chart?.resize();
  });
});

onUnmounted(() => {
  // 清理
  chart?.dispose();
  window.removeEventListener('resize', () => {
    chart?.resize();
  });
});
</script>

<style scoped>
.world-map-container {
  width: 90%;
  height: 90%;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  position: relative;
  padding: 10px;
  margin-top: -15px;
  margin-left: 30px;
}

.chart-container {

  width: 100%;
  height: 100%;
  min-height: 500px;

  box-sizing: border-box;
}

.zoom-controls {
  position: absolute;
  bottom: 20px;
  right: 20px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  z-index: 100;
}

.zoom-btn {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background-color: white;
  border: 1px solid #ddd;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  cursor: pointer;
  transition: all 0.3s;
}

.zoom-btn:hover {
  background-color: #f5f5f5;
  transform: scale(1.05);
}

.zoom-btn:active {
  background-color: #e8e8e8;
  transform: scale(0.95);
}
</style>

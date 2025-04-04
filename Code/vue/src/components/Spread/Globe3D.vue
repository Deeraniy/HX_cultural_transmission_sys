<template>
  <div class="globe-container">
    <div ref="globeCanvas" class="globe-canvas"></div>
    
    <!-- 标题 -->
    <div class="title-panel">
      <h1>传播效果智能分析</h1>
      <div class="subtitle">Intelligent analysis of communication effect</div>
    </div>

    <!-- 左侧面板组 -->
    <div class="left-panels">
      
      
      <!-- 词云图卡片 -->
      <div class="data-panel word-cloud-card">
        <h3>热点词云</h3>
        <div ref="wordCloudChart" class="word-cloud-container"></div>
      </div>
    </div>

    <!-- 右侧面板组 -->
    <div class="right-panels">
      <!-- 修改左上角统计卡片结构 -->
      <div class="data-panel stats-card" style="left: 20px; top: 20px;">
        <div class="data-grid">
          <div class="data-item">
            <div class="data-value">2273</div>
            <div class="data-label">总评论数量</div>
          </div>
          <div class="data-item">
            <div class="data-value">19</div>
            <div class="data-label">评论涉及种数</div>
          </div>
          <div class="data-item">
            <div class="data-value">2</div>
            <div class="data-label">分析国家总数</div>
          </div>
          <div class="data-item">
            <div class="data-value">41</div>
            <div class="data-label">评论时间跨度</div>
          </div>
        </div>
      </div>
      <!-- 趋势图卡片 -->
      <div class="data-panel trend-card">
        <h3>传播趋势</h3>
        <div ref="trendChart" class="trend-container"></div>
      </div>
    </div>

    <!-- 控制按钮组 -->
    <div class="control-panel">
      <div class="control-item" @click="toggleRotation">
        <i class="iconfont icon-rotate"></i>
        <span>自动旋转</span>
      </div>
      <div class="control-item" @click="resetCamera">
        <i class="iconfont icon-reset"></i>
        <span>重置视角</span>
      </div>
      <div class="control-item" @click="toggleFullscreen">
        <i class="iconfont icon-fullscreen"></i>
        <span>全屏显示</span>
      </div>
    </div>

    <!-- 时间轴 -->
    <div class="timeline-panel">
      <div class="timeline-header">
        <span>传播时间轴</span>
        <span class="timeline-date">2024-01-01 至 2024-02-11</span>
      </div>
      <div ref="timelineChart" class="timeline-chart"></div>
    </div>

    <!-- 左下角面板 -->
    <div class="data-panel bottom-left">
      <h3>热点分布</h3>
      <div class="stats-list">
        <div v-for="(stat, region) in commentStats" 
             :key="region" 
             class="stat-item">
          <span class="region">{{ region }}</span>
          <span class="count">{{ stat.count }}</span>
          <div class="heat-bar" :style="{ width: `${stat.percentage}%`, backgroundColor: stat.color }"></div>
        </div>
      </div>
    </div>

    <!-- 右下角面板 -->
    <div class="relation-panel">
      <h3>传播关系网络</h3>
      <div ref="relationChart" class="relation-container"></div>
    </div>

    <!-- 添加图例说明 -->
    <div class="legend-panel">
      <div class="legend-item">
        <span class="legend-dot" style="background: #4a9eff"></span>
        <span>评论热度</span>
      </div>
      <div class="legend-item">
        <span class="legend-dot" style="background: #ff6b6b"></span>
        <span>传播强度</span>
      </div>
    </div>

  

    <!-- 添加顶部数据卡片 -->
    <div class="top-stats">
      <div class="stat-card">
        <div class="stat-icon">
          <i class="iconfont icon-speed"></i>
        </div>
        <div class="stat-info">
          <div class="stat-label">传播速度</div>
          <div class="stat-value">
            <span class="number">128</span>
            <span class="unit">条/小时</span>
          </div>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon">
          <i class="iconfont icon-trend"></i>
        </div>
        <div class="stat-info">
          <div class="stat-label">传播趋势</div>
          <div class="stat-value">
            <span class="number up">+24.5%</span>
            <span class="unit">较昨日</span>
          </div>
        </div>
      </div>

    <!-- 添加顶部状态栏 -->
    <div class="status-bar">
          <div class="status-item">
            <i class="iconfont icon-signal"></i>
            <span>实时监测中</span>
            <div class="pulse-dot"></div>
          </div>
          <div class="status-item">
            <i class="iconfont icon-clock"></i>
            <span>{{ currentTime }}</span>
          </div>
        </div>

    </div>

    <!-- 添加关系图面板 -->
    <div class="data-panel analysis-panel">
      <h3>传播分析</h3>
      <div class="trend-chart">
        <!-- 这里可以添加趋势图表 -->
      </div>
    </div>

    <!-- 修改返回按钮区域 -->
    <div class="nav-buttons">
      <div class="back-btn" @click="goBack">
        <i class="iconfont icon-back"></i>
        <span>返回首页</span>
      </div>
      <div class="view-data-btn" @click="viewAllData">
        <i class="iconfont icon-data"></i>
        <span>查看所有评论数据</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue';
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';
import countriesData from '@/json/world.json';
import * as echarts from 'echarts';
import 'echarts-wordcloud';
import { useRouter } from 'vue-router';

const globeCanvas = ref(null);
let scene, camera, renderer, globe, controls;

const router = useRouter();

// 模拟的评论数据
const mockComments = [
  { region: '湖南', ip: '127.0.0.1', count: 150 },
  { region: '北京', ip: '192.168.1.1', count: 80 },
  { region: '上海', ip: '192.168.1.2', count: 120 },
  { region: '广东', ip: '192.168.1.3', count: 200 },
  { region: '四川', ip: '192.168.1.4', count: 90 }
];

// 评论统计
const commentStats = ref({});

// 地区坐标映射
const regionCoordinates = {
  '湖南': { lat: 28.112444, lng: 112.982279 },
  '北京': { lat: 39.904989, lng: 116.405285 },
  '上海': { lat: 31.230416, lng: 121.473701 },
  '广东': { lat: 23.125178, lng: 113.280637 },
  '四川': { lat: 30.572815, lng: 104.066801 }
};

// 存储国家亮度
const countryBrightness = new Map();

// 添加国家评论热度映射
const countryComments = {
  'China': 0  // 初始化中国的评论数
};

// 更新中国城市坐标点数据，使用实际的评论数据
const chinaCityData = mockComments.map(comment => ({
  name: comment.region,
  lat: regionCoordinates[comment.region].lat,
  lng: regionCoordinates[comment.region].lng,
  value: comment.count
}));

// 添加射线检测器
const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();

// 添加鼠标移动事件处理
const onMouseMove = (event) => {
  // 添加节流
  if (!onMouseMove.throttleTimer) {
    onMouseMove.throttleTimer = setTimeout(() => {
      const rect = globeCanvas.value.getBoundingClientRect();
      mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
      mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;

      raycaster.setFromCamera(mouse, camera);
      const intersects = raycaster.intersectObjects(globe.children, true);
      
      // 重置所有国家的发光效果
      globe.children.forEach(child => {
        if (child.userData.countryName === 'China') {
          const baseStyle = getCountryColor('China');
          child.material.emissiveIntensity = baseStyle.emissiveIntensity;
        }
      });

      // 处理相交的对象
      if (intersects.length > 0) {
        const intersected = intersects[0].object;
        if (intersected.userData.countryName === 'China') {
          intersected.material.emissiveIntensity = 1.0;
        }
      }

      onMouseMove.throttleTimer = null;
    }, 50); // 50ms的节流时间
  }
};

// 将 getCountryColor 函数移到外部
const getCountryColor = (countryName) => {
  if (countryName === 'China') {
    const intensity = Math.min(countryComments['China'] / 500, 1);
    return {
      color: new THREE.Color(0x1a1a1a),  // 暗色基础
      opacity: 0.3,
      emissive: new THREE.Color(0xff5500),
      emissiveIntensity: 0.1
    };
  }
  return {
    color: new THREE.Color(0x1a4d7c),
    opacity: 0.3,
    emissive: new THREE.Color(0x112244),
    emissiveIntensity: 0.1
  };
};

// 修改点云效果函数
const addPointCloud = (globe) => {
  chinaCityData.forEach(city => {
    const pointCount = Math.floor(city.value);
    const points = [];
    
    // 在城市周围生成随机点
    for (let i = 0; i < pointCount; i++) {
      const offset = 1.0; // 增加分布范围
      const randomLat = city.lat + (Math.random() - 0.5) * offset;
      const randomLng = city.lng + (Math.random() - 0.5) * offset;
      
      const phi = (90 - randomLat) * (Math.PI / 180);
      const theta = (randomLng + 180) * (Math.PI / 180);
      const radius = 5.02; // 略高于地球表面

      const x = -radius * Math.sin(phi) * Math.cos(theta);
      const y = radius * Math.cos(phi);
      const z = radius * Math.sin(phi) * Math.sin(theta);

      points.push(new THREE.Vector3(x, y, z));
    }

    // 创建点云几何体
    const geometry = new THREE.BufferGeometry().setFromPoints(points);
    
    // 创建点云材质
    const intensity = Math.min(city.value / 200, 1);
    const material = new THREE.PointsMaterial({
      color: new THREE.Color(1, 0.5 + intensity * 0.5, 0),
      size: 0.08,
      transparent: true,
      opacity: 0.6,
      blending: THREE.AdditiveBlending,
      sizeAttenuation: true,
      depthWrite: false // 防止点云遮挡问题
    });

    // 创建点云对象
    const pointCloud = new THREE.Points(geometry, material);
    globe.add(pointCloud);
  });
};

// 修改 drawCountryBoundaries 函数
const drawCountryBoundaries = (globe) => {
  // 计算中国的总评论数
  mockComments.forEach(comment => {
    countryComments['China'] = (countryComments['China'] || 0) + comment.count;
  });

  const lineMaterial = new THREE.LineBasicMaterial({
    color: 0xaaaaaa,
    transparent: true,
    opacity: 0.5
  });

  countriesData.features.forEach(country => {
    if (!country.geometry) return;

    const coordinates = country.geometry.type === 'MultiPolygon' 
      ? country.geometry.coordinates 
      : [country.geometry.coordinates];

    coordinates.forEach(polygon => {
      polygon.forEach(ring => {
        const points = [];
        const vertices = [];
        
        ring.forEach(coord => {
          const lng = coord[0];
          const lat = coord[1];
          const phi = (90 - lat) * (Math.PI / 180);
          const theta = (lng + 180) * (Math.PI / 180);
          const radius = 5.01;

          const x = -radius * Math.sin(phi) * Math.cos(theta);
          const y = radius * Math.cos(phi);
          const z = radius * Math.sin(phi) * Math.sin(theta);

          points.push(new THREE.Vector3(x, y, z));
          vertices.push(x, y, z);
        });

        // 创建边界线
        if (points.length > 0) {
          points.push(points[0]);
          const lineGeometry = new THREE.BufferGeometry().setFromPoints(points);
          const line = new THREE.Line(lineGeometry, lineMaterial);
          globe.add(line);
        }

        // 创建国家填充面
        if (vertices.length > 9) {
          const countryGeometry = new THREE.BufferGeometry();
          countryGeometry.setAttribute('position', new THREE.Float32BufferAttribute(vertices, 3));
          
          const countryName = country.properties?.name;
          const style = getCountryColor(countryName);
          
          const countryMesh = createCountryMesh(countryGeometry, countryName);
          globe.add(countryMesh);
        }
      });
    });
  });
};

// 修改初始化场景函数
const initScene = () => {
  scene = new THREE.Scene();
  
  // 减少星星数量
  const starsGeometry = new THREE.BufferGeometry();
  const starsVertices = [];
  for (let i = 0; i < 2000; i++) {  // 从10000减少到2000
    const r = 1000;
    const theta = 2 * Math.PI * Math.random();
    const phi = Math.acos(2 * Math.random() - 1);
    const x = r * Math.sin(phi) * Math.cos(theta);
    const y = r * Math.sin(phi) * Math.sin(theta);
    const z = r * Math.cos(phi);
    starsVertices.push(x, y, z);
  }
  starsGeometry.setAttribute('position', new THREE.Float32BufferAttribute(starsVertices, 3));
  const starsMaterial = new THREE.PointsMaterial({
    color: 0xffffff,
    size: 2,
    transparent: true,
    opacity: 0.8,
    sizeAttenuation: true
  });
  const starField = new THREE.Points(starsGeometry, starsMaterial);
  scene.add(starField);

  camera = new THREE.PerspectiveCamera(
    75,
    globeCanvas.value.clientWidth / globeCanvas.value.clientHeight,
    0.1,
    1000
  );
  
  renderer = new THREE.WebGLRenderer({ 
    antialias: true, 
    alpha: true,
    logarithmicDepthBuffer: true
  });
  renderer.setSize(globeCanvas.value.clientWidth, globeCanvas.value.clientHeight);
  renderer.setPixelRatio(window.devicePixelRatio);
  globeCanvas.value.appendChild(renderer.domElement);

  const textureLoader = new THREE.TextureLoader();
  
  // 加载纹理
  const earthTexture = textureLoader.load('/textures/earth/earthmap1k.jpg');
  const bumpMap = textureLoader.load('/textures/earth/earthbump1k.jpg');
  const cloudsTexture = textureLoader.load('/textures/earth/earthcloudmap.jpg');
  const nightTexture = textureLoader.load('/textures/earth/earthlights1k.jpg');

  // 创建基础地球
  const earthGeometry = new THREE.SphereGeometry(5, 128, 128);
  const earthMaterial = new THREE.MeshPhongMaterial({
    color: 0x1a4d7c,
    shininess: 25,
    emissive: new THREE.Color(0x112244),
    emissiveIntensity: 0.2,
    transparent: true,
    opacity: 0.9
  });
  globe = new THREE.Mesh(earthGeometry, earthMaterial);
  scene.add(globe);

  // 添加国家边界
  drawCountryBoundaries(globe);
  
  // 添加点云效果
  addPointCloud(globe);

  // 添加大气层效果
  const atmosphereGeometry = new THREE.SphereGeometry(5.2, 128, 128);
  const atmosphereMaterial = new THREE.MeshPhongMaterial({
    color: 0x3399ff,
    transparent: true,
    opacity: 0.15,
    side: THREE.BackSide
  });
  const atmosphere = new THREE.Mesh(atmosphereGeometry, atmosphereMaterial);
  scene.add(atmosphere);

  // 调整光照
  const ambientLight = new THREE.AmbientLight(0xffffff, 0.3);
  scene.add(ambientLight);

  const directionalLight = new THREE.DirectionalLight(0xffffff, 1.5);
  directionalLight.position.set(5, 3, 5);
  scene.add(directionalLight);

  // 添加多个点光源
  const pointLight1 = new THREE.PointLight(0xffa500, 1, 50);
  pointLight1.position.set(10, 10, 10);
  scene.add(pointLight1);

  const pointLight2 = new THREE.PointLight(0xff7700, 1, 50);
  pointLight2.position.set(-10, -10, -10);
  scene.add(pointLight2);

  // 调整相机位置
  camera.position.z = 15;
  camera.position.y = 2;
  camera.position.x = 0;

  // 调整控制器
  controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;
  controls.dampingFactor = 0.05;
  controls.rotateSpeed = 0.5;
  controls.minDistance = 10;
  controls.maxDistance = 30;

  // 添加鼠标事件监听
  globeCanvas.value.addEventListener('mousemove', onMouseMove);
};

// 修改热点添加函数
const addHotspots = () => {
  // 计算中国的总评论数和最大亮度
  const chinaComments = mockComments.reduce((sum, comment) => sum + comment.count, 0);
  const maxBrightness = Math.min(chinaComments / 500, 1) * 2;  // 增加最大亮度

  // 更新中国区域的亮度 - 不闪烁
  globe.children.forEach(child => {
    if (child.userData.countryName === 'China') {
      child.material.emissive = new THREE.Color(0xffaa00);
      child.material.emissiveIntensity = maxBrightness;
      countryBrightness.set('China', maxBrightness);
    }
  });

  mockComments.forEach(comment => {
    const coords = regionCoordinates[comment.region];
    if (!coords) return;

    const phi = (90 - coords.lat) * (Math.PI / 180);
    const theta = (coords.lng + 180) * (Math.PI / 180);
    const radius = 5.02; // 略高于地球表面

    const x = -radius * Math.sin(phi) * Math.cos(theta);
    const y = radius * Math.cos(phi);
    const z = radius * Math.sin(phi) * Math.sin(theta);

    // 缩小热点尺寸
    const hotspotGeometry = new THREE.SphereGeometry(0.08, 16, 16);
    const intensity = Math.min(comment.count / 200, 1);
    const hotspotMaterial = new THREE.MeshPhongMaterial({
      color: new THREE.Color(1, 0.5 * intensity, 0),
      emissive: new THREE.Color(1, 0.5 * intensity, 0),
      emissiveIntensity: intensity * 1.5
    });

    const hotspot = new THREE.Mesh(hotspotGeometry, hotspotMaterial);
    hotspot.position.set(x, y, z);
    globe.add(hotspot);

    // 调整光晕大小
    const glowGeometry = new THREE.SphereGeometry(0.12, 16, 16);
    const glowMaterial = new THREE.MeshPhongMaterial({
      color: new THREE.Color(1, 0.7 * intensity, 0),
      transparent: true,
      opacity: 0.3,
      side: THREE.BackSide
    });
    const glow = new THREE.Mesh(glowGeometry, glowMaterial);
    glow.position.copy(hotspot.position);
    globe.add(glow);

    // 更新统计信息
    commentStats.value[comment.region] = {
      count: comment.count,
      percentage: (comment.count / 200) * 100,
      color: `rgb(255, ${Math.floor(128 + intensity * 127)}, 0)`
    };
  });
};

// 修改动画循环
const animate = () => {
  requestAnimationFrame(animate);
  
  if (isAutoRotating.value) {
    globe.rotation.y += 0.001;
  }

  // 更新点云动画
  globe.children.forEach(child => {
    if (child instanceof THREE.Points) {
      const time = Date.now() * 0.001;
      child.material.opacity = 0.4 + Math.sin(time) * 0.2;
    }
  });

  controls.update();
  renderer.render(scene, camera);
};

// 处理窗口大小变化
const handleResize = () => {
  if (!globeCanvas.value) return;
  
  camera.aspect = globeCanvas.value.clientWidth / globeCanvas.value.clientHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(globeCanvas.value.clientWidth, globeCanvas.value.clientHeight);
};

// 修改 drawCountryBoundaries 函数中的国家材质创建部分
const createCountryMesh = (geometry, countryName) => {
  const style = getCountryColor(countryName);
  const material = new THREE.MeshPhongMaterial({
    color: style.color,
    transparent: true,
    opacity: style.opacity,
    side: THREE.FrontSide, // 改为单面渲染
    emissive: style.emissive,
    emissiveIntensity: style.emissiveIntensity,
    shininess: 30,
    specular: new THREE.Color(0x333333)
  });

  const mesh = new THREE.Mesh(geometry, material);
  mesh.userData.countryName = countryName;
  
  // 如果是中国，添加额外属性
  if (countryName === 'China') {
    mesh.userData.isHighlightable = true;
    // 存储原始材质属性，用于恢复
    mesh.userData.originalEmissiveIntensity = style.emissiveIntensity;
  }
  
  return mesh;
};

// 添加控制功能
const toggleRotation = () => {
  isAutoRotating.value = !isAutoRotating.value;
  if (isAutoRotating.value) {
    animate();
  }
};

const resetCamera = () => {
  camera.position.set(0, -2, 18);
  camera.lookAt(0, 0, 0);
  controls.reset();
};

const toggleFullscreen = () => {
  if (!document.fullscreenElement) {
    document.documentElement.requestFullscreen();
  } else {
    document.exitFullscreen();
  }
};

// 添加图表初始化
let trendChart = null;
let wordCloudChart = null;
let timelineChart = null;

// 初始化趋势图
const initTrendChart = () => {
  trendChart = echarts.init(document.querySelector('.trend-container'));
  trendChart.setOption({
    grid: {
      top: 20,
      right: 20,
      bottom: 20,
      left: 40,
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: ['1月', '2月', '3月', '4月', '5月'],
      axisLine: {
        lineStyle: { color: 'rgba(255,255,255,0.3)' }
      },
      axisLabel: { color: 'rgba(255,255,255,0.7)' }
    },
    yAxis: {
      type: 'value',
      axisLine: {
        lineStyle: { color: 'rgba(255,255,255,0.3)' }
      },
      axisLabel: { color: 'rgba(255,255,255,0.7)' },
      splitLine: {
        lineStyle: { color: 'rgba(255,255,255,0.1)' }
      }
    },
    series: [{
      data: [150, 230, 224, 218, 135],
      type: 'line',
      smooth: true,
      symbol: 'circle',
      symbolSize: 8,
      lineStyle: {
        width: 3,
        color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [{
          offset: 0,
          color: '#4a9eff'
        }, {
          offset: 1,
          color: '#ff6b6b'
        }])
      },
      itemStyle: {
        color: '#4a9eff',
        borderWidth: 2,
        borderColor: '#fff'
      },
      areaStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
          offset: 0,
          color: 'rgba(74,158,255,0.3)'
        }, {
          offset: 1,
          color: 'rgba(74,158,255,0.1)'
        }])
      }
    }]
  });
};

// 初始化词云图
const initWordCloud = () => {
  wordCloudChart = echarts.init(document.querySelector('.word-cloud-container'));
  wordCloudChart.setOption({
    series: [{
      type: 'wordCloud',
      shape: 'circle',
      left: 'center',
      top: 'center',
      width: '90%',
      height: '90%',
      right: null,
      bottom: null,
      sizeRange: [12, 30],
      rotationRange: [-90, 90],
      rotationStep: 45,
      gridSize: 8,
      drawOutOfBound: false,
      textStyle: {
        fontFamily: 'sans-serif',
        fontWeight: 'bold',
        color: function () {
          return 'rgb(' + [
            Math.round(Math.random() * 160 + 95),
            Math.round(Math.random() * 160 + 95),
            Math.round(Math.random() * 160 + 95)
          ].join(',') + ')';
        }
      },
      emphasis: {
        focus: 'self',
        textStyle: {
          shadowBlur: 10,
          shadowColor: '#333'
        }
      },
      data: [
        { name: '传播', value: 100 },
        { name: '效果', value: 80 },
        { name: '分析', value: 70 },
        // ... 添加更多词云数据
      ]
    }]
  });
};

// 添加实时时间
const currentTime = ref('');

const updateTime = () => {
  const now = new Date();
  currentTime.value = now.toLocaleTimeString('zh-CN', {
    hour12: false,
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  });
};

// 添加关系图初始化
const initRelationChart = () => {
  const relationChart = echarts.init(document.querySelector('.relation-container'));
  relationChart.setOption({
    tooltip: {
      trigger: 'item'
    },
    legend: {
      show: false
    },
    animationDurationUpdate: 1500,
    animationEasingUpdate: 'quinticInOut',
    series: [{
      type: 'graph',
      layout: 'force',
      force: {
        repulsion: 100,
        gravity: 0.1,
        edgeLength: 80,
        layoutAnimation: true
      },
      roam: true,
      label: {
        show: true,
        color: '#fff',
        fontSize: 12
      },
      edgeLabel: {
        show: false
      },
      edgeSymbol: ['circle', 'arrow'],
      edgeSymbolSize: [4, 8],
      data: [
        { name: '热点事件', value: 20, symbolSize: 50, itemStyle: { color: '#4a9eff' } },
        { name: '微博', value: 15, symbolSize: 40, itemStyle: { color: '#ff6b6b' } },
        { name: '抖音', value: 15, symbolSize: 40, itemStyle: { color: '#ff6b6b' } },
        { name: '新闻媒体', value: 15, symbolSize: 40, itemStyle: { color: '#ff6b6b' } },
        { name: '用户群体A', value: 10, symbolSize: 30, itemStyle: { color: '#4CAF50' } },
        { name: '用户群体B', value: 10, symbolSize: 30, itemStyle: { color: '#4CAF50' } },
        { name: '用户群体C', value: 10, symbolSize: 30, itemStyle: { color: '#4CAF50' } }
      ],
      links: [
        { source: '热点事件', target: '微博', value: 5, lineStyle: { color: '#4a9eff', width: 2 } },
        { source: '热点事件', target: '抖音', value: 5, lineStyle: { color: '#4a9eff', width: 2 } },
        { source: '热点事件', target: '新闻媒体', value: 5, lineStyle: { color: '#4a9eff', width: 2 } },
        { source: '微博', target: '用户群体A', value: 3, lineStyle: { color: '#ff6b6b', width: 1 } },
        { source: '抖音', target: '用户群体B', value: 3, lineStyle: { color: '#ff6b6b', width: 1 } },
        { source: '新闻媒体', target: '用户群体C', value: 3, lineStyle: { color: '#ff6b6b', width: 1 } }
      ],
      lineStyle: {
        opacity: 0.9,
        curveness: 0.3
      }
    }]
  });

  // 添加到全局变量
  charts.relationChart = relationChart;
};

const goBack = () => {
  router.push('/index');  // 返回到传播页面
};

// 添加查看数据方法
const viewAllData = () => {
  router.push('/comments');  // 跳转到评论数据页面
};

// 实现控制功能
let isAutoRotating = ref(false);

onMounted(async () => {
  initScene();
  addHotspots();
  animate();
  window.addEventListener('resize', handleResize);
  
  // 在这里添加事件监听
  if (globeCanvas.value) {
    globeCanvas.value.addEventListener('mousemove', onMouseMove);
    globeCanvas.value.addEventListener('click', onClick);
  }
  
  await nextTick();
  initTrendChart();
  initWordCloud();
  initRelationChart();
  
  // 监听窗口大小变化
  window.addEventListener('resize', () => {
    trendChart?.resize();
    wordCloudChart?.resize();
    charts.relationChart?.resize();
  });

  updateTime();
  setInterval(updateTime, 1000);
});

onUnmounted(() => {
  window.removeEventListener('resize', handleResize);
  if (controls) controls.dispose();
  if (renderer) renderer.dispose();
  if (globeCanvas.value) {
    globeCanvas.value.removeEventListener('mousemove', onMouseMove);
  }
});

// 可以添加点击事件处理
const onClick = (event) => {
  // 类似的射线检测逻辑
  const rect = globeCanvas.value.getBoundingClientRect();
  mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
  mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;

  raycaster.setFromCamera(mouse, camera);
  const intersects = raycaster.intersectObjects(globe.children);

  if (intersects.length > 0) {
    const intersected = intersects[0].object;
    if (intersected.userData.countryName === 'China') {
      // 处理点击事件，比如显示详细信息
      console.log('点击了中国区域');
      // 这里可以触发一个事件或更新某些状态
    }
  }
};
</script>

<style scoped>
.globe-container {
  width: 100%;
  height: 100vh;
  position: relative;
  background: linear-gradient(to bottom, #000510, #000000);
  overflow: hidden;
}

.globe-canvas {
  width: 100%;
  height: 100%;
  display: block;
}

.data-panel {
  position: absolute;
  background: rgba(255, 255, 255, 0.05);  /* 降低背景透明度 */
  backdrop-filter: blur(8px);
  border-radius: 15px;
  padding: 20px;
  color: white;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.05);
}

/* 添加发光边框效果 */
.data-panel::before {
  content: '';
  position: absolute;
  top: -1px;
  left: -1px;
  right: -1px;
  bottom: -1px;
  border-radius: 15px;
  background: linear-gradient(45deg, rgba(74, 158, 255, 0.2), rgba(255, 107, 107, 0.2));
  z-index: -1;
  pointer-events: none;
}

.top-left {
  top: 20px;
  left: 20px;
  width: 300px;
}

.top-right {
  top: 20px;
  right: 20px;
  width: 300px;
}

.bottom-left {
  top: 70px;
  bottom: auto;
  left: 20px;
  width: 350px;
}

.bottom-right {
  bottom: 20px;
  right: 20px;
  height: 235px;
  width: 300px;
}

h3 {
  margin: 0 0 15px 0;
  font-size: 18px;
  font-weight: normal;
  color: rgba(255, 255, 255, 0.9);
}

.data-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}

.data-item {
  text-align: center;
}

.data-value {
  font-size: 24px;
  font-weight: bold;
  color: #4a9eff;
  margin-bottom: 5px;
}

.data-label {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.7);
}

.stats-list {
  margin-top: 10px;
}

.stat-item {
  display: flex;
  align-items: center;
  margin: 10px 0;
  font-size: 14px;
}

.region {
  width: 60px;
  color: rgba(255, 255, 255, 0.9);
}

.count {
  width: 50px;
  text-align: right;
  margin: 0 10px;
  color: #4a9eff;
}

.heat-bar {
  flex-grow: 1;
  height: 4px;
  background: linear-gradient(to right, #4a9eff, #ff6b6b);
  border-radius: 2px;
  transition: width 0.3s ease;
}

/* 添加玻璃态hover效果 */
.data-panel:hover {
  background: rgba(255, 255, 255, 0.1);
  transform: translateY(-2px);
  transition: all 0.3s ease;
}

/* 添加新样式 */
.title-panel {
  position: absolute;
  top: 20px;
  left: 49%;
  transform: translateX(-50%);
  text-align: center;
  color: white;
}

.title-panel h1 {
  font-size: 28px;
  margin: 0;
  font-weight: normal;
  text-shadow: 0 0 10px rgba(74, 158, 255, 0.5);
}

.subtitle {
  font-size: 14px;
  opacity: 0.7;
  margin-top: 5px;
}

.timeline-panel {
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  width: 60%;  /* 增加宽度以容纳控制面板 */
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(8px);
  border-radius: 15px;
  padding: 15px;
}

.timeline-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
  color: white;
}

.timeline-date {
  opacity: 0.7;
}

.control-panel {
  position: absolute;
  bottom: 20%;  /* 放在时间轴上方 */
  height: 40px;
  transform: translateY(-20%);
  width: 60%;  /* 与时间轴相同宽度 */
  display: flex;
  flex-direction: row;  /* 改为横向排列 */
  gap: 15px;
  padding: 0;
}

.control-item {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(8px);
  border-radius: 10px;
  padding: 10px 15px 10px 10px;  /* 增加水平内边距 */
  color: white;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
}

.control-item:hover {
  background: rgba(255, 255, 255, 0.15);
  transform: translateY(-2px);  /* 改为向上浮动 */
}

.control-item i {
  font-size: 16px;
}

.legend-panel {
  position: absolute;
  top: 84%;
  left: 29%;
  display: flex;
  gap: 30px;
  color: white;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(8px);
  padding: 10px 20px;
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
}

.legend-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  box-shadow: 0 0 10px currentColor;
}

/* 添加动画效果 */
@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.05); }
  100% { transform: scale(1); }
}

.data-panel:hover {
  animation: pulse 2s infinite;
}

/* 修改样式 */
.left-panels, .right-panels {
  position: absolute;
  top: 20px;
  width: 300px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.left-panels {
  left: 20px;
}

.right-panels {
  right: 20px;
  width: 450px;
  top: 0px;
}

.stats-card {
  height: auto;
  padding: 15px 20px;
  width: 400px;

}
.trend-card{
  width: 450px;  /* 加宽 */
  height: 180px;  /* 降低高度使其扁平 */
  padding: 15px;
  top: 120px;
  right: 0px;
}

.word-cloud-card{
  top: 262px;
  height: 180px;
  width: 300px;
  padding: 15px;
}
.trend-card {
  width: 300px;
  padding: 15px;
}

.word-cloud-container, .trend-container {
  width: 100%;
  height: calc(100% - 30px);
}

.control-panel {
  position: absolute;
  left: 47%;
  top: 88%;
  transform: translateY(-80%);
}

.timeline-panel {
  bottom: 20px;
  width: 45%;
}

/* 添加顶部状态栏 */
.status-bar {
  position: absolute;
  top: 520px;
  left: 50%;
  width: 150px;
  transform: translateX(-50%);
  display: flex;
  gap: 30px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(8px);
  padding: 8px 20px;
  border-radius: 20px;
  color: white;
  font-size: 14px;
  z-index: 10;
}

.status-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.pulse-dot {
  width: 8px;
  height: 8px;
  background: #4CAF50;
  border-radius: 50%;
  animation: pulse 1.5s infinite;
}

/* 添加顶部数据卡片 */
.top-stats {
  position: absolute;
  top: 90px;
  left: 49%;
  transform: translateX(-50%);
  display: flex;
  gap: 20px;
  z-index: 10;
}

.stat-card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(8px);
  border-radius: 15px;
  top:20px;
  padding: 15px 25px;
  display: flex;
  align-items: center;
  gap: 15px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
}

.stat-card:hover {
  background: rgba(255, 255, 255, 0.15);
  transform: translateY(-2px);
}

.stat-icon {
  width: 40px;
  height: 40px;
  background: rgba(74, 158, 255, 0.2);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-icon i {
  font-size: 24px;
  color: #4a9eff;
}

.stat-info {
  color: white;
}

.stat-label {
  font-size: 14px;
  opacity: 0.8;
  margin-bottom: 4px;
}

.stat-value {
  display: flex;
  align-items: baseline;
  gap: 4px;
}

.stat-value .number {
  font-size: 24px;
  font-weight: bold;
}

.stat-value .unit {
  font-size: 12px;
  opacity: 0.7;
}

.stat-value .up {
  color: #4CAF50;
}

.stat-value .down {
  color: #F44336;
}

/* 添加脉冲动画 */
@keyframes pulse {
  0% {
    transform: scale(1);
    box-shadow: 0 0 0 0 rgba(76, 175, 80, 0.7);
  }
  70% {
    transform: scale(1);
    box-shadow: 0 0 0 10px rgba(76, 175, 80, 0);
  }
  100% {
    transform: scale(1);
    box-shadow: 0 0 0 0 rgba(76, 175, 80, 0);
  }
}

/* 添加关系图面板 */
.relation-panel {
  position: absolute;
  bottom: 20px;
  right: 20px;
  width: 300px;
  height: 370px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(8px);
  border-radius: 15px;
  padding: 15px;
  color: white;
}

.relation-container {
  width: 100%;
  height: calc(100% - 30px);
}

/* 修改传播分析面板样式 */
.data-panel.analysis-panel {  /* 添加新的类名 */
  position: absolute;
  bottom: 20px;
  left: 20px;
  width: 300px;
  height: 210px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(8px);
  border-radius: 15px;
  padding: 15px;
  color: white;
}

/* 修改导航按钮样式 */
.nav-buttons {
  position: absolute;
  top: 20px;
  left: 20px;
  display: flex;
  gap: 10px;
  z-index: 100;
}

.back-btn, .view-data-btn {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(8px);
  border-radius: 10px;
  padding: 8px 15px;
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s ease;
}

.back-btn:hover, .view-data-btn:hover {
  background: rgba(255, 255, 255, 0.15);
  transform: translateX(5px);
}
</style> 
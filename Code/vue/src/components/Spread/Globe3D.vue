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
      <div class="control-item" @click="toggleDanmaku">
        <i class="iconfont" :class="isDanmakuEnabled ? 'icon-danmaku-on' : 'icon-danmaku-off'"></i>
        <span>{{ isDanmakuEnabled ? '关闭弹幕' : '开启弹幕' }}</span>
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
      <div class="theme-select">
        <select v-model="selectedTheme" @change="handleThemeChange">
          <option value="">选择主题</option>
          <option value="culture">文化传承</option>
          <option value="tourism">旅游体验</option>
          <option value="food">美食文化</option>
          <option value="art">艺术展示</option>
          <option value="education">教育推广</option>
        </select>
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
  
  // 创建星空背景
  const createStarField = () => {
    // 创建多层星空，每层具有不同特性
    const starLayers = [
      { count: 3000, size: 1.5, speed: 0.0001, color: 0xffffff, distance: 900 },  // 小而密的白色星星
      { count: 1500, size: 2, speed: 0.00015, color: 0x4a9eff, distance: 800 },   // 中等大小的蓝色星星
      { count: 800, size: 2.5, speed: 0.0002, color: 0xff6b6b, distance: 700 }    // 较大的红色星星
    ];

    starLayers.forEach(layer => {
      const starsGeometry = new THREE.BufferGeometry();
      const starsVertices = [];
      const starsSpeeds = [];
      
      for (let i = 0; i < layer.count; i++) {
        const r = layer.distance;
        const theta = 2 * Math.PI * Math.random();
        const phi = Math.acos(2 * Math.random() - 1);
        const x = r * Math.sin(phi) * Math.cos(theta);
        const y = r * Math.sin(phi) * Math.sin(theta);
        const z = r * Math.cos(phi);
        starsVertices.push(x, y, z);
        starsSpeeds.push(Math.random() * layer.speed);
      }
      
      starsGeometry.setAttribute('position', new THREE.Float32BufferAttribute(starsVertices, 3));
      starsGeometry.setAttribute('speed', new THREE.Float32BufferAttribute(starsSpeeds, 1));
      
      const starsMaterial = new THREE.PointsMaterial({
        size: layer.size,
        color: layer.color,
        transparent: true,
        opacity: 0.8,
        sizeAttenuation: true,
        blending: THREE.AdditiveBlending,
        depthWrite: false
      });
      
      const starField = new THREE.Points(starsGeometry, starsMaterial);
      scene.add(starField);
      animatedObjects.push(starField);
    });

    // 添加一个大的背景渐变球体
    const bgSphereGeometry = new THREE.SphereGeometry(1000, 32, 32);
    const bgSphereMaterial = new THREE.ShaderMaterial({
      uniforms: {
        color1: { value: new THREE.Color(0x000510) },
        color2: { value: new THREE.Color(0x000000) }
      },
      vertexShader: `
        varying vec3 vPosition;
        void main() {
          vPosition = position;
          gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
        }
      `,
      fragmentShader: `
        uniform vec3 color1;
        uniform vec3 color2;
        varying vec3 vPosition;
        void main() {
          float blend = (vPosition.y + 1000.0) / 2000.0;
          gl_FragColor = vec4(mix(color2, color1, blend), 1.0);
        }
      `,
      side: THREE.BackSide
    });
    
    const bgSphere = new THREE.Mesh(bgSphereGeometry, bgSphereMaterial);
    scene.add(bgSphere);
  };

  // 存储需要动画的对象
  const animatedObjects = [];
  
  // 创建星空
  createStarField();
  
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

  // 添加弹幕系统
  const updateDanmakus = createDanmakuSystem();

  // 修改动画循环
  const animate = () => {
    requestAnimationFrame(animate);
    
    // 更新星星位置
    animatedObjects.forEach(obj => {
      if (obj instanceof THREE.Points) {
        const positions = obj.geometry.attributes.position;
        const speeds = obj.geometry.attributes.speed;
        
        for (let i = 0; i < positions.count; i++) {
          const speed = speeds.array[i];
          positions.array[i * 3] += speed;
          
          // 如果星星移动到太远，重置位置
          if (positions.array[i * 3] > 1000) {
            positions.array[i * 3] = -1000;
          }
        }
        positions.needsUpdate = true;
      }
    });

    if (isAutoRotating.value) {
      globe.rotation.y += 0.001;
    }

    // 更新弹幕
    updateDanmakus();

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

  animate();
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

// 添加全局变量来存储弹幕组
let danmakuGroup = null;

// 修改弹幕系统创建函数
const createDanmakuSystem = () => {
  danmakuGroup = new THREE.Group();  // 保存引用
  scene.add(danmakuGroup);

  // 增加画布尺寸以支持更大的文字
  const canvas = document.createElement('canvas');
  const context = canvas.getContext('2d');
  canvas.width = 1024;  // 进一步加大画布尺寸
  canvas.height = 256;

  // 扩充更多弹幕文字
  const danmakuTexts = [
    '中国传统文化博大精深！', 
    '非物质文化遗产传承有序',
    '让世界了解中国文化底蕴',
    '文化自信是最基本的自信',
    '传统文化需要创新发展',
    '让传统文化走向世界',
    '中华文化源远流长',
    '文化传承永续发展',
    '弘扬中华优秀传统文化',
    '文化自信自强',
    '传统文化焕发新活力',
    '中华文明五千年',
    '文化是民族的根魂',
    '传统与现代的完美融合',
    '让世界聆听中国声音',
    '文化交流促进世界和平',
    '中国故事感动世界',
    '文化自信助力中国梦',
    '传统文化创新发展',
    '文化传承代代相传'
  ];

  // 修改y轴间距和范围
  const ySpacing = 6;  // 增加间距，防止重叠
  const yRange = 30;   // 垂直范围
  const yPositions = [];
  
  // 预生成所有可能的y轴位置
  for (let y = -yRange; y <= yRange; y += ySpacing) {
    yPositions.push(y);
  }

  // 跟踪已使用的y轴位置和对应的弹幕
  const usedYPositions = new Map();  // 使用Map来跟踪每个位置的弹幕

  const getAvailableYPosition = () => {
    // 过滤出未使用的y轴位置
    const availablePositions = yPositions.filter(y => !usedYPositions.has(y));
    
    if (availablePositions.length === 0) {
      // 如果没有可用位置，找出最左边的弹幕的位置
      let leftmostY = null;
      let leftmostX = Infinity;
      
      usedYPositions.forEach((danmaku, y) => {
        if (danmaku.position.x < leftmostX) {
          leftmostX = danmaku.position.x;
          leftmostY = y;
        }
      });
      
      if (leftmostY !== null) {
        usedYPositions.delete(leftmostY);
        return leftmostY;
      }
      
      return yPositions[Math.floor(Math.random() * yPositions.length)];
    }
    
    return availablePositions[Math.floor(Math.random() * availablePositions.length)];
  };

  const createDanmaku = (text) => {
    context.clearRect(0, 0, canvas.width, canvas.height);
    
    // 减弱文字发光效果
    context.shadowColor = 'rgba(255, 255, 255, 0.4)';
    context.shadowBlur = 15;
    
    // 使用更大的字体，降低不透明度
    context.fillStyle = 'rgba(255, 255, 255, 0.6)';
    // 使用 HelveticaNeue2 字体，需要确保字体已加载
    context.font = '98px HelveticaNeue, serif';  // 添加后备字体
    
    // 确保字体已加载
    document.fonts.ready.then(() => {
      context.textAlign = 'center';
      context.textBaseline = 'middle';
      context.fillText(text, canvas.width / 2, canvas.height / 2);
    });

    const texture = new THREE.CanvasTexture(canvas);
    const material = new THREE.MeshBasicMaterial({
      map: texture,
      transparent: true,
      side: THREE.DoubleSide,
      depthWrite: false,
      opacity: 0.6
    });

    // 增加弹幕平面的大小
    const geometry = new THREE.PlaneGeometry(12, 3);  // 保持平面大小
    const mesh = new THREE.Mesh(geometry, material);

    // 修改弹幕的运动范围
    const radius = 25;  // 轨道半径
    const y = getAvailableYPosition();
    
    // 始终从最右侧开始
    const startAngle = 0;  // 改为0，表示从正右方开始
    mesh.position.set(
      radius,  // 直接设置为radius，确保从最右侧开始
      y,
      0       // z设为0，确保从正右方开始
    );

    mesh.userData.angle = startAngle;
    mesh.userData.speed = 0.004 + Math.random() * 0.002;  // 加快速度
    mesh.userData.radius = radius;
    mesh.userData.y = y;

    mesh.lookAt(camera.position);
    usedYPositions.set(y, mesh);  // 记录该位置已被使用
    
    return mesh;
  };

  const danmakus = [];
  const createMultipleDanmakus = () => {
    const danmaku = createDanmaku(
      danmakuTexts[Math.floor(Math.random() * danmakuTexts.length)]
    );
    danmakuGroup.add(danmaku);
    danmakus.push(danmaku);

    // 当弹幕被移除时，释放其y轴位置
    if (danmakus.length > 50) {
      const oldDanmaku = danmakus.shift();
      usedYPositions.delete(oldDanmaku.userData.y);
      danmakuGroup.remove(oldDanmaku);
      oldDanmaku.geometry.dispose();
      oldDanmaku.material.dispose();
    }
  };

  // 更新弹幕位置
  const updateDanmakus = () => {
    danmakus.forEach(danmaku => {
      danmaku.userData.angle -= danmaku.userData.speed;
      
      // 更新位置
      danmaku.position.x = danmaku.userData.radius * Math.cos(danmaku.userData.angle);
      danmaku.position.z = danmaku.userData.radius * Math.sin(danmaku.userData.angle);
      
      // 当弹幕移动到最左侧时，重置到右侧
      if (danmaku.position.x < -danmaku.userData.radius) {  // 使用x坐标判断，确保到最左边
        usedYPositions.delete(danmaku.userData.y);  // 释放旧的y位置
        const newY = getAvailableYPosition();
        danmaku.userData.angle = 0;
        danmaku.userData.y = newY;
        danmaku.position.set(
          danmaku.userData.radius,
          newY,
          0
        );
        usedYPositions.set(newY, danmaku);  // 记录新位置
      }
      
      danmaku.lookAt(camera.position);
    });
  };

  // 保存定时器引用
  danmakuInterval = setInterval(createMultipleDanmakus, 800);

  // 设置初始可见性
  danmakuGroup.visible = isDanmakuEnabled.value;

  return updateDanmakus;
};

// 添加弹幕控制状态
const isDanmakuEnabled = ref(true);

// 修改弹幕开关方法
const toggleDanmaku = () => {
  isDanmakuEnabled.value = !isDanmakuEnabled.value;
  if (danmakuGroup) {
    danmakuGroup.visible = isDanmakuEnabled.value;
    
    // 如果关闭弹幕，停止创建新弹幕
    if (!isDanmakuEnabled.value) {
      clearInterval(danmakuInterval);
    } else {
      // 重新开始创建弹幕
      danmakuInterval = setInterval(createMultipleDanmakus, 800);
    }
  }
};

// 修改弹幕创建定时器的处理
let danmakuInterval = null;

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

  // 确保字体加载
  await document.fonts.load('98px HelveticaNeue2');
});

onUnmounted(() => {
  window.removeEventListener('resize', handleResize);
  if (controls) controls.dispose();
  if (renderer) renderer.dispose();
  if (globeCanvas.value) {
    globeCanvas.value.removeEventListener('mousemove', onMouseMove);
  }
  if (danmakuInterval) {
    clearInterval(danmakuInterval);
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

// 初始化时间轴
const initTimelineChart = () => {
  const timelineChart = echarts.init(document.querySelector('.timeline-chart'));
  timelineChart.setOption({
    tooltip: {
      trigger: 'axis',
      formatter: '{b}: {c}'
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '15%',
      top: '10%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: ['1月1日', '1月5日', '1月10日', '1月15日', '1月20日', '1月25日', '1月30日', '2月5日', '2月10日'],
      axisLine: { lineStyle: { color: 'rgba(255,255,255,0.3)' } },
      axisLabel: { color: 'rgba(255,255,255,0.7)' }
    },
    yAxis: {
      type: 'value',
      axisLine: { lineStyle: { color: 'rgba(255,255,255,0.3)' } },
      axisLabel: { color: 'rgba(255,255,255,0.7)' },
      splitLine: { lineStyle: { color: 'rgba(255,255,255,0.1)' } }
    },
    dataZoom: [{
      type: 'slider',
      show: true,
      start: 0,
      end: 100,
      height: 20,
      bottom: 0,
      borderColor: 'rgba(255,255,255,0.2)',
      textStyle: {
        color: 'rgba(255,255,255,0.7)'
      },
      handleStyle: {
        color: '#4a9eff',
        borderColor: '#4a9eff'
      },
      handleSize: '150%',
      backgroundColor: 'rgba(255,255,255,0.05)',
      fillerColor: 'rgba(74,158,255,0.2)',
      moveHandleSize: 6
    }],
    series: [{
      data: [120, 180, 150, 230, 210, 160, 190, 140, 170],
      type: 'line',
      smooth: true,
      symbol: 'circle',
      symbolSize: 8,
      itemStyle: {
        color: '#4a9eff'
      },
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

// 添加主题选择相关逻辑
const selectedTheme = ref('');

const handleThemeChange = () => {
  // 根据选择的主题更新数据
  console.log('Selected theme:', selectedTheme.value);
  // 这里可以添加主题切换的具体逻辑
};
</script>

<style scoped>
.globe-container {
  width: 100vw;  /* 使用视口宽度 */
  height: 100vh;  /* 使用视口高度 */
  position: fixed;  /* 改为固定定位 */
  top: 0;
  left: 0;
  background: linear-gradient(to bottom, #000510, #000000);
  overflow: hidden;  /* 确保内容不会溢出 */
}

.globe-canvas {
  width: 100%;
  height: 100%;
  display: block;
}

/* 确保body和html也不会出现滚动条 */
:root, body {
  margin: 0;
  padding: 0;
  overflow: hidden;
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
  padding: 10px -10px 10px -15px;  /* 增加水平内边距 */
  color: white;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 5px;
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
  left: 26.5%;
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
  left: 42.5%;
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
  align-items: center;
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

/* 添加弹幕按钮样式 */
.icon-danmaku-on {
  color: #4a9eff;
}

.icon-danmaku-off {
  opacity: 0.7;
}

.control-item {
  /* ... 其他样式保持不变 ... */
  min-width: 100px;  /* 确保按钮宽度一致 */
  justify-content: center;  /* 内容居中 */
}

/* 添加主题选择下拉列表样式 */
.theme-select {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(8px);
  border-radius: 10px;
  overflow: hidden;
}

.theme-select select {
  background: transparent;
  border: none;
  padding: 8px 15px;
  color: white;
  font-size: 14px;
  cursor: pointer;
  outline: none;
  width: 120px;
  option {
    background: #1a1a1a;
    color: white;
  }
}
</style> 
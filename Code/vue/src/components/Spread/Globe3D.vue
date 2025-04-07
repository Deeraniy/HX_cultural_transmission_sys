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

    <!-- 修改右下角面板,添加切换功能 -->
    <div class="relation-panel">
      <div class="panel-header">
        <div class="tab-buttons">
          <div 
            class="tab-btn" 
            :class="{ active: activeTab === 'relation' }"
            @click="activeTab = 'relation'"
          >
            <i class="iconfont icon-relation"></i>
            传播关系网络
          </div>
          <div 
            class="tab-btn" 
            :class="{ active: activeTab === 'alert' }"
            @click="activeTab = 'alert'"
          >
            <i class="iconfont icon-warning"></i>
            实时预警
            <span v-if="alerts.length" class="alert-badge">{{ alerts.length }}</span>
          </div>
        </div>
      </div>

      <!-- 关系图内容 -->
      <div v-show="activeTab === 'relation'" class="panel-content">
        <div ref="relationChart" class="relation-container"></div>
      </div>

      <!-- 预警内容 -->
      <div v-show="activeTab === 'alert'" class="panel-content">
        <div class="alert-list">
          <div v-for="alert in alerts" :key="alert.id" class="alert-item" :class="alert.level">
            <i class="iconfont icon-warning"></i>
            <div class="alert-content">
              <div class="alert-title">{{ alert.title }}</div>
              <div class="alert-desc">{{ alert.description }}</div>
              <div class="alert-time">{{ alert.time }}</div>
            </div>
          </div>
        </div>
      </div>
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
      <h3>传播数据分析</h3>
      <div class="analysis-content">
        <!-- 将前两项放在同一行 -->
        <div class="analysis-row">
          <div class="analysis-item half">
            <div class="analysis-label">传播速度指数</div>
            <div class="analysis-value">
              <span class="number">89.5</span>
              <div class="trend up">↑12.3%</div>
            </div>
          </div>
          <div class="analysis-item half">
            <div class="analysis-label">互动参与度</div>
            <div class="analysis-value">
              <span class="number">76.2</span>
              <div class="trend up">↑8.7%</div>
            </div>
          </div>
        </div>
        <!-- 情感倾向保持原样 -->
        <div class="analysis-item">
          <div class="analysis-label">情感倾向</div>
          <div class="sentiment-bars">
            <div class="sentiment-bar positive" style="width: 65%">正面 65%</div>
            <div class="sentiment-bar neutral" style="width: 25%">中性 25%</div>
            <div class="sentiment-bar negative" style="width: 10%">负面 10%</div>
          </div>
        </div>
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
import { FBXLoader } from 'three/examples/jsm/loaders/FBXLoader';

// 初始化全局变量
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

// 存储国家亮度
const countryBrightness = new Map();

// 添加国家评论热度映射
const countryComments = {
  'China': 0  // 初始化中国的评论数
};

// 更新中国城市坐标点数据，使用实际的评论数据
const chinaCityData = mockComments.map(comment => ({
  name: comment.region,
  lat: comment.lat,
  lng: comment.lng,
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

// 修改文本精灵创建函数
const createTextSprite = (text) => {
  const canvas = document.createElement('canvas');
  const context = canvas.getContext('2d');
  canvas.width = 256;  // 调整画布大小
  canvas.height = 64;
  
  // 设置渐变背景
  const gradient = context.createLinearGradient(0, 0, canvas.width, 0);
  gradient.addColorStop(0, 'rgba(0, 0, 0, 0.8)');
  gradient.addColorStop(1, 'rgba(0, 0, 0, 0.8)');
  context.fillStyle = gradient;
  context.fillRect(0, 0, canvas.width, canvas.height);
  
  // 设置文字样式
  context.font = '24px HelveticaNeue2';  // 调整字体大小
  context.fillStyle = '#ffffff';
  context.textAlign = 'center';
  context.textBaseline = 'middle';
  
  // 添加文字阴影
  context.shadowColor = '#000000';
  context.shadowBlur = 4;
  context.shadowOffsetX = 2;
  context.shadowOffsetY = 2;
  
  // 绘制文字
  context.fillText(text, canvas.width / 2, canvas.height / 2);
  
  const texture = new THREE.CanvasTexture(canvas);
  const spriteMaterial = new THREE.SpriteMaterial({ 
    map: texture,
    transparent: true,
    opacity: 0.95
  });
  
  const sprite = new THREE.Sprite(spriteMaterial);
  sprite.scale.set(1.5, 0.4, 1);  // 调整精灵大小
  return sprite;
};

// 修改数据环创建函数
const createDataRing = (radius, data, color, height) => {
  const ringGeometry = new THREE.RingGeometry(radius, radius + 0.2, 64);
  const ringMaterial = new THREE.MeshBasicMaterial({
    color: color,
    transparent: true,
    opacity: 0.3,
    side: THREE.DoubleSide
  });
  const ring = new THREE.Mesh(ringGeometry, ringMaterial);
  ring.rotation.x = Math.PI / 2;
  ring.position.y = height;
  
  data.forEach((item, index) => {
    const angle = (index / data.length) * Math.PI * 2;
    
    // 增大数据点
    const dotGeometry = new THREE.SphereGeometry(0.2, 12, 12);
    const dotMaterial = new THREE.MeshPhongMaterial({
      color: color,
      emissive: color,
      emissiveIntensity: item.value / 100
    });
    const dot = new THREE.Mesh(dotGeometry, dotMaterial);
    
    // 调整点的位置
    dot.position.x = Math.cos(angle) * radius;
    dot.position.z = Math.sin(angle) * radius;
    
    // 增加标签距离并调整位置
    const labelRadius = radius * 1.4;  // 增加标签距离
    const textSprite = createTextSprite(`${item.name}: ${item.value}%`);
    textSprite.position.set(
      Math.cos(angle) * labelRadius,
      0,
      Math.sin(angle) * labelRadius
    );
    
    // 添加更明显的连接线
    const lineMaterial = new THREE.LineBasicMaterial({ 
      color: color,
      transparent: true,
      opacity: 0.5,  // 增加线的不透明度
      linewidth: 2   // 注意：在WebGL中linewidth可能不起作用
    });
    const lineGeometry = new THREE.BufferGeometry().setFromPoints([
      new THREE.Vector3(dot.position.x, 0, dot.position.z),
      new THREE.Vector3(textSprite.position.x, 0, textSprite.position.z)
    ]);
    const line = new THREE.Line(lineGeometry, lineMaterial);
    
    ring.add(line);
    ring.add(textSprite);
    ring.add(dot);
  });
  
  return ring;
};

// 1. 首先在组件顶部声明全局变量
let animationFrameId = null; // 用于存储requestAnimationFrame的ID

// 2. 定义全局动画函数
const animate = () => {
  animationFrameId = requestAnimationFrame(animate);
  
  if (globe) {
    globe.rotation.y += 0.001;
    
    // 更新粒子位置
    const particles = globe.children.find(child => child instanceof THREE.Points);
    if (particles) {
      const positions = particles.geometry.attributes.position.array;
      const time = Date.now() * 0.0005;

      for(let i = 0; i < positions.length; i += 3) {
        const x = positions[i];
        const y = positions[i + 1];
        const z = positions[i + 2];
        const distance = Math.sqrt(x * x + y * y + z * z);

        const breathe = Math.sin(time + distance * 0.3) * 0.15;
        const targetRadius = 8 + breathe;
        const scale = targetRadius / distance;

        positions[i] = x * scale;
        positions[i + 1] = y * scale;
        positions[i + 2] = z * scale;
      }

      particles.geometry.attributes.position.needsUpdate = true;
    }
  }

  if (isDanmakuEnabled.value && danmakuGroup) {
    updateDanmakus();
  }
  
  if (controls) controls.update();
  if (renderer) renderer.render(scene, camera);
};

// 3. 修改initScene函数
const initScene = () => {
  scene = new THREE.Scene();
  
  // 创建渐变背景
  const createGradientBackground = () => {
    // 1. 创建渐变背景
    const bgGeometry = new THREE.PlaneGeometry(2, 2, 1, 1);
    const bgMaterial = new THREE.ShaderMaterial({
      uniforms: {
        color1: { value: new THREE.Color(0x0a192f) },  // 深蓝色
        color2: { value: new THREE.Color(0x000000) }   // 黑色
      },
      vertexShader: `
        varying vec2 vUv;
        void main() {
          vUv = uv;
          gl_Position = vec4(position, 1.0);
        }
      `,
      fragmentShader: `
        uniform vec3 color1;
        uniform vec3 color2;
        varying vec2 vUv;
        void main() {
          gl_FragColor = vec4(mix(color2, color1, vUv.y), 1.0);
        }
      `,
      depthWrite: false
    });
    
    const bgMesh = new THREE.Mesh(bgGeometry, bgMaterial);
    bgMesh.position.z = -1;
    scene.add(bgMesh);

    // 2. 增加星星数量和调整参数
    const starsGeometry = new THREE.BufferGeometry();
    const starsPositions = [];
    const starsSizes = [];
    const starsColors = [];

    // 增加星星数量到8000
    for(let i = 0; i < 8000; i++) {
      // 调整分布范围，让星星更密集
      const x = Math.random() * 1500 - 750;
      const y = Math.random() * 1500 - 750;
      const z = Math.random() * -500;  // 减小z轴范围，让星星更集中
      
      starsPositions.push(x, y, z);
      
      // 增加星星大小变化范围
      starsSizes.push(Math.random() * 4 + 1);  // 最小1，最大5
      
      // 调整颜色分布
      const colorChoice = Math.random();
      if (colorChoice > 0.85) {
        // 金色调
        starsColors.push(1, 0.9, 0.5);
      } else if (colorChoice > 0.6) {
        // 蓝色调
        starsColors.push(0.6, 0.8, 1);
      } else if (colorChoice > 0.3) {
        // 白色调
        starsColors.push(1, 1, 1);
      } else {
        // 淡蓝色调
        starsColors.push(0.8, 0.9, 1);
      }
    }

    starsGeometry.setAttribute('position', new THREE.Float32BufferAttribute(starsPositions, 3));
    starsGeometry.setAttribute('size', new THREE.Float32BufferAttribute(starsSizes, 1));
    starsGeometry.setAttribute('color', new THREE.Float32BufferAttribute(starsColors, 3));

    const starsMaterial = new THREE.ShaderMaterial({
      uniforms: {
        time: { value: 0 }
      },
      vertexShader: `
        attribute float size;
        attribute vec3 color;
        varying vec3 vColor;
        uniform float time;
        void main() {
          vColor = color;
          vec4 mvPosition = modelViewMatrix * vec4(position, 1.0);
          // 增强闪烁效果
          float twinkle = sin(time + position.x * 0.05) * 0.5 + 0.5;
          gl_PointSize = size * (200.0 / -mvPosition.z) * (0.7 + 0.3 * twinkle);
          gl_Position = projectionMatrix * mvPosition;
        }
      `,
      fragmentShader: `
        varying vec3 vColor;
        void main() {
          float r = length(gl_PointCoord - vec2(0.5));
          float alpha = smoothstep(0.5, 0.0, r);
          gl_FragColor = vec4(vColor, alpha * 1.2);  // 增加亮度
        }
      `,
      transparent: true,
      depthWrite: false,
      blending: THREE.AdditiveBlending
    });

    const stars = new THREE.Points(starsGeometry, starsMaterial);
    scene.add(stars);

    // 3. 调整动画速度
    const animateStars = () => {
      requestAnimationFrame(animateStars);
      if (stars.material.uniforms) {
        stars.material.uniforms.time.value += 0.002;  // 降低闪烁速度使效果更柔和
      }
    };
    animateStars();
  };

  createGradientBackground();
  
  camera = new THREE.PerspectiveCamera(
    75,
    globeCanvas.value.clientWidth / globeCanvas.value.clientHeight,
    0.1,
    1000
  );
  
  renderer = new THREE.WebGLRenderer({ 
    antialias: true,
    alpha: true,
    shadowMap: {
      enabled: true,
      type: THREE.PCFSoftShadowMap
    }
  });
  renderer.setSize(globeCanvas.value.clientWidth, globeCanvas.value.clientHeight);
  renderer.setPixelRatio(window.devicePixelRatio);
  globeCanvas.value.appendChild(renderer.domElement);

  // 添加光照
  const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
  scene.add(ambientLight);

  const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
  directionalLight.position.set(5, 3, 5);
  directionalLight.castShadow = true;
  directionalLight.shadow.mapSize.width = 1024;
  directionalLight.shadow.mapSize.height = 1024;
  directionalLight.shadow.camera.near = 0.5;
  directionalLight.shadow.camera.far = 50;
  directionalLight.shadow.bias = -0.0001;
  scene.add(directionalLight);

  // 创建粒子团
  globe = createDataSphere();

  // 调整相机位置
  camera.position.z = 20;

  // 添加控制器
  controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;
  controls.dampingFactor = 0.05;
  controls.rotateSpeed = 0.5;
  controls.minDistance = 15;
  controls.maxDistance = 40;

  // 初始化弹幕组
  danmakuGroup = new THREE.Group();
  scene.add(danmakuGroup);

  // 创建弹幕系统
  const createDanmaku = (text) => {
    const canvas = document.createElement('canvas');
    const context = canvas.getContext('2d');
    canvas.width = 512;
    canvas.height = 128;

    context.fillStyle = 'rgba(255, 255, 255, 0.8)';
    context.font = '36px HelveticaNeue';
    context.textAlign = 'center';
    context.textBaseline = 'middle';
    context.fillText(text, canvas.width / 2, canvas.height / 2);

    const texture = new THREE.CanvasTexture(canvas);
    const material = new THREE.SpriteMaterial({
      map: texture,
      transparent: true,
      opacity: 0.8
    });

    const sprite = new THREE.Sprite(material);
    sprite.scale.set(8, 2, 1);

    const angle = Math.random() * Math.PI * 2;
    const radiusX = 15;
    const radiusZ = 10;
    
    sprite.position.set(
      Math.cos(angle) * radiusX,
      (Math.random() - 0.5) * 10,
      Math.sin(angle) * radiusZ
    );

    sprite.userData = {
      angle: angle,
      speed: 0.005 + Math.random() * 0.003,  // 降低速度范围
      radiusX: radiusX,
      radiusZ: radiusZ,
      y: sprite.position.y
    };

    return sprite;
  };

  // 管理弹幕
  const maxDanmakus = 12;
  const danmakus = [];

  const createNewDanmaku = () => {
    if (danmakus.length >= maxDanmakus) {
      const oldDanmaku = danmakus.shift();
      danmakuGroup.remove(oldDanmaku);
    }

    const text = danmakuTexts[Math.floor(Math.random() * danmakuTexts.length)];
    const danmaku = createDanmaku(text);
    danmakuGroup.add(danmaku);
    danmakus.push(danmaku);
  };

  // 启动弹幕系统
  danmakuInterval = setInterval(createNewDanmaku, 3000);  // 增加间隔时间到3秒

  // 创建场景内容
  globe = createDataSphere();
  
  // 启动动画
  animate();
};

// 修改模型加载部分
const createDataSphere = () => {
  const group = new THREE.Group();

  // 创建粒子系统
  const comments = [
    ...Array(2273).fill().map(() => ({
      sentiment: Math.random() > 0.6 ? 'positive' : 
                Math.random() > 0.5 ? 'negative' : 'neutral'
    }))
  ];

  const particlesCount = comments.length;
  const positions = new Float32Array(particlesCount * 3);
  const colors = new Float32Array(particlesCount * 3);
  const sizes = new Float32Array(particlesCount);

  // 定义情感颜色
  const sentimentColors = {
    positive: new THREE.Color(0x4CAF50),
    negative: new THREE.Color(0xff6b6b),
    neutral: new THREE.Color(0x4a9eff)
  };

  // 创建粒子，避开中心区域
  for(let i = 0; i < particlesCount; i++) {
    let radius = 8 * (0.8 + Math.random() * 0.2);
    if (radius < 4) radius += 4;
    
    const theta = Math.random() * Math.PI * 2;
    const phi = Math.acos(2 * Math.random() - 1);

    positions[i * 3] = radius * Math.sin(phi) * Math.cos(theta);
    positions[i * 3 + 1] = radius * Math.sin(phi) * Math.sin(theta);
    positions[i * 3 + 2] = radius * Math.cos(phi);

    const color = sentimentColors[comments[i].sentiment];
    colors[i * 3] = color.r;
    colors[i * 3 + 1] = color.g;
    colors[i * 3 + 2] = color.b;

    sizes[i] = 0.2;
  }

  const geometry = new THREE.BufferGeometry();
  geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  geometry.setAttribute('size', new THREE.BufferAttribute(sizes, 1));

  const material = new THREE.PointsMaterial({
    size: 0.2,
    vertexColors: true,
    transparent: true,
    opacity: 0.8,
    blending: THREE.AdditiveBlending,
    sizeAttenuation: true,
    depthWrite: false,
    map: createCircleTexture(),  // 添加圆形纹理
  });

  const particles = new THREE.Points(geometry, material);
  group.add(particles);

  // 尝试加载模型
  try {
    const loader = new FBXLoader();
    const modelPath = new URL('./Pagoda_Essence_0405070753_texture.fbx', import.meta.url).href;
    
    loader.load(
      modelPath,
      (object) => {
        console.log('模型加载成功:', object);
        object.position.set(0, 0, 0);
        object.scale.set(0.02, 0.02, 0.02);
        
        // 加载贴图
        const textureLoader = new THREE.TextureLoader();
        const texturePath = new URL('./Pagoda_Essence_0405070753_texture.png', import.meta.url).href;
        const texture = textureLoader.load(texturePath);

        object.traverse((child) => {
          if (child.isMesh) {
            // 应用贴图到材质
            child.material = new THREE.MeshPhongMaterial({
              map: texture,  // 使用贴图
              color: 0xffffff,  // 基础白色
              emissive: 0x333333,  // 进一步降低自发光强度
              emissiveIntensity: 0.05,  // 进一步降低自发光
              specular: 0x888888,  // 调整高光颜色
              shininess: 50,  // 降低光泽度
              transparent: true,
              opacity: 0.95,
              side: THREE.DoubleSide,
              flatShading: false  // 使用平滑着色
            });
            
            // 启用阴影
            child.castShadow = true;
            child.receiveShadow = true;
          }
        });
        
        // 调整光源设置
        const lights = [
          { position: [2, 2, 2], intensity: 0.4, distance: 15, color: 0xffffff },
          { position: [-2, 1, -2], intensity: 0.3, distance: 15, color: 0xccccff },
          { position: [0, -2, 0], intensity: 0.2, distance: 15, color: 0xffffcc }
        ];
        
        lights.forEach(light => {
          const pointLight = new THREE.PointLight(
            light.color,
            light.intensity,
            light.distance
          );
          pointLight.position.set(...light.position);
          object.add(pointLight);
        });
        
        group.add(object);
      },
      (xhr) => {
        console.log((xhr.loaded / xhr.total * 100) + '% 加载中');
      },
      (error) => {
        console.error('模型加载失败:', error);
        // 创建替代物体
        const geometry = new THREE.SphereGeometry(1, 32, 32);
        const material = new THREE.MeshPhongMaterial({
          color: 0xffffff,
          emissive: 0x333333,
          emissiveIntensity: 0.05,
          specular: 0x888888,
          shininess: 50
        });
        const sphere = new THREE.Mesh(geometry, material);
        group.add(sphere);
      }
    );
  } catch (error) {
    console.error('创建模型时出错:', error);
  }

  scene.add(group);
  return group;
};

// 添加创建圆形纹理的函数
const createCircleTexture = () => {
  const canvas = document.createElement('canvas');
  canvas.width = 64;
  canvas.height = 64;
  
  const context = canvas.getContext('2d');
  const centerX = canvas.width / 2;
  const centerY = canvas.height / 2;
  const radius = canvas.width / 3;
  
  // 创建径向渐变
  const gradient = context.createRadialGradient(
    centerX, centerY, 0,
    centerX, centerY, radius
  );
  gradient.addColorStop(0, 'rgba(255,255,255,1)');
  gradient.addColorStop(1, 'rgba(255,255,255,0)');
  
  // 绘制圆形
  context.beginPath();
  context.arc(centerX, centerY, radius, 0, Math.PI * 2);
  context.fillStyle = gradient;
  context.fill();
  
  const texture = new THREE.CanvasTexture(canvas);
  texture.needsUpdate = true;
  return texture;
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
    const coords = comment;
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

// 添加弹幕文字数组
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
  '中华文明五千年'
];

// 添加弹幕控制状态
let danmakuInterval = null;
const isDanmakuEnabled = ref(true);

// 2. 定义updateDanmakus函数
const updateDanmakus = () => {
  if (!danmakuGroup) return;
  
  danmakuGroup.children.forEach(danmaku => {
    danmaku.userData.angle -= danmaku.userData.speed;
    
    danmaku.position.x = Math.cos(danmaku.userData.angle) * danmaku.userData.radiusX;
    danmaku.position.z = Math.sin(danmaku.userData.angle) * danmaku.userData.radiusZ;
    danmaku.position.y = danmaku.userData.y;

    const opacity = 0.3 + Math.max(0, danmaku.position.x / danmaku.userData.radiusX) * 0.7;
    danmaku.material.opacity = opacity;

    danmaku.lookAt(camera.position);
  });
};

onMounted(async () => {
  await nextTick();
  initScene();
  addHotspots();
  
  // 添加事件监听
  window.addEventListener('resize', handleResize);
  if (globeCanvas.value) {
    globeCanvas.value.addEventListener('mousemove', onMouseMove);
    globeCanvas.value.addEventListener('click', onClick);
  }
  
  // 初始化图表
  initTrendChart();
  initWordCloud();
  initRelationChart();
  initTimelineChart();
  
  // 更新时间
  updateTime();
  setInterval(updateTime, 1000);
});

onUnmounted(() => {
  if (animationFrameId) {
    cancelAnimationFrame(animationFrameId);
  }
  if (danmakuInterval) {
    clearInterval(danmakuInterval);
  }
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

// 在script setup中添加
const alerts = ref([
  {
    id: 1,
    level: 'high',
    title: '传播速度异常增长',
    description: '近1小时传播速度增长超过200%',
    time: '10分钟前'
  },
  {
    id: 2,
    level: 'medium',
    title: '负面情感聚集',
    description: '检测到负面评论密集出现',
    time: '15分钟前'
  },
  {
    id: 3,
    level: 'low',
    title: '话题热度上升',
    description: '相关话题讨论热度持续上升',
    time: '20分钟前'
  }
]);

// 添加activeTab状态
const activeTab = ref('relation');
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
  height: 170px;
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

/* 修改relation-panel样式 */
.relation-panel {
  position: absolute;
  bottom: 20px;
  right: 20px;
  width: 330px;
  height: 400px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(8px);
  border-radius: 15px;
  padding: 0;  /* 移除内边距 */
  color: white;
  overflow: hidden;  /* 确保内容不会溢出 */
}

.panel-header {
  padding: 15px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.tab-buttons {
  display: flex;
  gap: 15px;
}

.tab-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 14px;
  opacity: 0.7;
  position: relative;
}

.tab-btn.active {
  background: rgba(74, 158, 255, 0.2);
  opacity: 1;
}

.tab-btn:hover {
  opacity: 1;
  background: rgba(255, 255, 255, 0.1);
}

.alert-badge {
  position: absolute;
  top: -5px;
  right: -5px;
  background: #F44336;
  color: white;
  font-size: 12px;
  padding: 2px 6px;
  border-radius: 10px;
  min-width: 18px;
  text-align: center;
}

.panel-content {
  height: calc(100% - 60px);  /* 减去header高度 */
  overflow-y: auto;
  padding: 15px;
}

/* 修改关系图容器样式 */
.relation-container {
  width: 100%;
  height: 100%;
}

/* 修改预警列表样式 */
.alert-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.alert-item {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  padding: 12px;
  display: flex;
  gap: 10px;
  transition: all 0.3s ease;
}

.alert-item:hover {
  background: rgba(255, 255, 255, 0.1);
  transform: translateX(5px);
}

.alert-item.high {
  border-left: 3px solid #F44336;
}

.alert-item.medium {
  border-left: 3px solid #FF9800;
}

.alert-item.low {
  border-left: 3px solid #4CAF50;
}

/* 添加滚动条样式 */
.panel-content::-webkit-scrollbar {
  width: 6px;
}

.panel-content::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 3px;
}

.panel-content::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.2);
  border-radius: 3px;
}

.panel-content::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.3);
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

/* 在style中添加 */
.analysis-panel {
  position: absolute;
  top: 500px;
  left: 20px;
  width: 300px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(8px);
  border-radius: 15px;
  padding: 20px;
  color: white;
}

.analysis-item {
  margin-bottom: 20px;
}

.analysis-label {
  font-size: 14px;
  opacity: 0.8;
  margin-bottom: 8px;
}

.analysis-value {
  display: flex;
  align-items: center;
  gap: 10px;
}

.analysis-value .number {
  font-size: 24px;
  font-weight: bold;
}

.trend {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
}

.trend.up {
  background: rgba(76, 175, 80, 0.2);
  color: #4CAF50;
}

.trend.down {
  background: rgba(244, 67, 54, 0.2);
  color: #F44336;
}

.sentiment-bars {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.sentiment-bar {
  height: 24px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  padding: 0 10px;
  font-size: 12px;
  color: white;
}

.sentiment-bar.positive {
  background: linear-gradient(90deg, rgba(76, 175, 80, 0.8), rgba(76, 175, 80, 0.4));
}

.sentiment-bar.neutral {
  background: linear-gradient(90deg, rgba(33, 150, 243, 0.8), rgba(33, 150, 243, 0.4));
}

.sentiment-bar.negative {
  background: linear-gradient(90deg, rgba(244, 67, 54, 0.8), rgba(244, 67, 54, 0.4));
}

/* 添加新的样式 */
.analysis-row {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
}

.analysis-item.half {
  flex: 1;
  margin-bottom: 0;  /* 移除底部边距 */
}

.analysis-item.half .number {
  font-size: 28px;  /* 稍微增大数字大小 */
}

.analysis-item.half .analysis-label {
  font-size: 13px;  /* 稍微减小标签文字大小 */
  margin-bottom: 6px;
}

.analysis-item.half .trend {
  padding: 3px 6px;  /* 调整趋势标签的内边距 */
  font-size: 11px;  /* 调整趋势标签的字体大小 */
}

/* 调整分析面板的整体高度 */
.analysis-panel {
  height: auto;  /* 让高度自适应内容 */
  padding: 15px 20px;  /* 调整内边距 */
}

.analysis-content {
  margin-top: 10px;  /* 添加顶部间距 */
}
</style> 
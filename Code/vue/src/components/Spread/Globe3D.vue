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
            <div class="data-value">{{ statsData.totalComments }}</div>
            <div class="data-label">总评论数量</div>
          </div>
          <div class="data-item">
            <div class="data-value">{{ statsData.platformCount }}</div>
            <div class="data-label">评论平台数</div>
          </div>
          <div class="data-item">
            <div class="data-value">{{ statsData.countryCount }}</div>
            <div class="data-label">分析国家总数</div>
          </div>
          <div class="data-item">
            <div class="data-value">{{ statsData.timeSpan }}</div>
            <div class="data-label">评论时间跨度</div>
          </div>
        </div>
      </div>
      <!-- 趋势图卡片 -->
      <div class="data-panel trend-card">
        <h3>正面传播趋势</h3>
        <div class="trend-data">
        <div ref="trendChart" class="trend-container"></div>
        </div>
      </div>
    </div>

    <!-- 控制按钮组 - 垂直排列在传播趋势右侧 -->
    <div class="vertical-control-panel">
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
      <div class="timeline-chart-container">
        <div ref="timelineChartRef" class="timeline-chart"></div>
      </div>
    </div>

    <!-- 左下角面板 -->
    <div class="data-panel bottom-left">
      <h3>热点分布</h3>
      <div class="stats-list">
        <div v-for="(stat, region) in commentStats" 
             :key="region" 
             class="stat-item">
          <template v-if="!region.includes('占位')">
            <span class="region">{{ region }}</span>
            <span class="count">{{ stat.count }}</span>
            <div class="heat-bar" :style="{ width: `${stat.percentage}%`, backgroundColor: stat.color }"></div>
          </template>
          <template v-else>
            <!-- 占位空间，保持高度一致 -->
            <div class="placeholder-item"></div>
          </template>
        </div>
        <!-- 添加空项占位，确保至少显示5行 -->
        <div v-for="i in 5 - Object.keys(commentStats).length" 
             :key="`empty-${i}`" 
             class="stat-item">
          <div class="placeholder-item"></div>
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
            <i class="iconfont icon-chart"></i>
            平台情感分析
          </div>
          <div 
            class="tab-btn" 
            :class="{ active: activeTab === 'alert' }"
            @click="activeTab = 'alert'"
          >
            <i class="iconfont icon-warning"></i>
            传播异常分析
            <span v-if="alerts.length" class="alert-badge">{{ alerts.length }}</span>
          </div>
        </div>
      </div>

      <!-- 雷达图内容 -->
      <div v-show="activeTab === 'relation'" class="panel-content">
        <div ref="radarChartRef" class="radar-container"></div>
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


  

    <!-- 添加顶部数据卡片 -->
    <div class="top-stats">
      <div class="stat-card">
        <div class="stat-icon">
          <i class="iconfont icon-speed"></i>
        </div>
        <div class="stat-info">
          <div class="stat-label">最新月评论</div>
          <div class="stat-value">
            <span class="number">{{ topStats.latestMonthComments }}</span>
            <span class="unit">条</span>
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
            <span class="number" :class="topStats.spreadTrend > 0 ? 'up' : 'down'">
              {{ topStats.spreadTrend > 0 ? '+' : '' }}{{ topStats.spreadTrend }}%
            </span>
            <span class="unit">较上期</span>
          </div>
        </div>
      </div>

      <!-- 添加顶部状态栏 -->
      <div class="status-bar">
        <div class="status-item">
          <i class="iconfont icon-signal"></i>
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
          <option value="spot">名胜古迹</option>
          <option value="literature">影视文学</option>
          <option value="food">美食文化</option>
          <option value="folk">非遗民俗</option>
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
import ThemeAPI from '@/api/theme'; // 引入API

// 初始化全局变量
const globeCanvas = ref(null);
const radarChartRef = ref(null);
const timelineChartRef = ref(null);
let scene, camera, renderer, globe, controls;
const router = useRouter();

// 当前主题
const currentTheme = ref('spot');

// 主题数据
const themeData = ref({});

// 平台情感数据
const platformSentimentData = ref([]);

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

// 存储所有图表实例
const charts = {
  trendChart: null,
  wordCloudChart: null, 
  timelineChart: null,
  radarChart: null
};


// 添加射线检测器
const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();


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
    console.log('danmakuTexts:', danmakuTexts);
    const yesdamaku = danmakuTexts.value;
    const text = yesdamaku[Math.floor(Math.random() * yesdamaku.length)];
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
  const totalParticles = 2273; // 总评论数
  const sentimentDistribution = {
    positive: 0.65, // 65% 正面
    neutral: 0.25,  // 25% 中性
    negative: 0.10  // 10% 负面
  };

  const particlesCount = totalParticles;
  const positions = new Float32Array(particlesCount * 3);
  const colors = new Float32Array(particlesCount * 3);
  const sizes = new Float32Array(particlesCount);

  // 定义情感颜色
  const sentimentColors = {
    positive: new THREE.Color(0x4CAF50), // 绿色 - 正面
    neutral: new THREE.Color(0x4a9eff),  // 蓝色 - 中性
    negative: new THREE.Color(0xff6b6b)  // 红色 - 负面
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

    // 根据情感分布比例分配颜色
    let sentiment;
    const random = Math.random();
    if (random < sentimentDistribution.positive) {
      sentiment = 'positive';
    } else if (random < sentimentDistribution.positive + sentimentDistribution.neutral) {
      sentiment = 'neutral';
    } else {
      sentiment = 'negative';
    }

    const color = sentimentColors[sentiment];
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
    map: createCircleTexture(),
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

// 控制弹幕显示/隐藏
const toggleDanmaku = () => {
  isDanmakuEnabled.value = !isDanmakuEnabled.value;
  
  if (isDanmakuEnabled.value) {
    // 开启弹幕
    if (danmakuGroup) {
      danmakuGroup.visible = true;
    }
    // 重新启动弹幕生成
    if (!danmakuInterval) {
      danmakuInterval = setInterval(createNewDanmaku, 3000);
    }
  } else {
    // 关闭弹幕
    if (danmakuGroup) {
      danmakuGroup.visible = false;
    }
    // 停止弹幕生成
    if (danmakuInterval) {
      clearInterval(danmakuInterval);
      danmakuInterval = null;
    }
  }
  
  console.log('弹幕状态:', isDanmakuEnabled.value ? '开启' : '关闭');
};

// 添加图表初始化
let trendChart = null;
let wordCloudChart = null;
let timelineChart = null;

// 初始化趋势图
const initTrendChart = () => {
  const trendChartEl = document.querySelector('.trend-container');
  if (!trendChartEl) return;
  
  charts.trendChart = echarts.init(trendChartEl);
  
  // 获取当前主题的正面评论数据
  const getPositiveTrendData = () => {
    if (!themeData.value || !currentTheme.value) return [];
    
    const theme = currentTheme.value;
    const themeInfo = themeData.value[theme];
    
    // 提取月份和正面评论数据
    const trendData = themeInfo.monthly_data.map(monthData => ({
      month: monthData.month,
      positive: monthData.platforms.reduce((sum, platform) => 
        sum + platform.sentiments.positive, 0)
    }));
    
    // 按月份排序
    trendData.sort((a, b) => new Date(a.month) - new Date(b.month));
    
    return trendData;
  };
  
  const trendData = getPositiveTrendData();
  
  charts.trendChart.setOption({
    grid: {
      top: 10,
      right: 10,
      bottom: 10,
      left: 30,
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: trendData.map(item => item.month),
      axisLine: {
        lineStyle: { color: 'rgba(255,255,255,0.3)' }
      },
      axisLabel: { 
        color: 'rgba(255,255,255,0.7)', 
        fontFamily: 'HelveticaNeue',
        fontSize: 10
      }
    },
    yAxis: {
      type: 'value',
      axisLine: {
        lineStyle: { color: 'rgba(255,255,255,0.3)' }
      },
      axisLabel: { 
        color: 'rgba(255,255,255,0.7)', 
        fontFamily: 'HelveticaNeue',
        fontSize: 10
      },
      splitLine: {
        lineStyle: { color: 'rgba(255,255,255,0.1)' }
      }
    },
    series: [{
      data: trendData.map(item => item.positive),
      type: 'line',
      smooth: true,
      symbol: 'circle',
      symbolSize: 6,
      lineStyle: {
        width: 2,
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
  
  // 立即调整大小以确保正确渲染
  setTimeout(() => {
    if (charts.trendChart) {
      charts.trendChart.resize();
    }
  }, 100);
};

// 初始化词云图
const initWordCloud = () => {
  // 什么也不做，我们将在fetchShortComments中直接渲染词云
  console.log('跳过词云图初始化');
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
const danmakuTexts = ref([
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
]);

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

// 添加获取主题评论情感数据
const fetchThemeCommentsSentiment = async () => {
  try {
    const response = await ThemeAPI.getThemeCommentsSentiment();
    if (response.code === 200) {
      themeData.value = response.data;
      console.log('主题情感数据:', themeData.value);
      
      // 处理当前主题的平台情感数据
      processPlatformSentimentData();
      
      // 初始化统计数据
      updateStatsData();
      
      // 初始化顶部统计数据
      updateTopStats();
      
      // 生成初始预警
      generateAlerts();
      
      // 确保DOM已更新
      await nextTick();
      
      // 初始化平台情感图表
      initPlatformChart();
    } else {
      console.error('获取主题情感数据失败:', response.message);
    }
  } catch (error) {
    console.error('获取主题情感数据出错:', error);
  }
};

// 平台名称映射
const platformNameMap = {
  'dy': '抖音',
  'bili': '哔哩哔哩',
  'bilibili': '哔哩哔哩',
  'zhihu': '知乎',
  'xhs': '小红书'
};

// 处理平台情感数据
const processPlatformSentimentData = () => {
  const theme = currentTheme.value;
  if (!themeData.value || !themeData.value[theme]) return;
  
  const themeInfo = themeData.value[theme];
  const platforms = new Set();
  const platformData = {};
  const allDates = new Set(); // 收集所有日期
  
  // 收集所有平台和日期
  themeInfo.monthly_data.forEach(monthData => {
    // 提取月份添加到日期集合
    allDates.add(monthData.month);
    
    monthData.platforms.forEach(platform => {
      let platformName = platform.platform;
      
      // 使用映射转换平台名称
      if (platformNameMap[platformName]) {
        platformName = platformNameMap[platformName];
      }
      
      platforms.add(platformName);
      
      if (!platformData[platformName]) {
        platformData[platformName] = {
          positive: 0,
          neutral: 0,
          negative: 0
        };
      }
      
      // 累加情感数据
      platformData[platformName].positive += platform.sentiments.positive;
      platformData[platformName].neutral += platform.sentiments.neutral;
      platformData[platformName].negative += platform.sentiments.negative;
    });
  });
  
  // 格式化为图表数据
  platformSentimentData.value = Array.from(platforms).map(platform => {
    const data = platformData[platform];
    const total = data.positive + data.neutral + data.negative;
    return {
      platform,
      positive: data.positive,
      neutral: data.neutral,
      negative: data.negative,
      total: total,
      positiveRate: total > 0 ? Math.round((data.positive / total) * 100) : 0,
      neutralRate: total > 0 ? Math.round((data.neutral / total) * 100) : 0,
      negativeRate: total > 0 ? Math.round((data.negative / total) * 100) : 0
    };
  });
  
  // 处理时间轴数据
  const sortedDates = Array.from(allDates).sort();
  timelineRange.value.dates = sortedDates;
  
  if (sortedDates.length > 0) {
    timelineRange.value.start = sortedDates[0];
    timelineRange.value.end = sortedDates[sortedDates.length - 1];
    
    // 初始化选中的时间范围
    selectedTimeRange.value.startDate = sortedDates[0];
    selectedTimeRange.value.endDate = sortedDates[sortedDates.length - 1];
  }
  
  // 更新时间轴图表
  initTimelineChart();
  
  console.log('平台情感数据:', platformSentimentData.value);
  console.log('时间轴范围:', timelineRange.value);
};


// 初始化平台情感图表
const initPlatformChart = () => {
  if (!radarChartRef.value) return;
  
  // 如果图表存在则销毁重建
  if (charts.radarChart) {
    charts.radarChart.dispose();
  }
  
  charts.radarChart = echarts.init(radarChartRef.value);
  
  // 确保有数据
  if (platformSentimentData.value.length === 0) {
    charts.radarChart.setOption({
      title: {
        text: '暂无平台数据',
        textStyle: { color: '#fff', fontSize: 14, fontFamily: 'HelveticaNeue' },
        left: 'center',
        top: 'middle'
      }
    });
    return;
  }
  
  // 准备平台名称
  const platforms = platformSentimentData.value.map(item => item.platform);
  
  // 如果只有一个平台，添加一个空白占位
  if (platforms.length === 1) {
    // 创建布局grid
    const gridOption = {
      textStyle: {
        fontFamily: 'HelveticaNeue, Helvetica Neue, Helvetica, Arial, sans-serif'
      },
      legend: {
        data: ['正面情感', '中性情感', '负面情感'],
        textStyle: { 
          color: '#fff',
          fontFamily: 'HelveticaNeue'
        },
        top: 0
      },
      grid: {
        top: '50%', // 上半部分放饼图
        bottom: '5%',
        left: 10,
        right: 10,
        height: '40%', // 给柱状图一点更多高度
        containLabel: true
      },
      xAxis: [
        {
          gridIndex: 0,
          type: 'category',
          data: platforms,
          axisLine: {
            lineStyle: { color: 'rgba(255, 255, 255, 0.3)' }
          },
          axisLabel: { 
            color: 'rgba(255, 255, 255, 0.7)',
            rotate: 0,
            fontFamily: 'HelveticaNeue'
          }
        }
      ],
      yAxis: [
        {
          gridIndex: 0,
          type: 'value',
          name: '评论数量',
          nameTextStyle: {
            color: 'rgba(255, 255, 255, 0.7)',
            fontFamily: 'HelveticaNeue'
          },
          axisLine: {
            lineStyle: { color: 'rgba(255, 255, 255, 0.3)' }
          },
          axisLabel: { 
            color: 'rgba(255, 255, 255, 0.7)',
            fontFamily: 'HelveticaNeue'
          },
          splitLine: {
            lineStyle: { color: 'rgba(255, 255, 255, 0.1)' }
          }
        }
      ],
      series: [
        {
          name: '正面情感',
          type: 'bar',
          stack: '情感',
          xAxisIndex: 0,
          yAxisIndex: 0,
          emphasis: {
            focus: 'series'
          },
          data: platformSentimentData.value.map(item => item.positive),
          barWidth: '40%',
          barMaxWidth: 40, // 限制柱子最大宽度
          itemStyle: {
            borderRadius: [0, 0, 0, 0]
          }
        },
        {
          name: '中性情感',
          type: 'bar',
          stack: '情感',
          xAxisIndex: 0,
          yAxisIndex: 0,
          emphasis: {
            focus: 'series'
          },
          data: platformSentimentData.value.map(item => item.neutral)
        },
        {
          name: '负面情感',
          type: 'bar',
          stack: '情感',
          xAxisIndex: 0,
          yAxisIndex: 0,
          emphasis: {
            focus: 'series'
          },
          data: platformSentimentData.value.map(item => item.negative)
        },
        {
          type: 'pie',
          radius: ['15%', '30%'],
          center: ['50%', '25%'], // 将饼图移到上半部分
          avoidLabelOverlap: false,
          itemStyle: {
            borderRadius: 10,
            borderColor: 'rgba(0, 0, 0, 0.1)',
            borderWidth: 2
          },
          label: {
            show: false
          },
          emphasis: {
            label: {
              show: true,
              fontSize: '14',
              fontWeight: 'bold',
              color: '#fff',
              fontFamily: 'HelveticaNeue'
            }
          },
          labelLine: {
            show: false
          },
          data: [
            { 
              value: platformSentimentData.value[0].positive, 
              name: '正面情感'
            },
            { 
              value: platformSentimentData.value[0].neutral, 
              name: '中性情感'
            },
            { 
              value: platformSentimentData.value[0].negative, 
              name: '负面情感'
            }
          ]
        }
      ]
    };
    
    // 使用组合图表展示
    charts.radarChart.setOption(gridOption);
  } else {
    // 多个平台时使用堆叠柱状图
    const option = {
      textStyle: {
        fontFamily: 'HelveticaNeue, Helvetica Neue, Helvetica, Arial, sans-serif'
      },
      color: ['#4a9eff', '#67e0e3', '#ff6b6b'],
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'shadow'
        },
        formatter: function(params) {
          // 取第一个系列的平台名
          const platformName = params[0].name;
          let html = `${platformName}<br/>`;
          
          // 添加每个系列的数据
          params.forEach(param => {
            html += `${param.marker}${param.seriesName}: ${param.value}条<br/>`;
          });
          
          return html;
        },
        backgroundColor: 'rgba(0,0,0,0.7)',
        borderColor: '#4a9eff',
        textStyle: {
          color: '#fff',
          fontFamily: 'HelveticaNeue'
        }
      },
      legend: {
        data: ['正面情感', '中性情感', '负面情感'],
        textStyle: { 
          color: '#fff',
          fontFamily: 'HelveticaNeue'
        },
        top: 0,
        itemWidth: 15,
        itemHeight: 10,
        itemGap: 15
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        top: '50px',
        height: '75%', // 减少图表高度，避免标签重叠
        containLabel: true
      },
      xAxis: {
        type: 'category',
        data: platforms,
        axisLine: {
          lineStyle: { color: 'rgba(255, 255, 255, 0.3)' }
        },
        axisLabel: { 
          color: 'rgba(255, 255, 255, 0.7)',
          rotate: platforms.length > 3 ? 30 : 0,
          fontFamily: 'HelveticaNeue',
          fontSize: 10,
          interval: 0
        }
      },
      yAxis: {
        type: 'value',
        name: '评论数量',
        nameTextStyle: {
          color: 'rgba(255, 255, 255, 0.7)',
          fontFamily: 'HelveticaNeue',
          fontSize: 10,
          padding: [0, 0, 0, 0]
        },
        axisLine: {
          lineStyle: { color: 'rgba(255, 255, 255, 0.3)' }
        },
        axisLabel: { 
          color: 'rgba(255, 255, 255, 0.7)',
          fontFamily: 'HelveticaNeue',
          fontSize: 10
        },
        splitLine: {
          lineStyle: { color: 'rgba(255, 255, 255, 0.1)' }
        },
        max: function(value) {
          // 给最大值增加一些余量，避免数据触顶
          return Math.ceil(value.max * 1.2);
        }
      },
      series: [
        {
          name: '正面情感',
          type: 'bar',
          stack: '情感',
          emphasis: {
            focus: 'series'
          },
          data: platformSentimentData.value.map(item => item.positive),
          barWidth: '40%',
          barMaxWidth: 40, // 限制柱子最大宽度
          itemStyle: {
            borderRadius: [4, 4, 0, 0],
            shadowColor: 'rgba(0, 0, 0, 0.2)',
            shadowBlur: 5
          }
        },
        {
          name: '中性情感',
          type: 'bar',
          stack: '情感',
          emphasis: {
            focus: 'series'
          },
          data: platformSentimentData.value.map(item => item.neutral),
          itemStyle: {
            shadowColor: 'rgba(0, 0, 0, 0.2)',
            shadowBlur: 5
          }
        },
        {
          name: '负面情感',
          type: 'bar',
          stack: '情感',
          emphasis: {
            focus: 'series'
          },
          data: platformSentimentData.value.map(item => item.negative),
          itemStyle: {
            borderRadius: [0, 0, 4, 4],
            shadowColor: 'rgba(0, 0, 0, 0.2)',
            shadowBlur: 5
          }
        }
      ]
    };
    
    charts.radarChart.setOption(option);
  }
};

// 更新图表方法
const updateCharts = () => {
  if (charts.radarChart) {
    charts.radarChart.resize();
  }
  if (charts.timelineChart) {
    charts.timelineChart.resize();
  }
  if (charts.trendChart) {
    charts.trendChart.resize();
  }
  if (charts.wordCloudChart) {
    charts.wordCloudChart.resize();
  }
};

// 修改handleThemeChange函数，加入主题变更后的数据刷新
const handleThemeChange = async () => {
  // 更新当前主题
  currentTheme.value = selectedTheme.value || 'spot';
  console.log('Selected theme:', currentTheme.value);
  
  // 重新处理数据并更新图表
  processPlatformSentimentData();
  
  // 获取新的短评论数据
  await fetchShortComments();
  
  // 获取新的IP分布数据
  await fetchIpDistribution();
  
  // 确保DOM已更新
  await nextTick();
  
  // 更新所有图表
  if (charts.radarChart) {
    initPlatformChart();
  }
  if (charts.trendChart) {
    initTrendChart();
  }
  
  // 更新统计数据
  updateStatsData();
  
  // 更新顶部统计数据
  updateTopStats();
  
  // 生成新的预警
  generateAlerts();
};

// 重写获取短评论数据的方法
const fetchShortComments = async () => {
  try {
    const response = await ThemeAPI.getThemeShortComments();
    console.log('短评论响应:', response);
    
    if (response.code === 200 && response.data) {
      const themeComments = response.data[currentTheme.value];
      console.log('当前主题评论:', themeComments);
      
      if (themeComments && themeComments.comments) {
        // 更新弹幕文本
        danmakuTexts.value = themeComments.comments.map(comment => comment.text);
        console.log('更新后的弹幕文本:', danmakuTexts.value);
        
        // 渲染词云图
        const wordCloudEl = document.querySelector('.word-cloud-container');
        console.log('词云图容器:', wordCloudEl);
        
        if (wordCloudEl) {
          // 确保容器有正确的尺寸
          console.log('词云图容器尺寸:', wordCloudEl.clientWidth, wordCloudEl.clientHeight);
          
          // 销毁旧实例
          if (charts.wordCloudChart) {
            charts.wordCloudChart.dispose();
            charts.wordCloudChart = null;
          }
          
          // 创建新实例
          charts.wordCloudChart = echarts.init(wordCloudEl);
          
          // 准备词云数据 - 直接使用文本
          const wordCloudData = [];
          
          // 遍历评论文本，直接构建词云数据
          themeComments.comments.forEach(comment => {
            wordCloudData.push({
              name: comment.text,
              value: Math.floor(Math.random() * 50) + 30
            });
          });
          
          console.log('词云数据:', wordCloudData);
          
          if (wordCloudData.length > 0) {
            // 设置词云图配置
            const option = {
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
                  fontFamily: 'HelveticaNeue',
                  fontWeight: 'bold',
                  color: function() {
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
                data: wordCloudData
              }]
            };
            
            console.log('设置词云图选项');
            charts.wordCloudChart.setOption(option);
            
            // 立即调整大小
            setTimeout(() => {
              if (charts.wordCloudChart) {
                console.log('调整词云图大小');
                charts.wordCloudChart.resize();
              }
            }, 100);
          }
        } else {
          console.error('找不到词云图容器元素');
        }
      } else {
        console.warn('没有找到当前主题的评论数据');
      }
    } else {
      console.error('获取短评论数据失败:', response.message || '未知错误');
    }
  } catch (error) {
    console.error('获取短评论数据出错:', error);
  }
};

// 在script setup中添加IP分布数据的响应式变量
const ipDistributionData = ref(null);

// 添加获取IP地区分布数据的方法
const fetchIpDistribution = async () => {
  try {
    const response = await ThemeAPI.getThemeIpDistribution();
    console.log('IP分布响应:', response);
    
    if (response.code === 200 && response.data) {
      ipDistributionData.value = response.data;
      console.log('当前主题IP分布:', ipDistributionData.value[currentTheme.value]);
      
      // 更新热点分布
      updateHotspots();
    } else {
      console.error('获取IP分布数据失败:', response.message || '未知错误');
    }
  } catch (error) {
    console.error('获取IP分布数据出错:', error);
  }
};

// 更新热点分布
const updateHotspots = () => {
  if (!ipDistributionData.value || !currentTheme.value || !ipDistributionData.value[currentTheme.value]) {
    console.warn('无法更新热点分布，数据不完整');
    return;
  }
  
  // 获取当前主题的IP分布数据
  const themeIpData = ipDistributionData.value[currentTheme.value];
  console.log('更新热点分布，当前主题:', currentTheme.value, '数据:', themeIpData);
  
  // 清除现有热点
  if (scene) {
    // 找到并移除现有热点
    const existingHotspots = scene.children.filter(child => child.name === 'hotspot');
    existingHotspots.forEach(hotspot => {
      scene.remove(hotspot);
    });
  }
  
  // 直接过滤掉"其他"，然后取前五个省份
  const realProvinces = themeIpData.ip_distribution.filter(item => item.province !== '其他').slice(0, 5);
  console.log('前5个真实省份数据:', realProvinces);
  
  // 计算这些省份的总评论数（用于计算百分比）
  const totalRealComments = realProvinces.reduce((sum, item) => sum + item.count, 0);
  
  // 创建一个新的commentStats对象
  commentStats.value = {};
  
  // 添加热点和更新统计数据
  realProvinces.forEach(item => {
    const province = item.province;
    const count = item.count;
    
    // 计算百分比（基于真实省份的总数）
    const percentage = Math.round((count / totalRealComments) * 100);
    
    // 更新统计信息
    commentStats.value[province] = {
      count: count,
      percentage: percentage,
      // 根据评论数量调整颜色亮度
      color: `rgb(255, ${Math.floor(128 + (percentage / 100) * 127)}, 0)`
    };
    
    // 添加热点
    const coords = getProvinceCoordinates(province);
    if (coords) {
      addHotspot(coords.lat, coords.lng, count);
    }
  });
  
  // 如果显示的省份不足5个，添加占位数据保持卡片高度
  const displayCount = Object.keys(commentStats.value).length;
  for (let i = displayCount + 1; i <= 5; i++) {
    commentStats.value[`占位${i}`] = {
      count: 0,
      percentage: 0,
      color: 'transparent'
    };
  }
  
  console.log('热点统计数据已更新:', commentStats.value);
};

// 省份名称到经纬度的映射表
const getProvinceCoordinates = (province) => {
  const provinceMap = {
    '北京': { lat: 39.9042, lng: 116.4074 },
    '上海': { lat: 31.2304, lng: 121.4737 },
    '广东': { lat: 23.1357, lng: 113.2644 },
    '江苏': { lat: 32.0603, lng: 118.7969 },
    '浙江': { lat: 30.2741, lng: 120.1551 },
    '山东': { lat: 36.6683, lng: 117.0207 },
    '河南': { lat: 34.7655, lng: 113.7662 },
    '河北': { lat: 38.0428, lng: 114.5149 },
    '辽宁': { lat: 41.8057, lng: 123.4315 },
    '四川': { lat: 30.6500, lng: 104.0761 },
    '湖北': { lat: 30.5928, lng: 114.3055 },
    '福建': { lat: 26.0992, lng: 119.2956 },
    '湖南': { lat: 28.1123, lng: 112.9837 },
    '安徽': { lat: 31.8612, lng: 117.2835 },
    '内蒙古': { lat: 40.8173, lng: 111.7660 },
    '陕西': { lat: 34.2656, lng: 108.9547 },
    '江西': { lat: 28.6760, lng: 115.9047 },
    '广西': { lat: 22.8152, lng: 108.3275 },
    '山西': { lat: 37.8736, lng: 112.5623 },
    '重庆': { lat: 29.4316, lng: 106.9123 },
    '吉林': { lat: 43.8169, lng: 125.3247 },
    '云南': { lat: 25.0453, lng: 102.7097 },
    '天津': { lat: 39.3433, lng: 117.3616 },
    '黑龙江': { lat: 45.7421, lng: 126.6615 },
    '新疆': { lat: 43.8266, lng: 87.6168 },
    '贵州': { lat: 26.5982, lng: 106.7072 },
    '甘肃': { lat: 36.0587, lng: 103.8263 },
    '海南': { lat: 20.0402, lng: 110.1995 },
    '宁夏': { lat: 38.4664, lng: 106.2731 },
    '青海': { lat: 36.6190, lng: 101.7784 },
    '西藏': { lat: 29.6499, lng: 91.1167 },
    '香港': { lat: 22.3193, lng: 114.1694 },
    '澳门': { lat: 22.1987, lng: 113.5439 },
    '台湾': { lat: 25.0328, lng: 121.5654 },
    '其他': { lat: 35.8617, lng: 104.1954 } // 使用中国中心点作为"其他"的坐标
  };
  
  return provinceMap[province];
};

// 修改热点添加方法，支持根据评论数量调整大小
const addHotspot = (lat, lng, count = 100) => {
  if (!scene) return;

  // 将经纬度转换为3D坐标
  const phi = (90 - lat) * Math.PI / 180;
  const theta = (lng + 180) * Math.PI / 180;
  
  // 球体半径 - 使用固定值替代globeRadius
  const radius = 10; // 固定为10作为半径
  
  // 三维坐标
  const x = -radius * Math.sin(phi) * Math.cos(theta);
  const y = radius * Math.cos(phi);
  const z = radius * Math.sin(phi) * Math.sin(theta);
  
  // 根据评论数量决定热点大小
  const size = Math.max(0.1, Math.min(0.3, 0.1 + (count / 1000) * 0.2));
  
  // 创建热点几何体
  const geometry = new THREE.SphereGeometry(size, 16, 16);
  const material = new THREE.MeshBasicMaterial({
    color: 0xff0000,
    transparent: true,
    opacity: 0.8
  });
  
  const hotspot = new THREE.Mesh(geometry, material);
  hotspot.position.set(x, y, z);
  hotspot.name = 'hotspot';
  hotspot.userData = { lat, lng, count };
  
  scene.add(hotspot);
  
  // 添加闪烁效果
  const pulse = new THREE.PointLight(0xff0000, 1, 2);
  pulse.position.set(x, y, z);
  pulse.name = 'hotspot';
  scene.add(pulse);
};

onMounted(async () => {
  await nextTick();
  initScene();
  // 不再调用原来的addHotspots，因为现在我们使用真实数据添加热点
  
  // 添加事件监听
  window.addEventListener('resize', handleResize);
  if (globeCanvas.value) {
    globeCanvas.value.addEventListener('click', onClick);
  }
  
  // 获取主题数据并初始化图表
  await fetchThemeCommentsSentiment();
  
  // 获取短评论数据
  await fetchShortComments();
  
  // 获取IP分布数据
  await fetchIpDistribution();
  
  // 确保DOM已更新
  await nextTick();
  
  // 初始化其他图表
  initTrendChart();
  initTimelineChart();
  
  // 初始化传播数据分析卡片
  updateAnalysisPanel();
  
  // 初始化统计数据
  updateStatsData();
  
  // 初始化顶部统计数据
  updateTopStats();
  
  // 更新时间
  updateTime();
  setInterval(updateTime, 1000);
  
  // 添加窗口大小变化时的图表重绘
  window.addEventListener('resize', updateCharts);
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
  
  // 移除窗口大小变化的监听
  window.removeEventListener('resize', updateCharts);
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
  console.log('开始初始化时间轴...');
  if (!timelineChartRef.value) {
    console.error('找不到时间轴元素 timelineChartRef.value');
    return;
  }

  if (charts.timelineChart) {
    console.log('销毁旧的时间轴图表');
    charts.timelineChart.dispose();
  }

  console.log('初始化时间轴图表尺寸', timelineChartRef.value.clientWidth, timelineChartRef.value.clientHeight);
  
  try {
    charts.timelineChart = echarts.init(timelineChartRef.value);
    console.log('时间轴图表初始化成功');
  } catch (error) {
    console.error('初始化时间轴图表失败:', error);
    return;
  }
  
  // 准备时间轴数据
  const dates = timelineRange.value.dates.length > 0 ? 
                timelineRange.value.dates : 
                ['2017-11', '2018-06', '2019-01', '2019-08', '2020-03', '2020-10', '2021-05', '2021-12', '2022-07', '2023-02', '2023-09', '2024-04'];
  
  console.log('时间轴日期数据:', dates);
  
  // 初始化选中的时间范围
  selectedTimeRange.value.startDate = dates[0];
  selectedTimeRange.value.endDate = dates[dates.length - 1];
  
  // 生成模拟数据
  const mockData = dates.map(date => {
    return {
      date: date,
      value: Math.floor(Math.random() * 100) + 50
    };
  });
  
  // 确保日期是有序的
  mockData.sort((a, b) => {
    return new Date(a.date) - new Date(b.date);
  });
  
  // 设置时间轴图表
  const option = {
    animation: false, // 关闭动画，可能有助于调试
    tooltip: {
      trigger: 'axis',
      formatter: '{b}: {c}条评论',
      backgroundColor: 'rgba(0,0,0,0.7)',
      borderColor: '#4a9eff',
      textStyle: {
        color: '#fff',
        fontFamily: 'HelveticaNeue'
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: 25, // 增加底部留出空间给滑块
      top: 5,
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: mockData.map(item => item.date),
      boundaryGap: false,
      axisLine: { 
        show: true,
        lineStyle: { color: 'rgba(255,255,255,0.5)' } 
      },
      axisTick: {
        show: true,
        alignWithLabel: true
      },
      axisLabel: { 
        show: true,
        color: 'rgba(255,255,255,0.8)', 
        fontFamily: 'HelveticaNeue',
        showMinLabel: true,
        showMaxLabel: true,
        interval: 'auto'
      }
    },
    yAxis: {
      type: 'value',
      show: true,
      axisLine: { 
        show: true,
        lineStyle: { color: 'rgba(255,255,255,0.5)' } 
      },
      axisLabel: { 
        show: true,
        color: 'rgba(255,255,255,0.8)', 
        fontFamily: 'HelveticaNeue' 
      },
      splitLine: { 
        show: true,
        lineStyle: { color: 'rgba(255,255,255,0.2)' } 
      }
    },
    dataZoom: [{
      type: 'slider',
      show: true,
      start: 0,
      end: 100,
      height: 15, // 增加滑块高度，使其可拖动
      bottom: 0,
      borderColor: 'rgba(255,255,255,0.4)',
      textStyle: {
        color: 'rgba(255,255,255,0.8)',
        fontFamily: 'HelveticaNeue',
        fontSize: 10
      },
      handleStyle: {
        color: '#4a9eff',
        borderColor: '#4a9eff',
        borderWidth: 2,
        opacity: 1, // 增加不透明度，使手柄更明显
        shadowBlur: 4,
        shadowColor: 'rgba(0,0,0,0.5)'
      },
      handleSize: '150%', // 增大手柄尺寸
      backgroundColor: 'rgba(50,50,50,0.2)',
      fillerColor: 'rgba(74,158,255,0.3)',
      moveHandleSize: 7, // 增大移动手柄
      showDetail: true, // 显示详细信息
      brushSelect: false
    }],
    series: [{
      data: mockData.map(item => item.value),
      type: 'line',
      smooth: true,
      symbol: 'circle',
      symbolSize: 8,
      showSymbol: true,
      itemStyle: {
        color: '#4a9eff',
        borderWidth: 2,
        borderColor: '#fff'
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
        opacity: 0.5,
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
          offset: 0,
          color: 'rgba(74,158,255,0.5)'
        }, {
          offset: 1,
          color: 'rgba(74,158,255,0.1)'
        }])
      }
    }]
  };
  
  console.log('设置时间轴选项', JSON.stringify(option.xAxis.data).substring(0, 100) + '...');
  try {
    charts.timelineChart.setOption(option);
    console.log('时间轴选项设置成功');
    
    // 添加dataZoom事件监听
    charts.timelineChart.on('datazoom', function(params) {
      // 获取当前选中的区间范围（百分比）
      const startValue = params.start;
      const endValue = params.end;
      
      // 计算选中区间对应的实际日期索引
      const startIndex = Math.floor(dates.length * startValue / 100);
      const endIndex = Math.min(Math.ceil(dates.length * endValue / 100), dates.length - 1);
      
      // 获取选中区间的日期
      const selectedDates = dates.slice(startIndex, endIndex + 1);
      
      if (selectedDates.length > 0) {
        // 更新全场数据，基于选中的时间区间
        updateDataByTimeRange(startValue, endValue, selectedDates);
      }
    });
    
  } catch (error) {
    console.error('设置时间轴选项失败:', error);
  }
  
  // 延迟resize以确保图表正确渲染
  setTimeout(() => {
    if (charts.timelineChart) {
      try {
        console.log('重新调整时间轴图表大小');
        charts.timelineChart.resize();
      } catch (error) {
        console.error('调整时间轴大小失败:', error);
      }
    }
  }, 300);
};

// 添加主题选择相关逻辑
const selectedTheme = ref('spot');

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

// 添加时间范围数据
const timelineRange = ref({
  start: '',
  end: '',
  dates: []
});

// 添加当前选中的时间范围
const selectedTimeRange = ref({
  startIndex: 0,
  endIndex: 100, // 初始显示全部数据
  startDate: '',
  endDate: ''
});

// 时间轴数据变化时更新全场数据
const updateDataByTimeRange = (startIndex, endIndex, dates) => {
  console.log(`更新时间区间数据: ${startIndex}% - ${endIndex}%, 日期范围: ${dates[0]} - ${dates[dates.length-1]}`);
  
  // 更新选中的时间范围
  selectedTimeRange.value = {
    startIndex,
    endIndex,
    startDate: dates[0],
    endDate: dates[dates.length-1]
  };
  
  // 根据时间范围更新平台情感数据
  updatePlatformDataByTimeRange();
  
  // 更新趋势图
  updateTrendChartByTimeRange();
  
  // 更新词云图
  updateWordCloudByTimeRange();
  
  // 更新传播数据分析卡片
  updateAnalysisPanel();
  
  // 更新统计数据
  updateStatsData();
  
  // 更新顶部统计数据
  updateTopStats();
  
  // 生成新的预警
  generateAlerts();
};

// 添加更新传播数据分析卡片的函数
const updateAnalysisPanel = () => {
  if (!themeData.value || !currentTheme.value) return;
  
  const theme = currentTheme.value;
  const themeInfo = themeData.value[theme];
  
  // 过滤符合当前时间范围的月份数据
  const filteredMonthlyData = themeInfo.monthly_data.filter(monthData => {
    return monthData.month >= selectedTimeRange.value.startDate && 
           monthData.month <= selectedTimeRange.value.endDate;
  });
  
  // 按月份排序
  filteredMonthlyData.sort((a, b) => new Date(a.month) - new Date(b.month));
  
  if (filteredMonthlyData.length >= 2) {
    // 计算传播速度指数（最新月份与上个月的评论总数比较）
    const latestMonth = filteredMonthlyData[filteredMonthlyData.length - 1];
    const previousMonth = filteredMonthlyData[filteredMonthlyData.length - 2];
    
    const latestTotal = latestMonth.platforms.reduce((sum, platform) => 
      sum + platform.sentiments.positive + platform.sentiments.neutral + platform.sentiments.negative, 0);
    
    const previousTotal = previousMonth.platforms.reduce((sum, platform) => 
      sum + platform.sentiments.positive + platform.sentiments.neutral + platform.sentiments.negative, 0);
    
    const speedIndex = previousTotal > 0 ? 
      Math.round((latestTotal - previousTotal) / previousTotal * 100) : 0;
    
    // 计算互动参与度（正面评论占比）
    const latestPositive = latestMonth.platforms.reduce((sum, platform) => 
      sum + platform.sentiments.positive, 0);
    
    const latestTotalComments = latestMonth.platforms.reduce((sum, platform) => 
      sum + platform.sentiments.positive + platform.sentiments.neutral + platform.sentiments.negative, 0);
    
    const engagementIndex = latestTotalComments > 0 ? 
      Math.round((latestPositive / latestTotalComments) * 100) : 0;
    
    // 计算整个时间区间的情感倾向
    let totalPositive = 0;
    let totalNeutral = 0;
    let totalNegative = 0;
    
    // 遍历整个时间区间内的所有月份数据
    filteredMonthlyData.forEach(monthData => {
      monthData.platforms.forEach(platform => {
        totalPositive += platform.sentiments.positive;
        totalNeutral += platform.sentiments.neutral;
        totalNegative += platform.sentiments.negative;
      });
    });
    
    const totalComments = totalPositive + totalNeutral + totalNegative;
    const positivePercentage = Math.round((totalPositive / totalComments) * 100);
    const neutralPercentage = Math.round((totalNeutral / totalComments) * 100);
    const negativePercentage = Math.round((totalNegative / totalComments) * 100);
    
    // 更新DOM中的数据
    const speedElement = document.querySelector('.analysis-value .number');
    const speedTrendElement = document.querySelector('.analysis-value .trend');
    const engagementElement = document.querySelector('.analysis-item.half:last-child .number');
    const engagementTrendElement = document.querySelector('.analysis-item.half:last-child .trend');
    
    if (speedElement && speedTrendElement) {
      speedElement.textContent = Math.abs(speedIndex);
      speedTrendElement.textContent = speedIndex >= 0 ? `↑${speedIndex}%` : `↓${Math.abs(speedIndex)}%`;
      speedTrendElement.className = `trend ${speedIndex >= 0 ? 'up' : 'down'}`;
    }
    
    if (engagementElement && engagementTrendElement) {
      engagementElement.textContent = engagementIndex;
      engagementTrendElement.textContent = `正面评论占比`;
      engagementTrendElement.className = 'trend up';
    }
    
    // 更新情感倾向条
    const positiveBar = document.querySelector('.sentiment-bar.positive');
    const neutralBar = document.querySelector('.sentiment-bar.neutral');
    const negativeBar = document.querySelector('.sentiment-bar.negative');
    
    if (positiveBar) {
      positiveBar.style.width = `${positivePercentage}%`;
      positiveBar.textContent = `正面 ${positivePercentage}%`;
    }
    if (neutralBar) {
      neutralBar.style.width = `${neutralPercentage}%`;
      neutralBar.textContent = `中性 ${neutralPercentage}%`;
    }
    if (negativeBar) {
      negativeBar.style.width = `${negativePercentage}%`;
      negativeBar.textContent = `负面 ${negativePercentage}%`;
    }
  }
};

// 根据时间范围更新平台情感数据
const updatePlatformDataByTimeRange = () => {
  if (!themeData.value || !currentTheme.value) return;
  
  const theme = currentTheme.value;
  const themeInfo = themeData.value[theme];
  
  // 过滤符合当前时间范围的月份数据
  const filteredMonthlyData = themeInfo.monthly_data.filter(monthData => {
    return monthData.month >= selectedTimeRange.value.startDate && 
           monthData.month <= selectedTimeRange.value.endDate;
  });
  
  // 使用过滤后的数据重新计算平台情感数据
  const platforms = new Set();
  const platformData = {};
  
  filteredMonthlyData.forEach(monthData => {
    monthData.platforms.forEach(platform => {
      let platformName = platform.platform;
      
      // 使用映射转换平台名称
      if (platformNameMap[platformName]) {
        platformName = platformNameMap[platformName];
      }
      
      platforms.add(platformName);
      
      if (!platformData[platformName]) {
        platformData[platformName] = {
          positive: 0,
          neutral: 0,
          negative: 0
        };
      }
      
      // 累加情感数据
      platformData[platformName].positive += platform.sentiments.positive;
      platformData[platformName].neutral += platform.sentiments.neutral;
      platformData[platformName].negative += platform.sentiments.negative;
    });
  });
  
  // 格式化为图表数据
  platformSentimentData.value = Array.from(platforms).map(platform => {
    const data = platformData[platform];
    const total = data.positive + data.neutral + data.negative;
    return {
      platform,
      positive: data.positive,
      neutral: data.neutral,
      negative: data.negative,
      total: total,
      positiveRate: total > 0 ? Math.round((data.positive / total) * 100) : 0,
      neutralRate: total > 0 ? Math.round((data.neutral / total) * 100) : 0,
      negativeRate: total > 0 ? Math.round((data.negative / total) * 100) : 0
    };
  });
  
  // 更新平台情感图表
  initPlatformChart();
};

// 更新趋势图数据（基于选中的时间范围）
const updateTrendChartByTimeRange = () => {
  if (!charts.trendChart || !themeData.value || !currentTheme.value) return;
  
  const theme = currentTheme.value;
  const themeInfo = themeData.value[theme];
  
  // 过滤符合当前时间范围的月份数据
  const filteredMonthlyData = themeInfo.monthly_data.filter(monthData => {
    return monthData.month >= selectedTimeRange.value.startDate && 
           monthData.month <= selectedTimeRange.value.endDate;
  });
  
  // 提取月份和正面评论数据
  const trendData = filteredMonthlyData.map(monthData => ({
    month: monthData.month,
    positive: monthData.platforms.reduce((sum, platform) => 
      sum + platform.sentiments.positive, 0)
  }));
  
  // 按月份排序
  trendData.sort((a, b) => new Date(a.month) - new Date(b.month));
  
  // 更新趋势图
  charts.trendChart.setOption({
    xAxis: {
      data: trendData.map(item => item.month)
    },
    series: [{
      data: trendData.map(item => item.positive)
    }]
  });
};

// 更新词云图数据（基于选中的时间范围）
const updateWordCloudByTimeRange = () => {
  if (!charts.wordCloudChart) return;
  
  // 这里可以添加根据时间范围更新词云图的逻辑
  // 实际应用中，可能需要从后端API获取特定时间范围的热词数据
};

// 添加统计数据的响应式变量
const statsData = ref({
  totalComments: 0,
  platformCount: 0,
  countryCount: 1,  // 默认为1（中国）
  timeSpan: 0
});

// 更新统计数据
const updateStatsData = () => {
  if (!themeData.value || !currentTheme.value) return;
  
  const theme = currentTheme.value;
  const themeInfo = themeData.value[theme];
  
  // 过滤符合当前时间范围的月份数据
  const filteredMonthlyData = themeInfo.monthly_data.filter(monthData => {
    return monthData.month >= selectedTimeRange.value.startDate && 
           monthData.month <= selectedTimeRange.value.endDate;
  });
  
  // 计算总评论数
  let totalComments = 0;
  
  // 收集平台
  const platforms = new Set();
  
  // 计算月份数（时间跨度）
  const months = new Set();
  
  filteredMonthlyData.forEach(monthData => {
    // 添加月份
    months.add(monthData.month);
    
    monthData.platforms.forEach(platform => {
      // 添加平台
      platforms.add(platform.platform);
      
      // 累加评论数
      totalComments += platform.sentiments.positive + 
                       platform.sentiments.neutral + 
                       platform.sentiments.negative;
    });
  });
  
  // 更新统计数据
  statsData.value = {
    totalComments,
    platformCount: platforms.size,
    countryCount: 1,  // 目前只有中国
    timeSpan: months.size
  };
  
  console.log('更新统计数据:', statsData.value);
};

// 添加顶部统计数据的响应式变量
const topStats = ref({
  spreadSpeed: 0,
  spreadTrend: 0,
  latestMonthComments: 0
});

// 更新顶部统计卡片数据
const updateTopStats = () => {
  if (!themeData.value || !currentTheme.value) return;
  
  const theme = currentTheme.value;
  const themeInfo = themeData.value[theme];
  
  // 过滤符合当前时间范围的月份数据
  const filteredMonthlyData = themeInfo.monthly_data.filter(monthData => {
    return monthData.month >= selectedTimeRange.value.startDate && 
           monthData.month <= selectedTimeRange.value.endDate;
  });
  
  // 按月份排序
  filteredMonthlyData.sort((a, b) => new Date(a.month) - new Date(b.month));
  
  // 计算最新月评论数
  let latestMonthComments = 0;
  
  if (filteredMonthlyData.length > 0) {
    const latestMonth = filteredMonthlyData[filteredMonthlyData.length - 1];
    
    latestMonth.platforms.forEach(platform => {
      latestMonthComments += platform.sentiments.positive + 
                           platform.sentiments.neutral + 
                           platform.sentiments.negative;
    });
  }
  
  // 计算传播趋势（最新月份与上个月的评论数比较）
  let spreadTrend = 0;
  
  if (filteredMonthlyData.length >= 2) {
    const latestMonth = filteredMonthlyData[filteredMonthlyData.length - 1];
    const previousMonth = filteredMonthlyData[filteredMonthlyData.length - 2];
    
    let latestMonthTotal = 0;
    let previousMonthTotal = 0;
    
    latestMonth.platforms.forEach(platform => {
      latestMonthTotal += platform.sentiments.positive + 
                         platform.sentiments.neutral + 
                         platform.sentiments.negative;
    });
    
    previousMonth.platforms.forEach(platform => {
      previousMonthTotal += platform.sentiments.positive + 
                           platform.sentiments.neutral + 
                           platform.sentiments.negative;
    });
    
    if (previousMonthTotal > 0) {
      spreadTrend = Math.round(((latestMonthTotal - previousMonthTotal) / previousMonthTotal) * 100);
    }
  }
  
  // 更新统计数据
  topStats.value = {
    latestMonthComments,
    spreadTrend
  };
  
  console.log('更新顶部统计数据:', topStats.value);
};

// 添加生成预警的函数
const generateAlerts = () => {
  if (!themeData.value || !currentTheme.value) return;
  
  const theme = currentTheme.value;
  const themeInfo = themeData.value[theme];
  
  // 过滤符合当前时间范围的月份数据
  const filteredMonthlyData = themeInfo.monthly_data.filter(monthData => {
    return monthData.month >= selectedTimeRange.value.startDate && 
           monthData.month <= selectedTimeRange.value.endDate;
  });
  
  // 按月份排序
  filteredMonthlyData.sort((a, b) => new Date(a.month) - new Date(b.month));
  
  // 清空现有预警
  alerts.value = [];
  
  // 只有当有足够数据时才生成预警
  if (filteredMonthlyData.length >= 2) {
    const latestMonth = filteredMonthlyData[filteredMonthlyData.length - 1];
    const previousMonth = filteredMonthlyData[filteredMonthlyData.length - 2];
    
    // 1. 检查负面情感突增
    let latestNegative = 0;
    let previousNegative = 0;
    
    latestMonth.platforms.forEach(platform => {
      latestNegative += platform.sentiments.negative;
    });
    
    previousMonth.platforms.forEach(platform => {
      previousNegative += platform.sentiments.negative;
    });
    
    // 负面情感增长率
    if (previousNegative > 0) {
      const negativeGrowth = (latestNegative - previousNegative) / previousNegative;
      
      if (negativeGrowth > 0.3) {
        // 负面情感增长超过30%
        alerts.value.push({
          id: 1,
          level: 'high',
          title: '负面情感明显增长',
          description: `${latestMonth.month}月负面评论同比增长${Math.round(negativeGrowth * 100)}%`,
          time: `${latestMonth.month}月数据`
        });
      }
    }
    
    // 2. 检查评论总量异常变化
    let latestTotal = 0;
    let previousTotal = 0;
    
    latestMonth.platforms.forEach(platform => {
      latestTotal += platform.sentiments.positive + platform.sentiments.neutral + platform.sentiments.negative;
    });
    
    previousMonth.platforms.forEach(platform => {
      previousTotal += platform.sentiments.positive + platform.sentiments.neutral + platform.sentiments.negative;
    });
    
    if (previousTotal > 0) {
      const totalGrowth = (latestTotal - previousTotal) / previousTotal;
      
      if (totalGrowth > 0.5) {
        // 评论总量增长超过50%
        alerts.value.push({
          id: 2,
          level: 'medium',
          title: '评论数量激增',
          description: `${latestMonth.month}月评论数量同比增长${Math.round(totalGrowth * 100)}%`,
          time: `${latestMonth.month}月数据`
        });
      } else if (totalGrowth < -0.3) {
        // 评论总量下降超过30%
        alerts.value.push({
          id: 3,
          level: 'low',
          title: '评论数量明显下降',
          description: `${latestMonth.month}月评论数量同比下降${Math.round(-totalGrowth * 100)}%`,
          time: `${latestMonth.month}月数据`
        });
      }
    }
    
    // 3. 检查平台占比变化
    const platformsLatest = new Map();
    const platformsPrevious = new Map();
    
    // 统计最新月份各平台评论数
    latestMonth.platforms.forEach(platform => {
      const count = platform.sentiments.positive + platform.sentiments.neutral + platform.sentiments.negative;
      platformsLatest.set(platform.platform, count);
    });
    
    // 统计上个月各平台评论数
    previousMonth.platforms.forEach(platform => {
      const count = platform.sentiments.positive + platform.sentiments.neutral + platform.sentiments.negative;
      platformsPrevious.set(platform.platform, count);
    });
    
    // 检查平台占比变化
    for (const [platform, count] of platformsLatest) {
      const previousCount = platformsPrevious.get(platform) || 0;
      
      if (previousCount > 0 && count > previousCount * 2) {
        // 某平台评论数增长超过100%
        alerts.value.push({
          id: 4,
          level: 'medium',
          title: `${platform}平台活跃度激增`,
          description: `${platform}平台评论数量比上月增长${Math.round((count - previousCount) / previousCount * 100)}%`,
          time: `${latestMonth.month}月数据`
        });
        break; // 只添加一个平台预警
      }
    }
  }
  
  // 如果没有生成任何预警，添加一个默认预警
  if (alerts.value.length === 0) {
    alerts.value.push({
      id: 5,
      level: 'low',
      title: '传播态势平稳',
      description: '当前时间区间内未检测到显著异常变化',
      time: '最新分析'
    });
  }
  
  console.log('已生成预警:', alerts.value);
};
</script> 

<style scoped>
@import './Globe3D.css';
</style> 
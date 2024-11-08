<template>
    <div ref="threeCanvas" class="three-container"></div>
  </template>
  
  <script>
  import * as THREE from 'three';
  import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
  import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
  import dragonModel from '@/assets/models/ceramics_chinese_dragon.glb';
  
  export default {
    name: "ThreeScene",
    mounted() {
      try {
        this.initThreeScene();
      } catch (error) {
        console.error('Three.js 初始化错误:', error);
      }
    },
    methods: {
      initThreeScene() {
        // 获取HTML容器
        const container = this.$refs.threeCanvas;
  
        // 创建场景
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0xf0f0f0); // 设置背景颜色
  
        // 创建相机
        const camera = new THREE.PerspectiveCamera(
          75,
          container.clientWidth / container.clientHeight,
          0.1,
          1000
        );
        camera.position.set(0, 1.6, 5);
  
        // 创建渲染器
        const renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(container.clientWidth, container.clientHeight);
        container.appendChild(renderer.domElement);
  
        // 添加轨道控制器
        const controls = new OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true; // 添加惯性
        controls.dampingFactor = 0.05; // 惯性系数
        controls.screenSpacePanning = false;
        controls.minDistance = 3; // 最小缩放距离
        controls.maxDistance = 10; // 最大缩放距离
        controls.maxPolarAngle = Math.PI / 2; // 限制垂直旋转角度
  
        // 添加光源
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.6); // 环境光
        scene.add(ambientLight);
  
        const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8); // 平行光
        directionalLight.position.set(5, 10, 7.5);
        scene.add(directionalLight);
  
        // 创建GLTF加载器并加载模型
        const loader = new GLTFLoader();
        loader.load(
          dragonModel,
          (gltf) => {
            console.log('模型加载成功:', gltf);
            const model = gltf.scene;
            model.scale.set(1.5, 1.5, 1.5);
            model.position.set(0, 0, 0);
            scene.add(model);
          },
          (progress) => {
            console.log('加载进度:', (progress.loaded / progress.total * 100) + '%');
          },
          (error) => {
            console.error("模型加载错误:", error);
          }
        );
  
        // 动画循环
        const animate = () => {
          requestAnimationFrame(animate);
          controls.update(); // 更新控制器
          renderer.render(scene, camera);
        };
  
        animate();
  
        // 窗口大小调整时更新相机和渲染器
        window.addEventListener("resize", () => {
          camera.aspect = container.clientWidth / container.clientHeight;
          camera.updateProjectionMatrix();
          renderer.setSize(container.clientWidth, container.clientHeight);
        });
      }
    }
  };
  </script>
  
  <style>
  .three-container {
    width: 100%;
    height: 100vh;
    overflow: hidden;
  }
  </style>
  
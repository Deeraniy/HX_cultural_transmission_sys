<template>
  <div class="features-container">
    <div class="features-content">
      <div class="features-left">
        <h2 class="section-title">我们的功能</h2>
        
        <div class="features-grid">
          <!-- 湖湘文化分类查询 -->
          <div class="feature-card">
            <h3 @click="showThemeSelector">湖湘文化分类查询</h3>
            <p>为研究者和爱好者提供湖湘文化的分类查询工具，旨在帮助读者了解和探索湖湘文化的各个方面和特点...</p>
            <a @click="showThemeSelector" class="more-link">更多</a>
          </div>
          
          <!-- 湖湘文化传播舆论情感分析 -->
          <div class="feature-card">
            <h3 @click="navigateTo('/globe')">湖湘文化传播舆论情感分析</h3>
            <p>分析当前舆论对于湖湘文化的情感倾向，展现群众对湖湘文化的价值认知与情感共鸣，识别潜在的舆论危机...</p>
            <a @click="navigateTo('/globe')" class="more-link">更多</a>
          </div>
          
          <!-- 湖湘文化影响力分析预测 -->
          <div class="feature-card">
            <h3 @click="navigateTo('/detail')">湖湘文化影响力分析预测</h3>
            <p>评估湖湘文化在各个领域的影响力，并基于现有数据和趋势进行未来影响力预测...</p>
            <a @click="navigateTo('/detail')" class="more-link">更多</a>
          </div>
          
          <!-- 湖湘文化自动生成传播效果分析报告 -->
          <div class="feature-card">
            <h3 @click="navigateTo('/report')">湖湘文化自动生成传播效果分析报告</h3>
            <p>自动生成对湖湘文化传播现状的分析报告，为研究者、文化工作者和政策制定者提供全面的信息支持...</p>
            <a @click="navigateTo('/report')" class="more-link">更多</a>
          </div>
        </div>
      </div>
      
      <div class="features-right">
        <div class="model-container">
          <iframe src="/static/model-viewer.html" frameborder="0" width="100%" height="100%"></iframe>
        </div>
      </div>
    </div>
    
    <!-- 主题选择弹窗 -->
    <div id="themeSelector" class="theme-selector-modal" :class="{ 'active': showThemeSelectorDialog }">
      <div class="theme-modal-content">
        <div class="theme-modal-header">
          <h3>选择主题</h3>
          <p>请选择一个主题来查看相关内容</p>
        </div>
        <div class="theme-options">
          <a href="#/food" class="theme-option" @click="navigateTo('/food')">
            <span class="theme-icon">🍜</span>
            <span class="theme-name">美食文化</span>
          </a>
          <a href="#/placeOfInterest" class="theme-option" @click="navigateTo('/placeOfInterest')">
            <span class="theme-icon">🏞️</span>
            <span class="theme-name">风景名胜</span>
          </a>
          <a href="#/filmLiterature" class="theme-option" @click="navigateTo('/filmLiterature')">
            <span class="theme-icon">📚</span>
            <span class="theme-name">影视文学</span>
          </a>
          <a href="#/folkCustom" class="theme-option" @click="navigateTo('/folkCustom')">
            <span class="theme-icon">🏮</span>
            <span class="theme-name">非遗民俗</span>
          </a>
          <a href="#/red" class="theme-option" @click="navigateTo('/red')">
            <span class="theme-icon">🐉</span>
            <span class="theme-name">红色文化</span>
          </a>
        </div>
        <button @click="closeThemeSelector" class="theme-modal-close">×</button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

export default {
  name: 'FeaturesSection',
  setup() {
    const router = useRouter();
    const showThemeSelectorDialog = ref(false);
    
    const showThemeSelector = () => {
      showThemeSelectorDialog.value = true;
    };
    
    const closeThemeSelector = () => {
      showThemeSelectorDialog.value = false;
    };
    
    const navigateTo = (path) => {
      closeThemeSelector();
      router.push(path);
    };
    
    // 点击弹窗外部关闭弹窗
    const handleClickOutside = (event) => {
      const modal = document.getElementById('themeSelector');
      if (modal && event.target === modal) {
        closeThemeSelector();
      }
    };
    
    // 添加和移除事件监听器
    const addEventListeners = () => {
      window.addEventListener('click', handleClickOutside);
    };
    
    const removeEventListeners = () => {
      window.removeEventListener('click', handleClickOutside);
    };
    
    return {
      showThemeSelectorDialog,
      showThemeSelector,
      closeThemeSelector,
      navigateTo,
      addEventListeners,
      removeEventListeners
    };
  },
  mounted() {
    this.addEventListeners();
  },
  beforeUnmount() {
    this.removeEventListeners();
  }
};
</script>

<style scoped>
.features-container {
  padding: 40px;
  background-color: transparent;
  color: #fff;
  position: relative;
}

.features-content {
  display: flex;
  flex-wrap: wrap;
  max-width: 1400px;
  margin: 0 auto;
  gap: 20px;
  align-items: stretch;
  height: 500px;
}

.features-left {
  padding: 20px 40px 60px 40px;
  background: linear-gradient(to bottom, 
    rgba(101, 30, 20, 1) 0%, 
    rgba(101, 30, 20, 0.9) 30%, 
    rgba(101, 30, 20, 0.7) 60%, 
    rgba(101, 30, 20, 0.3) 90%, 
    rgba(101, 30, 20, 0.0) 100%);
  border-radius: 10px;
  flex: 1;
  min-width: 300px;
  padding-right: 30px;
  display: flex;
  max-height: 380px;
  flex-direction: column;
}

.features-right {
  flex: 0 0 350px;
  display: flex;
  align-items: stretch;
  height: auto;
}

.model-container {
  width: 100%;
  height: 100%;
  height: 450px;
  background: linear-gradient(135deg, rgba(240, 234, 214, 0.5), rgba(226, 219, 196, 0.3));
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 
    0 10px 30px rgba(0, 0, 0, 0.1),
    inset 0 0 10px rgba(0, 0, 0, 0.1),
    inset 0 0 30px rgba(0, 0, 0, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.3);
  backdrop-filter: blur(5px);
  position: relative;
}

.model-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(circle at 30% 40%, rgba(255, 255, 255, 0.15) 0%, transparent 60%);
  box-shadow: inset 0 0 30px rgba(0, 0, 0, 0.1);
  border-radius: 10px;
  pointer-events: none;
}

.model-container::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  box-shadow: 
    inset 0 0 50px rgba(0, 0, 0, 0.15),
    inset 0 0 100px rgba(0, 0, 0, 0.05);
  border-radius: 10px;
  pointer-events: none;
}

.model-container iframe {
  position: relative;
  z-index: 1;
}

.section-title {
  font-family: 'HelveticaNeue', '汇文明朝体', serif;
  font-size: 28px;
  margin-top: 10px;
  margin-bottom: 20px;
  text-align: left;
  padding-left: 20px;
  border-left: 4px solid #f0e8d5;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 30px;
}

.feature-card {
  display: flex;
  flex-direction: column;
  height: 130px;
  padding: 10px 20px;
  border-radius: 10px;
  background-color: rgba(255, 255, 255, 0.05);
  transition: all 0.3s ease;
  position: relative;
  backdrop-filter: blur(5px);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.feature-card:hover {
  background-color: rgba(255, 255, 255, 0.15);
  transform: translateY(-5px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.feature-icon {
  font-size: 24px;
  margin-bottom: 15px;
}

.feature-card h3 {
  font-family: 'HelveticaNeue', '汇文明朝体', serif;
  font-size: 20px;
  margin-top: 5px;
  margin-bottom: 5px;
  cursor: pointer;
}

.feature-card p {
  font-size: 14px;
  line-height: 1.6;
  margin-bottom: 10px;
  margin-bottom: 10px;
}

.more-link {
  align-self: flex-start;
  color: #f0e8d5;
  text-decoration: none;
  font-size: 14px;
  cursor: pointer;
  margin-top: 10px;
  transition: color 0.2s;
}

.more-link:hover {
  color: #fff;
  text-decoration: underline;
}

/* 主题选择弹窗样式 */
.theme-selector-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(5px);
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  visibility: hidden;
  transition: all 0.3s ease;
}

.theme-selector-modal.active {
  opacity: 1;
  visibility: visible;
}

.theme-modal-content {
  background: linear-gradient(to bottom, rgba(240, 234, 214, 0.95), rgba(226, 219, 196, 0.9));
  width: 90%;
  max-width: 400px;
  border-radius: 20px;
  padding: 40px 30px;
  position: relative;
  box-shadow: 
    0 20px 50px rgba(0, 0, 0, 0.15),
    inset 0 0 30px rgba(255, 255, 255, 0.4);
  transform: translateY(20px) scale(0.98);
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  border: 1px solid rgba(255, 255, 255, 0.5);
  overflow: hidden;
}

.theme-selector-modal.active .theme-modal-content {
  transform: translateY(0) scale(1);
}

.theme-modal-header {
  text-align: center;
  margin-bottom: 35px;
  position: relative;
}

.theme-modal-header h3 {
  color: #651e14;
  font-size: 32px;
  margin: 0 0 15px;
  font-family: 'HelveticaNeue', '汇文明朝体', serif;
  font-weight: 500;
  letter-spacing: 1px;
}

.theme-modal-header p {
  color: rgba(101, 30, 20, 0.7);
  font-size: 16px;
  margin: 0;
  font-family: 'HelveticaNeue', '汇文明朝体', serif;
}

.theme-modal-header::after {
  content: '';
  display: block;
  width: 80px;
  height: 3px;
  background: linear-gradient(to right, transparent, #651e14, transparent);
  margin: 15px auto 0;
}

.theme-modal-close {
  position: absolute;
  top: 15px;
  right: 15px;
  width: 40px;
  height: 40px;
  background-color: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 22px;
  color: #651e14;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1);
  transition: all 0.2s;
  border: 1px solid rgba(255, 255, 255, 0.3);
  z-index: 2;
}

.theme-modal-close:hover {
  transform: rotate(90deg);
  background-color: rgba(255, 255, 255, 0.5);
}

.theme-options {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-top: 20px;
  max-height: 400px;
  overflow-y: auto;
  width: 300px;
  margin-left: 50px;
  padding-right: 10px;
}

.theme-options::-webkit-scrollbar {
  width: 6px;
  background-color: rgba(255, 255, 255, 0.2);
  border-radius: 3px;
}

.theme-options::-webkit-scrollbar-thumb {
  background-color: rgba(101, 30, 20, 0.3);
  border-radius: 3px;
}

.theme-options::-webkit-scrollbar-thumb:hover {
  background-color: rgba(101, 30, 20, 0.5);
}

.theme-option {
  display: flex;
  flex-direction: row;
  align-items: center;
  padding: 12px 20px;
  border-radius: 10px;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.4), rgba(255, 255, 255, 0.1));
  box-shadow: 
    0 3px 10px rgba(0, 0, 0, 0.05),
    inset 0 0 10px rgba(255, 255, 255, 0.5);
  transition: all 0.3s ease;
  cursor: pointer;
  text-decoration: none;
  color: #651e14;
  position: relative;
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.5);
}

.theme-option:hover {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.6), rgba(255, 255, 255, 0.3));
  transform: translateX(8px);
  box-shadow: 
    0 5px 15px rgba(0, 0, 0, 0.08),
    inset 0 0 15px rgba(255, 255, 255, 0.7);
}

.theme-icon {
  font-size: 32px;
  margin-right: 20px;
  position: relative;
  z-index: 1;
}

.theme-name {
  font-size: 18px;
  text-align: left;
  font-family: 'HelveticaNeue', '汇文明朝体', serif;
  font-weight: 500;
  position: relative;
  z-index: 1;
  flex-grow: 1;
}

.theme-option::after {
  content: '→';
  font-size: 20px;
  color: rgba(101, 30, 20, 0.5);
  position: relative;
  z-index: 1;
  transition: all 0.3s ease;
  opacity: 0;
  transform: translateX(-10px);
}

.theme-option:hover::after {
  opacity: 1;
  transform: translateX(0);
}

/* 响应式设计 */
@media (max-width: 1100px) {
  .features-content {
    flex-direction: column;
  }
  
  .features-right {
    margin-top: 30px;
    width: 100%;
    flex: 0 0 100%;
    max-width: 500px;
    align-self: center;
  }
  
  .model-container {
    height: 380px;
    min-height: 380px;
  }
}

@media (max-width: 768px) {
  .features-grid {
    grid-template-columns: 1fr;
  }
  
  .section-title {
    font-size: 24px;
  }
  
  .feature-card {
    padding: 10px 15px;
    height: 130px;
  }
  
  .feature-card h3 {
    font-size: 18px;
  }
  
  .feature-card p {
    font-size: 13px;
  }
  
  .features-left {
    padding-right: 0;
  }
  
  .model-container {
    height: 380px;
    min-height: 380px;
  }
  
  .theme-option {
    padding: 10px 15px;
  }
  
  .theme-icon {
    font-size: 26px;
    margin-right: 15px;
  }
  
  .theme-name {
    font-size: 16px;
  }
  
  .theme-modal-header h3 {
    font-size: 28px;
  }
  
  .theme-modal-content {
    padding: 30px 20px;
  }
}

@media (max-width: 500px) {
  .theme-option {
    padding: 8px 12px;
  }
  
  .theme-icon {
    font-size: 22px;
    margin-right: 12px;
  }
  
  .theme-name {
    font-size: 14px;
  }
  
  .theme-modal-header h3 {
    font-size: 24px;
  }
  
  .theme-modal-content {
    padding: 25px 15px;
    width: 95%;
  }
  
  .theme-options {
    max-height: 300px;
  }
}
</style> 
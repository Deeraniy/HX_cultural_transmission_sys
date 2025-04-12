<template>
  <div class="button-container">
    <!-- 返回按钮和标题 -->
    <el-page-header @back="onBack" class="header" style="color: #fff8f0;font-size: 30px">
      <template #content>
        <span class="title" style="font-size: 30px">{{ title }}</span>
      </template>
    </el-page-header>

    <!-- 外部主题选择标签（当对话框打开时显示） -->
    <div v-if="dialogVisible" class="theme-tabs">
      <div class="theme-tabs-container">
        <div v-for="theme in themes" 
             :key="theme.id"
             :class="['theme-tab', { active: currentTheme === theme.id }]"
             @click="handleThemeSelect(theme)">
          <div class="vertical-text-reverse">{{ t(`detail.themeTabs.${theme.key}`) }}</div>
        </div>
      </div>
    </div>

    <!-- 修改按钮显示逻辑 -->
    <el-button
      v-if="hasRequiredParams"
      @click="dialogVisible = true"
      class="theme-select-btn"
    >
      {{ t('detail.selectTheme') }}
    </el-button>

    <el-dialog
      v-model="dialogVisible"
      :title="t('detail.selectTheme')"
      class="theme-dialog"
      :modal="true"
      :lock-scroll="true"
      :close-on-click-modal="hasRequiredParams"
      :close-on-press-escape="hasRequiredParams"
      :show-close="hasRequiredParams"
      style="position: fixed; width: 1000px; height: 600px;margin-left: 200px;margin-top: 100px;
      overflow-y: auto; /* 允许内容滚动 */
      overscroll-behavior: contain; /* 防止滚动传播 */"
    >
      <!-- 全局加载动画 -->
      <div v-if="loading" class="global-loading-container">
        <div class="loading-spinner">
          <div class="spinner-ring"></div>
          <span class="loading-text">{{ t('common.loading') }}</span>
        </div>
      </div>

      <div class="dialog-content">
        <!-- 左侧标签 -->
        <div class="theme-tabs">
          <div v-for="theme in themes" 
               :key="theme.id"
               :class="['theme-tab', { active: currentTheme === theme.id }]"
               @click="handleThemeSelect(theme)">
            <div class="vertical-text-reverse">{{ t(`detail.themeTabs.${theme.key}`) }}</div>
          </div>
        </div>

        <!-- 右侧内容区域 -->
        <div class="content-area">
          <div class="search-box">
            <el-input
              v-model="searchQuery"
              :placeholder="t('detail.searchPlaceholder')"
              :prefix-icon="Search"
            />
          </div>
          <div class="content-wrapper">
            <!-- 内容区域 -->
            <div v-if="filterItems.length > 0" class="items-wrapper">
              <div class="items-grid">
                <div 
                  v-for="item in filterItems" 
                  :key="item.id || item.spot_id || item.food_id || item.folk_id"
                  class="item-card"
                  @click="selectItem(item)"
                >
                  <img 
                    :src="getImageUrl(item.image_url)"
                    :alt="getItemTitle(item)"
                    @error="(e) => e.target.src = defaultEmptyImg"
                    class="card-image"
                  >
                  <div class="item-overlay">
                    <p class="title">
                      {{ getItemTitle(item) }}
                    </p>
                  </div>
                </div>
              </div>
            </div>
            <!-- 无数据提示 -->
            <div v-else class="empty-container">
              <el-empty :description="t('common.noData')" />
            </div>
          </div>
        </div>
      </div>
    </el-dialog>

    <!-- 添加文学子主题选择器 -->
    <div v-if="currentTheme === '2'" class="literature-subtypes">
      <div v-for="type in literatureSubThemes"
           :key="type.id"
           :class="['subtype-item', { active: currentLiteratureType === type.id }]"
           @click="handleLiteratureTypeChange(type.id)">
        {{ t(`detail.literature.types.${type.key}`) }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch, onUnmounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useI18n } from 'vue-i18n';
import { Search, ArrowRight, ArrowDown } from '@element-plus/icons-vue';
import SpotsAPI from '@/api/spot';
import FoodAPI from '@/api/food';
import FolkAPI from '@/api/folk';
import FilmLiteratureAPI from '@/api/filmLiterature';
import defaultEmptyImg from '@/assets/img_1.png';
import cultureElements from '@/json/culture_elements_translated.json';

const { t, locale } = useI18n();
const route = useRoute();
const router = useRouter();
const dialogVisible = ref(!route.query.name);
const searchQuery = ref('');
const currentTheme = ref('1');
const currentSubTheme = ref('');
const literatureCache = ref(null);  // 缓存文学数据
const spotItems = ref([]);
const foodItems = ref([]);
const folkItems = ref([]);
const currentItems = ref([]);
const isExpanded = ref(false);
const loading = ref(false);

// 计算当前标题
const title = computed(() => {
  if (!route.query.name) return t('detail.defaultTitle');
  
  // 从翻译文件中查找对应的元素
  const element = cultureElements.find(item => 
    item.title === decodeURIComponent(route.query.name)
  );
  
  if (element) {
    // 根据当前语言返回对应的标题
    return locale.value === 'en' ? element['title-en'] : element.title;
  }
  
  // 如果没找到翻译，返回原始标题
  return decodeURIComponent(route.query.name);
});

// 检查是否有必要的路由参数
const hasRequiredParams = computed(() => {
  return route.query.name && route.query.value && route.query.theme;
});

// 修改文学类型映射和数据加载逻辑
const literatureTypes = [
  { id: 1, name: '文学' },
  { id: 2, name: '表演艺术' },
  { id: 3, name: '新媒体艺术' },
  { id: 4, name: '古诗词' }
];

// 文学类型映射
const literatureTypeMapping = {
  '文学': 1,
  '表演艺术': 2,
  '新媒体艺术': 3,
  '古诗词': 4
};

// 文学子主题映射
const literatureSubThemes = [
  { id: 1, key: 'literature', name: '文学' },
  { id: 2, key: 'performance', name: '表演艺术' },
  { id: 3, key: 'newMedia', name: '新媒体艺术' },
  { id: 4, key: 'poetry', name: '古诗词' }
];

// 当前选中的文学子主题
const currentLiteratureType = ref(1);

// 监听对话框打开
watch(dialogVisible, async (newVal) => {
  if (newVal) {
    currentItems.value = [];
    loading.value = true;
    console.log('对话框打开，加载默认主题数据');
    await loadAllData();
    loading.value = false;
  } else {
    document.body.style.overflow = '';
  }
});

// 主题列表
const themes = ref([
  { id: '1', key: 'places', name: '名胜古迹' },
  { id: '2', key: 'film', name: '影视文学' },
  { id: '3', key: 'food', name: '美食文化' },
  { id: '4', key: 'folk', name: '非遗民俗' },
]);

// 修改过滤逻辑
const filterItems = computed(() => {
  if (!searchQuery.value || !currentItems.value) {
    return currentItems.value || [];
  }
  return currentItems.value.filter(item => {
    const name = item.spot_name || item.food_name || item.folk_name || 
                item.name || item.title || item.liter_name || '';  // 添加 book_name
    return name.toLowerCase().includes(searchQuery.value.toLowerCase());
  });
});

// 初始加载所有数据
onMounted(async () => {
  console.log('组件挂载，开始加载数据');
  await loadAllData();
});

// 修改数据处理函数
const processSpotData = (data) => {
  console.log('处理前的景点数据:', data);
  try {
    if (typeof data === 'string') {
      // 使用正则表达式匹配每个对象的属性
      const spots = [];
      const regex = /'spot_id':\s*(\d+),\s*'spot_name':\s*'([^']+)',\s*'description':\s*'([^']+)',\s*'image_url':\s*'([^']+)',\s*'rating':\s*(?:Decimal\(')?(\d+\.?\d*)(?:'\))?,\s*'city_id':\s*(\d+)/g;
      
      let match;
      while ((match = regex.exec(data)) !== null) {
        spots.push({
          spot_id: parseInt(match[1]),
          spot_name: match[2],
          description: match[3],
          image_url: match[4],
          rating: parseFloat(match[5]),
          city_id: parseInt(match[6])
        });
      }

      console.log('解析后的数据:', spots);
      return spots;
    }
    
    // 如果已经是数组则直接返回
    if (Array.isArray(data)) {
      return data;
    }
    
    // 如果是单个对象，转换为数组
    if (typeof data === 'object' && data !== null) {
      return [data];
    }

    return [];
  } catch (e) {
    console.error('数据解析失败:', e);
    return [];
  }
};

// 修改数据加载函数
const loadAllData = async () => {
  try {
    currentItems.value = [];
    loading.value = true;
    
    switch (currentTheme.value) {
      case '1':
        const spotsRes = await SpotsAPI.getSpotsAPI();
        console.log('获取到的景点数据:', spotsRes);
        if (spotsRes) {
          const processedSpots = processSpotData(spotsRes);
          console.log('最终处理后的景点数据:', processedSpots);
          if (processedSpots && processedSpots.length > 0) {
            spotItems.value = processedSpots;
            currentItems.value = processedSpots;
            console.log('成功加载景点数据，数量:', processedSpots.length);
          } else {
            console.error('处理后的数据为空');
          }
        }
        break;
      case '3':
        const foodRes = await FoodAPI.getFoodAPI();
        if (foodRes && foodRes.status === 'ok') {
          foodItems.value = foodRes.data;
          currentItems.value = foodRes.data;
        }
        break;
      case '4':
        const folkRes = await FolkAPI.getFolkCustomAPI();
        if (folkRes && folkRes.status === 'ok') {
          folkItems.value = folkRes.data;
          currentItems.value = folkRes.data;
        }
        break;
    }
  } catch (error) {
    console.error('数据加载失败:', error);
  } finally {
    loading.value = false;
  }
};

// 修改主题选择处理函数
const handleThemeSelect = async (theme) => {
  try {
    currentItems.value = [];
    loading.value = true;
    currentTheme.value = theme.id;
    
    switch (theme.id) {
      case '1':
        // 景点数据
        if (spotItems.value.length > 0) {
          currentItems.value = spotItems.value;
          break;
        }
        const spotsRes = await SpotsAPI.getSpotsAPI();
        if (spotsRes) {
          const processedSpots = processSpotData(spotsRes);
          if (processedSpots && processedSpots.length > 0) {
            spotItems.value = processedSpots;
            currentItems.value = processedSpots;
          }
        }
        break;

      case '2':
        try {
          // 如果有缓存，直接使用缓存数据
          if (literatureCache.value) {
            currentItems.value = literatureCache.value;
            break;
          }
          
          // 加载所有文学类型的数据
          const allLiteratureData = [];
          
          // 依次加载每个子主题的数据
          for (const subTheme of literatureSubThemes) {
            const response = await FilmLiteratureAPI.getBook(subTheme.name);
            if (response && response.data) {
              const processedData = response.data.map(item => ({
                ...item,
                title: item.title || item.liter_name || item.name || '',
                subTheme: subTheme.name,
                subThemeId: subTheme.id
              }));
              allLiteratureData.push(...processedData);
            }
          }
          
          // 保存到缓存
          if (allLiteratureData.length > 0) {
            literatureCache.value = allLiteratureData;
            currentItems.value = allLiteratureData;
          }
        } catch (error) {
          console.error('加载文学数据失败:', error);
        }
        break;

      case '3':
        const foodRes = await FoodAPI.getFoodAPI();
        if (foodRes && foodRes.status === 'ok') {
          foodItems.value = foodRes.data;
          currentItems.value = foodRes.data;
        }
        break;

      case '4':
        const folkRes = await FolkAPI.getFolkCustomAPI();
        if (folkRes && folkRes.status === 'ok') {
          folkItems.value = folkRes.data;
          currentItems.value = folkRes.data;
        }
        break;
    }
  } catch (error) {
    console.error('数据加载失败:', error);
  } finally {
    loading.value = false;
  }
};

// 修改选择项目的处理函数
const selectItem = async (item) => {
  // 构建路由参数
  const routeParams = {
    name: item.spot_name || item.food_name || item.folk_name || item.liter_name || item.name || '',
    value: (() => {
      switch (currentTheme.value) {
        case '1': return 1;  // 景点
        case '2': return 2;  // 文学固定为2
        case '3': return 3;  // 美食
        case '4': return 4;  // 非遗民俗
        default: return 1;
      }
    })(),
    theme: currentTheme.value === '2' ? currentLiteratureType.value : 1
  };
  
  // 更新路由
  await router.push({
    path: '/detail',
    query: routeParams
  });
  
  // 关闭对话框
  dialogVisible.value = false;
};

// 监听路由变化
watch(
  () => route.query,
  async (newQuery) => {
    if (newQuery.theme) {
      // 如果当前是文学主题，使用 theme 值作为子主题
      if (currentTheme.value === '2') {
        currentLiteratureType.value = parseInt(newQuery.theme) || 1;
      }
      // 根据主题ID加载对应数据
      const theme = themes.find(t => t.id === newQuery.theme);
      if (theme) {
        await handleThemeSelect(theme);
      }
    }
  }
);

// 修改文学子主题切换函数
const handleLiteratureTypeChange = async (typeId) => {
  if (currentTheme.value === '2') {  // 只在文学主题下生效
    currentLiteratureType.value = typeId;
    
    // 如果有缓存数据，根据子主题筛选显示
    if (literatureCache.value) {
      currentItems.value = literatureCache.value.filter(item => item.subThemeId === typeId);
    }
    
    // 如果当前有选中的项目，更新路由
    if (route.query.name) {
      await router.push({
        path: '/detail',
        query: {
          name: route.query.name,
          value: 2,  // 文学固定为2
          theme: typeId  // 使用子主题值
        }
      });
    }
  }
};

// 修改返回按钮处理函数
const onBack = () => {
  // 获取当前历史记录
  const currentHistory = window.history;
  const currentPath = route.fullPath;
  
  // 如果当前路径是 /detail（没有参数）或前一个路径包含 detail，返回首页
  if (currentPath === '/detail' || 
      (currentHistory.state && currentHistory.state.back && 
       currentHistory.state.back.includes('/detail'))) {
    // 直接返回首页
    router.push('/index');
    return;
  }
  
  // 其他情况使用默认返回
  window.history.back();
};

// 获取默认图片
const getDefaultImage = (themeId) => {
  const defaultImages = {
    '1': '/images/default-spot.jpg',
    '2': '/images/default-literature.jpg',
    '3': '/images/default-food.jpg',
    '4': '/images/default-folk.jpg'
  };
  return defaultImages[themeId] || defaultImages['1'];
};

const handleClose = () => {
  dialogVisible.value = false;
};

// 添加打开对话框时禁止背景滚动的逻辑
watch(dialogVisible, (val) => {
  if (val) {
    document.body.style.overflow = 'hidden';
  } else {
    document.body.style.overflow = '';
  }
});

// 组件卸载时确保恢复滚动
onUnmounted(() => {
  document.body.style.overflow = '';
});

// 修改图片显示相关代码
const getImageUrl = (url) => {
  if (!url) return defaultEmptyImg;
  try {
    return url;
  } catch (error) {
    console.error('图片URL处理失败:', error);
    return defaultEmptyImg;
  }
};

// 获取项目标题的函数
const getItemTitle = (item) => {
  const name = item.spot_name || item.food_name || item.folk_name || 
               item.name || item.title || item.liter_name || '';
               
  // 从翻译文件中查找对应的元素
  const element = cultureElements.find(el => el.title === name);
  
  if (element) {
    // 根据当前语言返回对应的标题
    return locale.value === 'en' ? element['title-en'] : element.title;
  }
  
  return name;
};
</script>
<style scoped>
@import '@/assets/font/font.css';

.button-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 20px;
  background-image: url('@/assets/img_4.png');
  background-size: cover;
  background-position: center;
  border-bottom-left-radius: 30px;
  border-bottom-right-radius: 30px;
  position: relative;
}

.title {
  color: #fff8f0;
  font-family: 'HelveticaNeue', serif;
  font-size: 20px;
  font-weight: bold;
}

.theme-tabs {
  position: fixed;
  left: 168px;
  top: 50%;
  transform: translateY(-50%);
  z-index: 2001;
  display: flex;
  flex-direction: column;
  gap: -15px;
}

.theme-tabs-container {
  display: flex;
  flex-direction: column;
  gap: -15px;
}

.theme-tab {
  padding: 15px 8px;
  background: #fff;
  border-radius: 8px 0 0 8px;
  cursor: pointer;
  position: relative;
  transition: transform 0.2s ease;
  box-shadow: -4px 2px 5px 0px rgba(0, 0, 0, 0.2);
  
  &:hover {
    transform: scale(1.1) translateX(-1px);
    background: #f5f7fa;
    z-index: 1;
  }
  
  &.active {
    background: #b71c1c;
    color: white;
  }
}

.vertical-text-reverse {
  writing-mode: vertical-lr;
  text-orientation: upright;
  letter-spacing: 4px;
  font-size: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  padding: 10px 0;
  transition: all 0.3s ease;
}

/* 确保其他标签在hover时保持原位 */
.theme-tab:not(:hover) {
  transform: scale(1) translateX(0);
  z-index: 0;
}

.sub-themes {
  position: absolute;
  left: 100%;
  top: 0;
  background: white;
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 8px 0;
  display: none;
  box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.05);
  white-space: nowrap;
}

.theme-tab:hover .sub-themes {
  display: block;
}

.sub-theme-item {
  padding: 8px 16px;
  
  &:hover {
    background: #f5f7fa;
  }
  
  &.active {
    color: #b71c1c;
  }
}

.theme-dialog {
  :deep(.el-dialog) {
    position: fixed !important;
    left: 50% !important;
    top: 50% !important;
    transform: translate(-50%, -50%) !important;
    margin: 0 !important;
    width: 1000px !important;
    height: 600px !important;
  display: flex;
    flex-direction: column;
  }

  :deep(.el-dialog__body) {
    padding: 0;
    height: calc(100% - 54px);
    overflow: hidden;
  }
}

.dialog-content {
  display: flex;
  height: 100%;
  overflow: hidden;
}

.content-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  height: 100%;
  overflow: hidden;
}

.search-box {
  padding: 15px;
  border-bottom: 1px solid #eee;
  background: #fff;
  flex-shrink: 0;
}

.content-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  margin-top: 20px;  /* 加载动画往下移 */
  position: relative;
  z-index: 1000;
}

.items-wrapper {
  flex: 1;
  overflow-y: auto;
  padding: 15px;
  min-height: 200px;
}

.items-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 15px;
  min-height: min-content;
}

.item-card {
  height: 130px;
  position: relative;
  border-radius: 8px;
  overflow: hidden;
  transition: transform 0.3s;
  cursor: pointer;
  
  &:hover {
    transform: translateY(-5px);
  }

  img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    background-color: #f5f5f5; /* 添加默认背景色 */
  }
}

.item-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 10px;
  text-align: center;
  transition: background-color 0.3s ease;
  font-size: 14px;
}

/* 自定义滚动条样式 */
.items-wrapper::-webkit-scrollbar {
  width: 6px;
}

.items-wrapper::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.items-wrapper::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 3px;
  
  &:hover {
    background: #555;
  }
}

.theme-select-btn {
  background-color: #fff8f0;
  border: 2px solid #d4af37;
  color: black;
  padding: 8px 24px;
  font-size: 16px;
  border-radius: 20px;
  transition: all 0.3s;

  &:hover {
    background-color: #FFC107;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(255, 215, 0, 0.3);
  }
}

.global-loading-container {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999; /* 确保在最上层 */
}

.loading-spinner {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 15px;
}

.spinner-ring {
  width: 40px;
  height: 40px;
  border: 3px solid #f3f3f3;
  border-top: 3px solid #b71c1c;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.loading-text {
  color: #b71c1c;
  font-size: 14px;
  font-weight: 500;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.empty-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: calc(100% - 60px);
  width: 100%;
  color: #909399;
}

.literature-subtypes {
  margin-top: 10px;
  display: flex;
  gap: 10px;
  padding: 0 15px;
}

.subtype-item {
  padding: 5px 15px;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
  
  &:hover {
    background: #f5f5f5;
  }
  
  &.active {
    background: #b71c1c;
    color: white;
  }
}
</style>

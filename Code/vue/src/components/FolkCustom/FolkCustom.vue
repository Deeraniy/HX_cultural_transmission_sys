<template>
  <el-main>
    <Lunbo />
    <div class="hunan-tourist-attractions">
      <!-- 搜索框 -->
      <div class="search-container">
        <input v-model="searchQuery" type="text" :placeholder="t('detail.folk.searchPlaceholder')" class="search-box" />
      </div>

      <!-- 展示的内容 -->
      <div class="folklore-container">
        <div v-for="(folk, index) in currentFolks" :key="index" class="card-container">
          <div class="flip-card">
            <div class="flip-card-inner" @click="showDetails(folk)">
              <div class="flip-card-front">
                <p>{{ getFolkName(folk.name) }}</p>
              </div>
              <div class="flip-card-back">
                <img :src="imageMap[folk.image]" alt="图片" />
              </div>
            </div>
          </div>
          <!-- 在每个卡片下方放按钮 -->
          <div class="card-buttons">
            <button class="emotion-btn" @click="goToPlaceDetail(folk.name)">{{ t('detail.place.sentimentAnalysis') }}</button>
          </div>
        </div>
      </div>

      <!-- 翻页按钮 -->
      <div class="pagination">
        <button @click="prevPage" :disabled="currentPage === 0">{{ t('detail.folk.prevPage') }}</button>
        <button @click="nextPage" :disabled="currentPage >= totalPages - 1">{{ t('detail.folk.nextPage') }}</button>
      </div>
    </div>

    <!-- 弹窗 -->
    <el-dialog v-model="dialogVisible" :title="t('menu.folk')" width="700px" class="folk-dialog">
      <!-- 添加右侧交互图标 -->
      <div class="side-interaction-icons">
        <div class="icon-wrapper" @click="toggleLike">
          <img
            :src="tagStatus.is_liked ? likeActiveIcon : likeIcon"
            :class="['icon', { 'active': tagStatus.is_liked }]"
            alt="赞"
          />
          <span>{{ tagStatus.total_likes || 0 }}</span>
        </div>
        <div class="icon-wrapper" @click="toggleFavorite">
          <img
            :src="tagStatus.is_favorite ? favoriteActiveIcon : favoriteIcon"
            :class="['icon', { 'active': tagStatus.is_favorite }]"
            alt="收藏"
          />
          <span>{{ t('detail.place.favorite') }}</span>
        </div>
      </div>

      <div v-if="selectedFolk" class="folk-dialog-content">
        <div class="folk-header">
          <img :src="imageMap[selectedFolk.image]" alt="详细图片" class="dialog-image" />
          <div class="folk-title-container">
            <h2>{{ getFolkName(selectedFolk.name) }}</h2>
            <h3>{{ t('detail.folk.rank') }}: {{selectedFolk.rank}}</h3>
          </div>
        </div>
        <div class="folk-description">
          <p>{{ getFolkDescription(selectedFolk) }}</p>
        </div>
      </div>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialogVisible = false" class="close-btn">{{ t('common.cancel') }}</el-button>
        </div>
      </template>
    </el-dialog>
  </el-main>
</template>

<script lang="ts" setup>
import { computed, onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useI18n } from 'vue-i18n';
import { ElDialog, ElButton, ElMessage } from 'element-plus';
import Lunbo from './LunBo.vue';
import FolkAPI from "@/api/folk";
import TagsAPI from '@/api/tags';
import { useUserStore } from '@/stores/user';
import cultureElements from '@/json/culture_elements_translated.json';
// 导入图标
import likeIcon from '@/assets/setting/赞.png'
import likeActiveIcon from '@/assets/setting/赞 (1).png'
import favoriteIcon from '@/assets/setting/收藏.png'
import favoriteActiveIcon from '@/assets/setting/收藏(1).png'
import UserAPI from "@/api/user";

const { t, locale } = useI18n();
const userStore = useUserStore();
const images = import.meta.glob('@/assets/feiyi/*.jpg', { eager: true });

// 生成图片路径映射表
const imageMap = {};
for (const path in images) {
  const imageName = path.split('/').pop(); // 提取文件名（如 3.jpg）
  imageMap[imageName] = images[path].default;
}
const tagStatus = ref({
  is_liked: false,
  is_favorite: false,
  total_likes: 0
});

// 获取用户ID
const getUserId = () => {
  // 首先从 userStore 中获取
  if (userStore.userId) {
    return userStore.userId;
  }

  // 如果 userStore 中没有，尝试从 localStorage 获取
  const userId = localStorage.getItem('userId');
  if (userId) {
    return userId;
  }

  // 如果都没有，返回 null
  console.warn('User ID is missing');
  return null;
};

// 初始化标签状态
const initTagStatus = async (folkId) => {
  console.log('Initializing tag status with ID:', folkId);
  if (!folkId) {
    console.error('Folk ID is missing');
    return;
  }

  try {
    const userId = getUserId();
    if (!userId) {
      console.warn('Cannot initialize tag status: User not logged in');
      // 未登录用户设置默认状态：未点赞、未收藏
      tagStatus.value = {
        is_liked: false,
        is_favorite: false,
        total_likes: 0
      };
      return;
    }

    const response = await TagsAPI.getTagByThemeAndOriginAPI('folk', folkId);

    if (response.code === 200 && response.data) {
      const tagId = response.data.id;
      const numericUserId = typeof userId === 'string' ? parseInt(userId, 10) : userId;
      const statusResponse = await TagsAPI.getTagStatusAPI(numericUserId, tagId);

      if (statusResponse.code === 200) {
        tagStatus.value = statusResponse.data;
      }
    }
  } catch (error) {
    console.error('获取标签状态失败:', error);
  }
};

// 点赞功能
const toggleLike = async () => {
  if (!selectedFolk.value?.id) {
    console.error('Folk ID is missing');
    return;
  }

  try {
    const userId = getUserId();
    if (!userId) {
      ElMessage.warning('请先登录后再点赞');
      return;
    }

    const response = await TagsAPI.getTagByThemeAndOriginAPI('folk', selectedFolk.value.id);
    if (response.code === 200 && response.data) {
      const tagId = response.data.id;

      const numericUserId = typeof userId === 'string' ? parseInt(userId, 10) : userId;
      const likeResponse = await TagsAPI.toggleLikeAPI(numericUserId, tagId);

      if (likeResponse.code === 200) {
        tagStatus.value = {
          ...tagStatus.value,
          is_liked: likeResponse.data.is_liked,
          total_likes: likeResponse.data.total_likes
        };
      }
    }
  } catch (error) {
    console.error('点赞操作失败:', error);
  }
};

// 收藏功能
const toggleFavorite = async () => {
  if (!selectedFolk.value?.id) {
    console.error('Folk ID is missing');
    return;
  }

  try {
    const userId = getUserId();
    if (!userId) {
      ElMessage.warning('请先登录后再收藏');
      return;
    }

    const response = await TagsAPI.getTagByThemeAndOriginAPI('folk', selectedFolk.value.id);
    if (response.code === 200 && response.data) {
      const tagId = response.data.id;

      const numericUserId = typeof userId === 'string' ? parseInt(userId, 10) : userId;
      const favoriteResponse = await TagsAPI.toggleFavoriteAPI(numericUserId, tagId);

      if (favoriteResponse.code === 200) {
        tagStatus.value.is_favorite = favoriteResponse.data.is_favorite;
      }
    }
  } catch (error) {
    console.error('收藏操作失败:', error);
  }
};

// 民俗文化数据
const folks = ref([]);

async function fetchFolkCustomData() {
  try {
    const response = await FolkAPI.getFolkCustomAPI();
    folks.value = response.data.map(item => ({
      id: item.folk_id,
      name: item.folk_name || '',
      image: `${item.folk_id}.jpg`, // 直接使用文件名
      description: item.description || '',
      rank: item.folk_rank || ''
    }));
  } catch (error) {
    console.error('Error fetching folk data:', error);
  }
}

onMounted(() => {
  fetchFolkCustomData();
});

// 跳转到详细页面并传递参数
const router = useRouter();
const goToPlaceDetail = (attractionName) => {
  router.push({
    path: '/detail',
    query: {
      name: attractionName,
      value: 4, // 这里是你要求的值
      theme: 1  // 新增 theme 参数
    }
  });
};

// 搜索查询
const searchQuery = ref('');

// 计算筛选后的书籍
const filteredFolks = computed(() => {
  return folks.value.filter(folk =>
    folk.name.toLowerCase().includes(searchQuery.value.toLowerCase())
  );
});

// 每页显示15个条目（3行 * 5列）
const itemsPerPage = 15;

// 计算总页数
const totalPages = computed(() => Math.ceil(filteredFolks.value.length / itemsPerPage));

// 当前页
const currentPage = ref(0);

// 获取当前页的书籍
const currentFolks = computed(() => {
  const start = currentPage.value * itemsPerPage;
  const end = start + itemsPerPage;
  return filteredFolks.value.slice(start, end);
});

// 翻页函数
const prevPage = () => {
  if (currentPage.value > 0) {
    currentPage.value--;
  }
};

const nextPage = () => {
  if (currentPage.value < totalPages.value - 1) {
    currentPage.value++;
  }
};

// 弹窗相关
const dialogVisible = ref(false);
const selectedFolk = ref(null);
const addHistory = async (item) => {
  try {
    const userId = getUserId();
    if (!userId) {
      ElMessage.warning('请先登录以记录浏览历史');
      return;
    }
    const historyData = {
      uid: userId,
      type: "folk", // 记录类型
      name: item.name, // 景点名称
      img_url: item.image, // 景点图片
      describe: item.description.substring(0, 50),
      // describe: item.description,
      // 截取前100字作为描述
    };

    const response = await UserAPI.AddUserHistory(historyData);
    if (response && response.code === 200) {
      console.log('浏览记录添加成功:', response);
    } else {
      console.error('浏览记录添加失败:', response);
    }
  } catch (error) {
    console.error('添加浏览记录失败:', error);
  }
};
// 显示详细信息的函数
const showDetails = async (folk) => {
  selectedFolk.value = folk;
  dialogVisible.value = true;
  addHistory(folk)
  // 确保有 folk.id 才初始化标签状态
  if (folk && folk.id) {
    await initTagStatus(folk.id);
  } else {
    console.warn('Folk ID is missing, cannot initialize tag status');
    // 设置默认状态
    tagStatus.value = {
      is_liked: false,
      is_favorite: false,
      total_likes: 0
    };
  }
};

// 获取民俗名称的翻译
const getFolkName = (name) => {
  const element = cultureElements.find(item => item.title === name);
  return locale.value === 'en' && element?.['title-en'] ?
    element['title-en'] :
    name;
};

// 获取民俗描述的翻译
const getFolkDescription = (folk) => {
  const element = cultureElements.find(item => item.title === folk.name);
  return locale.value === 'en' && element?.['description-en'] ?
    element['description-en'] :
    folk.description;
};
</script>

<style scoped lang="scss">
/* 总容器样式 */
.hunan-tourist-attractions {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 50px;
}

/* 标题样式 */
.title-container h3 {
  font-size: 32px;
  font-weight: bold;
  color: #333;
  margin-bottom: 10px;
}

/* 民俗文化条目容器 */
.folklore-container {
  display: grid;  /* 使用 grid 布局 */
  grid-template-columns: repeat(5, 1fr);  /* 每行 5 个 */
  gap: 60px;  /* 增大条目之间的间距 */
  justify-items: center; /* 居中显示条目 */
  margin-top: 20px;
}

/* 单个卡片的容器 */
.card-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  gap: 10px; /* 确保卡片和按钮之间有间隙 */
}

/* 翻牌效果 */
.flip-card {
  width: 150px; /* 控制每个卡片的宽度 */
  height: 200px; /* 控制每个卡片的高度 */
  perspective: 1000px;
  border-radius: 10px; /* 卡片圆角 */
  overflow: hidden; /* 确保圆角不被溢出 */
  position: relative;  /* 给 flip-card 设置相对定位 */
}

.flip-card-inner {
  position: relative;
  width: 100%;
  height: 100%;
  transform-style: preserve-3d;
  transition: transform 0.6s;
  transform-origin: center; /* 设置旋转的中心 */
}

.flip-card:hover .flip-card-inner {
  transform: rotateY(180deg);
}

.flip-card-front,
.flip-card-back {
  position: absolute;
  width: 100%;
  height: 100%;
  backface-visibility: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
  background-size: 100% 100%; /* 背景图拉伸至卡片的宽度和高度 */
  background-position: center; /* 背景图居中显示 */
}
.el-dialog {
  z-index: 9999 !important; /* 强制使弹窗在最上层 */
}

/* 正面内容（去掉圆角） */
.flip-card-front {
  background-image: url("@/assets/FolkF.png");
  color: #000;
  font-size: 30px;
  font-family: 'HelveticaNeue', serif;
  text-align: center;
  white-space: normal;
  word-wrap: break-word;
  width: 100%;
  border-radius: 0;
}

/* 根据语言设置不同的文字方向 */
:root[lang="zh"] .flip-card-front {
  writing-mode: vertical-rl;
}

:root[lang="en"] .flip-card-front {
  writing-mode: horizontal-tb;
  font-size: 20px;
  padding: 0px;
}

/* 背面内容（设置圆角） */
.flip-card-back {
  background-image: url("@/assets/FolkF.png");
  color: #333;
  font-size: 14px;
  font-family: 'HelveticaNeue', serif;
  transform: rotateY(180deg);
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 10px;
  z-index: 1;  /* 确保背面被旋转后处于合适层级 */
}

.flip-card-back img {
  width: 100%;
  height: 100%;
  object-fit: cover; /* 确保图片完全填充 */
}

/* 按钮样式 */
.card-buttons {
  display: flex;
  gap: 10px;
  justify-content: center;
  width: 100%;
}

.card-buttons button {
  padding: 5px 10px;
  background-color: #b71c1c;
  color: white;
  border: 1px solid #b71c1c; /* 给按钮添加边框，确保它们显现 */
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
}

.card-buttons button:hover {
  background-color: #9b1e1e;
}

/* 翻页按钮样式 */
.pagination {
  margin-top: 30px;
  display: flex;
  justify-content: center;
  gap: 15px;
}

.pagination button {
  padding: 10px 20px;
  background-color: #b71c1c;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.pagination button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

/* 弹窗样式 */
.folk-dialog {
  :deep(.el-dialog__header) {
    background-color: #b71c1c;
    color: white;
    padding: 15px 20px;
    border-radius: 8px 8px 0 0;
  }

  :deep(.el-dialog__title) {
    color: white;
    font-size: 22px;
    font-weight: bold;
    font-family: 'HelveticaNeue', serif;
  }

  :deep(.el-dialog__body) {
    padding: 0;
  }

  :deep(.el-dialog__headerbtn .el-dialog__close) {
    color: white;
  }

  :deep(.el-dialog__footer) {
    border-top: 1px solid #eee;
    padding: 15px 20px;
  }
}

.folk-dialog-content {
  padding: 0;
}

.folk-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  background-color: rgba(255, 248, 240, 0.9);
  padding-bottom: 0px;
}

.dialog-image {
  width: 100%;
  height: 280px;
  object-fit: cover;
  border-radius: 0;
}

.folk-title-container {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: rgba(183, 28, 28, 0.568);
  padding: 15px 20px;
  color: white;
  text-align: center;
}

.folk-title-container h2 {
  margin: 0 0 5px 0;
  font-size: 26px;
  font-family: 'HelveticaNeue', serif;
}

.folk-title-container h3 {
  margin: 0;
  font-size: 18px;
  font-weight: normal;
  font-family: 'HelveticaNeue', serif;
}

.folk-description {
  padding: 25px;
  background-color: #fff8f0;
  font-family: 'HelveticaNeue', serif;
}

.folk-description p {
  margin: 0;
  line-height: 1.8;
  font-size: 16px;
  text-indent: 2em;
  color: #333;
}

.close-btn {
  background-color: #b71c1c;
  color: white;
  border: none;
  font-family: 'HelveticaNeue', serif;
}

.close-btn:hover {
  background-color: #9b1e1e;
}

.side-interaction-icons {
  position: absolute;
  right: -60px;
  top: 50%;
  transform: translateY(-50%);
  display: flex;
  flex-direction: column;
  gap: 20px;
  z-index: 100;
}

.icon-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  cursor: pointer;
  background-color: rgba(255, 255, 255, 0.9);
  padding: 8px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease;
}

.icon-wrapper:hover {
  transform: scale(1.1);
  background-color: rgba(255, 248, 240, 1);
}

.icon {
  width: 24px;
  height: 24px;
  opacity: 0.6;
  transition: opacity 0.3s ease;
}

.icon.active {
  opacity: 1;
}

.icon-wrapper span {
  font-size: 12px;
  color: #666;
  text-align: center;
}

/* 调整弹窗内容以适应右侧图标 */
.el-dialog {
  position: relative;
  margin-right: 60px !important;
  border-radius: 8px;
  overflow: hidden;
}

.search-container {
  width: 100%;
  display: flex;
  justify-content: center; /* 居中对齐 */
  margin-bottom: 20px;
}

.search-box {
  width: 300px;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 16px;
  outline: none;
}

.search-box:focus {
  border-color: #b71c1c;
}

/* 英文状态下的样式调整 */
:root[lang="en"] .search-box {
  width: 300px; /* 英文搜索框宽度增加 */
}

:root[lang="en"] .flip-card-front {
  font-size: 24px; /* 英文字体稍微小一点 */
}

:root[lang="en"] .card-buttons button {
  min-width: 120px; /* 确保英文按钮文字不会换行 */
  font-size: 12px; /* 英文按钮字体稍微小一点 */
}

:root[lang="en"] .folk-title-container h2 {
  font-size: 22px; /* 英文标题字体稍微小一点 */
}

:root[lang="en"] .folk-description p {
  line-height: 1.6; /* 英文描述行高稍微调整 */
}
</style>

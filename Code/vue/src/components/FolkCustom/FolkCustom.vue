<template>
  <el-main>
    <Lunbo />
    <div class="hunan-tourist-attractions">
      <!-- 搜索框 -->
      <div class="search-container">
        <input v-model="searchQuery" type="text" placeholder="搜索民俗文化..." class="search-box" />
      </div>

      <!-- 展示的内容 -->
      <div class="folklore-container">
        <div v-for="(folk, index) in currentFolks" :key="index" class="card-container">
          <div class="flip-card">
            <div class="flip-card-inner" @click="showDetails(folk)">
              <div class="flip-card-front">
                <p>{{ folk.name }}</p>
              </div>
              <div class="flip-card-back">
                <img :src="folk.image" alt="图片" />
              </div>
            </div>
          </div>
          <!-- 在每个卡片下方放按钮 -->
          <div class="card-buttons">
            <button class="emotion-btn" @click="goToPlaceDetail(folk.name)">情感分析</button>
          </div>
        </div>
      </div>

      <!-- 翻页按钮 -->
      <div class="pagination">
        <button @click="prevPage" :disabled="currentPage === 0">上一页</button>
        <button @click="nextPage" :disabled="currentPage >= totalPages - 1">下一页</button>
      </div>
    </div>

    <!-- 弹窗 -->
    <el-dialog v-model="dialogVisible" title="民俗文化详情" width="600px">
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
          <span>收藏</span>
        </div>
      </div>

      <div v-if="selectedFolk">
        <h2>{{ selectedFolk.name }}</h2>
        <h3>级别：{{selectedFolk.rank}}</h3>
        <img :src="selectedFolk.image" alt="详细图片" class="dialog-image" />
        <p>{{ selectedFolk.description }}</p>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">关闭</el-button>
      </span>
    </el-dialog>
  </el-main>
</template>

<script lang="ts" setup>
import { computed, onMounted, ref } from 'vue';
import { useRouter } from 'vue-router'; // 导入 useRouter
import { ElDialog, ElButton, ElMessage } from 'element-plus';
import Lunbo from './LunBo.vue';
import FolkAPI from "@/api/folk";
import TagsAPI from '@/api/tags';
import { useUserStore } from '@/stores/user';
// 导入图标
import likeIcon from '@/assets/setting/赞.png'
import likeActiveIcon from '@/assets/setting/赞 (1).png'
import favoriteIcon from '@/assets/setting/收藏.png'
import favoriteActiveIcon from '@/assets/setting/收藏(1).png'

const userStore = useUserStore();
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
      image: item.image_url || '',
      description: item.description || '',
      rank: item.folk_rank || ''
    }));
    console.log('Folk data:', folks.value);
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

// 显示详细信息的函数
const showDetails = async (folk) => {
  selectedFolk.value = folk;
  dialogVisible.value = true;
  
  // 初始化标签状态
  await initTagStatus(folk.id);
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
  writing-mode: vertical-rl; /* 设置文字竖排，从右到左 */
  text-align: center; /* 文字居中对齐 */
  white-space: normal; /* 允许文字换行 */
  word-wrap: break-word; /* 长单词或长句子可以在需要的地方换行 */
  width: 100%; /* 确保宽度适应容器 */
  border-radius: 0; /* 正面没有圆角 */
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
.dialog-image {
  width: 100%;
  height: auto;
  object-fit: cover;
  margin-bottom: 20px;
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
  transition: transform 0.2s ease;
}

.icon-wrapper:hover {
  transform: scale(1.1);
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
}
</style>

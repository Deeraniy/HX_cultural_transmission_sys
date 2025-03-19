<template>
  <div class="modal-overlay" @click="closeModal">
    <div class="modal-content" @click.stop>
      <!-- 右上角关闭按钮 -->
      <button class="close-button" @click="closeModal">X</button>
      
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

      <div class="scene">
        <article class="book">
          <section
              v-for="(page, index) in pages"
              :key="index"
              :class="['page', { active: page.isActive, flipped: page.isFlipped }]">
            <div class="front" @click="handlePageClick(index, 'front')">
              <!-- 第一页展示封面，后续展示书名/描述 -->
              <div v-if="index === 0">
                <img :src="book.image_url" alt="Book Cover" class="book-cover" />
              </div>
              <div v-else>
                <p>{{ page.frontText }}</p>
              </div>
            </div>
            <div class="back" @click="handlePageClick(index, 'back')">
              <div v-if="index === 0">
                <h2 class="centered-title">{{ page.title }}</h2>
                <div class="button-container">
                  <button class="jump-button" @click="handlePageClick(index, 'button')">情感分析</button>
                </div>
              </div>
              <div v-else>
                <p>{{ page.backText }}</p>
              </div>
            </div>
          </section>
        </article>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, defineEmits, onMounted } from 'vue';
import router from "@/router.js";
import TagsAPI from '@/api/tags';
import { useUserStore } from '@/stores/user';
import { ElMessage } from 'element-plus';
// 直接导入图片
import likeIcon from '@/assets/setting/赞.png'
import likeActiveIcon from '@/assets/setting/赞 (1).png'
import favoriteIcon from '@/assets/setting/收藏.png'
import favoriteActiveIcon from '@/assets/setting/收藏(1).png'

// 传入的 book 对象
const props = defineProps({
  book: Object
});

// 定义 emit 事件
const emit = defineEmits();

// 分割文本逻辑
const splitText = (text, maxLength) => {
  if (text.length <= maxLength) {
    return [text, ''];
  } else {
    const frontText = text.substring(0, maxLength);
    const backText = text.substring(maxLength);
    return [frontText, backText];
  }
};

// 初始化页面数据，第一页为封面，后续页为书名和描述
const pages = ref([
  {
    frontImage: props.book.image_url,
    backImage: 'https://placeimg.com/480/640/any?4',
    title: props.book.liter_name,
    frontText: '',
    backText: '',
    isActive: true,
    isFlipped: false
  }, // 封面
  {
    frontImage: '',
    backImage: 'https://placeimg.com/480/640/any?4',
    title: '',
    frontText: '',
    backText: '',
    isActive: false,
    isFlipped: false
  }  // 书名和描述
]);

// 在初始化时分割文本
const maxTextLength = 491; // 假设每页最多显示 150 个字符
const [frontText, backText] = splitText(props.book.text, maxTextLength);
pages.value[1].frontText = frontText;
pages.value[1].backText = backText;

// 触摸事件变量
let touchStartX = 0;
let touchEndX = 0;

// 添加用户存储
const userStore = useUserStore();

// 添加标签状态
const tagStatus = ref({
  is_liked: false,
  is_favorite: false,
  total_likes: 0,
  click_count: 0
});

// 获取用户ID的函数
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

// 获取图片URL的辅助函数
const getImageUrl = (imagePath) => {
  try {
    if (imagePath.startsWith('http')) {
      return imagePath;
    }
    return new URL(`../../../../assets/${imagePath}`, import.meta.url).href;
  } catch (e) {
    console.error('图片加载失败', e);
    return '';
  }
};

// 初始化标签状态
const initTagStatus = async () => {
  try {
    const response = await TagsAPI.getTagByThemeAndOriginAPI('literature', props.book.liter_id);
    if (response.code === 200) {
      const tagId = response.data.id;
      
      const userId = getUserId();
      if (!userId) {
        console.warn('Cannot initialize tag status: User not logged in');
        // 未登录用户设置默认状态：未点赞、未收藏
        tagStatus.value = {
          is_liked: false,
          is_favorite: false,
          total_likes: 0,
          click_count: 0
        };
        return;
      }
      
      // 确保 userId 是数字类型
      const numericUserId = typeof userId === 'string' ? parseInt(userId, 10) : userId;
      
      // 记录浏览
      await TagsAPI.viewTagAPI(numericUserId, tagId);
      
      // 获取标签状态
      const statusResponse = await TagsAPI.getTagStatusAPI(numericUserId, tagId);
      if (statusResponse.code === 200) {
        tagStatus.value = statusResponse.data;
      }
    }
  } catch (error) {
    console.error('获取标签状态失败:', error);
  }
};

// 点赞函数
const toggleLike = async () => {
  try {
    const userId = getUserId();
    if (!userId) {
      ElMessage.warning('请先登录后再点赞');
      return;
    }
    
    const response = await TagsAPI.getTagByThemeAndOriginAPI('literature', props.book.liter_id);
    if (response.code === 200) {
      const tagId = response.data.id;
      
      // 确保 userId 是数字类型
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

// 收藏函数
const toggleFavorite = async () => {
  try {
    const userId = getUserId();
    if (!userId) {
      ElMessage.warning('请先登录后再收藏');
      return;
    }
    
    const response = await TagsAPI.getTagByThemeAndOriginAPI('literature', props.book.liter_id);
    if (response.code === 200) {
      const tagId = response.data.id;
      
      // 确保 userId 是数字类型
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

// 在组件挂载时初始化标签状态
onMounted(() => {
  // 确保有 book.liter_id 才初始化标签状态
  if (props.book && props.book.liter_id) {
    initTagStatus();
  } else {
    console.warn('Book ID is missing, cannot initialize tag status');
  }
});

// 翻转到背面
const flipPageToBack = (page) => {
  page.isFlipped = true;
  page.isActive = false;

  const nextPage = pages.value[pages.value.indexOf(page) + 1];
  if (nextPage) {
    nextPage.isActive = true;
  }
};

// 翻转到正面
const flipPageToFront = (page) => {
  page.isFlipped = false; // 修正翻转到正面时的状态
  page.isActive = false;

  const prevPage = pages.value[pages.value.indexOf(page) - 1];
  if (prevPage) {
    prevPage.isActive = true;
  }
};

// 关闭模态框
const closeModal = () => {
  emit('close');
};

// 处理点击事件：判断点击位置
const handlePageClick = (index, side) => {
  const activePage = pages.value.find(page => page.isActive);
  if (!activePage) return; // 如果没有活动页面，返回

  const currentPageIndex = pages.value.indexOf(activePage);
  const nextPage = pages.value[currentPageIndex + 1];
  const prevPage = pages.value[currentPageIndex - 1];

  // 如果点击的是跳转按钮，执行跳转操作
  if (side === 'button') {
    analyze(); // 触发跳转逻辑
    return;
  }

  if (side === 'front') {
    // 点击正面，翻到上一页
    if (!activePage.isFlipped) {
      flipPageToBack(activePage);
    } else {
      flipPageToFront(activePage);
    }
  } else if (side === 'back') {
    // 点击背面，翻到下一页
    if (!activePage.isFlipped) {
      flipPageToBack(activePage);
    } else {
      flipPageToFront(activePage);
    }
  }
};


const analyze = () => {
  // 跳转到 PlaceDetail 页面，带上书名和2的参数
  router.push({
    path: '/detail',
    query: { name: props.book.liter_name, value: 2 ,theme:props.book.type_id}
  });
};



// 翻到下一页
const goToNextPage = () => {
  const activePage = pages.value.find(page => page.isActive);
  if (!activePage) return;

  const currentPageIndex = pages.value.indexOf(activePage);
  const nextPage = pages.value[currentPageIndex + 1];

  if (nextPage) {
    nextPage.isActive = true;
    flipPageToBack(activePage);
  }
};

// 翻到上一页
const goToPrevPage = () => {
  const activePage = pages.value.find(page => page.isActive);
  if (!activePage) return;

  const currentPageIndex = pages.value.indexOf(activePage);
  const prevPage = pages.value[currentPageIndex - 1];

  if (prevPage) {
    prevPage.isActive = true;
    flipPageToFront(activePage); // 确保翻转回正面
  }
};
</script>

<style scoped>
@import '@/assets/font/font.css';
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.7); /* 更透明的背景 */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999; /* 确保模态框在最上层 */
}

.modal-content {
  position: relative;
  margin-right: 60px; /* 为右侧图标留出空间 */
  background-color: transparent;
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  max-width: 90%;
  max-height: 80%;
}
.centered-title{
  font-size: 60px;
  font-family: 'HelveticaNeue', serif;
}
.close-button {
  position: absolute;
  top: 10px;
  right: 10px;
  background-color: transparent;
  color: #fff;
  border: none;
  font-size: 24px;
  cursor: pointer;
  z-index: 100;
}

.scene {
  width: 400px; /* 减小宽度 */
  height: 540px; /* 减小高度 */
  margin: 16px auto;
  perspective: 1500px; /* 提高透视效果 */
}
.jump-button {
  position: absolute;
  bottom: 20px; /* 距离底部 20px */
  left: 50%; /* 水平居中 */
  transform: translateX(-50%); /* 精确居中 */
  background-color: #007bff;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s;
  z-index: 1000; /* 确保按钮在顶部 */
}

.jump-button:hover {
  background-color: #0056b3;
}

.jump-button:focus {
  outline: none;
}

.book {
  position: relative;
  width: 100%;
  height: 100%;
  transform-style: preserve-3d;
}

.page {
  cursor: pointer;
  position: absolute;
  color: black;
  width: 100%;
  height: 100%;
  transition: 1.5s transform;
  transform-style: preserve-3d;
  transform-origin: left center;

}

.front,
.back {
  position: absolute;
  width: 100%;
  height: 100%;
  box-sizing: border-box;
  backface-visibility: hidden;
  background-color: #fff8f0; /* 书页背景色 */
  padding: 25px; /* 增加边距 */
  overflow: hidden; /* 防止内容溢出 */
}

.front img,
.back img {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover; /* 确保图片填充书页区域 */
}

.back {
  transform: rotateY(180deg);
}

.page.active {
  z-index: 1;
}

.page.flipped {
  transform: rotateY(-180deg);
}

.page.flipped:last-of-type {
  z-index: 1;
}

.book-cover {
  width: 100%;
  height: auto;
  max-height: 100%;
}
.centered-title {
  font-size: 60px;
  font-family: 'HelveticaNeue', serif;
  writing-mode: vertical-rl; /* 竖排文本 */
  transform: rotate(180deg); /* 如果你想调整方向，可以旋转 */
}

.button-container {
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  width: 40%; /* 减小容器宽度 */
}

.button-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 10px; /* 减小间距 */
}

.jump-button {
  background-color: #4285f4;
  color: white;
  border: none;
  padding: 8px 16px; /* 减小内边距 */
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px; /* 减小字体大小 */
  transition: background-color 0.3s;
  white-space: nowrap;
}

.jump-button:hover {
  background-color: #3367d6;
}

.interaction-icons {
  display: flex;
  gap: 10px; /* 减小图标间距 */
  align-items: center;
}

.icon-wrapper {
  display: flex;
  align-items: center;
  gap: 4px;
  cursor: pointer;
}

.icon {
  width: 20px; /* 减小图标尺寸 */
  height: 20px;
  opacity: 0.6;
  transition: opacity 0.3s ease;
}

.icon.active {
  opacity: 1;
}

.icon-wrapper span {
  font-size: 12px; /* 减小文字大小 */
  color: #666;
}

.icon-wrapper:hover span {
  color: #333;
}

.side-interaction-icons {
  position: absolute;
  right: -60px; /* 改为右侧 */
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
</style>

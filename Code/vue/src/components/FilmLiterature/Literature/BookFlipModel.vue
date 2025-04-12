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
            :alt="t('detail.place.like')"
          />
          <span>{{ tagStatus.total_likes || 0 }}</span>
        </div>
        <div class="icon-wrapper" @click="toggleFavorite">
          <img
            :src="tagStatus.is_favorite ? favoriteActiveIcon : favoriteIcon"
            :class="['icon', { 'active': tagStatus.is_favorite }]"
            :alt="t('detail.place.favorite')"
          />
          <span>{{ t('detail.place.favorite') }}</span>
        </div>
      </div>

      <div class="scene">
        <article class="book">
          <section
            v-for="page in pages"
            :key="page.pageNumber"
            :class="['page', { active: page.isActive, flipped: page.isFlipped }]"
          >
            <div class="front" @click="nextPage">
              <!-- 封面 -->
              <div v-if="page.front.type === 'cover'" class="cover">
                <img :src="page.front.content" alt="Book Cover" class="book-cover" />
              </div>
              <!-- 内容页 -->
              <div v-else class="content">
                <p>{{ page.front.content }}</p>
              </div>
            </div>

            <div class="back" @click="prevPage">
              <!-- 标题页 -->
              <div v-if="page.back.type === 'title'" class="title-page">
                <h2 class="centered-title">{{ page.back.content }}</h2>
                <div class="button-container">
                  <button class="jump-button" @click.stop="analyze">{{ t('detail.place.sentimentAnalysis') }}</button>
                </div>
              </div>
              <!-- 内容页 -->
              <div v-else class="content">
                <p>{{ page.back.content }}</p>
              </div>
            </div>
          </section>
        </article>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, defineEmits, onMounted, watch } from 'vue';
import router from "@/router.js";
import TagsAPI from '@/api/tags';
import { useUserStore } from '@/stores/user';
import { ElMessage } from 'element-plus';
import UserAPI  from "@/api/user.ts";
import { useI18n } from 'vue-i18n';
import cultureElements from '@/json/culture_elements_translated.json';
// 直接导入图片
import likeIcon from '@/assets/setting/赞.png'
import likeActiveIcon from '@/assets/setting/赞 (1).png'
import favoriteIcon from '@/assets/setting/收藏.png'
import favoriteActiveIcon from '@/assets/setting/收藏(1).png'

const { t, locale } = useI18n();

// 传入的 book 对象
const props = defineProps({
  book: Object
});

// 获取书籍显示名称
const getBookDisplayName = (name) => {
  const element = cultureElements.find(item => item.title === name);
  return locale.value === 'en' && element?.['title-en'] ? element['title-en'] : name;
};

// 获取书籍描述
const getBookDescription = (name) => {
  const element = cultureElements.find(item => item.title === name);
  return locale.value === 'en' && element?.['description-en'] ? element['description-en'] : element?.description || '';
};

const addHistory = async () => {
  try {
    const userId = getUserId();
    if (!userId){
      return;
    }// 未登录用户不记录

    const historyData = {
      uid: userId,
      type: "literature",
      name: props.book.liter_name,
      img_url: props.book.image_url,
      describe: props.book.text?.substring(0, 100) || "文学作品", // 截取前100字作为描述
    };
    const response=UserAPI.AddUserHistory(historyData);
    console.log(historyData)
    console.log(response)
  } catch (error) {
    console.error('添加历史记录失败:', error);
  }
};
// 定义 emit 事件
const emit = defineEmits();

// 修改分割文本逻辑
const splitText = (text) => {
  if (!text) return [];

  // 根据语言设置每页显示的字符数
  const charsPerPage = locale.value === 'en' ? 600 : 300;

  // 分割文本为页面内容
  const pages = [];
  let currentPage = '';
  let currentLength = 0;

  // 按句子分割文本
  const sentences = text.split(/(?<=[。！？.!?])/);

  for (const sentence of sentences) {
    if (currentLength + sentence.length > charsPerPage) {
      // 当前页已满，保存当前页
      if (currentPage) {
        pages.push(currentPage.trim());
      }
      currentPage = sentence;
      currentLength = sentence.length;
    } else {
      currentPage += sentence;
      currentLength += sentence.length;
    }
  }

  // 添加最后一页
  if (currentPage) {
    pages.push(currentPage.trim());
  }

  // 如果页数是奇数，添加一个空页确保每个物理页面都有正反面
  if (pages.length % 2 !== 0) {
    pages.push('');
  }

  return pages;
};

// 修改翻页逻辑
const prevPage = () => {
  if (currentPageIndex.value > 0) {
    const currentPage = pages.value[currentPageIndex.value];
    if (currentPage.isFlipped) {
      // 添加翻页动画
      currentPage.isFlipping = true;
      currentPage.isFlipped = false;

      setTimeout(() => {
        currentPage.isFlipping = false;
      }, 600); // 与动画时长匹配
    } else {
      currentPage.isActive = false;
      currentPageIndex.value--;
      const prevPage = pages.value[currentPageIndex.value];
      prevPage.isActive = true;
      prevPage.isFlipped = false; // 确保前一页是未翻转状态
    }
  }
};

const nextPage = () => {
  const currentPage = pages.value[currentPageIndex.value];
  const isLastPage = currentPageIndex.value === pages.value.length - 1;

  if (!currentPage.isFlipped) {
    // 添加翻页动画
    currentPage.isFlipping = true;
    currentPage.isFlipped = true;

    setTimeout(() => {
      currentPage.isFlipping = false;
    }, 600); // 与动画时长匹配
  }
  else if (!isLastPage) {
    currentPage.isActive = false;
    currentPageIndex.value++;
    const nextPage = pages.value[currentPageIndex.value];
    nextPage.isActive = true;
    nextPage.isFlipped = false; // 确保下一页是未翻转状态
  }
};

// 修改初始化页面数据的逻辑
const initializePages = () => {
  // 获取翻译后的文本
  const translatedText = getBookDescription(props.book.liter_name);
  const contents = splitText(translatedText || props.book.text);

  // 创建页面数组，从封面开始
  pages.value = [
    // 第一页：封面和标题页
    {
      pageNumber: 0,
      front: {
        type: 'cover',
        content: props.book.image_url
      },
      back: {
        type: 'title',
        content: getBookDisplayName(props.book.liter_name)
      },
      isActive: true,
      isFlipped: false
    }
  ];

  // 添加内容页，每两页内容组成一个物理页面（正反面）
  for (let i = 0; i < contents.length; i += 2) {
    const nextContent = contents[i + 1] || ''; // 如果没有下一页内容，使用空字符串
    pages.value.push({
      pageNumber: Math.floor(i/2) + 1,
      front: {
        type: 'content',
        content: contents[i]
      },
      back: {
        type: 'content',
        content: nextContent,
        isEmpty: !nextContent // 标记是否为空页
      },
      isActive: false,
      isFlipped: false
    });
  }
};

// 监听语言变化，重新初始化页面
watch(locale, () => {
  initializePages();
});

// 页面数组
const pages = ref([]);

// 在组件挂载时初始化页面
onMounted(() => {
  initializePages();
  addHistory()
  // 确保有 book.liter_id 才初始化标签状态
  if (props.book && props.book.liter_id) {
    initTagStatus();
  } else {
    console.warn('Book ID is missing, cannot initialize tag status');
  }
});

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
    await addHistory()
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

// 当前页码
const currentPageIndex = ref(0);

// 关闭模态框
const closeModal = () => {
  emit('close');
};

const analyze = () => {
  // 跳转到 PlaceDetail 页面，带上书名和2的参数
  router.push({
    path: '/detail',
    query: { name: props.book.liter_name, value: 2, theme: props.book.type_id }
  });
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
  width: 400px;
  height: 540px;
  perspective: 2400px;
}
.jump-button {
  position: absolute;
  bottom: 20px; /* 距离底部 20px */
  left: 50%; /* 水平居中 */
  transform: translateX(-50%); /* 精确居中 */
  background-color: #b71c1c;
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
  background-color: #9c1818;
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
  position: absolute;
  width: 100%;
  height: 100%;
  transform-origin: left center;
  transform-style: preserve-3d;
  transition: transform 0.8s cubic-bezier(0.4, 0.0, 0.2, 1);
}

/* 正面左侧阴影 */
.front::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  width: 30px;
  height: 100%;
  background: linear-gradient(to right,
    rgba(0, 0, 0, 0.2),
    rgba(0, 0, 0, 0.1) 50%,
    transparent);
  opacity: 0.8;
  pointer-events: none;
}

/* 背面右侧阴影 */
.back::before {
  content: '';
  position: absolute;
  right: 0;
  top: 0;
  width: 30px;
  height: 100%;
  background: linear-gradient(to left,
    rgba(0, 0, 0, 0.2),
    rgba(0, 0, 0, 0.1) 50%,
    transparent);
  opacity: 0.8;
  pointer-events: none;
}

/* 翻页时的动态阴影 */
.page.flipping .front::after {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(to right,
    transparent,
    rgba(0, 0, 0, 0.1) 40%,
    rgba(0, 0, 0, 0.2) 50%,
    rgba(0, 0, 0, 0.1) 60%,
    transparent);
  opacity: 0;
  animation: shadowMove 0.8s ease-in-out;
  pointer-events: none;
}

@keyframes shadowMove {
  0% {
    opacity: 0;
    transform: translateX(-100%);
  }
  50% {
    opacity: 1;
  }
  100% {
    opacity: 0;
    transform: translateX(100%);
  }
}

/* 翻页动画 */
@keyframes pageFlipForward {
  0% {
    transform: rotateY(0);
  }
  50% {
    transform: rotateY(-100deg) scale(0.98);
  }
  100% {
    transform: rotateY(-180deg);
  }
}

@keyframes pageFlipBackward {
  0% {
    transform: rotateY(-180deg);
  }
  50% {
    transform: rotateY(-80deg) scale(0.98);
  }
  100% {
    transform: rotateY(0);
  }
}

/* 应用翻页动画 */
.page.flipping:not(.flipped) {
  animation: pageFlipBackward 0.8s cubic-bezier(0.4, 0.0, 0.2, 1) forwards;
}

.page.flipping.flipped {
  animation: pageFlipForward 0.8s cubic-bezier(0.4, 0.0, 0.2, 1) forwards;
}

/* 书脊阴影 */
.book::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  width: 20px;
  height: 100%;
  background: linear-gradient(to right,
    rgba(0, 0, 0, 0.3),
    rgba(0, 0, 0, 0.1) 70%,
    transparent);
  transform: translateX(-100%);
}

.front, .back {
  position: absolute;
  width: 100%;
  height: 100%;
  backface-visibility: hidden;
  background-color: #fff8f0;
  padding: 20px;
  box-sizing: border-box;
  box-shadow: inset -20px 0 50px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.back {
  transform: rotateY(180deg);
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
  height: 100%;
  object-fit: cover;
}
.centered-title {
  font-size: 48px;
  font-family: 'HelveticaNeue', serif;
  margin: 0 auto;
  text-align: center;
  writing-mode: vertical-rl;
  text-orientation: mixed;
}

/* 添加英文状态下的标题样式 */
:root[lang="en"] .centered-title {
  writing-mode: horizontal-tb;
  text-orientation: unset;
  line-height: 1.2;
  padding: 20px;
  word-break: break-word;
}

.button-container {
  position: absolute;
  bottom: 20px;
  left: 50%; /* 水平居中 */
  transform: translateX(-50%); /* 精确居中 */
  width: 40%; /* 减小容器宽度 */
}

.button-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 10px; /* 减小间距 */
}

.jump-button {
  background-color: #b71c1c;
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
  background-color: #9c1818;
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

/* 移除点击区域相关样式 */
.page-click-area {
  display: none;
}

/* 添加点击效果 */
.front, .back {
  cursor: pointer;
}

.front:hover, .back:hover {
  background-color: #fff3e0;
}

/* 确保按钮点击不会触发翻页 */
.button-container {
  position: relative;
  z-index: 2;
}

/* 修改内容显示样式 */
.content {
  padding: 30px;
  height: 100%;
  box-sizing: border-box;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden; /* 移除滚动条 */
}

.content p {
  margin: 0;
  font-size: 16px;
  line-height: 1.8;
  text-align: justify;
  height: 100%;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* 调整书页大小以适应更多文本 */
.scene {
  width: 400px;
  height: 540px;
}

/* 优化翻页效果 */
.page {
  transform-origin: left center;
  transition: transform 0.6s ease;
}

.page.flipped {
  transform: rotateY(-180deg);
}

.front, .back {
  position: absolute;
  width: 100%;
  height: 100%;
  backface-visibility: hidden;
  background-color: #fff8f0;
  padding: 20px;
  box-sizing: border-box;
}

.back {
  transform: rotateY(180deg);
}

/* 确保封面图片正确显示 */
.cover {
  padding: 0;
  height: 100%;
}

.book-cover {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* 封面背面样式 */
.title-page {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  position: relative;
}

.centered-title {
  font-size: 48px;
  font-family: 'HelveticaNeue', serif;
  writing-mode: vertical-rl;
  text-orientation: mixed;
  margin: 0 auto;
}

.button-container {
  position: absolute;
  bottom: 40px;
  width: 100%;
  display: flex;
  justify-content: center;
}

.jump-button {
  background-color: #b71c1c;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s;
}

.jump-button:hover {
  background-color: #9c1818;
}

/* 添加空页样式 */
.back[data-empty="true"] {
  background-color: #f8f4e6;
}

/* 确保最后一页可以翻转 */
.page:last-child.flipped {
  z-index: 2;
}
</style>

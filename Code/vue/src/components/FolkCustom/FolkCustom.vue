<template>
  <el-main>
    <Lunbo/>
    <div class="hunan-tourist-attractions">

      <!-- 搜索框 -->
      <div class="search-container">
        <input v-model="searchQuery" type="text" placeholder="搜索民俗文化..." class="search-box" />
      </div>

      <!-- 展示的内容 -->
      <div class="folklore-container">
        <div v-for="(book, index) in filteredBooks" :key="index" class="card-container">
          <div class="flip-card">
            <div class="flip-card-inner" @click="showDetails(book)">
              <div class="flip-card-front">
                <p>{{ book.content }}</p>
              </div>
              <div class="flip-card-back">
                <img :src="book.image" alt="图片" />
              </div>
            </div>
          </div>
          <!-- 在每个卡片下方放按钮 -->
          <div class="card-buttons">
            <button class="emotion-btn">情感分析</button>
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
      <div v-if="selectedBook">
        <h3>{{ selectedBook.content }}</h3>
        <img :src="selectedBook.image" alt="详细图片" class="dialog-image" />
        <p>这里可以展示更详细的民俗文化内容...</p>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">关闭</el-button>
      </span>
    </el-dialog>

  </el-main>
</template>


<script lang="ts" setup>
import { computed, ref } from 'vue';
import { ElDialog, ElButton } from 'element-plus';
import Lunbo from './LunBo.vue'

// 民俗文化数据
const books = ref([
  { content: '汨罗江端午习俗', image: 'https://th.bing.com/th/id/OIP.R_51sqcxCcrFxLag7A_yTQHaLH?rs=1&pid=ImgDetMain' },
  { content: '湘昆', image: 'https://th.bing.com/th/id/OIP.R_51sqcxCcrFxLag7A_yTQHaLH?rs=1&pid=ImgDetMain' },
  { content: '湘剧', image: 'https://th.bing.com/th/id/OIP.R_51sqcxCcrFxLag7A_yTQHaLH?rs=1&pid=ImgDetMain' },
  { content: '皮影戏', image: 'https://th.bing.com/th/id/OIP.R_51sqcxCcrFxLag7A_yTQHaLH?rs=1&pid=ImgDetMain' },
  { content: '湘绣', image: 'https://th.bing.com/th/id/OIP.R_51sqcxCcrFxLag7A_yTQHaLH?rs=1&pid=ImgDetMain' },
  { content: '赶尸', image: 'https://th.bing.com/th/id/OIP.R_51sqcxCcrFxLag7A_yTQHaLH?rs=1&pid=ImgDetMain' },
  { content: '湖南傩戏', image: 'https://th.bing.com/th/id/OIP.R_51sqcxCcrFxLag7A_yTQHaLH?rs=1&pid=ImgDetMain' },
  { content: '龙船调', image: 'https://th.bing.com/th/id/OIP.R_51sqcxCcrFxLag7A_yTQHaLH?rs=1&pid=ImgDetMain' },
  { content: '打铁花', image: '/assets/book9.jpg' },
  { content: '毛笔字', image: '/assets/book10.jpg' },
  { content: '竹编', image: '/assets/book11.jpg' },
  { content: '糖画', image: '/assets/book12.jpg' },
  { content: '湘绣', image: '/assets/book13.jpg' },
  { content: '岳阳楼', image: '/assets/book14.jpg' },
  { content: '橘子洲', image: '/assets/book15.jpg' },
]);

// 搜索查询
const searchQuery = ref('');

// 计算筛选后的书籍
const filteredBooks = computed(() => {
  return books.value.filter(book =>
      book.content.toLowerCase().includes(searchQuery.value.toLowerCase())
  );
});

// 每页显示15个条目（3行 * 5列）
const booksPerPage = 15;

// 计算总页数
const totalPages = computed(() => Math.ceil(filteredBooks.value.length / booksPerPage));

// 当前页
const currentPage = ref(0);

// 获取当前页的书籍
const currentBooks = computed(() => {
  const start = currentPage.value * booksPerPage;
  const end = start + booksPerPage;
  return filteredBooks.value.slice(start, end);
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
const selectedBook = ref(null);

// 显示详细信息的函数
const showDetails = (book) => {
  selectedBook.value = book;
  dialogVisible.value = true;
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
</style>

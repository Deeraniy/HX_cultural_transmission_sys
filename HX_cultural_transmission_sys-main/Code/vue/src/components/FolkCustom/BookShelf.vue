<template>
  <div class="bookshelf-container">
    <!-- 搜索框 -->
    <!-- 搜索框和分类选择器放一行 -->
    <div class="search-category-container">
      <input
          type="text"
          v-model="searchTerm"
          placeholder="搜索非物质文化..."
          class="search-input"
      />
      <select v-model="selectedCategory" class="category-select">
        <option value="">所有分类</option>
        <option v-for="category in categories" :key="category" :value="category">
          {{ category }}
        </option>
      </select>
      <!-- 触发过滤的按钮 -->
      <button @click="applyFilters" class="search-button">搜索</button>
    </div>

    <!-- 动态生成书架 -->
    <div v-for="(shelf, shelfIndex) in currentShelves" :key="'shelf-' + shelfIndex" class="bookshelf">
      <div class="shelf">
        <!-- 动态生成书籍行 -->
        <div v-for="(row, rowIndex) in shelf" :key="'row-' + rowIndex" class="row">
          <div
              v-for="(book, index) in row"
              :key="index"
              class="sample"
              :style="{backgroundImage: `url(${book.image})`}"
              @click="onBookClick(shelfIndex, rowIndex, index)"
              @mouseenter="hoveredBook = book"
              @mouseleave="hoveredBook = null"
          >
          </div>
          <div v-if="hoveredBook === book" class="book-content">
            {{ book.content }}
          </div>
        </div>
      </div>
    </div>

    <!-- 翻页按钮 -->
    <div class="pagination">
      <button @click="prevPage" :disabled="currentPage === 0">上一页</button>
      <button @click="nextPage" :disabled="currentPage >= totalPages - 1">下一页</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

// 书籍数据
const books = ref([
  { image: '/src/assets/folkCustom/汨罗江端午习俗.jpg', content: 'Content for page 2', category: '非遗' },
  { image: '/src/assets/folkCustom/湘昆.jpg', content: 'Content for page 2', category: '非遗' },
  { image: '/src/assets/folkCustom/湘剧.jpg', content: 'Content for page 2', category: '非遗' },
  { image: '/src/assets/folkCustom/皮影戏.jpg', content: 'Content for page 2', category: '非遗' },
  { image: '/src/assets/folkCustom/湘绣.jpg', content: 'Content for page 2', category: '非遗' },
  { image: '/src/assets/folkCustom/赶尸.png', content: 'Content for page 2', category: '民俗' },
  { image: '/src/assets/folkCustom/湖南傩戏.jpg', content: 'Content for page 2', category: '民俗' },

  // 继续添加更多书籍
]);

// 总页数计算
const totalPages = computed(() => Math.ceil(books.value.length / 2));  // 简单示例，总页数可以按实际规则计算

// 搜索和分类
const searchTerm = ref('');
const selectedCategory = ref('');
const categories = ['非遗', '民俗']; // 示例分类

// 计算过滤后的书籍
const filteredBooks = computed(() => {
  let result = books.value;

  // 搜索过滤
  if (searchTerm.value) {
    result = result.filter(book =>
        book.content.toLowerCase().includes(searchTerm.value.toLowerCase()) ||
        book.category.toLowerCase().includes(searchTerm.value.toLowerCase())
    );
  }

  // 分类过滤
  if (selectedCategory.value) {
    result = result.filter(book => book.category === selectedCategory.value);
  }

  return result;
});

// 每个书架最多显示5本书，动态计算每个书架的内容
const shelves = computed(() => {
  const booksPerShelf = 5; // 每个书架最多显示5本书
  const rowsPerShelf = 1; // 每个书架只有一行书
  const totalBooks = filteredBooks.value.length;  // 通过计算属性过滤的书籍

  const result = [];
  let currentBooks = [...filteredBooks.value];

  // 按照每个书架显示5本书的规则，动态分配书架
  while (currentBooks.length > 0) {
    const shelf = [];
    for (let i = 0; i < rowsPerShelf; i++) {
      shelf.push(currentBooks.slice(0, booksPerShelf)); // 每行最多5本书
      currentBooks = currentBooks.slice(booksPerShelf); // 更新剩余的书籍
    }
    result.push(shelf);
  }

  return result;
});

// 分页控制
const currentPage = ref(0);
const booksPerPage = 3; // 每页最多显示3个书架

// 当前页书架
const currentShelves = computed(() => {
  const start = currentPage.value * booksPerPage;
  const end = start + booksPerPage;
  return shelves.value.slice(start, end);
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

// 点击书籍翻页
const onBookClick = (shelfIndex, rowIndex, bookIndex) => {
  const book = filteredBooks.value[bookIndex];
  console.log('Clicked on book:', book);
};
</script>

<style scoped>
@import '@/assets/font/font.css';
.bookshelf-container {
  margin-top: 80px;
  display: flex;
  flex-direction: column;
  gap: 40px; /* 每个书架之间的间距 */
  align-items: center;
}

.bookshelf {
  display: flex;
  justify-content: center;
  width: 1000px;
  background-image: url('@/assets/wall-bookshelf.png'); /* 书架背景图 */
  background-size: 100% 100px; /* 保证书架完整显示 */
  background-repeat: no-repeat;
  background-position: bottom; /* 背景对齐底部 */
  height: 240px; /* 设置每个书架的高度 */
}

.shelf {
  width: 100%;
  max-width: 800px; /* 限制书架的最大宽度 */
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center; /* 中心对齐书架中的书籍 */
}

.row {
  display: flex;
  justify-content: center; /* 将书籍居中 */
  gap: 60px; /* 每本书之间的间隔 */
  width: 100%; /* 确保每行书籍占据满行 */
}

.sample {
  width: 120px; /* 书本宽度 */
  height: 160px; /* 书本高度 */
  background-size: cover;
  background-position: center;
  transition: transform 0.3s ease-in-out;
  border-radius: 4px; /* 书本四角略微圆角 */
}

.sample:hover {
  transform: scale(1.1); /* 鼠标悬停时稍微放大书本 */
}



.pagination button {
  font-family: 'HelveticaNeue', serif;
  margin: 0 10px;
  padding: 10px 20px;
  background-color: #b71c1c;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.pagination button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.search-category-container {
  display: flex;
  justify-content: space-between; /* 分散布局，元素两端对齐 */
  gap: 10px; /* 元素之间的间距 */
  margin-bottom: 20px;
  width: 100%;
  max-width: 700px; /* 限制最大宽度，使其适应屏幕 */
}

.search-input {
  font-family: 'HelveticaNeue', serif;
  padding: 10px;
  font-size: 16px;
  width: 250px;
  border: 2px solid #ccc; /* 边框颜色 */
  border-radius: 5px;
  transition: border 0.3s ease;
}

.search-input:focus {
  border-color:#b71c1c; /* 聚焦时的边框颜色 */
  outline: none; /* 去除默认的焦点外框 */
}

.category-select {
  font-family: 'HelveticaNeue', serif;

  padding: 10px;
  font-size: 16px;
  border: 2px solid #ccc;
  border-radius: 5px;
  width: 180px; /* 设置分类选择器的宽度 */
  background-color: #fff;
  transition: border 0.3s ease;
}

.category-select:focus {
  border-color: #b71c1c; /* 聚焦时的边框颜色 */
  outline: none;
}

.search-button {
  font-family: 'HelveticaNeue', serif;

  padding: 10px 20px;
  background-color: #b71c1c; /* 按钮背景为红色 */
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s ease;
}

.search-button:hover {
  background-color: darkred; /* 悬停时的颜色 */
}

.search-button:focus {
  outline: none; /* 去除按钮的聚焦外框 */
}
</style>

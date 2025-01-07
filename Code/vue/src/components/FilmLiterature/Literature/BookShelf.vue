<template>
  <div class="bookshelf-container">
    <!-- 搜索框 -->
    <div class="search-category-container">
      <input
          type="text"
          v-model="searchTerm"
          placeholder="搜索书籍..."
          class="search-input"
      />
      <select v-model="selectedCategory" class="category-select">
        <option value="">所有分类</option>
        <option v-for="category in categories" :key="category" :value="category">
          {{ category }}
        </option>
      </select>
      <button @click="applyFilters" class="search-button">搜索</button>
    </div>

    <!-- 动态生成书架 -->
    <div v-for="(shelf, shelfIndex) in currentShelves" :key="'shelf-' + shelfIndex" class="bookshelf">
      <div class="shelf">
        <div v-for="(row, rowIndex) in shelf" :key="'row-' + rowIndex" class="row">
          <div
              v-for="(book, index) in row"
              :key="index"
              class="sample"
              :style="{ backgroundImage: 'url(' + book.image + ')' }"
              @click="onBookClick(book)">
          </div>
        </div>
      </div>
    </div>

    <!-- 翻页按钮 -->
    <div class="pagination">
      <button @click="prevPage" :disabled="currentPage === 0">上一页</button>
      <button @click="nextPage" :disabled="currentPage >= totalPages - 1">下一页</button>
    </div>

    <!-- 弹出书籍翻书效果 -->
    <BookFlipModal v-if="showBookModal" :book="selectedBook" @close="closeBookModal" />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import BookFlipModal from './BookFlipModel.vue'; // 引入翻书效果组件

// 书籍数据
const books = ref([
  { image: 'https://turnjs.com/pics/book1.jpg', content: 'Content for page 1', category: '小说' },
  { image: 'https://turnjs.com/pics/book2.jpg', content: 'Content for page 2', category: '历史' },
  { image: 'https://turnjs.com/pics/book3.jpg', content: 'Content for page 3', category: '小说' },
  { image: 'https://turnjs.com/pics/book4.jpg', content: 'Content for page 4', category: '科技' },
  { image: 'https://turnjs.com/pics/book5.jpg', content: 'Content for page 5', category: '历史' },
  { image: 'https://turnjs.com/pics/book6.jpg', content: 'Content for page 6', category: '小说' },
]);

// 分类和搜索功能
const searchTerm = ref('');
const selectedCategory = ref('');
const categories = ['小说', '历史', '科技'];

const filteredBooks = computed(() => {
  let result = books.value;

  if (searchTerm.value) {
    result = result.filter(book =>
        book.content.toLowerCase().includes(searchTerm.value.toLowerCase()) ||
        book.category.toLowerCase().includes(searchTerm.value.toLowerCase())
    );
  }

  if (selectedCategory.value) {
    result = result.filter(book => book.category === selectedCategory.value);
  }

  return result;
});

// 每个书架最多显示5本书，动态计算每个书架的内容
const shelves = computed(() => {
  const booksPerShelf = 5;
  const rowsPerShelf = 1;
  let currentBooks = [...filteredBooks.value];
  const result = [];

  while (currentBooks.length > 0) {
    const shelf = [];
    for (let i = 0; i < rowsPerShelf; i++) {
      shelf.push(currentBooks.slice(0, booksPerShelf));
      currentBooks = currentBooks.slice(booksPerShelf);
    }
    result.push(shelf);
  }

  return result;
});

// 分页控制
const currentPage = ref(0);
const booksPerPage = 3;

const totalPages = computed(() => Math.ceil(filteredBooks.value.length / 5));

const currentShelves = computed(() => {
  const start = currentPage.value * booksPerPage;
  const end = start + booksPerPage;
  return shelves.value.slice(start, end);
});

const prevPage = () => { if (currentPage.value > 0) currentPage.value--; };
const nextPage = () => { if (currentPage.value < totalPages.value - 1) currentPage.value++; };

// 显示书籍翻页效果的模态框
const showBookModal = ref(false);
const selectedBook = ref(null);

const onBookClick = (book) => {
  selectedBook.value = book;
  showBookModal.value = true;
};

const closeBookModal = () => {
  showBookModal.value = false;
};
</script>

<style scoped>
.bookshelf-container {
  margin-top: 40px;
  display: flex;
  flex-direction: column;
  gap: 40px;
  align-items: center;
}

.bookshelf {
  display: flex;
  justify-content: center;
  width: 1000px;
  background-image: url('@/assets/wall-bookshelf.png');
  background-size: 100% 100px;
  background-repeat: no-repeat;
  background-position: bottom;
  height: 240px;
}

.shelf {
  width: 100%;
  max-width: 800px;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
}

.row {
  display: flex;
  justify-content: center;
  gap: 60px;
  width: 100%;
}

.sample {
  width: 120px;
  height: 160px;
  background-size: cover;
  background-position: center;
  transition: transform 0.3s ease-in-out;
  border-radius: 4px;
}

.sample:hover {
  transform: scale(1.1);
}

.pagination button {
  margin-top: -10px;
  margin-left: 10px;
  margin-right: 10px;
  margin-bottom: 20px;
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
  justify-content: space-between;
  gap: 10px;
  margin-bottom: 20px;
  width: 100%;
  max-width: 700px;
}

.search-input {
  font-family: 'HelveticaNeue', serif;
  padding: 10px;
  font-size: 16px;
  width: 250px;
  border: 2px solid #ccc;
  border-radius: 5px;
  transition: border 0.3s ease;
}

.search-input:focus {
  border-color:#b71c1c;
  outline: none;
}

.category-select {
  font-family: 'HelveticaNeue', serif;
  padding: 10px;
  font-size: 16px;
  border: 2px solid #ccc;
  border-radius: 5px;
  width: 180px;
  background-color: #fff;
  transition: border 0.3s ease;
}

.category-select:focus {
  border-color: #b71c1c;
  outline: none;
}

.search-button {
  font-family: 'HelveticaNeue', serif;
  padding: 10px 20px;
  background-color: #b71c1c;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s ease;
}

.search-button:hover {
  background-color: darkred;
}

.search-button:focus {
  outline: none;
}
</style>

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
              :style="{ backgroundImage: 'url(' + book.image_url + ')' }"
              :class="{ highlighted: book.liter_id === currentIndex }"
              @click="onBookClick(book)"
              @mouseover="showBubble(book)"
              @mouseleave="hideBubble">
            <!-- 气泡提示 -->
            <div v-if="book.showBubble" class="bubble">
              <span>{{ book.liter_name }}</span> <!-- 显示书籍名称 -->
            </div>
        </div>
      </div>
    </div>
  </div>

  <!-- 翻页按钮 -->
  <div class="pagination">
    <button @click="prevPage" :disabled="currentPage === 0">上一页</button>
    <button @click="nextPage" :disabled="currentPage >= totalPages - 1">下一页</button>
  </div>

  <!-- 弹出书籍翻页效果 -->
  <BookFlipModal v-if="showBookModal" :book="selectedBook" @close="closeBookModal" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import BookFlipModal from './BookFlipModel.vue'; // 引入翻书效果组件
import FilmLiteratureAPI from "@/api/filmLiterature"; // 引入 API
import { useRouter } from 'vue-router';

// 接收来自父组件的 currentIndex 和 type_id
const props = defineProps({
  currentIndex: {
    type: Number,
    required: true
  },
  type_id: {
    type: Number,
    required: true
  }
});

const router = useRouter();

// 书籍数据
const books = ref([]);

// 搜索功能
const searchTerm = ref('');

const filteredBooks = computed(() => {
  let result = books.value;

  // 根据搜索词过滤
  if (searchTerm.value) {
    result = result.filter(book =>
        book.liter_name.toLowerCase().includes(searchTerm.value.toLowerCase()) ||
        book.type_id.toString().toLowerCase().includes(searchTerm.value.toLowerCase())
    );
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
// 显示气泡
const showBubble = (book) => {
  book.showBubble = true;
};

// 隐藏气泡
const hideBubble = (book) => {
  book.showBubble = false;
};

// 获取书籍数据并根据 type_id 传递相应的 type_name
onMounted(async () => {
  const typeMapping = {
    1: '文学',
    2: '表演艺术',
    3: '新媒体艺术',
    4: '古诗词'
  };

  const type_name = typeMapping[props.currentIndex]; // 获取对应的 type_name
  console.log(props.currentIndex);
  console.log(type_name);
  const response = await FilmLiteratureAPI.getBook(type_name); // 向后端请求数据
  console.log(response);

  if (response.status === 'success') {
    books.value = response.data.map(book => ({
      ...book,
      showBubble: false // 添加 showBubble 属性来控制气泡显示
    })); // 初始化书籍数据
  }
});
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
  position: relative; /* 关键位置，用来定位气泡 */
}

.sample:hover {
  transform: scale(1.1);
}

.bubble {
  position: absolute;
  bottom: 10px;
  left: 50%;
  transform: translateX(-50%);
  background-color: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 5px 10px;
  border-radius: 15px;
  font-size: 12px;
  white-space: nowrap;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.sample:hover .bubble {
  opacity: 1; /* 只在 hover 时显示气泡 */
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
  justify-content: center;
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

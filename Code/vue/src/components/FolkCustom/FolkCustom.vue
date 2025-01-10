<template>
  <el-main>
    <div class="hunan-tourist-attractions">
      <div>
        <img src="http://whyimg.wentiyun.cn/feiyi/20230629/017cd4df-c763-4768-84a3-1b8165f603c5.png" style="width: 100%;max-height: 500px">
      </div>
      <div style="display: flex">
        <div class="attraction-container" style="width: 230px">
          <el-row>
            <el-col style="width: 200px">
              <el-menu
                  class="custom-menu"
                  default-active="1"
                  :collapse="false"
                  unique-opened
                  :default-openeds="['1', '1-1', '1-1-1', '1-1-2', '1-1-3', '1-1-4', '1-1-5', '1-1-6', '1-1-7', ]"
              >
                <!-- 一级菜单: 分类 -->
                <el-sub-menu index="1">
                  <template #title>
                    <span style="color: white; font-family: 'Book Antiqua'"><b>分类</b></span>
                  </template>
                  <!-- 二级菜单: 艺术 -->
                  <el-sub-menu index="1-1">
                    <template #title><b>艺术</b></template>
                    <el-menu-item index="1-1-1">
                      <el-checkbox>传统医药</el-checkbox>
                    </el-menu-item>
                    <el-menu-item index="1-1-2">
                      <el-checkbox>传统音乐</el-checkbox>
                    </el-menu-item>
                    <el-menu-item index="1-1-3">
                      <el-checkbox>传统舞蹈</el-checkbox>
                    </el-menu-item>
                    <el-menu-item index="1-1-4">
                      <el-checkbox>传统戏剧</el-checkbox>
                    </el-menu-item>
                    <el-menu-item index="1-1-5">
                      <el-checkbox>曲艺</el-checkbox>
                    </el-menu-item>
                    <el-menu-item index="1-1-6">
                      <el-checkbox>传统医药</el-checkbox>
                    </el-menu-item>
                    <el-menu-item index="1-1-7">
                      <el-checkbox>传统技艺</el-checkbox>
                    </el-menu-item>
                  </el-sub-menu>
                  <!-- 二级菜单: 民俗 -->
                  <el-sub-menu index="1-2">
                    <template #title><b>民俗</b></template>
                    <el-menu-item index="1-2-1">
                      <el-checkbox>民俗</el-checkbox>
                    </el-menu-item>
                    <el-menu-item index="1-2-2">
                      <el-checkbox>传统体育、游艺与杂技</el-checkbox>
                    </el-menu-item>
                    <el-menu-item index="1-2-3">
                      <el-checkbox>民间文学</el-checkbox>
                    </el-menu-item>
                  </el-sub-menu>
                </el-sub-menu>

                <!-- 一级菜单: 地域 -->
                <el-sub-menu index="3">
                  <template #title>
                    <span style="color: white; font-family: 'Book Antiqua'">地域</span>
                  </template>
                  <!-- 二级菜单: 湖南 -->
                  <el-sub-menu index="3-1">
                    <template #title><b>湖南</b></template>
                    <!-- 三级菜单: 中国的地区 -->
                    <el-menu-item index="3-1-1">
                      <el-checkbox>长沙</el-checkbox>
                    </el-menu-item>
                    <el-menu-item index="3-1-2">
                      <el-checkbox>湘潭</el-checkbox>
                    </el-menu-item>
                    <el-menu-item index="3-1-3">
                      <el-checkbox>株洲</el-checkbox>
                    </el-menu-item>
                    <el-menu-item index="3-1-4">
                      <el-checkbox>永州</el-checkbox>
                    </el-menu-item>
                    <el-menu-item index="3-1-5">
                      <el-checkbox>湘西</el-checkbox>
                    </el-menu-item>
                    <el-menu-item index="3-1-6">
                      <el-checkbox>郴州</el-checkbox>
                    </el-menu-item>
                    <el-menu-item index="3-1-7">
                      <el-checkbox>岳阳</el-checkbox>
                    </el-menu-item>
                  </el-sub-menu>
                </el-sub-menu>
              </el-menu>
            </el-col>
          </el-row>
        </div>





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
              >
                <div v-if="hoveredBook === book" class="book-content" style="text-align: center;color: white;font-family: 'Book Antiqua'">
                  {{ book.content }}
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
      </div>
      </div>
    </div>


  </el-main>
</template>

<script lang="ts" setup>
import {computed, nextTick, onMounted, ref, watch} from 'vue';
import {
  Document,
  Menu as IconMenu,
  Location,
  Setting,
} from '@element-plus/icons-vue'

import $ from 'jquery'

import turn from '@/utils/turn'
import BookShelf from "./BookShelf.vue";
// Carousel 数据
const handleOpen = (key: string, keyPath: string[]) => {
  console.log(key, keyPath)
}
const handleClose = (key: string, keyPath: string[]) => {
  console.log(key, keyPath)
}
const hoveredBook= ref(null);
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
const booksPerPage = 2; // 每页最多显示3个书架

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
const carouselData = ref([
  {
    title: '故宫日历·2025年·汉英对照',
    description: '2025年，乙巳年，生肖蛇，适逢故宫博物院建院一百周年。汉英对照版日历通过文物展示故宫百年来的发展历程。',
    image: 'https://img.dpm.org.cn/Uploads/image/2024/12/18/出版推荐448-546汉英日历-XHuSkowdJ260.png',
    editor: '陈丽华',
    isbn: '978-7-5134-1668-9',
    publisher: '故宫出版社',
    price: '96元',
    edition: '2024年11月第1版',
    prints: '16',
    format: '48开'
  },
  {
    title: '汉代玉器研究',
    description: '汉代是玉器发展史中的繁荣时代，玉器艺术进入高峰。',
    image: 'https://img.dpm.org.cn/Uploads/image/2024/12/18/出版推荐448-546汉代玉器研究-FXpuCWAOK260.png',
    editor: '徐琳',
    isbn: '978-7-5134-1614-6',
    publisher: '故宫出版社',
    price: '236元',
    edition: '2024年9月第1版',
    prints: '34',
    format: '16开'
  },
  {
    title: '清代大运彩瓷（全二册）',
    description: '清代大运瓷器是御窑厂每年烧制并送往清宫的基本任务。',
    image: 'https://img.dpm.org.cn/Uploads/image/2024/12/18/出版推荐448-546清代大运彩瓷-QWGTJeobg260.png',
    editor: '故宫博物院',
    isbn: '978-7-5134-1653-5',
    publisher: '故宫出版社',
    price: '880元',
    edition: '2024年8月第1版',
    prints: '66.5',
    format: '12开'
  }
]);
const imageArray = carouselData.value.map(item => item.image);
console.log(imageArray);

const currentIndex = ref(0);
// 监听 currentIndex 的变化
watch(currentIndex, (newIndex) => {
  nextTick(() => {
    console.log("currentIndex updated to:", newIndex);
  });
});
// 轮播变化时手动更新
const onCarouselChange = (index: number) => {
  currentIndex.value = index;
  console.log("Carousel changed to index:", index);
};
// 切换上一张
const prevSlide = () => {
  if (currentIndex.value > 0) {
    currentIndex.value -= 1;
  } else {
    currentIndex.value = carouselData.value.length - 1;
  }
};

// 切换下一张
const nextSlide = () => {
  if (currentIndex.value < carouselData.value.length - 1) {
    currentIndex.value += 1;
  } else {
    currentIndex.value = 0;
  }
};
onMounted(() => {
  nextTick(() => {
    console.log("Mounted, currentIndex:", currentIndex.value);
  });
});
</script>

<style scoped lang="scss">
@import '@/assets/font/font.css';
.attraction-container {
  padding: 16px;
  border-radius: 8px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

.custom-menu {

  border-radius: 8px; /* 圆角 */
  background-color: #0d7b6f; /* 翠绿色背景 */

}
.el-menu{
  font-size: 14px; /* 设置字体大小 */
  color: #ffffff; /* 菜单字体白色 */
  font-family: 'Arial', 'Microsoft YaHei', sans-serif; /* 自定义字体 */

}



.menu-title {
  font-size: 16px;
  font-weight: bold;
  color: #3b5999;
  margin-bottom: 12px;
}

.custom-menu {

  border: none;
}

.custom-menu .el-sub-menu__title {
  color: #ffffff; /* 一级菜单字体白色 */
  font-weight: bold; /* 一级菜单字体加粗 */
  padding: 10px 15px; /* 内边距增加用户体验 */
  border-radius: 5px; /* 一级菜单标题的圆角 */
  transition: all 0.3s ease; /* 平滑过渡效果 */
}

.custom-menu .el-menu-item {
  font-size: 14px;
  color: #333;
  padding-left: 24px;

}

.custom-menu .el-checkbox {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.custom-menu .count {
  color: #d9534f;
  margin-left: 4px;
}

.custom-menu .total {
  color: #888;
  margin-left: 8px;
}
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


#app {
  height: 100vh;
  margin: 0;
}

.el-main {
  --el-main-padding:0;

}

.hunan-tourist-attractions {

  background-size: cover;
  background-repeat: no-repeat;
  background-position: center;
}
.attraction-container {
  display: flex;
  align-items: flex-start; /* 图片和文本在一行显示 */
  justify-content: space-between;
  width: 100%;
}





.centered-text {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
}



.fancy-name {
  font-family: 'ZhuanTi', serif; /* 使用纂体字体 */
  font-size: 13px; /* 根据需要调整字体大小 */
  color: #555; /* 设置字体颜色 */
}


.image-carousel {
  width: 500px;
  height: 500px; /* 允许容器根据内容自适应高度 */
  margin-right: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
}


.location-box {
  font-family: 'HelveticaNeue', serif;
  margin-top: 20px;
  margin-left: 40px;
  margin-right: 20px;
  width: 650px;
  height: 320px; /* 设置固定高度 */
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  background-color: #fff;
  overflow-y: auto; /* 内容超出时显示滚动条 */

  /* 设置右下角背景图片 */
  background-image: url('@/assets/水墨小人.png');
  background-position: right 10px bottom -10px; /* 向下偏移一点 */
  background-repeat: no-repeat;     /* 不重复显示背景 */
  background-size: 200px 250px;     /* 将背景图大小调整为 100px */
  //opacity: 0.3;
}



.carousel-image-container {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.carousel-image-container img {
  max-height: 100%;
  width: auto;
  object-fit: contain; /* 保证图片完整显示，避免裁剪 */
}

.pic img {
  width: 100%; /* 让图片填满容器的宽度 */
  height: 100%; /* 让图片填满容器的高度 */
  object-fit: cover; /* 保证图片不变形，填充整个容器 */
}


.s-title {
  margin-left: 10px;
  margin-top: 8px;
  font-size: 34px;
  font-weight: bold;
  color: #333;
}

.p {
  margin-left: 10px;
  font-size: 26px;
  color: #666;
  margin-top: 10px;
}

.ts {
  margin-left: 10px;
  font-size: 18px;
  color: #999;
}

/* 使用 :deep() 来深度修改 el-carousel 的垂直指示器样式 */
.hunan-tourist-attractions :deep(.el-carousel__indicators--vertical li button) {
  width: 10px;          /* 设置指示器的宽度 */
  height: 10px;         /* 设置指示器的高度 */
  border-radius: 50%;   /* 使按钮变圆 */
  background-color: #ccc; /* 设置默认颜色 */
  margin: 4px 0;        /* 上下间距 */
  transition: background-color 0.3s ease; /* 平滑过渡 */
}

/* 修改当前激活状态指示器的样式 */
.hunan-tourist-attractions :deep(.el-carousel__indicators--vertical li.is-active button) {
  background-color: #b71c1c; /* 激活时的颜色 */
}


/* 样式修改 */
.el-carousel {
  margin-left: 20px;
  width: 500px;
  height: auto;
}

</style>

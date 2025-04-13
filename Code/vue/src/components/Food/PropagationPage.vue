<template>
  <div class="analysis-table">
    <h2>{{ $t('hu-nan-yin-shi-ge-cai-chuan-bo-xiao-guo-fen-xi-0') }}</h2>

    <el-table :data="pagedData" border style="width: 97%;font-size: 20px; font-family: 'HelveticaNeue', serif;margin: 20px" :fit="true">
      <!-- 菜品图片列 -->
      <el-table-column :label="locale === 'en' ? 'Dish Image' : '菜品图片'" align="center">
        <template #default="{ row }">
          <img :src="row.image_url" alt="Dish Image" class="dish-image" />
        </template>
      </el-table-column>

      <!-- 菜品名称列 -->
      <el-table-column :label="locale === 'en' ? 'Dish Name' : '菜品名称'" prop="food_name" align="center"></el-table-column>

      <!-- 参与度列 -->
      <el-table-column :label="locale === 'en' ? 'Participation' : '参与度'" prop="participation" sortable align="center"></el-table-column>

      <!-- 讨论度列 -->
      <el-table-column :label="locale === 'en' ? 'Discussion' : '讨论度'" prop="discussion" sortable align="center"></el-table-column>

      <!-- 知名度列 -->
      <el-table-column :label="locale === 'en' ? 'Fame' : '知名度'" prop="fame" sortable align="center"></el-table-column>

    </el-table>

    <!-- 分页组件 -->
    <el-pagination
        :current-page="currentPage"
        :page-size="pageSize"
        :total="tableData.length"
        @current-change="handlePageChange"
        @size-change="handleSizeChange"
        layout="total, sizes, prev, pager, next"
        :page-sizes="[ 10, 20, 30]"
        style="margin-top: 20px; text-align: center;"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useI18n } from 'vue-i18n';
import FoodAPI from "@/api/food.ts";
import food1 from '@/assets/foodImg/food1.jpg';
import food2 from '@/assets/foodImg/food2.jpg';
import food3 from '@/assets/foodImg/food3.jpg';
import food4 from '@/assets/foodImg/food4.jpg';
import food5 from '@/assets/foodImg/food5.jpg';
import cultureElements from '@/json/culture_elements_translated.json'; // 假设包含菜名的翻译数据

const { locale } = useI18n();  // 获取当前语言

// 获取美食显示名称
const getFoodDisplayName = (name) => {
  const element = cultureElements.find(item => item.title === name);
  return locale.value === 'en' && element?.['title-en'] ? element['title-en'] : name;
};

onMounted(() => {
  fetchFoodInfluenceData();
});

const fetchFoodInfluenceData = async () => {
  try {
    const response = await FoodAPI.getFoodInfluence();
    console.log(response.data);

    // 在此方法中处理菜名的国际化
    tableData.value = response.data.map(food => ({
      ...food,
      food_name: getFoodDisplayName(food.food_name) // 根据locale动态获取菜名
    }));
  } catch (error) {
    console.error('Error fetching data:', error);
  }
};

// 更新后的表格数据，包括图片路径
const tableData = ref([
  {
    food_name: '糖油粑粑',
    image_url: food1,
    participation: '75%',
    discussion: '1500条评论',
    fame: '80%'
  },
  {
    food_name: '毛家红烧肉',
    image_url: food2,
    participation: '80%',
    discussion: '5000条评论',
    fame: '90%'
  },
  {
    food_name: '湘西外婆菜',
    image_url: food3,
    participation: '60%',
    discussion: '1000条评论',
    fame: '65%'
  },
  {
    food_name: '臭豆腐',
    image_url: food4,
    participation: '90%',
    discussion: '2000条评论',
    fame: '70%'
  },
  {
    food_name: '辣椒炒肉',
    image_url: food5,
    participation: '85%',
    discussion: '1200条评论',
    fame: '75%'
  }
]);

// 当前页数和每页条数
const currentPage = ref(1);
const pageSize = ref(10);  // 默认每页显示 5 条

// 计算当前页的数据
const pagedData = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value;
  const end = start + pageSize.value;
  return tableData.value.slice(start, end);
});

// 处理分页的页面切换
const handlePageChange = (newPage) => {
  currentPage.value = newPage;
};

// 处理 pageSize 的改变
const handleSizeChange = (newSize) => {
  pageSize.value = newSize;
  currentPage.value = 1;  // 重置到第一页
};
</script>


<style scoped>
@import '@/assets/font/font.css';
.el-table {
  font-family: 'HelveticaNeue', serif;
  --el-table-border-color: transparent;
  --el-table-border: none;
  --el-table-text-color: #fffffff;
  --el-table-header-text-color: #fffffff;
  --el-table-row-hover-bg-color: transparent;
  --el-table-current-row-bg-color: transparent;
  --el-table-bg-color: rgba(255, 255, 255, 0.7);
  --el-table-header-bg-color: transparent;
  --el-table-tr-bg-color: transparent;
  --el-table-expanded-cell-bg-color: transparent;
  text-align: center;
  border-radius: 15px;  
}

.el-table .cell {
  text-align: center;
}

.analysis-table {
  font-family: 'HelveticaNeue', serif;
  font-size: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
}

h2 {
  font-family: 'HelveticaNeue', serif;
  text-align: center;
  margin-bottom: 20px;
}

.dish-image {
  width: 100%;
  height: 120px;
  max-width: 180px;
  object-fit: cover;
  border-radius: 8px;
  display: block;
  margin: 0 auto;
}
</style>

<template>
  <div class="analysis-table" >
    <h2>湖南饮食各菜传播效果分析</h2>
    <el-table :data="pagedData" border style="width: 100%;font-size: 20px;font-family: 'Bell MT'" :fit="true" >
      <!-- 菜品图片列 -->
      <el-table-column label="菜品图片">
        <template #default="{ row }">
          <img :src="row.image_url" alt="Dish Image" class="dish-image" />
        </template>
      </el-table-column>

      <!-- 菜品名称列 -->
      <el-table-column label="菜品名称" prop="food_name"></el-table-column>

      <!-- 参与度列 -->
      <el-table-column label="参与度" prop="participation" sortable></el-table-column>

      <!-- 讨论度列 -->
      <el-table-column label="讨论度" prop="discussion" sortable></el-table-column>

      <!-- 知名度列 -->
      <el-table-column label="知名度" prop="fame" sortable></el-table-column>



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
import {ref, computed, onMounted} from 'vue'
import food1 from '@/assets/foodImg/food1.jpg'
import food2 from '@/assets/foodImg/food2.jpg'
import food3 from '@/assets/foodImg/food3.jpg'
import food4 from '@/assets/foodImg/food4.jpg'
import food5 from '@/assets/foodImg/food5.jpg'
import FoodAPI from "@/api/food.ts";
onMounted(() => {
  fetchFoodInfluenceData();
});
const fetchFoodInfluenceData = async () => {
  try {
    const response = await FoodAPI.getFoodInfluence()
    console.log(response.data);
    tableData.value = response.data;
  } catch (error) {
    console.error('Error fetching data:', error);
  }
};
// 更新后的表格数据，包括图片路径
const tableData = ref([
  {
    dish: '糖油粑粑',
    img: food1,
    participation: '75%',
    discussion: '1500条评论',
    fame: '80%'
  },
  {
    dish: '毛家红烧肉',
    img: food2,
    participation: '80%',
    discussion: '5000条评论',
    fame: '90%'
  },
  {
    dish: '湘西外婆菜',
    img: food3,
    participation: '60%',
    discussion: '1000条评论',
    fame: '65%'
  },
  {
    dish: '臭豆腐',
    img: food4,
    participation: '90%',
    discussion: '2000条评论',
    fame: '70%'
  },
  {
    dish: '辣椒炒肉',
    img: food5,
    participation: '85%',
    discussion: '1200条评论',
    fame: '75%'
  }
])

// 当前页数和每页条数
const currentPage = ref(1)
const pageSize = ref(10)  // 默认每页显示 5 条

// 计算当前页的数据
const pagedData = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return tableData.value.slice(start, end)
})

// 处理分页的页面切换
const handlePageChange = (newPage) => {
  currentPage.value = newPage
}

// 处理 pageSize 的改变
const handleSizeChange = (newSize) => {
  pageSize.value = newSize
  currentPage.value = 1  // 重置到第一页
}
// 处理排序变化
const handleSortChange = (column) => {
  let sortKey = column
  const isDescending = sortOrders[column] === 'descending'
  tableData.value.sort((a, b) => {
    let valA = a[sortKey]
    let valB = b[sortKey]
    // 如果是参与度、讨论度、知名度这些是百分比或数字，进行转化处理
    if (sortKey === 'participation' || sortKey === 'fame') {
      valA = parseFloat(valA.replace('%', ''))
      valB = parseFloat(valB.replace('%', ''))
    } else if (sortKey === 'discussion') {
      valA = parseInt(valA.replace('条评论', ''))
      valB = parseInt(valB.replace('条评论', ''))
    }

    if (isDescending) {
      return valB - valA
    } else {
      return valA - valB
    }
  })
  // 更新排序方向
  sortOrders[column] = isDescending ? 'ascending' : 'descending'
}

// 存储排序方向
const sortOrders = {
  participation: 'ascending',
  discussion: 'ascending',
  fame: 'ascending'
}

</script>

<style scoped>

.el-table {
  --el-table-border-color: transparent;
  --el-table-border: none;
  --el-table-text-color: #fffffff;
  --el-table-header-text-color: #fffffff;
  --el-table-row-hover-bg-color: transparent;
  --el-table-current-row-bg-color: transparent;
  --el-table-bg-color: rgba(255, 255, 255, 0.4); /* 表格背景半透明黑色 */
  --el-table-header-bg-color: transparent;
  --el-table-tr-bg-color: transparent;
  --el-table-expanded-cell-bg-color: transparent;
}

.analysis-table {
  padding: 20px;
}

h2 {
  text-align: center;
  margin-bottom: 20px;
}

.dish-image {
  width: 100%;
  height: 120px;
  max-width: 180px;
  object-fit: cover;
  border-radius: 8px;
}
</style>

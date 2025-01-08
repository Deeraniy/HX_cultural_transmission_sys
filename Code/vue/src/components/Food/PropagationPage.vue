<template>
  <div class="analysis-table">
    <h2>湖南饮食各菜传播效果分析</h2>

    <!-- Element Plus 表格 -->
    <el-table :data="pagedData" border style="width: 100%" :fit="true">
      <!-- 菜品图片列 -->
      <el-table-column label="菜品图片">
        <template #default="{ row }">
          <img :src="row.img" alt="Dish Image" class="dish-image" />
        </template>
      </el-table-column>

      <!-- 菜品名称列 -->
      <el-table-column label="菜品名称" prop="dish"></el-table-column>

      <!-- 参与度列 -->
      <el-table-column label="参与度" prop="participation"></el-table-column>

      <!-- 讨论度列 -->
      <el-table-column label="讨论度" prop="discussion"></el-table-column>

      <!-- 知名度列 -->
      <el-table-column label="知名度" prop="fame"></el-table-column>
    </el-table>

    <!-- 分页组件 -->
    <el-pagination
        :current-page="currentPage"
        :page-size="pageSize"
        :total="tableData.length"
        @current-change="handlePageChange"
        @size-change="handleSizeChange"
        layout="total, sizes, prev, pager, next"
        :page-sizes="[1, 5, 10, 15]"
        style="margin-top: 20px; text-align: center;"
    />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import food1 from '@/assets/foodImg/food1.jpg'
import food2 from '@/assets/foodImg/food2.jpg'
import food3 from '@/assets/foodImg/food3.jpg'
import food4 from '@/assets/foodImg/food4.jpg'
import food5 from '@/assets/foodImg/food5.jpg'

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
    discussion: '800条评论',
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
const pageSize = ref(5)  // 默认每页显示 5 条

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
</script>

<style scoped>
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

<template>
  <div>
    <el-header>
      <div class="flex justify-between mb-4">
        <el-button type="primary" @click="handleAddCulture">
          <el-icon><Plus /></el-icon> 新增文化
        </el-button>
        <el-input v-model="searchKeyword" placeholder="搜索文化名称" style="width: 300px">
          <template #append>
            <el-button @click="handleSearch">
              <el-icon><Search /></el-icon>
            </el-button>
          </template>
        </el-input>
      </div>
    </el-header>
    <el-table :data="paginatedCultureList" stripe>
      <el-table-column prop="name" label="文化名称" />
      <el-table-column prop="topic" label="主题" />
      <el-table-column prop="status" label="状态">
        <template #default="{ row }">
          <el-tag :type="row.status === '已发布' ? 'success' : 'warning'">
            {{ row.status }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="createTime" label="创建时间" />
      <el-table-column label="操作" width="180">
        <template #default="{ row }">
          <el-button size="small" type="primary" @click="handleEdit(row)">编辑</el-button>
          <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-pagination
        class="mt-4"
        background
        layout="prev, pager, next, jumper, ->, sizes, total"
        :total="filteredCultureList.length"
        :page-size="pageSize"
        :current-page="currentPage"
        :page-sizes="[1, 5, 10, 15]"
        @current-change="handlePageChange"
        @size-change="handleSizeChange"
    />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { ElButton, ElInput, ElTable, ElTableColumn, ElTag, ElPagination } from 'element-plus'
import { Plus, Search, Edit, Delete } from '@element-plus/icons-vue'

// 测试数据
const cultureList = ref([
  {
    id: 1,
    name: '湘绣文化',
    topic: '非遗名俗',
    status: '已发布',
    createTime: '2024-03-20'
  },
  {
    id: 2,
    name: '岳阳楼文化',
    topic: '名胜古迹',
    status: '草稿',
    createTime: '2024-03-19'
  },
  // 更多测试数据...
])

const searchKeyword = ref('')
const currentPage = ref(1)
const pageSize = ref(10)

// 过滤文化列表
const filteredCultureList = computed(() => {
  return cultureList.value.filter((item) =>
      item.name.includes(searchKeyword.value)
  )
})

// 分页处理
const paginatedCultureList = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value;
  const end = start + pageSize.value;
  return filteredCultureList.value.slice(start, end);
})

const handlePageChange = (page) => {
  currentPage.value = page
}

const handleSizeChange = (size) => {
  pageSize.value = size
  currentPage.value = 1 // 当改变每页条数时，重置到第一页
}

// 新增文化
const handleAddCulture = () => {
  console.log('新增文化')
}

// 编辑文化
const handleEdit = (row) => {
  console.log('编辑文化:', row)
}

// 删除文化
const handleDelete = (row) => {
  console.log('删除文化:', row)
}

// 搜索文化
const handleSearch = () => {
  console.log('搜索文化:', searchKeyword.value)
}
</script>

<style scoped>
.pagination {
  margin-top: 20px;
  text-align: right;
}
</style>

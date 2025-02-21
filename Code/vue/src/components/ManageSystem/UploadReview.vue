<template>
  <div>
    <el-header>
      <el-input
          v-model="searchKeyword"
          placeholder="搜索上传内容"
          style="width: 300px; margin-bottom: 10px;"
      >
        <template #append>
          <el-button :icon="Search" @click="handleSearch" />
        </template>
      </el-input>
    </el-header>
    <el-table :data="paginatedUploadList" stripe style="width: 100%">
      <el-table-column prop="title" label="标题" />
      <el-table-column prop="uploader" label="上传者" />
      <el-table-column prop="type" label="类型" />
      <el-table-column prop="status" label="状态">
        <template #default="{ row }">
          <el-tag :type="getStatusTagType(row.status)">
            {{ row.status }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="uploadTime" label="上传时间" />
      <el-table-column label="操作" width="200">
        <template #default="{ row }">
          <el-button size="small" type="success" @click="handleApprove(row)">通过</el-button>
          <el-button size="small" type="danger" @click="handleReject(row)">拒绝</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination
        class="pagination"
        background
        layout="prev, pager, next, jumper, ->, sizes, total"
        :total="filteredUploadList.length"
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
import { Search } from '@element-plus/icons-vue'

// 测试数据
const uploadList = ref([
  {
    id: 1,
    title: '湘绣艺术展',
    uploader: '用户A',
    type: '图片',
    status: '待审核',
    uploadTime: '2024-03-20'
  },
  {
    id: 2,
    title: '岳阳楼历史介绍',
    uploader: '用户B',
    type: '视频',
    status: '已通过',
    uploadTime: '2024-03-19'
  },
  // 更多测试数据...
])

const searchKeyword = ref('')
const currentPage = ref(1)
const pageSize = ref(10)

// 过滤上传列表
const filteredUploadList = computed(() => {
  return uploadList.value.filter((item) =>
      item.title.toLowerCase().includes(searchKeyword.value.toLowerCase()) ||
      item.uploader.toLowerCase().includes(searchKeyword.value.toLowerCase())
  )
})

// 分页处理
const paginatedUploadList = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value;
  const end = start + pageSize.value;
  return filteredUploadList.value.slice(start, end);
})

const handlePageChange = (page) => {
  currentPage.value = page
}

const handleSizeChange = (size) => {
  pageSize.value = size
  currentPage.value = 1 // 当改变每页条数时，重置到第一页
}

// 刷新列表
const refreshList = () => {
  console.log('刷新列表')
}

// 搜索上传内容
const handleSearch = () => {
  console.log('搜索上传内容:', searchKeyword.value)
}

// 通过审核
const handleApprove = (row) => {
  console.log('通过审核:', row)
  row.status = '已通过'
}

// 拒绝审核
const handleReject = (row) => {
  console.log('拒绝审核:', row)
  row.status = '已拒绝'
}

// 根据状态获取标签类型
const getStatusTagType = (status) => {
  switch (status) {
    case '待审核':
      return 'warning'
    case '已通过':
      return 'success'
    case '已拒绝':
      return 'danger'
    default:
      return 'info'
  }
}
</script>

<style scoped>
.pagination {
  margin-top: 20px;
  text-align: right;
}
</style>

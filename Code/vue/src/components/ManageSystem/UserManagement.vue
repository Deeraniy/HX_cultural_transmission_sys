<template>
  <div>
    <el-header>
      <el-input
          v-model="searchKeyword"
          placeholder="搜索用户"
          style="width: 300px; margin-bottom: 10px;"
      >
        <template #append>
          <el-button :icon="Search" @click="handleSearch" />
        </template>
      </el-input>
    </el-header>
    <el-table :data="paginatedUsers" style="width: 100%">
      <el-table-column prop="name" label="用户名" />
      <el-table-column prop="id" label="用户ID" /><!--唯一-->
      <el-table-column prop="email" label="邮箱" />
      <el-table-column prop="role" label="角色" />
      <el-table-column label="操作">
        <template #default="{ row }">
          <el-button size="small" type="primary" @click="editUser(row)">编辑</el-button>
          <el-button size="small" type="danger" @click="deleteUser(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination
        class="pagination"
        background
        layout="prev, pager, next, jumper, ->, sizes, total"
        :total="filteredUsers.length"
        :page-size="pageSize"
        :current-page="currentPage"
        :page-sizes="[1, 5, 10, 15]"
        @current-change="handlePageChange"
        @size-change="handleSizeChange"
    />
  </div>
</template>

<script>
import { Search } from '@element-plus/icons-vue'

export default {
  name: 'UserManagement',
  components: {
    Search,
  },
  data() {
    return {
      users: [
        {name: '刁磊', id:222,email: 'hello8@example.com', role: '普通用户'},
        {name: '郑佳', id:123,email: '2237245963@qq.com', role: '管理员'},
        // 更多用户数据...
      ],
      searchKeyword: '',
      currentPage: 1,
      pageSize: 10,
    };
  },
  computed: {
    Search() {
      return Search
    },
    filteredUsers() {
      return this.users.filter(user =>
          user.name.toLowerCase().includes(this.searchKeyword.toLowerCase()) ||
          user.email.toLowerCase().includes(this.searchKeyword.toLowerCase())
      );
    },
    paginatedUsers() {
      const start = (this.currentPage - 1) * this.pageSize;
      const end = start + this.pageSize;
      return this.filteredUsers.slice(start, end);
    },
  },
  methods: {
    editUser(user) {
      this.$message.info(`编辑用户：${user.name}`);
    },
    deleteUser(user) {
      this.$message.error(`删除用户：${user.name}`);
    },
    handleSearch() {
      console.log('搜索用户:', this.searchKeyword);
    },
    handlePageChange(page) {
      this.currentPage = page;
    },
    handleSizeChange(size) {
      this.pageSize = size;
      this.currentPage = 1; // 当改变每页条数时，重置到第一页
    },
  },
};
</script>

<style scoped>
.pagination {
  margin-top: 20px;
  text-align: right;
}
</style>

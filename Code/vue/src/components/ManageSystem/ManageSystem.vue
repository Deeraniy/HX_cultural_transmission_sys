<template>
  <el-container style="height: 100vh">
    <el-header style="background-color: #d9534f; color: white; display: flex; justify-content: flex-end; align-items: center;">
      <el-dropdown @command="handleCommand">
        <span class="el-dropdown-link">
          <el-avatar :size="40" :src="avatarUrl"/>
          <div class="username">Admin</div>
        </span>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item command="profile">个人资料</el-dropdown-item>
            <el-dropdown-item command="changePassword">修改密码</el-dropdown-item>
            <el-dropdown-item command="logout">退出登录</el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </el-header>
    <el-container>
      <el-aside width="200px" style="background-color: indianred;">
        <el-menu default-active="1" class="el-menu-vertical-demo">
          <el-menu-item index="1" @click="navigateTo('user')" :icon="User">
            用户管理
          </el-menu-item>
          <el-menu-item index="2" @click="navigateTo('culture')" :icon="Collection">
            文化管理
          </el-menu-item>
          <el-menu-item index="3" @click="navigateTo('upload')" :icon="Upload">
            上传审核
          </el-menu-item>
        </el-menu>
      </el-aside>
      <el-main>
        <component :is="currentComponent"></component>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
import { ref } from 'vue';
import UserManagement from './UserManagement.vue';
import CultureManagement from './CultureManagement.vue';
import UploadReview from './UploadReview.vue';
import { User, Collection, Upload } from '@element-plus/icons-vue';

export default {
  name: 'ManageSystem',
  components: {
    User,
    Collection,
    UserManagement,
    CultureManagement,
    UploadReview,
  },
  setup() {
    const currentComponent = ref('UserManagement');
    const avatarUrl = ref('https://c-ssl.duitang.com/uploads/item/201807/23/20180723170155_mjfiq.jpg'); // 替换为实际的头像URL

    const navigateTo = (component) => {
      switch (component) {
        case 'user':
          currentComponent.value = 'UserManagement';
          break;
        case 'culture':
          currentComponent.value = 'CultureManagement';
          break;
        case 'upload':
          currentComponent.value = 'UploadReview';
          break;
      }
    };

    const handleCommand = (command) => {
      switch (command) {
        case 'profile':
          handleProfile();
          break;
        case 'changePassword':
          handleChangePassword();
          break;
        case 'logout':
          handleLogout();
          break;
      }
    };

    const handleProfile = () => {
      this.$message.info("查看个人资料");
      // 可添加查看个人资料的逻辑
    };

    const handleChangePassword = () => {
      this.$message.info("修改密码");
      // 可添加修改密码的逻辑
    };

    const handleLogout = () => {
      this.$message.warning("注销成功");
      // 可添加注销逻辑，例如清除token、重定向到登录页等
    };

    return {
      currentComponent,
      avatarUrl,
      navigateTo,
      handleCommand,
      handleProfile,
      handleChangePassword,
      handleLogout,
      User,
      Collection,
      Upload,
    };
  },
};
</script>

<style scoped>
.el-header {
  background-color: #d9534f;
  color: white;
  display: flex;
  justify-content: flex-end;
  align-items: center;
  padding: 0 20px;
}

.el-aside {
  background-color: indianred;
  color: white;
}

.el-dropdown-link {
  cursor: pointer;
  color: white;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.el-dropdown-link:hover {
  color: #f0f0f0;
}

.username {
  margin-top: 5px;
  font-size: 14px;
}
</style>

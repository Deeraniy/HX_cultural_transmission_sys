<template>
  <div>
    <!-- 顶栏 -->
    <div class="header-bar">
      <div class="header-content">
        <el-button
          class="back-button"
          type="primary"
          plain
          @click="goToHome"
        >
          <el-icon><ArrowLeft /></el-icon>
          返回主页
        </el-button>
        <div class="welcome-text">
          {{ userData[0].nickname || '用户' }}，欢迎来到个人中心！
        </div>
        <div class="placeholder"></div>
      </div>
    </div>

    <el-card class="box-card">
      <!-- 用户基础信息展示 -->
      <div class="user-profile">
        <div class="header-section">
          <!-- 左侧：头像和基本信息 -->
          <div class="left-section">
            <div class="avatar-name-section">
              <img :src="userData[0].avatar || '/default-avatar.png'" class="avatar">
              <div class="user-name">
                <h3>{{ userData[0].nickname || '未设置昵称' }}</h3>
                <p>账号：{{ userData[0].account }}</p>
              </div>
            </div>
            <!-- 基本信息 -->
            <div class="basic-info">
              <p class="info-item">性别: {{ formatGender(userData[0].gender) || '未设置' }}</p>
              <p class="info-item">年龄: {{ userData[0].age || '未设置' }}</p>
              <p class="info-item">地区: {{ userData[0].location || '未设置' }}</p>
              <p class="info-item">邮箱: {{ userData[0].email || '未设置' }}</p>
              <p class="info-item">电话: {{ userData[0].mobile || '未设置' }}</p>
            </div>
          </div>

          <!-- 右侧：标签展示 -->
          <div class="tag-section">
            <div class="section-title">我的标签</div>
            <div class="tags-container">
              <el-tag
                v-for="tag in tags"
                :key="tag.name"
                class="tag"
                :type="getTagType(tag.count)"
              >
                {{ tag.name }}
              </el-tag>
              <div v-if="tags.length === 0" class="no-tags">
                暂无标签
              </div>
            </div>
          </div>
        </div>

        <!-- 个人简介 -->
        <div class="description-section">
          <div class="description-header">
            <div class="section-title">个人简介</div>
          </div>
          <p>{{ userData[0].description }}</p>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import UserAPI from '@/api/user';
import { onMounted, ref, onUnmounted } from "vue";
import RecommendAPI from '@/api/recommend';
import { useUserStore } from '@/stores/user';
import { useRouter } from 'vue-router';
import { ArrowLeft } from '@element-plus/icons-vue';

const userStore = useUserStore();
const router = useRouter();

// 初始化默认值
let userData = ref([{
  uid: userStore.userId || 0,
  nickname: userStore.username || '',
  account: userStore.userId || '',
  gender: '',
  age: '',
  location: '',
  email: '',
  mobile: '',
  description: '这个人很懒，什么都没写~',
  avatar: new URL('@/assets/default-avatar.png', import.meta.url).href,
}]);

const tags = ref([]);

// 根据标签使用次数返回不同的标签类型
const getTagType = (count) => {
  if (count >= 10) return 'success';
  if (count >= 5) return 'warning';
  return 'info';
};

const goToHome = () => {
  router.push('/index');  // 返回主页
};

const formatGender = (gender) => {
  if (gender === '男' || gender === 'male') return '男';
  if (gender === '女' || gender === 'female') return '女';
  if (gender === '其他' || gender === 'other') return '其他';
  return gender;
};

// 添加刷新用户信息的方法
const refreshUserInfo = async () => {
  try {
    const res = await UserAPI.getUserFullInfo(userStore.userId);
    if (res && res.status === 'success' && res.data) {
      userData.value = [{
        ...userData.value[0],
        ...res.data,
        nickname: res.data.nickname || userStore.username,
        account: res.data.account || userStore.userId,
        gender: res.data.gender || '未设置',
        age: res.data.age || '未设置',
        location: res.data.location || '未设置',
        email: res.data.email || '未设置',
        mobile: res.data.mobile || '未设置',
        description: res.data.description || '这个人很懒，什么都没写~',
        avatar: res.data.avatar || new URL('@/assets/default-avatar.png', import.meta.url).href,
      }];
    }
  } catch (error) {
    console.error('刷新用户信息失败:', error);
  }
};

// 监听用户信息更新事件
const handleUserInfoUpdate = () => {
  refreshUserInfo();
};

onMounted(() => {
  if (userStore.isLoggedIn) {
    refreshUserInfo();
    RecommendAPI.getPerferenceAPI(userStore.userId).then(async res => {
      console.log('用户主页获取标签', res);
      // 处理详细偏好数据
      if (res.data?.detailed_preferences?.folk) {
        // 获取前5个标签的ID
        const tagList = res.data.detailed_preferences.folk.slice(0, 7);
        const tagIds = tagList.map(tag => tag.tag_id);

        try {
          // 获取标签详细信息
          const tagDetails = await RecommendAPI.getTagDetailAPI(tagIds);
          console.log('标签详细信息:', tagDetails);

          if (tagDetails?.status === 'success') {
            // 直接使用返回的标签详细信息
            tags.value = tagDetails.tag_details.map((tag, index) => ({
              name: tag.tag_name,  // 保留完整的标签名称，包括括号
              count: Math.round(tagList[index].score * 100)
            }));
            console.log('处理后的标签数据:', tags.value);
          }
        } catch (err) {
          console.error('获取标签详细信息失败:', err);
        }
      } else {
        console.log('没有找到folk标签数据:', res.data);
      }
    }).catch(err => {
      console.error('获取标签失败:', err);
    });
  }
});

// 添加事件监听
window.addEventListener('user-info-updated', handleUserInfoUpdate);

// 清理事件监听
onUnmounted(() => {
  window.removeEventListener('user-info-updated', handleUserInfoUpdate);
});
</script>

<style scoped>
.box-card {
  width: 100%;
  margin: 20px 40px;
  border-radius: 16px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  width: 920px;
  margin-left: 20px;
  margin-right: 20px;
  margin-top: 70px;
}

.user-profile {
  padding-top: 10px;
  padding-left: 40px;
  padding-right: 40px;
  padding-bottom: -10px;
}

.header-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #eee;
  padding: 20px 0;
}

.left-section {
  display: flex;
  align-items: center;
  gap: 40px;
}

.avatar-name-section {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  border: 3px solid #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.user-name {
  text-align: center;
  margin-top: 10px;
}

.user-name h3 {
  margin: 0;
  font-size: 26px;
  font-weight: 600;
}

.user-name p {
  margin: 8px 0 0;
  color: #666;
  font-size: 16px;
}

.basic-info {
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  height: 100%;
  padding: 10px 0;
  gap: 8px;
}

.info-item {
  font-size: 14px;
  color: #666;
  display: flex;
  align-items: center;
  line-height: 1.5;
}

.section-title {
  font-size: 20px;
  font-weight: bold;
  margin: 0;
  padding-left: 12px;
  border-left: 4px solid #b71c1c;
  min-width: 100px;
}

.tag-section {
  flex: 1;
  margin-left: 40px;
  padding: 20px;
  background-color: rgba(248, 249, 250, 0.9);
  border-radius: 12px;
  max-width: 400px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.tags-container {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 10px;
  align-items: center;
  min-height: 100px;
}

.tag {
  margin-right: 12px;
  padding: 0 15px;
  height: 32px;
  line-height: 32px;
  border-radius: 16px;
  transition: all 0.3s;
}

.tag:hover {
  transform: scale(1.05);
}

.description-section {
  background-color: rgba(248, 249, 250, 0.9);
  padding: 20px;
  border-radius: 12px;
  margin-top: 20px;
}

.description-header {
  display: flex;
  align-items: center;
  gap: 20px;
}

.description-section p {
  margin: 0;
  line-height: 1.6;
  color: #666;
  font-size: 15px;
}

.no-tags {
  color: #909399;
  font-size: 14px;
  padding: 20px 0;
  text-align: center;
  width: 100%;
}

.header-bar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  background-color: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(10px);
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 12px 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.welcome-text {
  font-size: 22px;
  font-weight: 500;
  color: #333;
  flex: 1;
  text-align: center;
  margin-right: 10px;
}

.back-button {
  display: flex;
  align-items: center;

  font-size: 16px;
  border-radius: 8px;
  transition: all 0.3s ease;
  margin-left: -80px;
}

.back-button:hover {
  transform: translateX(-5px);
}

.placeholder {
  width: 100px;
}
</style>

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
          {{ t('user.home.returnHome') }}
        </el-button>
        <div class="welcome-text">
          {{ userData[0].nickname || t('user.home.defaultUser', { defaultValue: '用户' }) }}，{{ t('user.home.welcome') }}
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
                <h3>{{ userData[0].nickname || t('user.home.defaultNickname', { defaultValue: '未设置昵称' }) }}</h3>
                <p>{{ t('user.home.account') }}：{{ userData[0].account }}</p>
              </div>
            </div>
            <!-- 基本信息 -->
            <div class="basic-info">
              <p class="info-item">{{ t('user.home.gender') }}: {{ formatGender(userData[0].gender) || t('user.home.notSet', { defaultValue: '未设置' }) }}</p>
              <p class="info-item">{{ t('user.home.age') }}: {{ userData[0].age || t('user.home.notSet', { defaultValue: '未设置' }) }}</p>
              <p class="info-item">{{ t('user.home.location') }}: {{ userData[0].location || t('user.home.notSet', { defaultValue: '未设置' }) }}</p>
              <p class="info-item">{{ t('user.home.email') }}: {{ userData[0].email || t('user.home.notSet', { defaultValue: '未设置' }) }}</p>
              <p class="info-item">{{ t('user.home.phone') }}: {{ userData[0].mobile || t('user.home.notSet', { defaultValue: '未设置' }) }}</p>
            </div>
          </div>

          <!-- 右侧：标签展示 -->
          <div class="tag-section">
            <div class="section-title">{{ t('user.home.tags') }}</div>
            <div class="tags-container">
              <el-tag
                v-for="tag in tags"
                :key="tag.name"
                class="tag"
                :type="getTagType(tag.count)"
              >
              {{ getName(tag.name) }}
              </el-tag>
              <div v-if="tags.length === 0" class="no-tags">
                {{ t('user.home.noTags') }}
              </div>
            </div>
          </div>
        </div>

        <!-- 个人简介 -->
        <div class="description-section">
          <div class="description-header">
            <div class="section-title">{{ t('user.home.introduction') }}</div>
          </div>
          <p>{{ userData[0].description || t('user.home.defaultDescription', { defaultValue: '这个人很懒，什么都没写~' }) }}</p>
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
import { useI18n } from 'vue-i18n';
import { ElMessage } from 'element-plus';
import cultureElements from '@/json/culture_elements_translated.json';
const userStore = useUserStore();
const router = useRouter();
const { t,locale } = useI18n();
// 获取名称的翻译
const getName = (name) => {
  const element = cultureElements.find(item => item.title === name);
  return locale.value === 'en' && element?.['title-en'] ? 
    element['title-en'] : 
    name;
};
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
  description: t('user.home.defaultDescription', { defaultValue: locale.value === 'en' ? 'This person is lazy, and nothing is written~' : '这个人很懒，什么都没写~' }),
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
  if (gender === 'MALE') return t('user.home.genderMap.MALE');
  if (gender === 'FEMALE') return t('user.home.genderMap.FEMALE');
  return t('user.home.genderMap.OTHER');
};

// 添加刷新用户信息的方法
const refreshUserInfo = async () => {
  try {
    const res = await UserAPI.getUserFullInfo(userStore.userId);
    if (res && res.status === 'success' && res.data) {
      userData.value = [{
        ...userData.value[0],
        ...res.data,
        nickname: res.data.nickname || userStore.username || t('user.home.defaultNickname'),
        account: res.data.account || userStore.userId,
        gender: formatGender(res.data.gender),
        age: res.data.age || t('user.home.notSet'),
        location: res.data.location || t('user.home.notSet'),
        email: res.data.email || t('user.home.notSet'),
        mobile: res.data.mobile || t('user.home.notSet'),
        description: res.data.description || t('user.home.defaultDescription'),
        avatar: res.data.avatar || new URL('@/assets/default-avatar.png', import.meta.url).href,
      }];
    }
  } catch (error) {
    console.error('刷新用户信息失败:', error);
    ElMessage.error(t('user.home.getInfoError'));
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
      
      // 合并所有主题的标签
      const allTags = [];
      const themes = ['food', 'literature', 'spot', 'folk'];
      
      // 遍历所有主题，收集标签
      themes.forEach(theme => {
        const themePreferences = res.data?.detailed_preferences?.[theme];
        if (themePreferences && Array.isArray(themePreferences)) {
          themePreferences.forEach(tag => {
            // 标签对象必须包含tag_id和score
            if (tag && tag.tag_id) {
              allTags.push({
                tag_id: tag.tag_id,
                score: tag.score || 0,
                theme: theme // 记录标签来源的主题
              });
            }
          });
        }
      });
      
      // 按评分排序
      allTags.sort((a, b) => b.score - a.score);
      
      // 获取前7个标签
      const topTags = allTags.slice(0, 7);
      
      if (topTags.length > 0) {
        // 获取标签IDs
        const tagIds = topTags.map(tag => tag.tag_id);
        
        try {
          // 获取标签详细信息
          const tagDetails = await RecommendAPI.getTagDetailAPI(tagIds);
          console.log('标签详细信息:', tagDetails);
          
          if (tagDetails?.status === 'success') {
            // 将标签详情与评分合并
            tags.value = tagDetails.tag_details.map((tag, index) => ({
              name: tag.tag_name, // 标签名称
              count: Math.round(topTags[index].score * 100), // 标签权重
              theme: topTags[index].theme // 标签来源主题
            }));
            console.log('处理后的标签数据:', tags.value);
          }
        } catch (err) {
          console.error('获取标签详细信息失败:', err);
        }
      } else {
        console.log('没有找到任何主题的标签数据');
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

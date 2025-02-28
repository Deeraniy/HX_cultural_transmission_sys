<template>
  <div>
    <el-card class="box-card">
      <!-- 用户基础信息展示 -->
      <div class="user-profile">
        <!-- 头部：头像和用户名 -->
        <div class="header-section">
          <img :src="userData[0].avatar" class="avatar">
          <div class="user-name">
            <h3>{{ userData[0].nickname }}</h3>
            <p>账号：{{ userData[0].account }}</p>
          </div>
          <!-- 基本信息 -->
          <div class="basic-info">
            <p class="info-item">性别: {{ userData[0].gender }}</p>
            <p class="info-item">年龄: {{ userData[0].age }}</p>
            <p class="info-item">邮箱: {{ userData[0].email }}</p>
            <p class="info-item">电话: {{ userData[0].mobile }}</p>
          </div>
        </div>

        <!-- 标签展示 -->
        <div class="tag-section">
          <div class="section-title">我的标签</div>
          <div>
            <el-tag
                v-for="tag in tags"
                :key="tag.name"
                class="tag"
            >
              {{ tag.name }}
            </el-tag>
          </div>
        </div>

        <!-- 简介 -->
        <div class="description-section">
          <div class="section-title">个人简介</div>
          <p>{{ userData[0].description }}</p>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { getUserInfo } from '@/apis/user';
import { onMounted, ref } from "vue";
import { getUserTagList } from '@/apis/user';

let userData = ref([{
  uid: 0,
  nickname: 'Osborn',
  account: '20230408',
  gender: 'man',
  age: '22',
  email: '2710740557@qq.com',
  mobile: '保密',
  description: '欢迎发邮件到我的信箱',
  avatar: '/src/assets/111.png'
}]);

const tags = ref([]);

onMounted(() => {
  getUserInfo().then(res => {
    userData.value = [res.data];
    console.log(userData.value[0]);
    console.log('获取用户信息成功');
  });

  getUserTagList(userData.value[0].uid).then(res => {
    console.log('用户主页获取标签', res);
    tags.value = res.data.pageInfo.list;
  });
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
}

.user-profile {
  padding-top: 10px;
  padding-left: 40px;
  padding-right: 40px;
  padding-bottom: -10px;
}

.header-section {
  display: flex;
  align-items: center;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid #eee;
}

.avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  margin-right: 25px;
  border: 3px solid #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
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
  margin-left: 40px;
}

.info-item {
  font-size: 14px;  /* 小字 */
  color: #666;
  margin-bottom: 8px;
}

.section-title {
  font-size: 20px;
  font-weight: bold;
  margin: 25px 0 15px;
  padding-left: 12px;
  border-left: 4px solid #409EFF;
}

.tag {
  margin-right: 12px;
  margin-bottom: 12px;
  padding: 0 15px;
  height: 32px;
  line-height: 32px;
  border-radius: 16px;
}

.tag-section {
  background-color: #f8f9fa;
  padding-left: 15px;
  padding-top: 0.5px;
  padding-bottom: 5px;
  border-radius: 12px;
  width: 100%;
}

.description-section {
  margin: 30px 0;
  padding-left: 15px;
  padding-top: 0.5px;
  padding-bottom: 15px;
  background-color: #f8f9fa;
  border-radius: 12px;
  width: 100%;
}

.description-section p {
  margin: 0;
  line-height: 1.6;
  color: #666;
  font-size: 15px;
}
</style>

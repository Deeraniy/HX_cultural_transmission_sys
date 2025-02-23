<!-- 用户文章界面 -->
<script setup>
import ArticleCardFull from '@/components/article/ArticleCardFull.vue';

import { getUserArticleList } from '@/apis/user';
import {onMounted, ref} from "vue";
import {Clock} from "@element-plus/icons-vue";

const articleList = ref([]);
const activeTab = ref('全部');
const tabs = ['全部', '美食', '文学', '风景','民俗'];
const searchQuery = ref('');

// Methods
const selectTab = (tab) => {
  activeTab.value = tab;
};

const clearSearch = () => {
  searchQuery.value = '';
};

const batchManage = () => {
  console.log('Batch management triggered');
};

onMounted(() => {
  // 获取后端文章数据
  getUserArticleList().then(res => {
    articleList.value = res.data.pageInfo.list;
    console.log(articleList.value)
  });

});
const virtualArticles = [
  {
    timestamp: '今天',
    title: '探索美食：亚洲街头小吃',
    description: '一起探索亚洲最具代表性的街头小吃，享受独特的美味和风味。',
    viewDuration: '5:30',
  },
  {
    timestamp: '近一周',
    title: '文学的力量：如何写出打动人心的故事',
    description: '通过一些经典的故事，分析如何构建感人的情节。',
    viewDuration: '6:45',
  },
  {
    timestamp: '近一周',
    title: '风景画的魅力：一探自然与艺术的结合',
    description: '了解风景画艺术背后的历史和技巧，感受大自然的美丽。',
    viewDuration: '4:15',
  },
  {
    timestamp: '一周前',
    title: '民俗探秘：揭秘中国传统节日的背后故事',
    description: '了解中国各大传统节日的历史与文化背景。',
    viewDuration: '7:00',
  },
  {
    timestamp: '一周前',
    title: '科技未来：人工智能的应用与挑战',
    description: '深入探讨人工智能技术如何改变我们的工作和生活。',
    viewDuration: '8:20',
  }
];

</script>

<template>
  <div>
    <div>
        <div>
          <el-icon style="font-size: 20px;"><Clock/></el-icon><el-text class="mainTitle" >浏览记录</el-text>
        </div>
      <div>
      </div>
      <div class="container" style="display: flex">
        <!-- Tabs Section -->
        <div class="tabs">
          <el-button
              v-for="(tab, index) in tabs"
              :key="index"
              :class="['tab', { active: activeTab === tab }]"
              @click="selectTab(tab)"
          >
            {{ tab }}
          </el-button>
        </div>

        <!-- Search Section -->
        <div class="search-section">
          <input
              type="text"
              v-model="searchQuery"
              placeholder="搜索标题/up主昵称"
              class="search-input"
          />
          <el-button @click="clearSearch">清空历史</el-button>
          <el-button @click="batchManage">批量管理</el-button>
        </div>
      </div>
    </div>
  <div>
    <el-timeline style="max-width: 600px">
      <el-timeline-item
          v-for="(article, index) in virtualArticles"
          :key="index"
          :timestamp="article.timestamp"
          placement="top"
      >
        <el-card>
          <h4>{{ article.title }}</h4>
          <p>{{ article.description }}</p>
          <p>观看时长: {{ article.viewDuration }}</p>
        </el-card>
      </el-timeline-item>
    </el-timeline>
  </div>
  </div>
</template>

<style scoped>
.mainTitle {
    margin-left: 30px;
    font-size: 18px;
    color: #000;
    font-weight: bolder;
}
</style>

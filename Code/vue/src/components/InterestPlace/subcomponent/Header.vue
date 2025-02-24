<template>
  <div class="button-container">
    <!-- 返回按钮和标题 -->
    <el-page-header @back="onBack" class="header" style="color: #fff8f0;font-size: 30px">
      <template #content>
        <span class="title" style="font-size: 30px">{{title}}</span>
      </template>
    </el-page-header>

    <!-- 添加搜索框和下拉列表 -->
    <div class="header-actions">
      <!-- 下拉列表 -->
      <el-dropdown trigger="click" @command="handleCommand">
        <el-button type="primary">
          {{ selectedType || '文化类型' }} <el-icon class="el-icon--right"><arrow-down /></el-icon>
        </el-button>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item command="1">名胜古迹</el-dropdown-item>
            <el-dropdown-item command="2">影视文学</el-dropdown-item>
            <el-dropdown-item command="3">美食文化</el-dropdown-item>
            <el-dropdown-item command="4">非遗民俗</el-dropdown-item>
            <el-dropdown-item command="5">红色文化</el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>

      <!-- 搜索框部分 -->
      <el-input
          v-model="searchQuery"
          placeholder="请输入搜索内容"
          style="width: 200px; margin-left: 20px;"
          clearable
          @keyup.enter="handleSearch"
      />


    </div>

    <!-- 用户信息和头像 -->
    <!-- 生成AI报告按钮 -->
    <div class="report-button">
      <el-button
          type="primary"
          :icon="Document"
          size="large"
          @click="drawer = true"
          class="generate-report-btn"
      >
        生成AI报告
      </el-button>
    </div>

    <!-- 抽屉组件 -->
    <el-drawer v-model="drawer" title="AI Report">
      <div v-html="markdownContent"></div>
    </el-drawer>
  </div>
</template>

<script setup>
import { ArrowLeft, Setting, Document } from "@element-plus/icons-vue";
import { ref, onMounted, watch } from 'vue';
import router from "@/router.js";
import { marked } from 'marked';
import SentimentAPI from "@/api/sentiment.ts";
import { ArrowDown } from '@element-plus/icons-vue'
import {useRoute} from "vue-router";  // 添加这行
const drawer = ref(false);
const searchQuery = ref(''); // 搜索框的绑定变量
const markdownContent = ref(''); // 存储转换后的 HTML 内容
const props = defineProps({title: String});
const route = useRoute()
const selectedType = ref('');

const emit = defineEmits(['update:type', 'update:search']);
// 处理下拉选择

// 处理下拉选择
const handleCommand = (command) => {
  const typeMap = {
    '1': '名胜古迹',
    '2': '影视文学',
    '3': '美食文化',
    '4': '非遗民俗',
    '5': '红色文化'
  };
  selectedType.value = typeMap[command];
  emit('update:type', command); // 发送类型ID给父组件
};

// 处理搜索输入
// 处理搜索输入
// 处理搜索输入（仅在按下 Enter 时触发）
const handleSearch = () => {
  if (searchQuery.value.trim()) {
    emit('update:search', searchQuery.value.trim());
    console.log('发送搜索内容:', searchQuery.value.trim());
    // 清空搜索框
    searchQuery.value = '';
    // 重置下拉列表选项
    selectedType.value = null;
  }
};

const onBack = () => {
  router.go(-1);
  console.log("返回按钮被点击");
};

onMounted(() => {
  console.log("Header组件被加载",route.query.value);
  SentimentAPI.getSentimentReportAPI(props.title, route.query.value)

      .then((res) => {
        console.log("AI报告：",props.title)
        console.log("AI 报告原始 Markdown:", res);

        if (res && res.report) {
          const cleanedMarkdown = res.report.replace(/^\s+/, "");
          markdownContent.value = marked(res.report); // 提取 report 字段，并转换为 HTML
          console.log("AI 报告解析后的 HTML:", markdownContent.value);
        } else {
          console.warn("API 返回的内容不包含 'report' 字段:", res);
        }
      })
      .catch((error) => {
        console.error("加载 AI 报告时出错:", error);
      });
});
</script>

<style scoped>
@import '@/assets/font/font.css';

/* 主容器的样式 */
.button-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 20px;
  background-image: url('@/assets/img_4.png');
  background-size: cover;
  background-position: center;
  border-bottom-left-radius: 30px;
  border-bottom-right-radius: 30px;
  position: relative;
}

.no-wrap {
  font-family: 'HelveticaNeue', serif;
  white-space: nowrap;
  display: inline-block;
}

/* 返回按钮样式 */
.header {
  width: 100%;
  display: flex;
  align-items: center;
  cursor: pointer;
}
.el-drawer div {
  padding: 20px;
  font-size: 14px;
  line-height: 1.5;
  color: #333;
}

/* 标题样式 */
.title {
  color: #fff8f0;
  font-family: 'HelveticaNeue', serif;
  font-size: 20px;
  font-weight: bold;
}

/* 用户信息区域 */
.user-info {
  display: flex;
  align-items: center;
  color: #fff8f0;
}

.sub-title {
  font-family: 'HelveticaNeue', serif;
  font-size: 18px;
  color: #fff8f0;
  margin-right: 15px;
}

.block {
  margin-right: 15px;
}

/* 搜索框和下拉列表的容器 */
.header-actions {
  margin-right: 350px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex: 1;
}

/* 工具栏图标样式 */
.toolbar .el-icon {
  color: #fff8f0;
}
.report-button {
  display: flex;
  align-items: center;
}

/* 修改按钮样式 */
.generate-report-btn {
  font-size: 16px;
  border: 2px solid #d4af37;  /* 添加金色边框 */
  padding: 12px 24px;
  border-radius: 25px;  /* 增加圆角 */
  background: #fff8f0;  /* 金色背景 */
  color: black;
  font-family: 'HelveticaNeue', serif;  /* 设置字体为更有质感的字体 */
  transition: all 0.3s;
}

.generate-report-btn:hover {
  background: #FFC107;  /* 金色的 hover 状态 */
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(255, 215, 0, 0.3);
  border-radius: 25px;  /* hover 状态也保持圆角 */
}

.generate-report-btn:focus {
  outline: none;  /* 去掉焦点时的边框 */
}
/* 修改下拉按钮样式 */
.el-dropdown .el-button {
  background-color: #fff8f0;  /* 金色背景 */
  border: 2px solid #d4af37;  /* 添加金色边框 */
  color: black;
  font-family: 'HelveticaNeue', serif;  /* 修改字体 */
  font-size: 16px;
}

.el-dropdown .el-button .el-icon--right {
  color: black !important;  /* 强制将下拉符号的颜色设置为黑色 */
}


.el-dropdown .el-button:hover {
  background-color: #FFC107;  /* 金色的 hover 状态 */
  box-shadow: 0 4px 12px rgba(255, 215, 0, 0.3);
}

.el-dropdown .el-button .el-icon--right {
  color: white;  /* 确保右侧箭头图标颜色也为白色 */
}

/* 修改下拉菜单样式 */
.el-dropdown-menu {
  background-color: rgba(255, 248, 240, 0.8);  /* 设置背景色为透明的米黄色 */
  color: black;  /* 设置文字颜色为白色 */
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  font-family: 'Georgia', serif;  /* 修改字体 */
}

.el-dropdown-item {
  padding: 10px 20px;
  color: white;  /* 白色字体 */
  font-size: 16px;
  font-family: 'Georgia', serif;  /* 修改字体 */
}

.el-dropdown-item:hover {
  background-color: #FFC107;  /* 金色 hover 状态 */
  color: black;  /* 高亮显示时字体颜色为黑色 */
}
</style>

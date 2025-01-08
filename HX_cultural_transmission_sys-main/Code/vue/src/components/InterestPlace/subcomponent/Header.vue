<template>
  <div class="button-container">
    <!-- 返回按钮和标题 -->
    <el-page-header @back="onBack" class="header" style="color: #fff8f0;font-size: 30px">
      <template #content>
        <span class="title" style="font-size: 30px">{{title}}</span>
      </template>
    </el-page-header>

    <!-- 用户信息和头像 -->
    <div class="user-info">
      <img
          src="@/assets/cat.gif"
          style="width: 100px; cursor: pointer;"
          @click="drawer = true"
      />

      <h3 class="no-wrap">👈👈👈点我查看报告😸</h3>
<!--      <div class="block">-->
<!--        <el-avatar :size="50" :src="circleUrl" />-->
<!--      </div>-->
<!--      <div class="toolbar">-->
<!--        <el-dropdown>-->
<!--          <el-icon style="margin-right: 0px; font-size: 25px; margin-top: 5px">-->
<!--            <Setting />-->
<!--          </el-icon>-->
<!--          <template #dropdown>-->
<!--            <el-dropdown-menu>-->
<!--              <el-dropdown-item>退出登录</el-dropdown-item>-->
<!--              <el-dropdown-item>个人信息</el-dropdown-item>-->
<!--              <el-dropdown-item>修改密码</el-dropdown-item>-->
<!--            </el-dropdown-menu>-->
<!--          </template>-->
<!--        </el-dropdown>-->
<!--      </div>-->
    </div>
    <el-drawer v-model="drawer" title="AI Report">
      <!-- 使用 v-html 动态渲染 Markdown 内容 -->
      <div v-html="markdownContent"></div>
    </el-drawer>

  </div>
</template>

<script setup>
import { ArrowLeft, Setting } from "@element-plus/icons-vue";
import router from "@/router.js";
const drawer = ref(false)
import { ref, onMounted } from 'vue';
import { marked } from 'marked';
import SentimentAPI from "@/api/sentiment.ts";

const markdownContent = ref(''); // 存储转换后的 HTML 内容
const drawerVisible = ref(false); // 控制抽屉的可见性


const openDrawer = () => {
  drawerVisible.value = true;
};

const closeDrawer = () => {
  drawerVisible.value = false;
};


const circleUrl = ref("https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png");
const props = defineProps({title:String})
const onBack = () => {
  router.go(-1);
  console.log("返回按钮被点击");
};

onMounted(() => {
  SentimentAPI.getSentimentReportAPI(props.title)
      .then((res) => {
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

/* 主容器的样式，与 tab 样式一致 */
.button-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 20px;
  background-image: url('@/assets/img_4.png'); /* 设置与标签栏一致的背景 */
  background-size: cover;
  background-position: center;
  border-bottom-left-radius: 30px;
  border-bottom-right-radius: 30px;
}
.no-wrap {
  font-family: 'HelveticaNeue', serif;
  white-space: nowrap; /* 强制不换行 */
  display: inline-block; /* 确保宽度由内容决定 */
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

.back-icon {
  color: #fff8f0;
  font-size: 25px;
  margin-right: 8px;
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
.header .el-page-header__content::before,
.header .el-page-header__content::after {
  content: none; /* 隐藏多余的分隔符 */
}
/* 工具栏图标样式 */
.toolbar .el-icon {
  color: #fff8f0;
}
</style>

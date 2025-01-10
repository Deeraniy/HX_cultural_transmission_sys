<template>
  <div>
    <!-- 渲染从 HTML 文件加载的内容 -->
    <div v-html="htmlContent"></div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      htmlContent: '',  // 存储加载的 HTML 内容
    };
  },
  mounted() {
    // 组件挂载时加载 HTML 文件
    this.loadHTML();
  },
  methods: {
    async loadHTML() {
      try {
        const response = await fetch(new URL('@/components/FolkCustom/lunbo.html', import.meta.url));  // 使用 Vite 动态加载静态资源
        if (response.ok) {
          this.htmlContent = await response.text();  // 获取文件内容
        } else {
          console.error('加载 HTML 文件失败');
        }
      } catch (error) {
        console.error('请求错误:', error);
      }
    }
  }
};
</script>

<style scoped>
/* 为 HTML 内容添加样式 */
</style>

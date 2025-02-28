<script setup lang="ts">
import { ref, onMounted } from "vue";
import { Upload, Link, Plus } from "@element-plus/icons-vue";

interface LinkItem {
  value: string;
  link: string;
}

const state = ref("");
const state1 = ref("");
const textarea = ref("");
const links = ref<LinkItem[]>([]);
const loading = ref(false);

// 加载建议数据
const loadAll = () => {
  return [
    { value: 'vue', link: 'https://github.com/vuejs/vue' },
    { value: 'element', link: 'https://github.com/ElemeFE/element' },
    { value: 'cooking', link: 'https://github.com/ElemeFE/cooking' },
    { value: 'mint-ui', link: 'https://github.com/ElemeFE/mint-ui' },
    { value: 'vuex', link: 'https://github.com/vuejs/vuex' },
    { value: 'vue-router', link: 'https://github.com/vuejs/vue-router' },
    { value: 'babel', link: 'https://github.com/babel/babel' },
  ];
};

let timeout: ReturnType<typeof setTimeout>;
const querySearchAsync = (queryString: string, cb: (arg: any) => void) => {
  const results = queryString
      ? links.value.filter(createFilter(queryString))
      : links.value;

  clearTimeout(timeout);
  timeout = setTimeout(() => {
    cb(results);
  }, 300);
};

const createFilter = (queryString: string) => {
  return (item: LinkItem) => {
    return item.value.toLowerCase().indexOf(queryString.toLowerCase()) === 0;
  };
};

const handleSelect = (item: Record<string, any>) => {
  console.log(item);
};

const handleSubmit = () => {
  if (!state.value || !state1.value || !textarea.value) {
    ElMessage.warning('请填写完整信息');
    return;
  }

  loading.value = true;
  // 模拟提交
  setTimeout(() => {
    ElMessage.success('关系创建成功');
    loading.value = false;
    // 清空表单
    state.value = '';
    state1.value = '';
    textarea.value = '';
  }, 1000);
};

onMounted(() => {
  links.value = loadAll();
});
</script>

<template>
  <div class="relation-container">
    <!-- 标题区域 -->
    <div class="header-section">
      <div class="title-wrapper">
        <el-icon><Link /></el-icon>
        <span class="main-title">创建关系</span>
      </div>
      <p class="subtitle">在知识图谱中创建节点之间的关系</p>
    </div>

    <!-- 主要内容卡片 -->
    <el-card class="relation-card" shadow="hover">
      <div class="form-container">
        <!-- 第一个节点 -->
        <div class="form-item">
          <div class="form-label">
            <span class="required">*</span>
            起始节点
          </div>
          <el-autocomplete
              v-model="state"
              :fetch-suggestions="querySearchAsync"
              placeholder="请选择或输入起始节点"
              class="node-input"
              :trigger-on-focus="true"
              @select="handleSelect"
          >
            <template #prefix>
              <el-icon><Plus /></el-icon>
            </template>
          </el-autocomplete>
        </div>

        <!-- 关系描述 -->
        <div class="form-item">
          <div class="form-label">
            <span class="required">*</span>
            关系描述
          </div>
          <el-input
              v-model="textarea"
              type="textarea"
              :rows="3"
              placeholder="请描述两个节点之间的关系"
              class="relation-input"
              maxlength="100"
              show-word-limit
          />
        </div>

        <!-- 第二个节点 -->
        <div class="form-item">
          <div class="form-label">
            <span class="required">*</span>
            目标节点
          </div>
          <el-autocomplete
              v-model="state1"
              :fetch-suggestions="querySearchAsync"
              placeholder="请选择或输入目标节点"
              class="node-input"
              :trigger-on-focus="true"
              @select="handleSelect"
          >
            <template #prefix>
              <el-icon><Plus /></el-icon>
            </template>
          </el-autocomplete>
        </div>

        <!-- 提交按钮 -->
        <div class="form-actions">
          <el-button type="primary" :loading="loading" @click="handleSubmit">
            <el-icon><Upload /></el-icon>
            创建关系
          </el-button>
          <el-button @click="state = state1 = textarea = ''">
            清空
          </el-button>
        </div>
      </div>
    </el-card>
  </div>
</template>

<style scoped>
.relation-container {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.header-section {
  margin-bottom: 30px;
}

.title-wrapper {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 10px;
}

.main-title {
  font-size: 24px;
  font-weight: 600;
  color: #303133;
}

.subtitle {
  color: #909399;
  font-size: 14px;
  margin: 0;
  margin-left: 34px;
}

.relation-card {
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
}

.form-container {
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.form-item {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.form-label {
  font-size: 14px;
  color: #606266;
  display: flex;
  align-items: center;
  gap: 4px;
}

.required {
  color: #f56c6c;
  margin-right: 4px;
}

.node-input {
  width: 100%;
}

.relation-input {
  width: 100%;
}

.form-actions {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 20px;
}

/* 深度选择器修改 element-plus 组件样式 */
:deep(.el-input__wrapper) {
  box-shadow: 0 0 0 1px #dcdfe6 inset;
}

:deep(.el-input__wrapper:hover) {
  box-shadow: 0 0 0 1px #409eff inset;
}

:deep(.el-textarea__inner) {
  min-height: 80px !important;
}

/* 响应式布局 */
@media screen and (max-width: 768px) {
  .relation-container {
    padding: 10px;
  }

  .form-container {
    padding: 15px;
  }

  .form-actions {
    flex-direction: column;
  }

  .form-actions .el-button {
    width: 100%;
  }
}

/* 动画效果 */
.relation-card {
  transition: all 0.3s ease;
}

.relation-card:hover {
  transform: translateY(-2px);
}

.form-item {
  transition: all 0.3s ease;
}

.form-item:hover {
  transform: translateX(5px);
}
</style>

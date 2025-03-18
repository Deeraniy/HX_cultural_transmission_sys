<script setup>
import { ref, onMounted } from 'vue';
import { getUserTagList, updateTagName, deleteTag, postNewTag } from '@/apis/user';
import { Plus, Edit, Delete, Check, Close } from '@element-plus/icons-vue';

// 数据
const tagsData = ref([]);
const msg = ref('');
const editedTag = ref({
  tagId: 0,
  name: ''
});
const edit = ref({
  tag: 0,
  status: false
});
const showAddForm = ref(false);

// 加载数据
const loadTagsData = async () => {
  try {
    const res = await getUserTagList();
    tagsData.value = res.data.pageInfo.list;
  } catch (error) {
    console.error('加载标签失败:', error);
  }
};

onMounted(() => {
  loadTagsData();
});

// 新增标签
const addNewTag = async () => {
  if (!editedTag.value.name.trim()) {
    ElMessage.warning('标签名不能为空');
    return;
  }

  try {
    await postNewTag({ name: editedTag.value.name });
    await loadTagsData();
    editedTag.value.name = '';
    showAddForm.value = false;
    ElMessage.success('标签添加成功');
  } catch (error) {
    ElMessage.error('添加失败');
  }
};

// 编辑标签
const openEdit = (tagId, currentName) => {
  edit.value.status = true;
  edit.value.tag = tagId;
  editedTag.value.name = currentName;
};

// 提交修改
const handleSubmit = async (tagId) => {
  if (!editedTag.value.name.trim()) {
    ElMessage.warning('标签名不能为空');
    return;
  }

  try {
    editedTag.value.tagId = tagId;
    await updateTagName(editedTag.value);
    await loadTagsData();
    edit.value.status = false;
    ElMessage.success('修改成功');
  } catch (error) {
    ElMessage.error('修改失败');
  }
};

// 删除标签
const handleDelete = async (tagId) => {
  try {
    await ElMessageBox.confirm('确定要删除这个标签吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    });

    await deleteTag(tagId);
    await loadTagsData();
    ElMessage.success('删除成功');
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败');
    }
  }
};
</script>

<template>
  <div class="tags-container">
    <!-- 标题区域 -->
    <div class="header-section">
      <div class="title-wrapper">
        <el-icon><Collection /></el-icon>
        <span class="main-title">我的标签</span>
      </div>
      <el-button type="primary" @click="showAddForm = true" v-if="!showAddForm">
        <el-icon><Plus /></el-icon>
        添加新标签
      </el-button>
    </div>

    <!-- 主要内容卡片 -->
    <el-card class="tags-card" shadow="hover">
      <!-- 提示信息 -->
      <el-alert
          v-if="msg"
          :title="msg"
          :type="msg.includes('成功') ? 'success' : 'error'"
          show-icon
          class="alert-message"
      />

      <!-- 新增标签表单 -->
      <div v-if="showAddForm" class="add-tag-form">
        <el-input
            v-model="editedTag.name"
            placeholder="输入新标签名称"
            maxlength="20"
            show-word-limit
            class="tag-input"
        >
          <template #append>
            <el-button type="primary" @click="addNewTag">
              <el-icon><Check /></el-icon>
              确认
            </el-button>
            <el-button @click="showAddForm = false">
              <el-icon><Close /></el-icon>
              取消
            </el-button>
          </template>
        </el-input>
      </div>

      <!-- 标签列表 -->
      <div class="tags-list">
        <div v-for="(tag, index) in tagsData" :key="tag.tagId" class="tag-item">
          <!-- 标签展示 -->
          <div class="tag-content" v-if="!(edit.status && tag.tagId === edit.tag)">
            <span class="tag-index">#{{ index + 1 }}</span>
            <el-tag size="large" class="tag-name">{{ tag.name }}</el-tag>
            <div class="tag-actions">
              <el-button
                  type="primary"
                  text
                  @click="openEdit(tag.tagId, tag.name)"
              >
                <el-icon><Edit /></el-icon>
                编辑
              </el-button>
              <el-button
                  type="danger"
                  text
                  @click="handleDelete(tag.tagId)"
              >
                <el-icon><Delete /></el-icon>
                删除
              </el-button>
            </div>
          </div>

          <!-- 编辑表单 -->
          <div v-else class="edit-form">
            <el-input
                v-model="editedTag.name"
                placeholder="输入新的标签名称"
                maxlength="20"
                show-word-limit
                class="tag-input"
            >
              <template #append>
                <el-button type="primary" @click="handleSubmit(tag.tagId)">
                  <el-icon><Check /></el-icon>
                  确认
                </el-button>
                <el-button @click="edit.status = false">
                  <el-icon><Close /></el-icon>
                  取消
                </el-button>
              </template>
            </el-input>
          </div>
        </div>
      </div>
    </el-card>
  </div>
</template>

<style scoped>
.tags-container {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.header-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.title-wrapper {
  display: flex;
  align-items: center;
  gap: 10px;
}

.main-title {
  font-size: 24px;
  font-weight: 600;
  color: #303133;
}

.tags-card {
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
}

.alert-message {
  margin-bottom: 20px;
}

.add-tag-form {
  margin-bottom: 20px;
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 8px;
}

.tag-input {
  max-width: 500px;
}

.tags-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.tag-item {
  padding: 10px;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.tag-item:hover {
  background-color: #f8f9fa;
}

.tag-content {
  display: flex;
  align-items: center;
  gap: 15px;
}

.tag-index {
  color: #909399;
  font-size: 14px;
  min-width: 40px;
}

.tag-name {
  font-size: 14px;
  padding: 8px 12px;
}

.tag-actions {
  margin-left: auto;
  display: flex;
  gap: 10px;
}

.edit-form {
  padding: 10px;
  background-color: #f8f9fa;
  border-radius: 8px;
}

/* 响应式布局 */
@media screen and (max-width: 768px) {
  .tags-container {
    padding: 10px;
  }

  .header-section {
    flex-direction: column;
    align-items: flex-start;
    gap: 15px;
  }

  .tag-content {
    flex-wrap: wrap;
    gap: 10px;
  }

  .tag-actions {
    width: 100%;
    justify-content: flex-end;
  }
}

/* 动画效果 */
.tag-item {
  transition: all 0.3s ease;
}

.tag-item:hover {
  transform: translateX(5px);
}

.edit-form {
  animation: slideDown 0.3s ease;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>

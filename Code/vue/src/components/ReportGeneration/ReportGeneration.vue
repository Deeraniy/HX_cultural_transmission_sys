<template>
  <div class="report-generation">
    <el-card class="form-card">
      <h2>宣传报道生成</h2>
      <el-form :model="report" ref="form" label-width="120px" class="form">
        <!-- 可选标签展示 -->
        <el-form-item label="选择标签" prop="tags">
          <div class="available-tags">
            <el-tag
                v-for="(tag, index) in availableTags"
                :key="index"
                :closable="isTagSelected(tag)"
                @close="removeTag(tag)"
                :type="isTagSelected(tag) ? 'success' : 'info'"
                @click="toggleTagSelection(tag)"
                class="tag-item"
            >
              {{ tag }}
            </el-tag>
          </div>
        </el-form-item>

        <!-- 已选择的标签展示 -->
        <div v-if="selectedTags.length" class="selected-tags">
          <span><strong>已选择标签：</strong></span>
          <el-tag
              v-for="(tag, index) in selectedTags"
              :key="index"
              closable
              @close="removeTag(tag)"
              class="selected-tag"
          >
            {{ tag }}
          </el-tag>
        </div>

        <!-- 标题输入 -->
        <el-form-item label="标题" prop="title" :rules="[{ required: true, message: '请输入标题', trigger: 'blur' }]">
          <el-input v-model="report.title" placeholder="请输入报道标题"/>
        </el-form-item>

        <!-- 内容输入 -->
        <el-form-item label="内容" prop="content"
                      :rules="[{ required: true, message: '请输入报道内容', trigger: 'blur' }]">
          <el-input
              type="textarea"
              v-model="report.content"
              placeholder="请输入报道内容"
              rows="6"
          />
        </el-form-item>

        <!-- 生成与润色按钮 -->
        <el-form-item>
          <el-button type="primary" @click="generateReport">生成报道</el-button>
          <el-button @click="polishReport">润色报道</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 生成的报道预览 弹窗 -->
    <el-dialog
        v-model:visible="dialogVisible"
        title="生成的报道"
        @close="resetForm"
        width="50%"
    >
      <div v-if="generatedReport">
        <p><strong>标题：</strong>{{ generatedReport.title }}</p>
        <p><strong>标签：</strong>{{ generatedReport.tags.join(', ') }}</p>
        <p><strong>内容：</strong>{{ generatedReport.content }}</p>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">关闭</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import {ref} from "vue";
import {ElForm, ElFormItem, ElInput, ElButton, ElTag, ElCard, ElDialog} from "element-plus";

export default {
  components: {
    ElForm,
    ElFormItem,
    ElInput,
    ElButton,
    ElTag,
    ElCard,
    ElDialog,
  },
  setup() {
    const availableTags = [
      "文化", "科技", "教育", "公益", "环境", "健康", "经济", "体育", "艺术", "创新",
      "社会", "旅游", "历史", "政治", "法律", "军事", "生态", "企业", "金融", "城市"
    ]; // 预定义标签
    const report = ref({
      title: "",
      content: "",
      tags: [],
    });
    const selectedTags = ref([]); // 选中的标签
    const generatedReport = ref(null);
    const dialogVisible = ref(false); // 控制弹窗的显示

    // 检查标签是否已选中
    const isTagSelected = (tag) => selectedTags.value.includes(tag);

    // 切换标签选中状态
    const toggleTagSelection = (tag) => {
      if (isTagSelected(tag)) {
        removeTag(tag);
      } else {
        selectedTags.value.push(tag);
      }
    };

    // 移除标签
    const removeTag = (tag) => {
      const index = selectedTags.value.indexOf(tag);
      if (index !== -1) {
        selectedTags.value.splice(index, 1);
      }
    };

    // 生成报道
      const generateReport = () => {
      const form = this.$refs.form;
      dialogVisible.value = true; // 显示弹窗
      form.validate((valid) => {
        if (valid) {
          generatedReport.value = {...report.value, tags: selectedTags.value}; // 添加已选标签
          dialogVisible.value = true; // 显示弹窗
        } else {
          return false;
        }
      });
    };

    // 润色报道
    const polishReport = () => {
      if (generatedReport.value) {
        generatedReport.value.content = generatedReport.value.content.replace(
            /(.+)/,
            "经过进一步润色，内容变得更加生动和有吸引力：$1"
        );
        dialogVisible.value = true; // 显示弹窗
      }
    };

    // 重置表单
    const resetForm = () => {
      dialogVisible.value = false;
      report.value = {
        title: "",
        content: "",
        tags: [],
      };
      selectedTags.value = [];
    };

    return {
      availableTags,
      report,
      selectedTags,
      generatedReport,
      dialogVisible,
      generateReport,
      polishReport,
      isTagSelected,
      toggleTagSelection,
      removeTag,
      resetForm,
    };
  },
};
</script>

<style scoped>
.report-generation {
  max-width: 800px;
  margin: 30px auto;
}

.form-card {
  padding: 20px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.selected-tags {
  margin-top: 10px;
}

.selected-tag {
  margin-right: 8px;
  margin-bottom: 8px;
}

.available-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.tag-item {
  cursor: pointer;
}

.generated-report {
  margin-top: 30px;
  padding: 20px;
  border: 1px solid #dcdfe6;
  background-color: #f9f9f9;
}

.generated-report h3 {
  margin-top: 0;
}

.generated-report p {
  margin: 10px 0;
}
</style>

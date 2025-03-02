<template>
  <div class="report-generation">
    <el-card class="form-card">
      <h2>生成的报道</h2>
      <el-form :model="report" label-width="120px" class="form">
        <!-- 标题 -->
        <el-form-item label="标题">
          <el-input v-model="report.title" />
        </el-form-item>

        <!-- 内容 -->
        <el-form-item label="内容">
          <el-input type="textarea" v-model="report.content" rows="8" />
        </el-form-item>

        <!-- 活动名 -->
        <el-form-item label="活动名">
          <el-input v-model="report.eventName" />
        </el-form-item>

        <!-- 活动属性 -->
        <el-form-item label="活动属性">
          <el-input v-model="report.eventType" />
        </el-form-item>

        <!-- 宣传途径 -->
        <el-form-item label="宣传途径">
          <el-input v-model="report.promotionMethod" />
        </el-form-item>

        <!-- 发布日期 -->
        <el-form-item label="发布日期">
          <el-input v-model="report.publishDate" />
        </el-form-item>

        <!-- 报道类型 -->
        <el-form-item label="报道类型">
          <el-select v-model="report.reportType" placeholder="请选择">
            <el-option label="新闻报道" value="news" />
            <el-option label="专题报道" value="feature" />
            <el-option label="深度报道" value="deep" />
          </el-select>
        </el-form-item>

        <!-- 保存按钮 -->
        <el-form-item>
          <el-button type="primary" @click="saveReport">保存修改</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import { ref } from "vue";
import { ElForm, ElFormItem, ElInput, ElCard, ElButton, ElSelect, ElOption } from "element-plus";

export default {
  components: {
    ElForm,
    ElFormItem,
    ElInput,
    ElCard,
    ElButton,
    ElSelect,
    ElOption,
  },
  setup() {
    // 虚拟数据
    const report = ref({
      title: "关于2025年春季文化活动的报道",
      content:
          "2025年春季文化活动将在全国范围内开展，活动主题是“传承与创新”。本次活动将通过一系列的文化交流、展览展示、讲座和艺术表演等形式进行，目的是向公众传递中华优秀文化的精髓，促进文化的多元化与创新发展。\n\n活动还将邀请国内外专家学者，围绕文化产业、创意设计等方面进行深入探讨，并通过线上线下同步进行宣传和推广。",
      eventName: "春季文化活动",
      eventType: "文化活动",
      promotionMethod:
          "电视台直播、社交媒体平台（如微博、抖音等）、在线新闻网站、各大门户网站和报纸等多种渠道进行宣传。",
      publishDate: "2025-03-01",
      reportType: "news", // 默认新闻报道
    });

    // 保存修改
    const saveReport = () => {
      // 模拟保存操作
      console.log("修改后的报道内容:", report.value);
      alert("修改内容已保存！");
    };

    return {
      report,
      saveReport,
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

.el-form-item {
  margin-bottom: 20px;
}

.el-input {
  background-color: #f5f5f5;
}

.el-textarea {
  resize: vertical;
}
</style>

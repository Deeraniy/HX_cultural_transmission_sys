<template>
  <el-table :data="tableData" stripe border style="width: 100%;" height="700">
    <el-table-column prop="topic" label="主题" align="center">
      <template #default="scope">
        <span class="table-cell">{{ scope.row.topic }}</span>
      </template>
    </el-table-column>
    <el-table-column prop="frequency" label="频数" align="center">
      <template #default="scope">
        <span class="table-cell">{{ scope.row.frequency }}</span>
      </template>
    </el-table-column>
    <el-table-column prop="sentiment" label="情感倾向" align="center">
      <template #default="scope">
        <span :class="getClassForSentiment(scope.row.sentiment)">
          {{ translateSentiment(scope.row.sentiment) }}
        </span>
      </template>
    </el-table-column>
  </el-table>
</template>

<script setup>
import { defineProps } from 'vue'

const props = defineProps({
  tableData: {
    type: Array,
    required: true
  }
})

// 翻译情感倾向
const translateSentiment = (sentiment) => {
  switch (sentiment) {
    case 'positive':
      return '正面';
    case 'neutral':
      return '中立';
    case 'negative':
      return '负面';
    default:
      return sentiment;
  }
}

// 根据情感倾向返回对应的类名
const getClassForSentiment = (sentiment) => {
  switch (sentiment) {
    case 'positive':
      return 'positive';
    case 'neutral':
      return 'neutral';
    case 'negative':
      return 'negative';
    default:
      return '';
  }
}
</script>

<style scoped>
/* 表格整体样式 */
.el-table {
  background-color: #fafafa;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

/* 单元格样式 */
.table-cell {
  font-weight: 500;
  color: #333;
  font-size: 14px;
}

/* 情感倾向颜色 */
.positive {
  color: #67C23A; /* 绿色 */
  font-weight: bold;
}
.neutral {
  color: #E6A23C; /* 橙色 */
  font-weight: bold;
}
.negative {
  color: #F56C6C; /* 红色 */
  font-weight: bold;
}

/* 表头样式 */
.el-table th {
  background-color: #f3f4f6;
  color: #606266;
  font-size: 16px;
  font-weight: 600;
  text-align: center;
}

/* 分隔线样式 */
.el-table__header, .el-table__body {
  border-collapse: separate;
  border-spacing: 0 8px;
}

.el-table--striped .el-table__row--striped {
  background-color: #f9f9f9;
}

/* 表格行高亮效果 */
.el-table__row:hover {
  background-color: #e8f4ff;
}
.el-table__body-wrapper {
  overflow-y: hidden;
}
</style>

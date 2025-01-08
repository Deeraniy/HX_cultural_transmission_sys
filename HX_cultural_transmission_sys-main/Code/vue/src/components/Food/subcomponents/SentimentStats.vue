<template>
  <el-table :data="tableData" stripe border style="width: 100%;" height="500">
    <el-table-column prop="word" label="评价词" align="center">
      <template #default="scope">
        <span class="word-cell">{{ scope.row.word }}</span>
      </template>
    </el-table-column>
    <el-table-column prop="frequency" label="频数" align="center">
      <template #default="scope">
        <span class="frequency-cell">{{ scope.row.frequency }}</span>
      </template>
    </el-table-column>
    <el-table-column prop="sentiment" label="情感倾向" align="center">
      <template #default="scope">
        <span :class="scope.row.sentiment === '正面' ? 'positive' : scope.row.sentiment === '负面' ? 'negative' : 'neutral'">
          {{ scope.row.sentiment }}
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
.word-cell, .frequency-cell {
  font-weight: 500;
  color: #333;
  font-size: 14px;
}

/* 情感倾向颜色 */
.positive {
  color: #67C23A;
  font-weight: bold;
}
.negative {
  color: #F56C6C;
  font-weight: bold;
}
.neutral {
  color: #E6A23C;
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
</style>

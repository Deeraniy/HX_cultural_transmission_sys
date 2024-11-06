<template>
  <el-table :data="tableData">
    <el-table-column prop="theme" label="主题" ></el-table-column>
    <el-table-column prop="keyword" label="关键词" ></el-table-column>
    <el-table-column prop="frequency" label="频数"></el-table-column>
    <el-table-column prop="sentiment" label="情感倾向" >
      <template #default="scope">
        <span :class="getClassForSentiment(scope.row.sentiment)">{{ scope.row.sentiment }}</span>
      </template>
    </el-table-column>
  </el-table>
</template>

<script setup>
import { ref } from 'vue'
import { ElTable, ElTableColumn } from 'element-plus'
const props = defineProps({
  tableData: {
    type: Array,
    required: true
  }
})
/*
const tableData = ref([
  { theme: '景色', keyword: '美丽', frequency: 15, sentiment: '正面' },
  { theme: '交通', keyword: '方便', frequency: 13, sentiment: '中立' },
  // 更多行
])
*/

// 根据情感倾向返回对应的类名
const getClassForSentiment = (sentiment) => {
  switch (sentiment) {
    case '正面':
      return 'positive';
    case '中立':
      return 'neutral';
    case '负面':
      return 'negative';
    default:
      return '';
  }
}
</script>

<style scoped>
.positive {
  color: green;
}
.neutral {
  color: orange;
}
.negative {
  color: red;
}
</style>

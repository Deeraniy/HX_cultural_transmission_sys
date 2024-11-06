<template>
  <el-table :data="tableData" >
    <el-table-column prop="word" label="评价词" ></el-table-column>
    <el-table-column prop="frequency" label="频数" ></el-table-column>
    <el-table-column prop="sentiment" label="情感倾向" >
      <template #default="scope">
        <span :class="scope.row.sentiment === '正面' ? 'positive' : 'negative'">{{ scope.row.sentiment }}</span>
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

/*const tableData = ref([
  { word: '震撼', frequency: 102, sentiment: '正面' },
  { word: '美丽', frequency: 77, sentiment: '正面' },
  { word: '失望', frequency: 34, sentiment: '负面' },
  { word: '满意', frequency: 89, sentiment: '正面' },
  { word: '糟糕', frequency: 23, sentiment: '负面' },
  { word: '完美', frequency: 120, sentiment: '正面' },
  { word: '一般', frequency: 65, sentiment: '中立' },
  { word: '差劲', frequency: 15, sentiment: '负面' },
  { word: '精彩', frequency: 95, sentiment: '正面' },
  { word: '无聊', frequency: 18, sentiment: '负面' },
  { word: '有趣', frequency: 70, sentiment: '正面' },
  { word: '失望透顶', frequency: 10, sentiment: '负面' },
  { word: '惊喜', frequency: 55, sentiment: '正面' },
  { word: '无语', frequency: 20, sentiment: '负面' },
  { word: '感动', frequency: 45, sentiment: '正面' },
  { word: '乏味', frequency: 12, sentiment: '负面' },
  { word: '惊艳', frequency: 110, sentiment: '正面' },
  { word: '糟糕透顶', frequency: 5, sentiment: '负面' },
  { word: '满意极了', frequency: 100, sentiment: '正面' },
  { word: '无法忍受', frequency: 8, sentiment: '负面' }
])*/
</script>

<style>
.positive {
  color: green;
}
.negative {
  color: red;
}
</style>

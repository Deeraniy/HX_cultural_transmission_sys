<template>
  <div class="whole">
    <div class="total">
      <!-- 固定显示的标题，不作为菜单项 -->
      <h2 class="fixed-title">非遗民俗分析界面</h2>

      <!-- 菜单区域 -->
      <el-menu
          :default-active="activeIndex"
          class="el-menu-demo"
          mode="horizontal"
          :ellipsis="false"
          @select="handleSelect"
      >
        <el-menu-item index="2">情感分析与预测</el-menu-item>
        <el-menu-item index="3">传播策略生成</el-menu-item>
        <el-menu-item index="4">风景名胜3D展示</el-menu-item>
        <el-menu-item index="5">社交分享信息展示</el-menu-item>
        <el-menu-item index="6">沉浸式故事叙述</el-menu-item>
        <el-sub-menu index="1">
          <template #title>
            <span class="work">工作台</span>
          </template>
          <el-menu-item index="1-1">item one</el-menu-item>
          <el-menu-item index="1-2">item two</el-menu-item>
          <el-menu-item index="1-3">item three</el-menu-item>
          <el-sub-menu index="1-4">
            <template #title>item four</template>
            <el-menu-item index="1-4-1">item one</el-menu-item>
            <el-menu-item index="1-4-2">item two</el-menu-item>
            <el-menu-item index="1-4-3">item three</el-menu-item>
          </el-sub-menu>
        </el-sub-menu>
      </el-menu>
    </div>
    <el-main>
      <img src="@/assets/folkCustom/湖湘非遗.png" style="width: 100%;height: 500px;opacity: 0.6;"/>

      <div id="table" >
        <div style=" color: #333; white-space: pre-wrap;">
          <p style="text-align: center">
            城市传播指数

            <br/>
            Urban Communication Index
          </p>
          &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;该模块主要通过跟踪各个城市在国外社交媒体的官方账号所发布的信息（包括视频、文章的阅读转发点赞等数据），从而通过这些信息用特定的方法计算出一个可以反映该城市在国际上传播的效果和影响力的指数。
          This module mainly tracks the information published by each city's official accounts on foreign social media (including videos, tweetss, reads, forwards, likes, etc.), so as to calculate an index that can reflect the city's international communication effect and influence through this information.

        </div>
      <el-table :data="paginatedData" border style="width: 100%;">
        <el-table-column prop="id" label="ID" width="180" />
        <el-table-column prop="img" label="PIC" width="180">
          <template #default="scope">
            <img :src="scope.row.img" alt="image" style="width: 100px; height: auto;" />
          </template>
        </el-table-column>
        <el-table-column prop="name" label="民俗" />
        <el-table-column prop="internationalIndex" sortable label="国际传播系数" />
        <el-table-column prop="externalPromotion" sortable label="对外宣传报道力度" />
        <el-table-column prop="socialMediaScore" sortable label="社交媒体综合评分" />
      </el-table>
      <el-pagination
          v-model:current-page="currentPage3"
          v-model:page-size="pageSize3"
          :size="size"
          :disabled="disabled"
          :background="background"
          layout="prev, pager, next, jumper"
          :total="1000"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          style="margin-left: 500px"
      />
      </div>
    </el-main>
  </div>


</template>

<script lang="ts" setup>
import {ref, onMounted, computed} from 'vue'
import FolkCustom from './FolkCustom.vue'
const activeIndex = ref('2')
const handleSelect = (key: string, keyPath: string[]) => {
  console.log(key, keyPath)
}
import { h } from 'vue'
import type { VNode } from 'vue'
import type {ComponentSize, TableColumnCtx} from 'element-plus'

interface Product {
  id: string
  name: string
  amount1: string
  amount2: string
  amount3: number
}

interface SummaryMethodProps<T = Product> {
  columns: TableColumnCtx<T>[]
  data: T[]
}
const background = ref(false)
const disabled = ref(false)
const currentPage3 = ref(5)
const pageSize3 = ref(15)
const size = ref<ComponentSize>('default')

const paginatedData = computed(() => {
  const start = (currentPage3.value - 1) * pageSize3.value
  const end = currentPage3.value * pageSize3.value
  return tableData.value.slice(start, end)
})


const handleSizeChange = (val: number) => {
  console.log(`${val} items per page`)
}
const handleCurrentChange = (val: number) => {
  console.log(`current page: ${val}`)
}
const getSummaries = (param: SummaryMethodProps) => {
  const { columns, data } = param
  const sums: (string | VNode)[] = []
  columns.forEach((column, index) => {
    if (index === 0) {
      sums[index] = h('div', { style: { textDecoration: 'underline' } }, [
        'Total Cost',
      ])
      return
    }
    const values = data.map((item) => Number(item[column.property]))
    if (!values.every((value) => Number.isNaN(value))) {
      sums[index] = `$ ${values.reduce((prev, curr) => {
        const value = Number(curr)
        if (!Number.isNaN(value)) {
          return prev + curr
        } else {
          return prev
        }
      }, 0)}`
    } else {
      sums[index] = 'N/A'
    }
  })

  return sums
}

const tableData = ref([
  {
    id: "1",
    img: "https://puui.qpic.cn/vpic_cover/x3352jeglqz/x3352jeglqz_hz.jpg/1280", // 替换为真实图片 URL
    name: "花鼓戏",
    internationalIndex: 82.5,
    externalPromotion: 78.6,
    socialMediaScore: 89.2,
  },
  {
    id: "2",
    img: "https://th.bing.com/th/id/OIP.8a5pb-c-kJ4ffFT46wkKKgHaEK?w=277&h=180&c=7&r=0&o=5&dpr=1.4&pid=1.7",
    name: "赶尸",
    internationalIndex: 65.3,
    externalPromotion: 72.1,
    socialMediaScore: 74.9,
  },
  {
    id: "3",
    img: "https://via.placeholder.com/100",
    name: "湘剧",
    internationalIndex: 79.1,
    externalPromotion: 75.3,
    socialMediaScore: 81.4,
  },
  {
    id: "4",
    img: "https://via.placeholder.com/100",
    name: "湘绣",
    internationalIndex: 85.7,
    externalPromotion: 80.4,
    socialMediaScore: 90.1,
  },
  {
    id: "5",
    img: "https://via.placeholder.com/100",
    name: "龙舟竞渡",
    internationalIndex: 70.8,
    externalPromotion: 74.5,
    socialMediaScore: 78.6,
  },
])
</script>

<style lang="scss" scoped>
@import '@/assets/font/font.css';
.el-table {
  --el-table-border-color: transparent;
  --el-table-border: none;
  --el-table-text-color: #fffffff;
  --el-table-header-text-color: #fffffff;
  --el-table-row-hover-bg-color: transparent;
  --el-table-current-row-bg-color: transparent;
  --el-table-header-bg-color: transparent;
  --el-table-bg-color: transparent;
  --el-table-tr-bg-color: transparent;
  --el-table-expanded-cell-bg-color: transparent;
}
#table {
  background-image: url('@/assets/纹理5.jpg');
}
.total{
  background-image: url('@/assets/img_4.png');
  background-size: cover;
  background-position: center;
  border-bottom-left-radius: 30px; /* 左下圆角 */
  border-bottom-right-radius: 30px; /* 右下圆角 */
}
.whole{
  background-image: url('@/assets/img2.png');
  background-color: #fff8f0;
  background-size: cover;
  background-position: center;
}
.el-main {
  padding: 0;
}
/* 固定标题样式 */
.fixed-title {
  color: #fff8f0;
  font-family: 'HelveticaNeue', serif;
  font-size: 45px;
  margin: 0 16px;
}

/* 菜单样式 */
.el-menu-demo {
  display: flex; /* 使用 flex 布局 */
  justify-content: flex-end;   /* 菜单项靠右对齐 */
  background-color: transparent !important; /* 将菜单背景设为透明 */
  box-shadow: none; /* 移除默认阴影（如果有的话） */
  padding-right: 20px;
  border-bottom-left-radius: 30px; /* 左下圆角 */
  border-bottom-right-radius: 30px; /* 右下圆角 */
  box-shadow: none;
}

/* 覆盖菜单项文字样式 */
.el-menu-item {
  color: #fff8f0 !important;
  font-size: 20px;
  font-family: 'HelveticaNeue', serif !important;
}

/* 选中和悬停菜单项的颜色和背景 */
.el-menu-item.is-active,
.el-menu-item:hover {
  color: #ffd700 !important; /* 设置选中和悬停状态的文字颜色为金色 */
  background-color: rgba(255, 255, 255, 0.2) !important; /* 透明度为20%的淡色背景 */
  border-bottom: 2px solid #ffd700; /* 添加选中和悬停菜单项的下边框 */
}

/* 覆盖“工作台”标题样式 */
.el-sub-menu >>> .el-sub-menu__title {
  color: #fff8f0 !important;
  font-family: 'HelveticaNeue', serif !important;
}

/* 子菜单的悬停和选中样式 */
.el-sub-menu__title:hover,
.el-sub-menu__title.is-active {
  color: #ffd700 !important;
  background-color: rgba(255, 255, 255, 0.2) !important;
}
</style>

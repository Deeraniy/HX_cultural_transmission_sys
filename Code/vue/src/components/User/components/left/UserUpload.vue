<script setup lang="ts">
import { ref,onMounted } from "vue";
import { Upload } from "@element-plus/icons-vue";

const searchNode1 = ref(""); // 搜索框绑定的值
const searchNode2 = ref(""); // 搜索框绑定的值
const searchSuggestions = ref([
  "节点A",
  "节点B",
  "节点C",
  "节点D",

]); // 模拟的节点数据
const state = ref("");
const state1 = ref("");
interface LinkItem {
  value: string
  link: string
}

const links = ref<LinkItem[]>([])

const loadAll = () => {
  return [
    { value: 'vue', link: 'https://github.com/vuejs/vue' },
    { value: 'element', link: 'https://github.com/ElemeFE/element' },
    { value: 'cooking', link: 'https://github.com/ElemeFE/cooking' },
    { value: 'mint-ui', link: 'https://github.com/ElemeFE/mint-ui' },
    { value: 'vuex', link: 'https://github.com/vuejs/vuex' },
    { value: 'vue-router', link: 'https://github.com/vuejs/vue-router' },
    { value: 'babel', link: 'https://github.com/babel/babel' },
  ]
}

let timeout: ReturnType<typeof setTimeout>
const querySearchAsync = (queryString: string, cb: (arg: any) => void) => {
  const results = queryString
      ? links.value.filter(createFilter(queryString))
      : links.value

  clearTimeout(timeout)
  timeout = setTimeout(() => {
    cb(results)
  }, 3000 * Math.random())
}
const createFilter = (queryString: string) => {
  return (restaurant: LinkItem) => {
    return (
        restaurant.value.toLowerCase().indexOf(queryString.toLowerCase()) === 0
    )
  }
}

const handleSelect = (item: Record<string, any>) => {
  console.log(item)
}

onMounted(() => {
  links.value = loadAll()
})
</script>

<template>
  <div>
    <div>
      <el-icon style="font-size: 20px"><Upload /></el-icon>
      <el-text class="mainTitle">关系上传</el-text>
    </div>

    <!-- 选择第一个节点 -->
    <div>
      <el-autocomplete
          v-model="state"
          :fetch-suggestions="querySearchAsync"
          placeholder="Please input"
          @select="handleSelect"
      />
    </div>

    <div style="margin-top: 50px">
      <el-input
          v-model="textarea"
          style="width: 240px"
          :rows="2"
          type="textarea"
          placeholder="输入两者关系"
      />
    </div>

    <!-- 选择第二个节点 -->
    <div style="margin-top: 50px">
      <el-autocomplete
          v-model="state1"
          :fetch-suggestions="querySearchAsync"
          placeholder="节点2"
          @select="handleSelect"
      />
    </div>

    <div style="margin-top: 50px">
      <el-button type="success">提交</el-button>
    </div>
  </div>
</template>

<style scoped>
.mainTitle {
  margin-left: 30px;
  font-size: 18px;
  color: #000;
  font-weight: bolder;
}
</style>

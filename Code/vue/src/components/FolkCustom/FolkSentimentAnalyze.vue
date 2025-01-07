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
      <div style="display: flex;height: 100% ">
        <div style="flex-grow: 1; justify-content: center; align-items: center;width: 100%">
          <div>
            我是文化作品名称
          </div>

          <div class="评分图">
            <div>
              我是评分图
            </div>
            <div>


            </div>

          </div>
          <div class="词云图">
            <div>
              我是词云图
            </div>
            <div>


            </div>

          </div>
          <div class="情感占比图">
            <div>
              我是情感占比图
            </div>
            <div>


            </div>

          </div>
          <div class="情感变化趋势图">
            <div>
              我是情感变化趋势图
            </div>
            <div>


            </div>

          </div>
          <div class="情感变化趋势图">
            <div>
              我是情感变化趋势图
            </div>
            <div>


            </div>

          </div>









        </div>
        <div style="flex-grow: 1; display: flex; justify-content: flex-end; align-items: center;width: 500px">
<!--          轮盘菜单-->
          <div style="border-top-left-radius: 1000px; border-bottom-left-radius: 1000px; position: relative; display: flex; flex-direction: column; align-items: flex-end; margin-top: 10px; width: 300px; background-image: url(src/assets/folkCustom/纹理6.jpg);">
            <div style="margin-bottom: 15px; text-align: right; margin-right: 5px;">
              <img src="@/assets/folkCustom/用户趋势.png" alt="" style="width: 40px; height: 40px;"/>
              <p style="margin: 5px 0 0; font-size: 14px; color: #333;">菜单1</p>
            </div>
            <div style="margin-bottom: 15px; text-align: right; margin-right: 100px;">
              <img src="@/assets/folkCustom/服务评分模板.png" alt="" style="width: 40px; height: 40px;"/>
              <p style="margin: 5px 0 0; font-size: 14px; color: #333;">菜单2</p>
            </div>
            <div style="margin-bottom: 15px; text-align: right; margin-right: 200px;">
              <img src="@/assets/folkCustom/智能分析＊.png" alt="" style="width: 40px; height: 40px;"/>
              <p style="margin: 5px 0 0; font-size: 14px; color: #333;">菜单3</p>
            </div>
            <div style="margin-bottom: 15px; text-align: right; margin-right: 200px; margin-top: 30px;">
              <img src="@/assets/folkCustom/词云图.png" alt="" style="width: 40px; height: 40px;"/>
              <p style="margin: 5px 0 0; font-size: 14px; color: #333;">菜单4</p>
            </div>
            <div style="margin-bottom: 15px; text-align: right; margin-right: 100px; margin-top: 20px;">
              <img src="@/assets/folkCustom/饼图.png" alt="" style="width: 40px; height: 40px;"/>
              <p style="margin: 5px 0 0; font-size: 14px; color: #333;">菜单5</p>
            </div>
            <div style="margin-bottom: 15px; text-align: right; margin-right: 5px;">
              <img src="@/assets/folkCustom/评论.png" alt="" style="width: 40px; height: 40px;"/>
              <p style="margin: 5px 0 0; font-size: 14px; color: #333;">菜单6</p>
            </div>
          </div>
        </div>
      </div>
    </el-main>
  </div>


</template>

<script lang="ts" setup>
import { ref,onMounted } from 'vue'
import FolkCustom from './FolkCustom.vue'
const activeIndex = ref('2')
const handleSelect = (key: string, keyPath: string[]) => {
  console.log(key, keyPath)
}
</script>

<style scoped>
@import '@/assets/font/font.css';
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

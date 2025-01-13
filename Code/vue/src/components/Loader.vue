<template>
  <div class="loader-overlay">
    <div class="intro">
      <div class="box">
        <!-- 单个猫元素 -->
        <div class="cat"></div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Loader',
};
</script>

<style scoped lang="scss">
@keyframes rotating {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(-360deg); /* 改为负数，表示逆时针旋转 */
  }
}

.loader-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

.intro {
  width: 90%;
  max-width: 36rem;
  padding-bottom: 1rem;
  margin: 0 auto 1em;
  padding-top: .5em;
  font-size: calc(1rem + 2vmin);
  text-transform: capitalize;
  text-align: center;
}

.box {
  position: relative;
  width: 100%;
  max-width: 12em; /* 控制猫猫的最大宽度 */
  overflow: visible; /* 防止裁剪 */
  display: flex;
  justify-content: center;
  align-items: center;
}

.cat {
  position: relative;
  width: 100px; /* 控制猫的宽度 */
  height: 100px; /* 控制猫的高度 */
  background-image: url('@/assets/load.png'); /* 替换为你的猫的图片路径 */
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
  animation: rotating 2s linear infinite; /* 添加旋转动画 */
}
</style>

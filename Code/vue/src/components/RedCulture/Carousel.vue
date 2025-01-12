<template>
  <div class="app">
    <!-- 轮播图 -->
    <Slider :slides="slides" />
    <!-- 分页按钮 -->
    <div class="pagination">
      <button @click="prevPage" :disabled="currentPage === 0">上一页</button>
      <button @click="nextPage" :disabled="currentPage === totalPages - 1">下一页</button>
    </div>
    <!-- 第二排图片 -->
    <div class="images-leaning">
      <div v-for="(image, index) in currentImages" :key="index" :style="getImageStyle(index)">
        <img :src="image.src" :alt="image.title" />
      </div>
      <p class="quote">可以强天下而保中国者，莫湘人若也</p>
    </div>
  </div>
</template>

<script>
import Slider from './Slider.vue';
import 任弼时 from '@/assets/Red/任弼时.jpg';
import 何叔衡 from '@/assets/Red/何叔衡.jpg';
import 刘少奇 from '@/assets/Red/刘少奇.jpg';
import 向警予 from '@/assets/Red/向警予.jpg';
import 彭德怀 from '@/assets/Red/彭德怀.jpg';
import 林伯渠 from '@/assets/Red/林伯渠.jpg';
import 毛泽东 from '@/assets/Red/毛泽东.jpg';
import 罗荣桓 from '@/assets/Red/罗荣桓.jpg';
import 贺龙 from '@/assets/Red/贺龙.jpg';
import 雷锋 from '@/assets/Red/雷锋.jpg';

export default {
  components: { Slider },
  data() {
    return {
      // 轮播图的图片内容
      slides: [
        { image: 任弼时, title: '任弼时' },
        { image: 何叔衡, title: '何叔衡' },
        { image: 刘少奇, title: '刘少奇' },
        { image: 向警予, title: '向警予' },
        { image: 彭德怀, title: '彭德怀' }
      ],
      // 所有图片资源
      allImages: [
        { src: 任弼时, title: '任弼时' },
        { src: 何叔衡, title: '何叔衡' },
        { src: 刘少奇, title: '刘少奇' },
        { src: 向警予, title: '向警予' },
        { src: 彭德怀, title: '彭德怀' },
        { src: 林伯渠, title: '林伯渠' },
        { src: 毛泽东, title: '毛泽东' },
        { src: 罗荣桓, title: '罗荣桓' },
        { src: 贺龙, title: '贺龙' },
        { src: 雷锋, title: '雷锋' }
      ],
      currentPage: 0, // 当前页
      pageSize: 5 // 每页显示五个
    };
  },
  computed: {
    // 计算当前页应该显示的图片
    currentImages() {
      const startIndex = this.currentPage * this.pageSize;
      return this.allImages.slice(startIndex, startIndex + this.pageSize);
    },
    // 计算总页数
    totalPages() {
      return Math.ceil(this.allImages.length / this.pageSize);
    }
  },
  methods: {
    // 更新轮播图的内容
    updateSlides() {
      const startIndex = this.currentPage * this.pageSize;
      const imagesForPage = this.allImages.slice(startIndex, startIndex + this.pageSize);

      this.slides = imagesForPage.map(image => ({
        image: image.src,
        title: image.title
      }));
    },
    // 计算图片样式
    getImageStyle(index) {
      const resizeValues = [0.895, 0.925, 0.96, 0.99, 0.92];
      const translateValues = [
        [-15.6, -8.0],
        [-19.6, -3.8],
        [-9, -1.9],
        [0, 0],
        [5, -5.8]
      ];

      const resize = resizeValues[index % resizeValues.length];
      const translate = translateValues[index % translateValues.length];

      return {
        '--resize': resize,
        transform: `scaleY(${resize}) translate(${translate[0]}em, ${translate[1]}em)`
      };
    },
    prevPage() {
      console.log('点击上一页前的当前页:', this.currentPage); // 输出当前页码
      if (this.currentPage > 0) {
        this.currentPage--; // 减少页码
        console.log('点击上一页后的当前页:', this.currentPage); // 输出更新后的页码
        this.updateSlides(); // 更新 slides 内容
      } else {
        console.log('当前已经是第一页，无法再上一页'); // 如果当前页是第一页，输出日志
      }
    },
    nextPage() {
      console.log('点击下一页前的当前页:', this.currentPage); // 输出当前页码
      if (this.currentPage < this.totalPages - 1) {
        this.currentPage++; // 增加页码
        console.log('点击下一页后的当前页:', this.currentPage); // 输出更新后的页码
        this.updateSlides(); // 更新 slides 内容
      } else {
        console.log('当前已经是最后一页，无法再下一页'); // 如果当前页是最后一页，输出日志
      }
    }
  },
  watch: {
    // 每次页面切换时，更新 slides 内容
    currentPage() {
      this.updateSlides();
    }
  }
};
</script>


<style>
@import '@/assets/font/font.css';
.app {
  display: flex;
  flex-direction: column;
  align-items: center;
}

/* 第二排图片摆放样式 */
.images-leaning {
  box-sizing: border-box;
  width: 100%;
  min-width: 800px;
  margin: 10em auto 0;
  min-height: 330px;
  position: relative;
  background-repeat: no-repeat;
  background-image: linear-gradient(352.9deg, transparent 0%, #bbbbbb 0%, #F7F7F7 45.6%, transparent 45.8%, transparent 100%),
  linear-gradient(30deg, transparent, transparent 100%);
  background-size: 100% 32.4em;
  background-position: 50% 100%;
}

.images-leaning > div {
  width: 250px;
  position: absolute;
  left: 50%;
  bottom: 8em;
  z-index: 0;
  display: flex;
  justify-content: flex-end;
}

/* 伪元素的阴影效果 */
.images-leaning > div::before {
  content: '';
  width: 60%;
  height: 100%;
  position: absolute;
  left: 0;
  top: 7%;
  z-index: 1;
  background-repeat: no-repeat;

  /* 裁剪 + 下移的渐变背景 */
  background-image:
      linear-gradient(
          120deg,
          transparent 42%,
          rgba(0, 0, 0, 0.15) 50%,
          rgba(0, 0, 0, 0.35) 60% /* 调整停止点裁掉底部 */
      );

  /* 下移整体背景 */
  background-position: 0 10px; /* 下移整个背景图 10px */
  background-size: 100% calc(100% - 50px); /* 裁掉底部 10px */

  transform: rotate(-8deg);
  filter: blur(2px); /* 使阴影更模糊 */
  opacity: 0.5; /* 调整阴影透明度 */
}


/* 添加投影遮罩效果 */
.images-leaning > div::after {
  content: '';
  width: 60%;
  height: 100%;
  position: absolute;
  z-index: 3;
  background-image: linear-gradient(45deg, rgba(0, 0, 0, 0.3), transparent 70%),
  linear-gradient(45deg, rgba(255, 255, 255, 0) 60%, rgba(255, 255, 255, 0.3) 80%);
  transform: perspective(20em) rotateY(1deg) rotateZ(-5deg) skewY(-2deg) skewX(-1deg) scaleX(var(--resize));
  filter: blur(3px); /* 使遮罩效果更平滑 */
  opacity: 0.7; /* 遮罩的透明度 */
}
.images-leaning > div::after {
  content: '';
  position: absolute;
  width: 0;
  height: 0;
  bottom: -10px; /* 将阴影放置在书本底部 */
  left: 50%; /* 让阴影居中 */
  transform: translateX(-50%); /* 阴影位置居中对齐 */
  border-left: 100px solid transparent; /* 左边透明 */
  border-right: 90px solid transparent; /* 右边透明 */
  border-top: 40px solid rgba(0, 0, 0, 0.1); /* 顶部为阴影的颜色 */
  filter: blur(5px); /* 添加模糊效果 */
  z-index: -1; /* 确保阴影在书本下方 */
  opacity: 0.7; /* 阴影透明度 */
}

/* 图片的基本样式 */
.images-leaning > div > img {
  width: 60%;
  height: 100%;
  display: block;
  position: relative;
  z-index: 2;
  border-left: 0.2em solid;
  border-image: linear-gradient(105deg, transparent 0.5%, #aaa 0.7%) 1;
  box-shadow: 0.1em 0.2em 0 -0.1em #666;
  filter: saturate(90%);
  transform: perspective(20em) rotateY(1deg) rotateZ(-5deg) skewY(-2deg) skewX(-1deg) scaleX(var(--resize));
}

/* 针对不同图像的大小和位置 */
.images-leaning > div:nth-of-type(4) {
  --resize: 0.99;
  margin-left: -40.4em;
}

.images-leaning > div:nth-of-type(3) {
  --resize: 0.96;
  margin-left: -15.3em;
  transform: scaleY(0.980) translate(-8em, -2.2em);
}

.images-leaning > div:nth-of-type(2) {
  --resize: 0.925;
  margin-left: 10em;
  transform: scaleY(0.965) translate(-17em, -4.6em);
}

.images-leaning > div:nth-of-type(1) {
  --resize: 0.895;
  margin-left: 35.2em;
  transform: scaleY(0.94) translate(-20.6em, -6.9em);
}

/* 基本图片排布样式 */
.images-basic {
  width: 600px;
  padding: 5em 0;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  flex-direction: row-reverse;
}

.images-basic > div {
  width: 130px;
}

.images-basic img {
  width: 100%;
  display: block;
}
/* 去掉阴影和改善按钮样式 */
/* 调整按钮为右下角 */
.pagination {

  display: flex;
  gap: 10px;
  transform: translate(-10vw, 5vh); /* 用 transform 进行右下角偏移 */
  z-index: 999; /* 确保按钮层级足够高 */
  pointer-events: auto; /* 确保按钮可以响应点击 */
}

.pagination button {
  padding: 8px 16px;
  font-size: 16px;
  color: #fff;
  background-color: #b71c1c; /* 按钮背景色 */
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: all 0.3s ease;

}

.pagination button:hover {
  background-color: #ce8483; /* 鼠标悬停时的背景色 */
}

.pagination button:disabled {
  background-color: #ce8483; /* 禁用时的背景色 */
  cursor: not-allowed;
}
/* 修改 quote 的样式 */
.quote {
  position: absolute; /* 设置绝对定位 */
  top: 130px; /* 距离顶部 20px */
  left: 70%; /* 水平居中 */
  z-index: 1000; /* 确保它显示在其他元素上面 */
  font-family: 'Arial', sans-serif;
  font-size: 50px;
  color: #fff; /* 金色字体 */
  text-align: center;
  font-family: 'HelveticaNeue',serif;
}

</style>

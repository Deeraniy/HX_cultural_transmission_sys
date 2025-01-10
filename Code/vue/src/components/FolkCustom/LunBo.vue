<template>
  <div class="carousel" @mouseenter="stopAutoPlay" @mouseleave="startAutoPlay">
    <!-- 图片和文字轮播 -->
    <div class="carousel-inner" :style="{ transform: `translateX(-${currentIndex * 100}%)` }">
      <div class="carousel-item" v-for="(image, index) in images" :key="index">
        <div class="content">
          <!-- 文字描述在左边 -->
          <div class="text-container" :class="{'special-text': image.isSpecial}">
            <h2>{{ image.title }}</h2>
            <p>{{ image.description }}</p>
          </div>
          <!-- 图片在右边 -->
          <div class="image-container">
            <img :src="image.src" class="main-image" :alt="image.alt" :style="image.style" />
          </div>
        </div>
        <!-- 底部圆形图像 -->
        <div class="circle-image-container">
          <img :src="image.circleImage" class="circle-image" :alt="`circle-${index}`" />
        </div>
      </div>
    </div>

    <!-- 底部导航点 -->
    <div class="carousel-dots">
      <span
          v-for="(image, index) in images"
          :key="index"
          :class="{ active: index === currentIndex }"
          @click="switchTo(index)"
      ></span>
    </div>

    <!-- 左右箭头 -->
    <div class="carousel-arrows">
      <span class="arrow left" @click="prevImage">&lt;</span>
      <span class="arrow right" @click="nextImage">&gt;</span>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from "vue";
import dragon from "@/assets/folkCustom/dragon.png";
import boat from "@/assets/folkCustom/boat.png";
import tiger from "@/assets/folkCustom/tiger.png";

// 添加底部圆形图像路径
import dragonCircle from "@/assets/folkCustom/dragon-back(1).png";
import boatCircle from "@/assets/folkCustom/boat-back.png";
import tigerCircle from "@/assets/folkCustom/tiger-back.png";

// 图片及文字内容，添加style字段来设置每张图片的大小
const images = [
  {
    src: dragon,
    alt: "龙舞（城步吊龙）",
    title: "龙舞（城步吊龙）",
    description:
        "龙舞（城步吊龙），湖南省城步苗族自治县传统舞蹈，国家级非物质文化遗产之一。 \n" +
        "流传于湖南省城步县丹口镇下团村的吊龙是一种道具制作和表演方法独特的龙舞：先用数根长、短竹片扁担和红绳分别制成“小吊”“中吊”，再将小吊挂在中吊上，将篾扎布裱的龙节吊在小吊上，然后再用一根横起的长扁担和高2米的竹竿制成“大提”将其吊起，共制成六组。舞时将龙头和龙节连缀，每位舞者高举竹竿，在打击乐的伴奏下，由舞龙珠者引领起舞，犹如“龙”在云中盘旋，场面蔚为壮观。\n" +
        "2011年龙舞（城步吊龙）经中华人民共和国国务院批准列入第三批国家级非物质文化遗产名录，遗产编号：Ⅲ-4。",
    style: {
      width: "100%", // 设置这张图片的宽度为100%
      height: "100%", // 设置这张图片的高度为100%
      transform: "translateY(-30px)", // 图片向上偏移20px
    },
    circleImage: dragonCircle, // 圆形图片路径
  },
  {
    src: boat,
    alt: "端午节（汨罗江畔端午习俗）",
    title: "汨罗江畔端午习俗",
    description:
        "端午节（汨罗江畔端午习俗），湖南省岳阳市汨罗市民俗，国家级非物质文化遗产名录之一。\n" +
        "端午节（汨罗江畔端午习俗）从农历五月初一开始，十五结束。端午节（汨罗江畔端午习俗）主要流行于汨罗江边楚塘、渔街、凤凰山、河市、归义、红花、新市、浯口、长乐等一带。\n" +
        "2006年5月20日，湖南省汨罗市申报的端午节（汨罗江畔端午习俗）经中华人民共和国国务院批准列入第一批国家级非物质文化遗产名录。遗产编号：Ⅹ-3。 2009年9月30日，“汨罗江畔端午习俗”作为端午节的重要组成部分，被列入联合国教科文组织人类非物质文化遗产代表作名录。",
    style: {
      width: "100%", // 设置这张图片的宽度为90%
      height: "100%" ,// 设置这张图片的高度为80%
      transform: "translateY(-30px)", // 图片向上偏移20px
    },
    circleImage: boatCircle, // 圆形图片路径
  },
  {
    src: tiger,
    alt: "湘绣",
    title: "湘绣",
    description:
        "湘绣，湖南省长沙市特产，中国国家地理标志产品。\n" +
        "湘绣是中国四大名绣之一，是以湖南长沙为中心的带有鲜明湘楚文化特色的湖南刺绣产品的总称，它起源于湖南的民间刺绣，吸取了苏绣和粤绣的优点而发展起来，已经有2000多年历史。 \n" +
        "19世纪末，绣工胡莲仙的儿子吴汉臣在长沙开设第一家自绣自销的“吴彩霞绣坊”，在湖南民间刺绣基础上吸收“苏绣”、“广绣”之优点，渐渐湘绣针法以参针为其特色。“参针”也称“乱插针”，与齐针相对应。可表现物象的立体形态和晕染效果。湘绣的风格是形象生动逼真、色彩丰富鲜艳、十分强调用色的阴阳浓淡、针法多变、劈线细致，绣工讲究“绣花能生香、绣鸟能听声、绣虎能奔跑，绣人能传神”。\n" +
        "湘绣以着色富于层次、绣品若画为特点，民间有苏猫、湘虎之说。湘绣狮虎毛纹刚健直竖，眼球有神，几可乱真，已发展到异色、异形、异面的双面全异绣。湘绣先后参加过日本、巴拿马、美国等地举办的国际博览会，多次获得优胜奖，在国际市场上享有盛誉。 \n" +
        "2011年3月28日，原国家质检总局批准对“湘绣”实施地理标志产品保护。",
    style: {
      width: "95%", // 设置这张图片的宽度为85%
      height: "95%", // 设置这张图片的高度为75%
      transform: "translateY(60px) translateX(80px)", // 图片向上偏移20px
    },
    circleImage: tigerCircle, // 圆形图片路径
    isSpecial: true,  // 新增字段，用来标记湘绣
  },
];

const currentIndex = ref(0);
let timer = null;

const switchTo = (index) => {
  currentIndex.value = index;
};
const nextImage = () => {
  currentIndex.value = (currentIndex.value + 1) % images.length;
};
const prevImage = () => {
  currentIndex.value = (currentIndex.value - 1 + images.length) % images.length;
};
const startAutoPlay = () => {
  timer = setInterval(nextImage, 3000);
};
const stopAutoPlay = () => {
  clearInterval(timer);
};

onMounted(() => startAutoPlay());
onUnmounted(() => stopAutoPlay());
</script>

<style scoped>
@import '@/assets/font/font.css';
.carousel {
  position: relative;
  width: 100%;
  height: 550px;
  overflow: hidden;
  border-radius: 10px;
}

.carousel-inner {
  display: flex;
  transition: transform 0.5s ease-in-out;
}

.carousel-item {
  flex: 0 0 100%;
  position: relative;
  display: flex;
  align-items: center;
}

.content {
  display: flex;
  justify-content: space-between;
  width: 100%;
}

.text-container {
  width: 30%; /* 文字部分占45% */
  padding: 20px;
  color: black; /* 文字颜色为黑色 */
  text-align: center; /* 将文字居中 */
  display: flex;
  flex-direction: column; /* 垂直排列 */
}

.text-container h2 {
  font-family: 'HelveticaNeue', serif;
margin-top: 0;
  margin-bottom: 0;
  font-size: 3rem;
}

.text-container p {
  font-family: 'HelveticaNeue', serif;
  margin: 10px 0;
  font-size: 1.5rem;
}

.text-container.special-text {
  width: 60%; /* 湘绣文字部分的宽度增加到40% */
}
.image-container {
  width: 70%; /* 图片部分占50% */
  display: flex;
  justify-content: center;
  align-items: center;
}

.main-image {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.carousel-dots span {
  background-color: white;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  opacity: 0.5;
}

.carousel-dots .active {
  background-color: red;
  opacity: 1;
}

.carousel-arrows {
  position: absolute;
  top: 50%;
  left: 10px;
  right: 10px;
  display: flex;
  justify-content: space-between;
  transform: translateY(-50%);
  z-index: 1;
}

.arrow {
  font-size: 2rem;
  color: white;
  cursor: pointer;
}

.arrow:hover {
  color: red;
}

/* 底部圆形图像样式 */
.circle-image-container {
  position: absolute;
  left: 70%;

  top: 5%;
  transform: translateX(-50%);
  width: 500px;
  height: 500px;
  border-radius: 50%;
  z-index: -10;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
}

.circle-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
</style>

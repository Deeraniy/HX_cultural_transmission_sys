<template>
  <div class="slider">
    <!-- Previous Button -->
    <button class="slider--btn slider--btn__prev" @click="changeSlide(-1)">
      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="m15 18-6-6 6-6" />
      </svg>
    </button>

    <!-- Slides Wrapper -->
    <div class="slides__wrapper">
      <div
          v-for="(slide, index) in slides"
          :key="index"
          class="slide"
          :class="{
          'slide--current': currentSlide === index,
          'slide--previous': previousSlide === index,
          'slide--next': nextSlide === index,
        }"
          :style="{
          transform: getSlideTransform(index),
          zIndex: getZIndex(index),
        }"
      >
        <div class="slide__inner">
          <div class="slide--image__wrapper">
            <img class="slide--image" :src="slide.image" :alt="slide.title" />
          </div>
          <div class="slide--info">
            <h2 class="slide--title">{{ slide.title }}</h2>
            <h3 class="slide--subtitle">{{ slide.subtitle }}</h3>
            <p class="slide--description">{{ slide.description }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Next Button -->
    <button class="slider--btn slider--btn__next" @click="changeSlide(1)">
      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="m9 18 6-6-6-6" />
      </svg>
    </button>
  </div>
</template>

<script>
export default {
  name: "Slider",
  props: {
    slides: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      currentSlide: 0,
    };
  },
  computed: {
    previousSlide() {
      return (this.currentSlide - 1 + this.slides.length) % this.slides.length;
    },
    nextSlide() {
      return (this.currentSlide + 1) % this.slides.length;
    },
  },
  methods: {
    changeSlide(direction) {
      this.currentSlide = (this.currentSlide + direction + this.slides.length) % this.slides.length;
    },
    getSlideTransform(index) {
      if (index === this.currentSlide) {
        return "translateX(0) scale(1.2)";
      } else if (index === this.previousSlide) {
        return "translateX(-100%) rotateY(20deg) scale(0.8)";
      } else if (index === this.nextSlide) {
        return "translateX(100%) rotateY(-20deg) scale(0.8)";
      }
      return "translateX(200%) scale(0.6)";
    },
    getZIndex(index) {
      if (index === this.currentSlide) {
        return 3;
      } else if (index === this.previousSlide || index === this.nextSlide) {
        return 2;
      }
      return 1;
    },
  },
};
</script>

<style scoped>
.slider {
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  width: 80%;
  height: 500px;
  overflow: hidden;
}

.slider--btn {
  position: absolute;
  top: 50%;
  z-index: 10;
  background: none;
  border: none;
  cursor: pointer;
  transform: translateY(-50%);
  opacity: 0.6;
  transition: opacity 0.3s ease;
}

.slider--btn:hover {
  opacity: 1;
}

.slider--btn__prev {
  left: 10px;
}

.slider--btn__next {
  right: 10px;
}


.slides__wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 50%; /* 控制轮转图的宽度，可以调整 */
  height: 70%; /* 控制轮转图的高度，可以调整 */
  perspective: 1000px;
  position: relative;
}


.slide {
  position: absolute;
  top: 0;
  left: 0;
  width: 50%;
  height: 100%;
  transition: transform 0.8s ease, z-index 0.8s ease;
  transform-origin: center center;
  overflow: hidden;
  border-radius: 10px;
  background: #000;
  box-shadow: 0px 8px 15px rgba(0, 0, 0, 0.3);
}

.slide--image__wrapper {
  width: 100%;
  height: 100%;
  overflow: hidden;
  object-fit: cover; /* 确保图片填充，不被拉伸且保持比例 */
}

.slide--image {
  width: 100%;
  height: 100%;
  object-fit: cover; /* 确保图片填充，不被拉伸且保持比例 */
  transition: transform 0.8s ease;
}

.slide--info {
  position: absolute;
  bottom: 10%;
  left: 5%;
  color: white;
}

.slide--title {
  font-size: 1.5rem;
  margin: 0;
  font-weight: bold;
}

.slide--subtitle {
  font-size: 1.2rem;
  margin: 0;
}

.slide--description {
  font-size: 0.9rem;
  margin: 0;
}
</style>

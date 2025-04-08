<template>
  <div class="walk-modal">
    <!-- 点击背景关闭弹窗 -->
    <div class="overlay" @click="closeModal"></div>

    <!-- 弹窗内容 -->
    <div class="walk-container">
      <!-- 小人 -->
      <div
          ref="sprite"
          class="sprite"
          :class="{ 
            'walk-right': walkingRight, 
            'walk-left': walkingLeft,
            'stand-right': !walkingRight && !walkingLeft && !lastWalkingLeft,
            'stand-left': !walkingRight && !walkingLeft && lastWalkingLeft
          }"
          :style="{ left: `${spritePosition}px` }"
      >
        <!-- 气泡 -->
        <div v-if="showBubble" class="speech-bubble">
          {{ bubbleMessage }}
        </div>
      </div>

      <!-- 时间线 -->
      <div class="time-line-container" :style="{ left: `${-scrollPosition}px`, width: `${timeLine.length * nodeSpacing}px` }">
        <div
            v-for="(item, index) in timeLine"
            :key="index"
            class="time-node"
            :style="{ left: `${index * nodeSpacing}px` }"
        >
        <div class="circle"></div>
        <div class="label">{{ item.year }}</div>
      </div>
    </div>

    <!-- 当前事件信息 -->
    <div v-if="currentMessage" class="message-box">{{ currentMessage }}</div>

    <!-- 关闭按钮 -->
    <button @click="closeModal" class="close-btn">X</button>
  </div>
  </div>
</template>

<script>
import maoTimeLine from "@/json/毛泽东.json";

export default {
  name: "Walk",
  props: {
    human: Object, // 获取人物信息
  },
  data() {
    return {
      timeLine: maoTimeLine, // 时间节点数据
      nodeSpacing: 200, // 时间节点间距
      spritePosition: 0, // 小人当前位置
      scrollPosition: 0, // 时间线滚动位置
      stepSize: 10, // 小人移动步长
      containerWidth: 800, // 可视区域宽度
      currentMessage: "", // 当前显示的事件信息
      walkingRight: false, // 是否向右走
      walkingLeft: false, // 是否向左走
      lastWalkingLeft: false, // 上一次行走方向是否向左
      showBubble: false, // 是否显示气泡
      bubbleMessage: "", // 气泡内容
      randomTargetIndex: null, // 随机目标时间点的索引
      key: { left: false, right: false }, // 键盘左右方向
    };
  },
  mounted() {
    this.setRandomTarget(); // 设置随机目标时间点
    this.loadTimeLineData(); // 初始加载时间线
    window.addEventListener("keydown", this.handleKeyDown);
    window.addEventListener("keyup", this.handleKeyUp);
  },
  beforeDestroy() {
    window.removeEventListener("keydown", this.handleKeyDown);
    window.removeEventListener("keyup", this.handleKeyUp);
  },
  methods: {
    // 加载时间线数据
    async loadTimeLineData() {
      try {
        const timeLineModule = await import(`@/json/${this.human.name}.json`);
        this.timeLine = timeLineModule.default;
      } catch (error) {
        console.error("Failed to load time line data:", error);
      }
    },

    // 设置随机目标时间点
    setRandomTarget() {
      this.randomTargetIndex =10;
    },
    // 键盘按下事件
    handleKeyDown(event) {
      const key = event.key;

      if (key === "ArrowRight") {
        this.key.right = true;
        this.walkingRight = true;
        this.lastWalkingLeft = false;
        this.walkRight();
      }

      if (key === "ArrowLeft") {
        this.key.left = true;
        this.walkingLeft = true;
        this.lastWalkingLeft = true;
        this.walkLeft();
      }
    },

    // 键盘松开事件
    handleKeyUp(event) {
      const key = event.key;

      if (key === "ArrowRight") {
        this.key.right = false;
        this.walkingRight = false;
      }

      if (key === "ArrowLeft") {
        this.key.left = false;
        this.walkingLeft = false;
      }
    },

    // 向右走
    walkRight() {
      const maxScroll = this.timeLine.length * this.nodeSpacing - this.containerWidth;

      if (this.scrollPosition < maxScroll) {
        this.scrollPosition += this.stepSize;
        if (this.scrollPosition > maxScroll) {
          this.scrollPosition = maxScroll;
        }
      } else {
        this.spritePosition += this.stepSize;
        const maxSpritePosition = this.containerWidth - 50;
        if (this.spritePosition > maxSpritePosition) {
          this.spritePosition = maxSpritePosition;
        }
      }

      this.checkCollisionWithNodes();
    },

    // 向左走
    walkLeft() {
      if (this.scrollPosition > 0) {
        this.scrollPosition -= this.stepSize;
        if (this.scrollPosition < 0) {
          this.scrollPosition = 0;
        }
      } else {
        this.spritePosition -= this.stepSize;
        if (this.spritePosition < 0) {
          this.spritePosition = 0;
        }
      }

      this.checkCollisionWithNodes();
    },

    // 检查是否碰撞到时间节点
    checkCollisionWithNodes() {
      const spriteAbsolutePosition = this.scrollPosition + this.spritePosition;

      this.timeLine.forEach((node, index) => {
        const nodePosition = index * this.nodeSpacing;

        // 小人和时间节点的位置差
        if (Math.abs(spriteAbsolutePosition - nodePosition) < 20) {
          this.currentMessage = `${node.year}: ${node.event}`;
          // 检查是否是随机目标时间点
          if (index === this.randomTargetIndex && !this.showBubble) {
            this.triggerBubble(node);
          }
        }
      });
    },
    triggerBubble(node) {
      this.bubbleMessage = `原来，这就是"${this.human.name}"的一生`;
      this.showBubble = true;

      setTimeout(() => {
        this.showBubble = false; // 气泡显示 3 秒后隐藏
        this.setRandomTarget(); // 重置随机目标
      }, 3000);
    },
    // 关闭弹窗的方法
    closeModal() {
      this.$emit("close"); // 向父组件发送关闭事件
    },
  },
};
</script>

<style scoped>
@import '@/assets/font/font.css';
.walk-modal {

  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000; /* 弹窗层级 */
}

.overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
}

.walk-container {
  position: relative;
  background: url('@/assets/RedR.jpg') no-repeat center center;
  padding: 20px;
  border-radius: 10px;
  width: 800px;
  height: 400px;
  z-index: 1; /* 保证内容显示在弹窗背景层上方 */
  overflow: hidden; /* 确保内容不会溢出 */
}

.time-line-container {
  position: absolute;
  top: 400px; /* 时间线垂直居中 */
  height: 2px;
  background-color: black;
  white-space: nowrap;
}

.time-node {
  position: absolute;
  top: -10px;
  width: 10px;
  height: 10px;
  background-color: #b71c1c;
  border-radius: 50%;
}

.circle {
  width: 15px;
  height: 15px;
  background-color: #b71c1c;
  border-radius: 50%;
  border: 2px solid white;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.5);
}

.label {
  margin-top: 5px;
  font-size: 12px;
  color: black;
  white-space: nowrap;
  text-align: center;
}

.sprite {
  position: absolute;
  bottom: 50px;
  width: 102px;
  height: 148px;
  background-image: url(https://atomicrobotdesign.com/blog_media/css-sprite/standing-right.png);
  background-size: cover;
}

.stand-right {
  background-image: url(https://atomicrobotdesign.com/blog_media/css-sprite/standing-right.png);
}

.stand-left {
  background-image: url(https://atomicrobotdesign.com/blog_media/css-sprite/standing-left.png);
}

.walk-right {
  background-image: url(https://atomicrobotdesign.com/blog_media/css-sprite/walk-right.png);
  animation: walk 0.9s steps(6) infinite;
}

.walk-left {
  background-image: url(https://atomicrobotdesign.com/blog_media/css-sprite/walk-left.png);
  animation: walk 0.9s steps(6) infinite;
}

@keyframes walk {
  from {
    background-position: 0px;
  }
  to {
    background-position: -612px;
  }
}

.message-box {
  font-family: 'HelveticaNeue', serif;
  position: fixed;
  top: 200px;
  left: 50%;
  transform: translateX(-50%);
  color: black;
  padding: 10px 20px;
  border-radius: 5px;
  font-size: 26px;
  font-weight: bold;
}

.close-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  padding: 5px 10px;
  background-color: transparent;
  color: #b71c1c;
  border: none;
  border-radius: 5px;
}
.speech-bubble {
  position: absolute;
  top: -50px; /* 气泡在小人头上方 */
  left: 50%;
  transform: translateX(-20%);
  background-color: rgba(255, 255, 255, 0.9);
  color: black;
  border: 0.5px solid black;
  border-radius: 10px;
  padding: 10px 15px;
  font-size: 14px;
  white-space: nowrap;
  z-index: 2;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
</style>

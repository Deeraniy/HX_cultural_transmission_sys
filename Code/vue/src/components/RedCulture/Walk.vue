<template>
  <div class="container">
    <!-- 时间线容器 -->
    <div class="time-line-container" :style="{ left: `${-scrollPosition}px` }">
      <!-- 时间节点 -->
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

    <!-- 小人 -->
    <div
        ref="sprite"
        class="sprite"
        :class="{ 'walk-right': key.right, 'walk-left': key.left }"
        :style="{ left: `${spritePosition}px` }"
    ></div>

    <!-- 显示的事件信息 -->
    <div v-if="currentMessage" class="message-box">{{ currentMessage }}</div>
  </div>
</template>

<script>
// 直接引入 JSON 文件
import maoTimeLine from "@/json/毛泽东时间顺序.json";

export default {
  name: "TimeLineGame",
  data() {
    return {
      timeLine: maoTimeLine, // 时间节点数据
      nodeSpacing: 200, // 时间节点间距
      spritePosition: 0, // 小人的水平位置
      scrollPosition: 0, // 时间线滚动位置
      stepSize: 10, // 小人移动步长
      containerWidth: 800, // 可视区域宽度（画布宽度）
      currentMessage: "", // 当前显示的事件信息
      key: { left: false, right: false }, // 记录左右移动状态
    };
  },
  mounted() {
    // 监听键盘事件
    window.addEventListener("keydown", this.handleKeyDown);
    window.addEventListener("keyup", this.handleKeyUp);
  },
  beforeDestroy() {
    // 移除键盘事件监听
    window.removeEventListener("keydown", this.handleKeyDown);
    window.removeEventListener("keyup", this.handleKeyUp);
  },
  methods: {
    // 处理键盘按下事件
    handleKeyDown(event) {
      const key = event.key;

      if (key === "ArrowRight") {
        this.key.right = true;
        this.moveRight();
      }

      if (key === "ArrowLeft") {
        this.key.left = true;
        this.moveLeft();
      }
    },

    // 处理键盘松开事件
    handleKeyUp(event) {
      const key = event.key;

      if (key === "ArrowRight") {
        this.key.right = false;
      }

      if (key === "ArrowLeft") {
        this.key.left = false;
      }
    },

    // 向右移动
    moveRight() {
      const maxScroll = this.timeLine.length * this.nodeSpacing - this.containerWidth;

      if (this.scrollPosition < maxScroll) {
        // 如果时间线还能滚动，则优先滚动时间线
        this.scrollPosition += this.stepSize;
        if (this.scrollPosition > maxScroll) {
          this.scrollPosition = maxScroll; // 限制滚动到最右
        }
      } else {
        // 时间线不能滚动时，小人移动
        this.spritePosition += this.stepSize;
        const maxSpritePosition = this.containerWidth - 50; // 小人不能超出画布范围
        if (this.spritePosition > maxSpritePosition) {
          this.spritePosition = maxSpritePosition;
        }
      }

      // 检查是否触碰到时间节点
      this.checkCollisionWithNodes();
    },

    // 向左移动
    moveLeft() {
      if (this.scrollPosition > 0) {
        // 如果时间线还能滚动，则优先滚动时间线
        this.scrollPosition -= this.stepSize;
        if (this.scrollPosition < 0) {
          this.scrollPosition = 0; // 限制滚动到最左
        }
      } else {
        // 时间线不能滚动时，小人移动
        this.spritePosition -= this.stepSize;
        if (this.spritePosition < 0) {
          this.spritePosition = 0; // 小人不能超出画布范围
        }
      }

      // 检查是否触碰到时间节点
      this.checkCollisionWithNodes();
    },

    // 检查是否触碰到时间节点
    checkCollisionWithNodes() {
      const spriteAbsolutePosition = this.scrollPosition + this.spritePosition; // 小人在时间线上的绝对位置
      this.timeLine.forEach((node, index) => {
        const nodePosition = index * this.nodeSpacing;

        // 判断小人是否触碰到节点（简单范围判断）
        if (Math.abs(spriteAbsolutePosition - nodePosition) < 20) {
          this.currentMessage = `${node.year}: ${node.event}`;
        }
      });
    },
  },
};
</script>

<style scoped>
.container {
  position: relative;
  width: 800px; /* 可视区域宽度 */
  height: 600px;
  overflow: hidden; /* 超出部分隐藏 */
  border: 2px solid #ddd;
  margin: 50px auto;
  background-color: #f8f8f8;
}

.time-line-container {
  position: absolute;
  top: 500px; /* 时间线居中 */
  height: 2px;
  background-color: black;
  white-space: nowrap;
}

.time-node {
  position: absolute;
  top: -10px; /* 调整节点位置 */
  width: 10px;
  height: 10px;
  background-color: red;
  border-radius: 50%;
}

.circle {
  width: 15px;
  height: 15px;
  background-color: red;
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

/* 小人 */
.sprite {
  position: absolute;
  bottom: 98px; /* 小人踩在线上 */
  width: 102px;
  height: 148px;
  background-image: url(https://atomicrobotdesign.com/blog_media/css-sprite/standing-right.png);
  background-size: cover;
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
  position: fixed;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  background-color: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 10px 20px;
  border-radius: 5px;
  font-size: 16px;
}
</style>

<template>
  <div class="card-container" :style="{ position: 'relative', width: '100%', height: '500px', overflow: 'hidden' }">
    <!-- 动态渲染每张卡片 -->
    <div
        v-for="(card, index) in cards"
        :key="index"
        class="card"
        :style="getCardStyle(index)"
        @touchstart="touchStart($event, index)"
        @touchmove="touchMove($event)"
        @touchend="touchEnd"
        :ref="`card${index}`"
    >
      <slot :name="'card' + (index + 1)"></slot>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, defineProps, defineEmits, onMounted } from 'vue';

// 组件的props定义
const props = defineProps({
  cardWidth: {
    type: Number,
    default: 200,
  },
  cardHeight: {
    type: Number,
    default: 200,
  },
  cardBgColor: {
    type: String,
    default: '#fff',
  },
  leftPad: {
    type: Number,
    default: 10,
  },
  topPad: {
    type: Number,
    default: 6,
  },
  borderRadius: {
    type: Number,
    default: 8,
  },
  throwTriggerDistance: {
    type: Number,
    default: 100,
  },
  dragDirection: {
    type: String,
    default: 'all', // 'horizontal', 'vertical', 'all'
  },
  hasShadow: {
    type: Boolean,
    default: false,
  },
  hasBorder: {
    type: Boolean,
    default: true,
  },
});

// 组件的事件定义
const emit = defineEmits([
  'onDragMove',
  'onDragStop',
  'onThrowDone',
  'onThrowFail',
]);

// 定义状态和数据
const state = reactive({
  left: 0,
  top: 0,
  startLeft: 0,
  startTop: 0,
  isThrow: false,
  isAnimating: false,
  cards: [1, 2, 3, 4], // 渲染的卡片数量
  actionName: '',
});

let currentCardIndex = 0;

// 获取每张卡片的样式
const getCardStyle = (index) => {
  const zIndex = state.cards.length - index;
  let left = 0;
  let top = 0;
  let opacity = 1;
  let width = props.cardWidth;
  let height = props.cardHeight;
  let borderRadius = `${props.borderRadius}px`;
  let boxShadow = props.hasShadow ? '0 2px 10px rgba(0, 0, 0, 0.1)' : 'none';
  let border = props.hasBorder ? '1px solid rgba(0, 0, 0, 0.2)' : 'none';

  // 根据拖拽方向调整卡片位置
  if (props.dragDirection === 'horizontal') {
    left = state.left;
  } else if (props.dragDirection === 'vertical') {
    top = state.top;
  } else if (props.dragDirection === 'all') {
    left = state.left;
    top = state.top;
  }

  return {
    position: 'absolute',
    backgroundColor: props.cardBgColor,
    left: `${left}px`,
    top: `${top}px`,
    width: `${width}px`,
    height: `${height}px`,
    zIndex,
    opacity,
    borderRadius,
    boxShadow,
    border,
    transition: state.isAnimating ? 'none' : 'all 0.4s ease',
  };
};

// 处理卡片拖动事件
const touchStart = (e, index) => {
  if (index !== currentCardIndex || state.isAnimating) return;
  const curTouch = e.touches[0];
  state.startLeft = curTouch.clientX - state.left;
  state.startTop = curTouch.clientY - state.top;
};

const touchMove = (e) => {
  if (state.isThrow || state.isAnimating) return;
  const curTouch = e.touches[0];

  if (props.dragDirection === 'horizontal') {
    state.left = curTouch.clientX - state.startLeft;
  } else if (props.dragDirection === 'vertical') {
    state.top = curTouch.clientY - state.startTop;
  } else {
    state.left = curTouch.clientX - state.startLeft;
    state.top = curTouch.clientY - state.startTop;
  }

  // 发射onDragMove事件
  emit('onDragMove', { left: state.left, top: state.top });
};

const touchEnd = () => {
  if (state.isThrow || state.isAnimating) return;

  // 计算卡片的移动距离
  const distance = getDistance(0, 0, state.left, state.top);
  if (distance > props.throwTriggerDistance) {
    makeCardThrow();
  } else {
    makeCardBack();
  }

  // 发射onDragStop事件
  emit('onDragStop', { left: state.left, top: state.top });
};

// 飞出去效果
const makeCardThrow = () => {
  state.isThrow = true;
  const angle = Math.atan2(state.top, state.left); // 计算角度
  state.left = Math.cos(angle) * 500; // 飞出500px
  state.top = Math.sin(angle) * 500;
  setTimeout(() => {
    moveToNextCard();
    // 发射onThrowDone事件
    emit('onThrowDone', { left: state.left, top: state.top });
  }, 400);
};

// 回位效果
const makeCardBack = () => {
  state.isThrow = false;
  state.left = 0;
  state.top = 0;
  // 发射onThrowFail事件
  emit('onThrowFail', { left: state.left, top: state.top });
};

// 计算两点之间的距离
const getDistance = (x1, y1, x2, y2) => {
  const _x = Math.abs(x1 - x2);
  const _y = Math.abs(y1 - y2);
  return Math.sqrt(_x * _x + _y * _y);
};

// 更新卡片的位置
const moveToNextCard = () => {
  if (currentCardIndex < state.cards.length - 1) {
    currentCardIndex++;
    updateCardPositions();
  } else {
    resetAllCards();
  }
};

const updateCardPositions = () => {
  state.left = 0;
  state.top = 0;
  // 在这里更新每张卡片的位置
  state.isAnimating = true;
  setTimeout(() => {
    state.isAnimating = false;
  }, 400);
};

const resetAllCards = () => {
  state.left = 0;
  state.top = 0;
  // 重置卡片
  state.isAnimating = true;
  setTimeout(() => {
    state.isAnimating = false;
  }, 400);
};

// 使用onMounted设置初始状态
onMounted(() => {
  updateCardPositions();
});
</script>

<style scoped>
.card-container {
  position: relative;
  width: 100%;
  height: 500px;
  overflow: hidden;
}

.card {
  position: absolute;
  background-color: rgba(0, 0, 0, 0.2);
  color: white;
  display: flex;
  justify-content: center;
  align-items: center;
  user-select: none;
  cursor: pointer;
}
</style>

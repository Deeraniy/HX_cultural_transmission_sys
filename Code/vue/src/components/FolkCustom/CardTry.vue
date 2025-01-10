<template>
  <DragCard
      :cardWidth="300"
      :cardHeight="120"
      :throwTriggerDistance="100"
      dragDirection="horizontal"
      :hasShadow="true"
      @onDragMove="onCardDragMove"
      @onDragStop="onCardDragStop"
      @onThrowDone="onCardThrowDone"
      @onThrowFail="onCardThrowFail"
  >
    <template #card1>
      <div>First Card Content</div>
    </template>
    <template #card2>
      <div>Second Card Content</div>
    </template>
    <template #card3>
      <div>Third Card Content</div>
    </template>
  </DragCard>
</template>

<script>
import DragCard from './Card.vue';  // 导入子组件

export default {
  components: {
    DragCard,  // 在此注册
  },
  data() {
    return {
      actionName: "",
    };
  },
  methods: {
    onCardDragMove(obj) {
      if (obj.left < -10) {
        this.actionName = "不喜欢";
      } else if (obj.left > 10) {
        this.actionName = "喜欢";
      } else {
        this.actionName = "";
      }
    },
    onCardDragStop(obj) {
      // Handle drag stop logic
    },
    onCardThrowDone(obj) {
      // Handle throw done logic
    },
    onCardThrowFail(obj) {
      // Handle throw fail logic
    }
  }
};
</script>

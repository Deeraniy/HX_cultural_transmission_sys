<template>
  <div class="block2">
    <div class="box">
      <div class="title">
        <h1>
          <span class="tit-span"><img src="@/assets/111.png" alt="Icon1" /></span>
          <span class="s1">湖湘</span>
          <span>美食</span>
          <span class="tit-span"><img src="@/assets/111.png" alt="Icon2" /></span>
        </h1>
      </div>

      <div class="num">
        <b>114514个</b>
      </div>

      <div class="tip" style="cursor: pointer;" @click="openAlert('.pop-type')">
        <span>湖湘美食查询</span>
      </div>
    </div>

    <ul class="list">
      <li
          class="sHoverItem"
          v-for="(dish, index) in dishes"
          :key="index"
          @mouseover="showDetails(index)"
          @mouseleave="hideDetails"
      >
        <img
            alt=""
            title=""
            class="lazyload"
            :src="dish.image"
        />
        <div class="mask" v-if="activeIndex === index">
          <a :href="dish.link">
            <p>{{ dish.name }}</p>
            <p>{{ dish.shortDescription }}</p>
            <p>{{ dish.fullDescription }}</p>
          </a>
        </div>
      </li>
    </ul>

    <!-- 藏品分类查询表的开始 -->
    <div class="popWindow pop-type">
      <a href="javascript:;" class="close"></a>
      <div>
        <div class="title">
          <h1 style="margin-top: 16px;">
            <b>二</b><b>十</b><b>三</b>个品类藏品
          </h1>
        </div>

        <div class="table">
          <ul>
            <li v-for="category in categories" :key="category">
              <a href="">{{ category }}</a>
            </li>
          </ul>
        </div>
      </div>
    </div>
    <!-- 藏品分类查询表的结束 -->
  </div>
</template>

<script>
export default {
  data() {
    return {
      dishes: [
        {
          name: '永州血鸭',
          shortDescription: '色泽红亮，味道鲜香，肉质滑嫩',
          fullDescription: '永州血鸭是一道经典的湘菜，以鸭肉为主料，搭配独特的香料和调料，制作出浓郁的风味，深受当地居民和游客的喜爱。',
          image: '@/assets/circle1.jpg',
          link: '/collection/paint/229937.html',
        },
        {
          name: '湘西外婆菜',
          shortDescription: '酸辣可口，丰富的营养，家常风味。',
          fullDescription: '外婆菜是湖南传统名菜之一，通常用腌制的蔬菜、豆蔻和辣椒等制作，味道鲜明，唤起人们对家乡的记忆和温暖的感觉。',
          image: '@/assets/circle1.jpg',
          link: '/collection/paint/230459.html',
        },
        {
          name: '剁椒鱼头',
          shortDescription: '选用新鲜鱼头，剁椒调味，肉质鲜嫩，麻辣可口。',
          fullDescription: '剁椒鱼头是一道经典的湘菜，以鲜嫩的鱼头为主料，搭配剁椒蒸制而成，味道鲜美，辣味十足，非常受欢迎。',
          image: '@/assets/circle1.jpg',
          link: '',
        },
      ],
      categories: [
        '陶瓷', '绘画', '法书', '铭刻', '青铜器', '玺印', '织绣', '文房用品',
        '家具', '钟表仪器', '珐琅', '漆器', '雕塑', '金银锡器', '玉石器', '玻璃器',
        '竹木牙角匏', '宫廷宗教', '首饰', '武备仪仗', '音乐戏曲', '生活器具', '外国文物', '藏品搜索'
      ],
      activeIndex: null, // 用于跟踪当前活动项的索引
    };
  },
  methods: {
    showDetails(index) {
      this.activeIndex = index; // 显示对应的详细信息
    },
    hideDetails() {
      this.activeIndex = null; // 隐藏所有详细信息
    },
    openAlert(selector) {
      // 这里可以控制弹窗的显示
      document.querySelector(selector).classList.toggle('active');
    }
  },
};
</script>

<style scoped>
/* 样式根据需要添加 */
.sHoverItem {
  position: relative;
}

.mask {
  display: none;
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  color: white;
  padding: 10px;
}

.sHoverItem:hover .mask {
  display: block;
}

.popWindow {
  /* 弹窗样式 */
}

.popWindow.active {
  display: block;
}
</style>


<template>
  <div class="about-container">
    <el-carousel 
      :interval="4000" 
      type="card" 
      height="700px"
      class="about-carousel"
    >
      <!-- 第一页：关于我们 -->
      <el-carousel-item>
        <div class="about-card">
          <div class="card-content">
            <h2 class="title" :style="{ fontSize: titleFontSize }" style="margin-top:0px;">{{ $t('index.footer.about.title') }}</h2>
            <div class="divider"></div>
            <p class="description" :style="{ fontSize: descriptionFontSize }">
              {{ $t('hu-xiang-wen-hua-shu-zhi-chuan-bo-wang-shi-you-hu-nan-shi-fan-da-xue-xin-xi-ke-xue-yu-gong-cheng-xue-yuan-cai-mei-ling-lao-shi-he-ma-hua-jiao-shou-zhi-dao-de-he-xin-kai-fa-tuan-dui-wan-cheng-de') }}
              <br><br>
              {{ $t('cai-mei-ling-lao-shi-zeng-zhu-chi-he-can-yu-guo-jia-zi-ran-ke-xue-ji-jin-xiang-mu-hu-nan-sheng-zi-ran-ke-xue-ji-jin-xiang-mu-deng-sheng-bu-ji-yi-shang-ke-yan-ke-ti-4-xiang-can-yu-le-duo-xiang-ying-yong-ruan-jian-xi-tong-de-kai-fa-ju-you-feng-fu-de-chan-pin-yan-fa-he-ying-yong-fu-wu-jing-yan') }}
              <br><br>
              {{ $t('ma-hua-jiao-shou-jin-wu-nian-lai-zhu-chi-guo-jia-zi-ran-ke-xue-ji-jin-mian-shang-xiang-mu-2-xiang-bing-zhu-chi-hu-nan-sheng-zhong-da-ke-ji-chuang-xin-ping-tai-zi-ke-ti-jiao-yu-bu-ren-wen-she-hui-ke-xue-yan-jiu-ji-jin-xiang-mu-jiao-cha-xue-ke-zong-he-yan-jiu-hu-nan-sheng-zi-ran-ke-xue-ji-jin-mian-shang-xiang-mu-hu-nan-sheng-jiao-yu-ting-ke-xue-yan-jiu-xiang-mu-zhong-dian-xiang-mu-deng-zong-xiang-ke-yan-ke-ti-5-xiang-jin-wu-nian-zhi-dao-xue-sheng-wan-cheng-da-xue-sheng-yan-jiu-xing-xue-xi-he-chuang-xin-xing-shi-yan-ji-hua-xiang-mu-guo-jia-ji-2-xiang-sheng-ji-2-xiang') }}
            </p>
          </div>
        </div>
      </el-carousel-item>

      <!-- 第二页：团队介绍 -->
      <el-carousel-item>
        <div class="about-card">
          <div class="card-content">
            <h2 class="title" :style="{ fontSize: titleFontSize }">{{ $t('tuan-dui-jie-shao') }}</h2>
            <div class="divider"></div>
            <div class="team-photo">
              <img src="@/assets/img_hx/合照.jpg" alt="$t('tuan-dui-he-zhao')">
            </div>
            <p class="description" :style="{ fontSize: descriptionFontSize }">
              {{ $t('gai-xi-tong-de-he-xin-kai-fa-tuan-dui-bao-kuo-lu-yu-xin-liu-meng-xuan-zheng-jia-jiang-yu-chen-diao-lei-wu-ren') }}
              <br><br>
              {{ $t('ben-xiang-mu-cheng-yuan-jun-wei-ruan-jian-gong-cheng-zhuan-ye-jun-zhan-xian-chu-za-shi-de-li-lun-ji-chu-min-jie-de-xue-xi-qu-xian-he-ling-ren-qi-dai-de-chuang-xin-qian-li-yi-ji-zai-jin-mi-xie-zuo-zhong-ti-xian-de-mo-qi-pei-he-wei-xiang-mu-zhu-ru-le-qiang-da-de-dong-li-he-huo-li-qie-fen-gong-jiao-wei-ming-que-tong-shi-jun-ju-bei-vuepytorch-deng-kai-fa-kuang-jia-yi-ji-zi-ran-yu-yan-chu-li-he-shen-jing-wang-luo-xiang-guan-de-zhi-shi-le-jie-jing-dian-de-shen-jing-wang-luo-mo-xing-ru-rnntransformer-deng-you-yi-ding-de-ji-shu-he-shi-jian-jing-li') }}
              <br><br>
              {{ $t('xiao-zu-cheng-yuan-zai-hu-nan-shi-fan-da-xue-xin-xi-ke-xue-yu-gong-cheng-xue-yuan-jiao-shou-ren-gong-zhi-neng-yu-jing-zhun-guo-ji-chuan-bo-yan-jiu-yuan-yan-jiu-zhong-xin-zhu-ren-ma-hua-de-zhi-dao-xia-can-yu-le-duo-ge-jing-zhun-guo-ji-chuan-bo-xiang-guan-xiang-mu-de-yan-jiu-ke-wei-ben-xiang-mu-ti-gong-guan-jian-de-ji-shu-ji-chu-he-shi-yan-ping-tai') }}
            </p>
          </div>
        </div>
      </el-carousel-item>

      <!-- 第三页：团队价值观 -->
      <el-carousel-item>
        <div class="about-card">
          <div class="card-content">
            <h2 class="title" :style="{ fontSize: titleFontSize }">{{ $t('shi-ming-yuan-jing') }}</h2>
            <div class="divider"></div>
            <p class="description" :style="{ fontSize: descriptionFontSize }" style="text-align: center; margin-bottom: 30px;">
              {{ $t('shu-lian-wan-li-hu-xiang-zhi-hui-qian-nian-wen-mai') }}
            </p>
            <p class="description" :style="{ fontSize: descriptionFontSize }">
              {{ $t('gai-xi-tong-cong-she-ji-dao-shi-xian-guo-cheng-zhong-de-dao-le-hu-nan-shi-fan-da-xue-de-guo-jia-shi-jie-yi-liu-jian-she-xue-ke-wai-guo-yu-yan-wen-xue-de-da-li-zhi-chi-wo-xiao-de-wai-guo-yu-yan-wen-xue-xue-ke-jian-chi-yi-wen-hua-chuan-bo-wei-zhua-shou-fu-wu-zhong-guo-wen-hua-zou-chu-qu-zhan-lve-chi-xu-tui-jin-zhong-hua-you-xiu-wen-hua-de-tui-guang-yi-cheng-wei-wo-guo-zhong-wai-wen-hua-chuan-bo-de-zhong-yao-ji-di-zhi-yi-tong-shi-zai-pei-yang-fu-he-xing-ba-jian-wai-yu-ren-cai-fu-wu-guo-jia-an-quan-wai-jiao-da-ju-yi-dai-yi-lu-jian-she-qu-yu-jing-ji-she-hui-fa-zhan-deng-fang-mian-xing-cheng-le-xian-ming-te-se-zai-ren-cai-pei-yang-mo-shi-gai-ge-gao-shui-ping-shi-zi-dui-wu-jian-she-biao-zhi-xing-ke-yan-cheng-guo-chan-chu-guo-ji-jiao-liu-he-zuo-deng-fang-mian-cheng-xiao-xian-zhu') }}
            </p>
          </div>
        </div>
      </el-carousel-item>
    </el-carousel>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useI18n } from 'vue-i18n';

const { locale } = useI18n();

const titleFontSize = computed(() => {
  return locale.value === 'en' ? '18px' : '24px';  // 设置英文模式下小一点的字体
});

const descriptionFontSize = computed(() => {
  return locale.value === 'en' ? '14px' : '16px';  // 英文模式下稍微小一点
});


</script>

<style scoped lang="scss">
.about-container {
  padding: 40px;
  height: 615px;
  perspective: 1000px;
  overflow: hidden;
  position: relative;

  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: radial-gradient(circle at center, transparent 0%, rgba(0, 0, 0, 0.05) 100%);
    pointer-events: none;
  }
}

.about-carousel {
  :deep(.el-carousel__item) {
    border-radius: 12px;
    transform-style: preserve-3d;
    perspective: 1000px;
    opacity: 0.4;
    transform: scale(0.85) translateY(50px);
    transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
    filter: blur(2px);
    width: 800px;
    margin-left: -60px;
    height: 620px;

    &.is-active {
      opacity: 1;
      transform: scale(1) translateY(0);
      filter: blur(0);
      z-index: 2;
      
      .about-card {
        box-shadow: 
          0 20px 40px rgba(0, 0, 0, 0.2),
          0 12px 24px rgba(0, 0, 0, 0.15),
          inset 2px 2px 5px rgba(255, 255, 255, 0.9),
          inset -2px -2px 5px rgba(0, 0, 0, 0.05);
      }
    }

    &:not(.is-active) {
      .about-card {
        pointer-events: none;
      }
    }
  }

  :deep(.el-carousel__arrow) {
    background-color: #b71c1c;
    border-radius: 50%;
    transform: scale(1.2);
    transition: all 0.3s ease;

    &:hover {
      background-color: rgb(131, 24, 18);
      transform: scale(1.3);
    }
  }

  :deep(.el-carousel__indicators) {
    z-index: 10;

    .el-carousel__button {
      background-color: rgba(218, 37, 28, 0.6);
      border-radius: 4px;
      transition: all 0.3s ease;
      width: 24px;
      height: 4px;

      &:hover {
        background-color: #b71c1c;
      }
    }

    .is-active .el-carousel__button {
      background-color: #b71c1c;
      width: 32px;
    }
  }
}

.about-card {
  height: 100%;
  background: linear-gradient(145deg, #ffffff, #f5f5f5);
  border-radius: 12px;
  box-shadow: 
    0 12px 24px rgba(0, 0, 0, 0.1),
    0 4px 6px rgba(0, 0, 0, 0.1),
    inset 2px 2px 5px rgba(255, 255, 255, 0.9),
    inset -2px -2px 5px rgba(0, 0, 0, 0.05);
  backdrop-filter: blur(10px);
  overflow: hidden;
  transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
  transform-style: preserve-3d;
  position: relative;

  &:hover {
    transform: translateY(-8px) scale(1.02) rotateX(2deg);
    box-shadow: 
      0 25px 50px rgba(0, 0, 0, 0.3),
      0 15px 20px rgba(0, 0, 0, 0.2),
      inset 2px 2px 5px rgba(255, 255, 255, 0.9),
      inset -2px -2px 5px rgba(0, 0, 0, 0.05);
  }
}

.card-content {
  padding: 20px;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  transform: translateZ(20px);
  position: relative;
}

.title {
  font-size: 38px;
  color: #b71c1c;
  margin-top: 0px;
  margin-bottom: 15px;
  font-weight: bold;
  text-align: center;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
}

.divider {
  width: 60px;
  height: 4px;
  background: linear-gradient(90deg, #b71c1c 0%, #ff6b6b 100%);
  margin: 20px auto;
  border-radius: 2px;
  box-shadow: 0 2px 4px rgba(218, 37, 28, 0.2);
}

.team-photo {
  width: 100%;
  max-width: 400px;
  margin: 20px auto;
  margin-top: -10px;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  
  img {
    width: 100%;
    height: 210px;
    display: block;
    transition: transform 0.3s ease;
    
    &:hover {
      transform: scale(1.02);
    }
  }
}

.description {
  margin-top:10px;
  font-size: 16px;
  line-height: 1.7;
  color: #333;
  text-align: justify;
  max-width: 900px;
  margin: 0 auto;
  padding: 0 20px;
  white-space: pre-line;
  
  br {
    display: block;
    content: "";
    margin-top: 10px;
  }
}

.values-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 25px;
  margin-top: 20px;
  width: 100%;
  max-width: 900px;
}

.value-item {
  background: linear-gradient(145deg, #ffffff, #f8f8f8);
  padding: 20px;
  border-radius: 8px;
  text-align: center;
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  border: 1px solid rgba(218, 37, 28, 0.1);
  box-shadow: 
    0 4px 8px rgba(0, 0, 0, 0.05),
    inset 1px 1px 3px rgba(255, 255, 255, 0.9),
    inset -1px -1px 3px rgba(0, 0, 0, 0.05);
  transform-style: preserve-3d;

  &:hover {
    transform: translateY(-3px) scale(1.03) rotateX(2deg);
    box-shadow: 
      0 8px 16px rgba(218, 37, 28, 0.15),
      0 4px 8px rgba(0, 0, 0, 0.1),
      inset 1px 1px 3px rgba(255, 255, 255, 0.9),
      inset -1px -1px 3px rgba(0, 0, 0, 0.05);
    border-color: #b71c1c;
  }

  h3 {
    color: #b71c1c;
    font-size: 24px;
    margin-bottom: 12px;
    text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
    transform: translateZ(10px);
  }


  p {
    color: #666;
    font-size: 16px;
    line-height: 1.5;
    transform: translateZ(5px);
  }
}

// 响应式设计
@media (max-width: 768px) {
  .about-container {
    padding: 20px;
  }

  .title {
    font-size: 28px;
  }

  .description {
    font-size: 16px;
  }

  .values-grid {
    grid-template-columns: 1fr;
    gap: 20px;
  }

  .value-item {
    padding: 20px;

    h3 {
      font-size: 20px;
    }

    p {
      font-size: 14px;
    }
  }
}

// 添加卡片边缘光效
.about-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  border-radius: 12px;
  background: linear-gradient(
    45deg,
    transparent 0%,
    rgba(255, 255, 255, 0.1) 45%,
    rgba(255, 255, 255, 0.2) 50%,
    rgba(255, 255, 255, 0.1) 55%,
    transparent 100%
  );
  pointer-events: none;
  transition: all 0.4s ease;
}

.about-card:hover::before {
  background-position: 100% 100%;
}

</style>
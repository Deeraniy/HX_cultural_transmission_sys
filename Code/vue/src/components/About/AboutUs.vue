// AboutUs.vue
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
            <h2 class="title" style="margin-top:0px;">关于我们</h2>
            <div class="divider"></div>
            <p class="description" style="font-size: 18px;">
              《湖湘文化数智传播网》是由湖南师范大学信息科学与工程学院蔡美玲老师和马华教授指导的核心开发团队完成的。
              <br><br>
              蔡美玲老师曾主持和参与国家自然科学基金项目、湖南省自然科学基金项目等省部级以上科研课题4项，参与了多项应用软件系统的开发，具有丰富的产品研发和应用服务经验。
              <br><br>
              马华教授近五年来主持国家自然科学基金面上项目2项，并主持湖南省重大科技创新平台子课题、教育部人文社会科学研究基金项目（交叉学科/综合研究）、湖南省自然科学基金面上项目、湖南省教育厅科学研究项目重点项目等纵向科研课题5项。近五年指导学生完成大学生研究性学习和创新性实验计划项目国家级2项、省级2项。
            </p>
          </div>
        </div>
      </el-carousel-item>

      <!-- 第二页：团队介绍 -->
      <el-carousel-item>
        <div class="about-card">
          <div class="card-content">
            <h2 class="title">团队介绍</h2>
            <div class="divider"></div>
            <div class="team-photo">
              <img src="@/assets/img_hx/合照.jpg" alt="团队合照">
            </div>
            <p class="description">
              该系统的核心开发团队包括陆雨昕、刘孟煊、郑佳、蒋宇晨、刁磊五人。
              <br><br>
              本项目成员均为软件工程专业，均展现出扎实的理论基础、敏捷的学习曲线和令人期待的创新潜力，以及在紧密协作中体现的默契配合，为项目注入了强大的动力和活力，且分工较为明确，同时均具备Vue、PyTorch等开发框架以及自然语言处理和神经网络相关的知识，了解经典的神经网络模型如RNN、Transformer等，有一定的技术和实践经历。
              <br><br>
              小组成员在湖南师范大学信息科学与工程学院教授、"人工智能与精准国际传播"研究院研究中心主任马华的指导下参与了多个精准国际传播相关项目的研究，可为本项目提供关键的技术基础和实验平台。
            </p>
          </div>
        </div>
      </el-carousel-item>

      <!-- 第三页：团队价值观 -->
      <el-carousel-item>
        <div class="about-card">
          <div class="card-content">
            <h2 class="title">使命愿景</h2>
            <div class="divider"></div>
            <p class="description" style="font-size: 20px; text-align: center; margin-bottom: 30px;">
              数联万里湖湘 · 智汇千年文脉
            </p>
            <p class="description" style="font-size: 18px;">
              该系统从设计到实现过程中，得到了湖南师范大学的国家"世界一流"建设学科"外国语言文学"的大力支持。我校的"外国语言文学"学科坚持"以文化传播为抓手，服务中国文化走出去战略"，持续推进中华优秀文化的推广，已成为我国中外文化传播的重要基地之一，同时，在培养复合型拔尖外语人才，服务国家安全、外交大局、"一带一路"建设、区域经济社会发展等方面形成了鲜明特色， 在人才培养模式改革、高水平师资队伍建设、标志性科研成果产出、国际交流合作等方面成效显著。
            </p>
          </div>
        </div>
      </el-carousel-item>
    </el-carousel>
  </div>
</template>

<script>
export default {
  name: 'AboutUs'
};
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
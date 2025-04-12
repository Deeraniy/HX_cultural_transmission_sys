// BackgroundIntro.vue
<template>
  <div class="background-container">
    <!-- 书签导航 -->
    <div class="bookmark-nav">
      <div 
        v-for="(tab, index) in tabs" 
        :key="index"
        :class="['bookmark-item', { active: currentTab === index }]"
        @click="currentTab = index"
      >
        {{ tab }}
      </div>
    </div>

    <!-- 内容区域 -->
    <div class="content-wrapper">
      <!-- 项目简介 -->
      <div v-show="currentTab === 0" class="content-section">
        <el-card class="intro-card" shadow="hover">
          <div class="card-header">
            <h2>项目简介</h2>
            <div class="divider"></div>
          </div>
          <div class="card-content">
            <p>
              推动中华文化走出去，提升中华文化影响力，需要将中华文化对外传播内容的丰富性、传播途径的多样性、文化影响的持久性进行有机整合。其中，湖南不仅有远古文化的丰厚遗存,还有着传统文化的守正创新,更有近代文化的卓越建树。因此，推动文化传播，于湖湘文化而言，不仅可以使其作为中华文化的重要组成部分被更多国际社会了解，也能够为区域文化国际传播积累实践经验，从而丰富全球化时代的文化多样性，并推动中国文化传播理论体系的发展。
              <br><br>
              基于此，"基于多模态人工智能的湖湘文化数智化传播系统"的设计理念应运而生，旨在填补当前文化传播领域的技术空白，并解决一些亟待解决的难题。该系统通过整合全球多元化的数据源，结合跨时空、跨语种的分析模型，能全面且系统地评估湖湘文化在全球范围内的传播效果。基于此，还引入了多模态人工智能技术，极大地提升了系统的精准度和全面性。
              <br><br>
              此外，该系统还通过优化界面设计，在文化传播中融合VR、沉浸式体验等前沿技术，以优化用户体验，提升传播效果，使得文化传播内容更加生动和富有冲击力。系统能够通过获取用户的访问历史和关注内容，为用户制作个性化的画像，提供定制化的文化内容推荐。平台还将使用大模型生成图文结合的宣传内容，结合活动主题、地区特色和用户需求，为湖湘文化的传播与区域经济发展做出积极贡献。
              <br><br>
              通过多模态人工智能技术的深度应用，本系统不仅为湖湘文化的国际传播提供了精准的数据支持和理论指导，更为文化的深度传播提供了坚实的技术保障。同时本系统将湖湘文化元素细致分类成五大模块，以此帮助更多湖湘文化爱好者从多方面深入了解湖湘文化的内涵和特色。通过本系统，文化研究者与文化传播者可以根据系统的评估结果，制定更加有效的传播策略，推动湖湘文化在国际的普及和发展。这一成果不仅为制定更加精准、科学的湖湘文化传播策略提供了坚实的数据支撑与理论指导，更为推动湖湘文化在全球范围内的传播与影响力提升贡献了重要力量。
            </p>
          </div>
        </el-card>
      </div>

      <!-- 背景介绍 -->
      <div v-show="currentTab === 1" class="content-section">
        <el-card class="intro-card" shadow="hover">
          <div class="card-header">
            <h2>背景介绍</h2>
            <div class="divider"></div>
          </div>
          <div class="card-content">
            <p>
              近年来，随着中国综合国力的提升和国际话语权的增强，文化自信和文化"走出去"战略成为国家发展的重要议题之一。习近平总书记在中央政治局第三十次集体学习时强调，"要更好推动中华文化走出去，以文载道、以文传声、以文化人，向世界阐释推介更多具有中国特色、体现中国精神、蕴藏中国智慧的优秀文化。"湖湘文化作为中华文化的重要组成部分，其独特的地域特色、深厚的历史积淀和丰富的文化内涵，使其在全球范围内的关注度逐渐上升。
              <br><br>
              湖湘文化的形成过程经历了复杂的历史演变：先秦、两汉时期的楚文化对其具有深远影响，而南北朝及唐宋以来，大规模的移民迁徙带来了中原文化的深度融合与发展，逐渐形成了周敦颐的理学思想、王夫之的"经世致用"理念以及魏源的"睁眼看世界"意识，塑造了湖湘文化"敢为人先、经世致用"的独特精神气质。这一文化形态不仅在中国历史上占据重要地位，更在近现代历史中凭借"湖南人才半国中"的影响力和"无湘不成军"的盛誉，推动了中国社会变革和思想解放。
              <br><br>
              然而，如何借助现代化的传播手段和技术手段，更好地展示湖湘文化的魅力、提升其国际影响力，成为当前学界和业界亟待解决的问题。党的二十大报告明确指出，要"着力提升国际传播效能 促进文明交流互鉴"，推动具有地域特色的中华文化更好地走向世界。为此，加强湖湘文化的国际传播能力建设，特别是运用现代数据分析和技术手段，系统地评估其传播效果及策略，具有重要的现实意义。
              <br><br>
              随着新媒体平台和数字信息技术的快速发展，社交媒体、短视频平台等新兴传播渠道突破了传统传播路径的局限，为湖湘文化走向世界提供了新的契机。近年来，学者们开始将机器学习、自然语言处理等技术应用于文化传播的效果评估中，如通过情感分析、文本挖掘、话语分析等手段，深入研究文化在不同语言环境和文化背景中的接受度及传播效果。然而，目前湖湘文化的国际传播研究主要集中在某些单个文化作品或现象的分析上，缺乏系统化的传播效果评估模型，难以全面反映湖湘文化在全球范围内的传播情况。为应对这一挑战，本系统应运而生。
            </p>
          </div>
        </el-card>
      </div>

      <!-- 技术路线 -->
      <div v-show="currentTab === 2" class="content-section">
        <el-card class="intro-card" shadow="hover">
          <div class="card-header">
            <h2>技术路线</h2>
            <div class="divider"></div>
          </div>
          <div class="card-content">
            <div class="tech-pagination">
              <div class="tech-page" v-for="(item, index) in techItems" :key="index" v-show="currentPage === index">
                <div class="tech-card">
                  <h3>{{ item.title }}</h3>
                  <p v-html="item.content"></p>
                </div>
              </div>
              <div class="pagination-controls">
                <el-pagination
                  background
                  layout="prev, pager, next"
                  :total="techItems.length * 10"
                  :page-size="10"
                  :current-page="currentPage + 1"
                  @current-change="handlePageChange"
                />
              </div>
            </div>
          </div>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script>
import KgRagImage from '@/assets/background/KG-RAG.jpg'
import ConfedeImage from '@/assets/background/ConFEDE结构图.jpg'
import LdaImage from '@/assets/background/LDA算法模型.jpg'
import CfImage from '@/assets/background/协同过滤.jpg'

export default {
  name: 'BackgroundIntro',
  data() {
    return {
      currentTab: 0,
      currentPage: 0,
      tabs: ['项目简介', '背景介绍', '技术路线'],
      techItems: [
        {
          title: '1. 数据采集与处理',
          content: '本项目采用多源数据采集策略，通过以下方式获取湖湘文化相关数据：<br><br>（1）社交媒体数据采集：利用网络爬虫和开发者API从国际主流社交媒体平台（如小红书、微博、X、Youtube等）获取用户评论、互动数据，分析用户对湖湘文化的关注点和情感倾向。<br><br>（2）官方数据整合：从湖南省人民政府门户网站、湖南省文化和旅游厅等官方渠道获取湖湘非遗名录项目、文化政策文件等权威数据。<br><br>（3）百科类数据补充：通过百度百科、维基百科等平台获取湖湘文化的背景知识、历史沿革等结构化数据。<br><br>（4）微信公众号内容采集：收集湖湘文化相关的公众号文章、视频等内容，获取更丰富的文化传播素材。<br><br>在数据处理方面，采用以下技术手段：数据清洗、数据标准化、数据分类、数据存储。'
        },
        {
          title: '2. 知识图谱与检索增强生成',
          content: `
            <div style="display: flex; align-items: start; gap: 20px;">
              <img src="${KgRagImage}" alt="KG-RAG架构图" style="width: 25%; object-fit: contain;">
              <div>
                <p style="margin-bottom: 15px;">① <strong>湖湘文化知识图谱构建</strong><br>
                通过多渠道获取湖湘文化相关数据，设计本体结构，进行实体与关系抽取，构建高质量三元组，存入neo4j数据库，实现结构化的知识表达与高效检索。</p>
                
                <p style="margin-bottom: 15px;">② <strong>检索增强生成（RAG）</strong><br>
                基于大语言模型，结合检索组件，提升问答的准确性与可靠性。针对湖湘文化专业知识，通过检索增强保证回答的专业性与全面性。</p>
                
                <p>③ <strong>图模互补</strong><br>
                知识图谱提供结构化存储与逻辑推理，RAG提供自然语言生成与语义检索，二者结合提升问答系统的准确性、覆盖度和可解释性。</p>
              </div>
            </div>`
        },
        {
          title: '3. 多模态情感分析',
          content: `
            <div style="display: flex; flex-direction: column; gap: 20px;">
              <div style="display: flex; align-items: start; gap: 20px;">
                <div style="width: 90%;">
                  <p style="margin-bottom: 15px;">① <strong>基于ConFEDE的多模态情感分析模型</strong><br>
                  采用结合对比学习和特征分解的框架，能够同时处理文本、图像和音频等多模态数据。通过多模态预测损失、单模态预测损失和对比损失三种损失函数的优化，实现了对湖湘文化相关内容的精准情感分析。</p>
                  
                  <p>② <strong>基于Qwen2.5-7B-Instruct的情感分析</strong><br>
                  采用参数高效微调方案，结合LoRA低秩适配器技术，在Qwen2.5-7B-Instruct大模型基础上进行优化。实验表明，微调后的模型在情感分析任务上准确率可达98%以上，显著优于未经微调的模型。</p>
                </div>
                <div style="width: 55%; display: flex; flex-direction: column; gap: 10px;margin-top: -40px;">
                  <img src="${ConfedeImage}" alt="ConFEDE结构图" style="width: 100%; object-fit: contain;">
                </div>
              </div>
              <div style="background: #f5f5f5; padding: 15px; border-radius: 8px;margin-top: -20px;">
                <p style="margin-top: 0px; margin-bottom: 0;"><strong>实验结果：</strong>在weibo_senti_100k数据集上，经过微调的大模型（包括Qwen2.5-7B-Instruct、DeepSeek-R1-Distill-Qwen-7B、Meta-Llama-3.1-8B-Instruct）均表现出色，准确率达到98.3%以上，显著优于未经微调的基线模型。</p>
              </div>
            </div>`
        },
        {
          title: '4. 基于LDA的主题提取模型',
          content: `
            <div style="display: flex; flex-direction: column; gap: 20px;">
              <div style="display: flex; align-items: start; gap: 20px;">
                <div style="width: 60%;">
                  采用LDA（Latent Dirichlet Allocation，潜在狄利克雷分配）作为核心建模方法，通过概率生成方式建模文本数据，假设每篇文档由多个主题的混合构成，每个主题由一组词汇的概率分布表示，从而有效揭示文档集合中的主题模式。</p>
                  
                  <p style="margin-bottom: 15px;"><strong>主要特点：</strong>• 通过文档-主题分布和主题-词语分布进行建模<br>
                  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• 采用变分EM算法进行模型训练和参数优化<br>
                  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• 能够有效识别评论数据中的高频主题<br>
                  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• 可用于热点追踪和情感分类的先验分析</p>
                </div>
                <div style="width: 40%; display: flex; flex-direction: column; gap: 10px;">
                  <img src="${LdaImage}" alt="LDA算法模型" style="width: 100%; object-fit: contain;margin-top:50px;">
                  <p style="text-align: center; margin: 0; font-size: 14px; color: #666;">图5 LDA算法模型</p>
                </div>
              </div>
              <div style="background: #f5f5f5; padding: 15px; border-radius: 8px;">
                <p style="margin: 0;"><strong>应用效果：</strong>实验结果表明，LDA在本项目的数据集上能够较好地区分不同情感倾向的评论主题，为情感分析任务提供有力支持，有效提升了湖湘文化传播效果分析的准确性。</p>
              </div>
            </div>`
        },
        {
          title: '5. 因果推理与情感走势预测',
          content: `
            <div style="display: flex; align-items: start; gap: 30px;">
              <div style="width: 50%;">
                <p style="margin-bottom: -10px;">① <strong>基于CausalImpact的因果推理模型</strong></p>
                <p style="margin-bottom: -10px;">采用CausalImpact作为核心方法，基于贝叶斯结构时间序列模型（BSTS）评估传播事件对情感走势的影响。模型结构包含：</p>
                <ul style="list-style-type: none; padding-left: 20px; margin-bottom: 5px;">
                  <li>• 局部线性趋势项：刻画长期变化趋势</li>
                  <li>• 周期性成分：反映7天周期的舆论起伏</li>
                  <li>• 协变量：包含节假日、特定事件等因素</li>
                  <li>• 随机扰动：建模数据的不确定性</li>
                </ul>
                <p>采用MCMC方法进行参数估计，通过10,000次采样实现稳健的因果效应推断，并使用后验概率验证影响显著性。</p>
              </div>
              
              <div style="width: 50%;">
                <p style="margin-bottom: -10px;">② <strong>基于LSTM的情感走势预测模型</strong></p>
                <p style="margin-bottom: -10px;">采用双向LSTM深度时序网络实现多步预测，挖掘情感数据的时间依赖性。主要特点：</p>
                <ul style="list-style-type: none; padding-left: 20px; margin-bottom: 5px;">
                  <li>• 双层LSTM编码器（256隐藏单元）</li>
                  <li>• 时间注意力机制增强特征提取</li>
                  <li>• 单层LSTM解码器预测未来7天走势</li>
                  <li>• 采用AdamW优化器，学习率1e-3</li>
                </ul>
                <p style="background: #f5f5f5; padding: 10px; border-radius: 5px;">
                  <strong>实验效果：</strong>在验证集上MAE达到0.148，相比ARIMA模型预测误差降低37.2%，展现出优越的预测性能。
                </p>
              </div>
            </div>`
        },
        {
          title: '6. 用户画像和兴趣预测',
          content: `
            <div style="display: flex; flex-direction: column; gap: 20px;">
              <div style="width: 50%; text-align: center; margin-bottom: -40px;margin-top: -40px;margin-left: 250px;">
                <img src="${CfImage}" alt="协同过滤示意图" style="width: 80%; object-fit: contain;">
              </div>
              <div style="display: flex; flex-direction: column; gap: 15px;">
                <p style="margin: 0;"><strong>协同过滤推荐模型</strong><br>
                采用协同过滤（Collaborative Filtering）方法，结合用户相似度计算和基于评分数据的兴趣预测，构建混合推荐模型。核心思想是基于相似用户在历史上通常具有相似的兴趣偏好这一特性。</p>
                
                  <p style="margin: 0;margin-top: -10px;"><strong>技术特点：</strong> • 使用皮尔逊相关系数计算用户相似度</p>
                  <ul style="list-style-type: none; padding-left: 20px; margin-top: -10px;">
                    <li>&nbsp;&nbsp;&nbsp;&nbsp;• 基于邻域的评分预测方法</li>
                    <li>&nbsp;&nbsp;&nbsp;&nbsp;• 考虑用户评分偏差的归一化处理</li>
                    <li>&nbsp;&nbsp;&nbsp;&nbsp;• 加权计算最终推荐分数</li>
                  </ul>
<p style="margin-top: -30px; margin-bottom: 0;"><strong>应用效果：</strong>该方法在湖湘文化相关数据集上的兴趣预测效果显著，相比基准模型误差降低明显，能够更准确地捕捉用户偏好，提供个性化的文化内容推荐。</p>
            
            
              </div>
            </div>`
        }
      ]
    };
  },
  methods: {
    handlePageChange(page) {
      this.currentPage = page - 1;
    }
  }
};
</script>

<style scoped lang="scss">
.background-container {
  padding: 20px;
  height:655px;
  max-width: 1200px;
  margin: 0 auto;
}

.bookmark-nav {
  display: flex;
  justify-content: center;
  margin-bottom: 0px;
  position: relative;
  padding: 0 20px;

  &::before {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 2px;
    z-index: 1;
  }
}

.bookmark-item {
  position: relative;
  padding: 12px 30px;
  margin: 0 10px;
  background: #f5f5f5;
  border-radius: 8px 8px 0 0;
  cursor: pointer;
  transition: all 0.3s ease;
  z-index: 2;
  font-size: 16px;
  color: #666;
  box-shadow: 0 -2px 5px rgba(0, 0, 0, 0.05);

  &:hover {
    background: #b71c1c;
    color: #fff;
  }

  &.active {
    background: #fff;
    color: #b71c1c;
    font-weight: bold;
    box-shadow: 0 -2px 5px rgba(0, 0, 0, 0.1);
    
    &::after {
      content: '';
      position: absolute;
      bottom: -2px;
      left: 0;
      right: 0;
      height: 2px;
      background: #b71c1c;
    }
  }
}

.content-wrapper {
  position: relative;
  min-height: 400px;
}

.content-section {
  animation: fadeIn 0.5s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.intro-card {
  margin-bottom: 30px;
  border-radius: 8px;
  overflow: hidden;
  transition: all 0.3s ease;

  &:hover {
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
  }
}

.card-header {
  padding: 20px;
  background: linear-gradient(145deg, #ffffff, #fff);
  border-bottom: 1px solid #eee;

  h2 {
    color: #b71c1c;
    font-size: 24px;
    margin: 0;
    font-weight: bold;
  }

  .divider {
    width: 50px;
    height: 3px;
    background: linear-gradient(90deg, #b71c1c 0%, #ff6b6b 100%);
    margin-top: 10px;
    border-radius: 2px;
  }
}

.card-content {
  padding: 20px;

  p {
    font-size: 16px;
    line-height: 1.8;
    color: #333;
    text-align: justify;
    margin: 0;
  }
}

.tech-pagination {
  min-height: 400px;
  position: relative;
}

.tech-page {
  animation: fadeIn 0.5s ease;
}

.tech-card {
  background: #fff;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;

  &:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
  }

  h3 {
    color: #b71c1c;
    font-size: 20px;
    margin-bottom: 20px;
    font-weight: bold;
  }

  p {
    font-size: 15px;
    line-height: 1.7;
    color: #555;
  }
}

.pagination-controls {
  margin-top: 20px;
  margin-bottom: -20px;
  display: flex;
  justify-content: center;

  :deep(.el-pagination) {
    .el-pager li {
      background: #f5f5f5;
      color: #666;
      
      &.active {
        background: #b71c1c;
        color: #fff;
      }
    }
    
    .btn-prev, .btn-next {
      background: #f5f5f5;
      color: #666;
      
      &:hover {
        color: #b71c1c;
      }
    }
  }
}

@media (max-width: 768px) {
  .background-container {
    padding: 10px;
  }

  .bookmark-nav {
    flex-wrap: wrap;
    padding: 0 10px;
  }

  .bookmark-item {
    padding: 8px 15px;
    margin: 5px;
    font-size: 14px;
  }

  .card-header h2 {
    font-size: 20px;
  }

  .card-content p {
    font-size: 14px;
  }

  .tech-card {
    padding: 20px;
    
    h3 {
      font-size: 18px;
    }
    
    p {
      font-size: 14px;
    }
  }
}
</style>
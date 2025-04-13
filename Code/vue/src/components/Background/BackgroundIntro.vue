
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
            <h2>{{ $t('xiang-mu-jian-jie') }}</h2>
            <div class="divider"></div>
          </div>
          <div class="card-content">
            <p>
              {{ $t('tui-dong-zhong-hua-wen-hua-zou-chu-qu-ti-sheng-zhong-hua-wen-hua-ying-xiang-li-xu-yao-jiang-zhong-hua-wen-hua-dui-wai-chuan-bo-nei-rong-de-feng-fu-xing-chuan-bo-tu-jing-de-duo-yang-xing-wen-hua-ying-xiang-de-chi-jiu-xing-jin-hang-you-ji-zheng-he-qi-zhong-hu-nan-bu-jin-you-yuan-gu-wen-hua-de-feng-hou-yi-cun-huan-you-zhuo-chuan-tong-wen-hua-de-shou-zheng-chuang-xin-geng-you-jin-dai-wen-hua-de-zhuo-yue-jian-shu-yin-ci-tui-dong-wen-hua-chuan-bo-yu-hu-xiang-wen-hua-er-yan-bu-jin-ke-yi-shi-qi-zuo-wei-zhong-hua-wen-hua-de-zhong-yao-zu-cheng-bu-fen-bei-geng-duo-guo-ji-she-hui-le-jie-ye-neng-gou-wei-qu-yu-wen-hua-guo-ji-chuan-bo-ji-lei-shi-jian-jing-yan-cong-er-feng-fu-quan-qiu-hua-shi-dai-de-wen-hua-duo-yang-xing-bing-tui-dong-zhong-guo-wen-hua-chuan-bo-li-lun-ti-xi-de-fa-zhan') }}
              <br><br>
              {{ $t('ji-yu-ci-ji-yu-duo-mo-tai-ren-gong-zhi-neng-de-hu-xiang-wen-hua-shu-zhi-hua-chuan-bo-xi-tong-de-she-ji-li-nian-ying-yun-er-sheng-zhi-zai-tian-bu-dang-qian-wen-hua-chuan-bo-ling-yu-de-ji-shu-kong-bai-bing-jie-jue-yi-xie-ji-dai-jie-jue-de-nan-ti-gai-xi-tong-tong-guo-zheng-he-quan-qiu-duo-yuan-hua-de-shu-ju-yuan-jie-he-kua-shi-kong-kua-yu-zhong-de-fen-xi-mo-xing-neng-quan-mian-qie-xi-tong-di-ping-gu-hu-xiang-wen-hua-zai-quan-qiu-fan-wei-nei-de-chuan-bo-xiao-guo-ji-yu-ci-huan-yin-ru-le-duo-mo-tai-ren-gong-zhi-neng-ji-shu-ji-da-di-ti-sheng-le-xi-tong-de-jing-zhun-du-he-quan-mian-xing') }}
              <br><br>
              {{ $t('ci-wai-gai-xi-tong-huan-tong-guo-you-hua-jie-mian-she-ji-zai-wen-hua-chuan-bo-zhong-rong-he-vr-chen-jin-shi-ti-yan-deng-qian-yan-ji-shu-yi-you-hua-yong-hu-ti-yan-ti-sheng-chuan-bo-xiao-guo-shi-de-wen-hua-chuan-bo-nei-rong-geng-jia-sheng-dong-he-fu-you-chong-ji-li-xi-tong-neng-gou-tong-guo-huo-qu-yong-hu-de-fang-wen-li-shi-he-guan-zhu-nei-rong-wei-yong-hu-zhi-zuo-ge-xing-hua-de-hua-xiang-ti-gong-ding-zhi-hua-de-wen-hua-nei-rong-tui-jian-ping-tai-huan-jiang-shi-yong-da-mo-xing-sheng-cheng-tu-wen-jie-he-de-xuan-chuan-nei-rong-jie-he-huo-dong-zhu-ti-di-qu-te-se-he-yong-hu-xu-qiu-wei-hu-xiang-wen-hua-de-chuan-bo-yu-qu-yu-jing-ji-fa-zhan-zuo-chu-ji-ji-gong-xian') }}
              <br><br>
              {{ $t('tong-guo-duo-mo-tai-ren-gong-zhi-neng-ji-shu-de-shen-du-ying-yong-ben-xi-tong-bu-jin-wei-hu-xiang-wen-hua-de-guo-ji-chuan-bo-ti-gong-le-jing-zhun-de-shu-ju-zhi-chi-he-li-lun-zhi-dao-geng-wei-wen-hua-de-shen-du-chuan-bo-ti-gong-le-jian-shi-de-ji-shu-bao-zhang-tong-shi-ben-xi-tong-jiang-hu-xiang-wen-hua-yuan-su-xi-zhi-fen-lei-cheng-wu-da-mo-kuai-yi-ci-bang-zhu-geng-duo-hu-xiang-wen-hua-ai-hao-zhe-cong-duo-fang-mian-shen-ru-le-jie-hu-xiang-wen-hua-de-nei-han-he-te-se-tong-guo-ben-xi-tong-wen-hua-yan-jiu-zhe-yu-wen-hua-chuan-bo-zhe-ke-yi-gen-ju-xi-tong-de-ping-gu-jie-guo-zhi-ding-geng-jia-you-xiao-de-chuan-bo-ce-lve-tui-dong-hu-xiang-wen-hua-zai-guo-ji-de-pu-ji-he-fa-zhan-zhe-yi-cheng-guo-bu-jin-wei-zhi-ding-geng-jia-jing-zhun-ke-xue-de-hu-xiang-wen-hua-chuan-bo-ce-lve-ti-gong-le-jian-shi-de-shu-ju-zhi-cheng-yu-li-lun-zhi-dao-geng-wei-tui-dong-hu-xiang-wen-hua-zai-quan-qiu-fan-wei-nei-de-chuan-bo-yu-ying-xiang-li-ti-sheng-gong-xian-le-zhong-yao-li-liang-0') }}
            </p>
          </div>
        </el-card>
      </div>

      <!-- 背景介绍 -->
      <div v-show="currentTab === 1" class="content-section">
        <el-card class="intro-card" shadow="hover">
          <div class="card-header">
            <h2>{{ $t('bei-jing-jie-shao-0') }}</h2>
            <div class="divider"></div>
          </div>
          <div class="card-content">
            <p>
              {{ $t('jin-nian-lai-sui-zhuo-zhong-guo-zong-he-guo-li-de-ti-sheng-he-guo-ji-hua-yu-quan-de-zeng-qiang-wen-hua-zi-xin-he-wen-hua-zou-chu-qu-zhan-lve-cheng-wei-guo-jia-fa-zhan-de-zhong-yao-yi-ti-zhi-yi-xi-jin-ping-zong-shu-ji-zai-zhong-yang-zheng-zhi-ju-di-san-shi-ci-ji-ti-xue-xi-shi-qiang-tiao-yao-geng-hao-tui-dong-zhong-hua-wen-hua-zou-chu-qu-yi-wen-zai-dao-yi-wen-chuan-sheng-yi-wen-hua-ren-xiang-shi-jie-chan-shi-tui-jie-geng-duo-ju-you-zhong-guo-te-se-ti-xian-zhong-guo-jing-shen-yun-cang-zhong-guo-zhi-hui-de-you-xiu-wen-hua-hu-xiang-wen-hua-zuo-wei-zhong-hua-wen-hua-de-zhong-yao-zu-cheng-bu-fen-qi-du-te-de-di-yu-te-se-shen-hou-de-li-shi-ji-dian-he-feng-fu-de-wen-hua-nei-han-shi-qi-zai-quan-qiu-fan-wei-nei-de-guan-zhu-du-zhu-jian-shang-sheng-1') }}
              <br><br>
              {{ $t('hu-xiang-wen-hua-de-xing-cheng-guo-cheng-jing-li-le-fu-za-de-li-shi-yan-bian-xian-qin-liang-han-shi-qi-de-chu-wen-hua-dui-qi-ju-you-shen-yuan-ying-xiang-er-nan-bei-zhao-ji-tang-song-yi-lai-da-gui-mo-de-yi-min-qian-xi-dai-lai-le-zhong-yuan-wen-hua-de-shen-du-rong-he-yu-fa-zhan-zhu-jian-xing-cheng-le-zhou-dun-yi-de-li-xue-si-xiang-wang-fu-zhi-de-jing-shi-zhi-yong-li-nian-yi-ji-wei-yuan-de-zheng-yan-kan-shi-jie-yi-shi-su-zao-le-hu-xiang-wen-hua-gan-wei-ren-xian-jing-shi-zhi-yong-de-du-te-jing-shen-qi-zhi-zhe-yi-wen-hua-xing-tai-bu-jin-zai-zhong-guo-li-shi-shang-zhan-ju-zhong-yao-di-wei-geng-zai-jin-xian-dai-li-shi-zhong-ping-jie-hu-nan-ren-cai-ban-guo-zhong-de-ying-xiang-li-he-wu-xiang-bu-cheng-jun-de-sheng-yu-tui-dong-le-zhong-guo-she-hui-bian-ge-he-si-xiang-jie-fang') }}
              <br><br>
              {{ $t('ran-er-ru-he-jie-zhu-xian-dai-hua-de-chuan-bo-shou-duan-he-ji-shu-shou-duan-geng-hao-di-zhan-shi-hu-xiang-wen-hua-de-mei-li-ti-sheng-qi-guo-ji-ying-xiang-li-cheng-wei-dang-qian-xue-jie-he-ye-jie-ji-dai-jie-jue-de-wen-ti-dang-de-er-shi-da-bao-gao-ming-que-zhi-chu-yao-zhuo-li-ti-sheng-guo-ji-chuan-bo-xiao-neng-cu-jin-wen-ming-jiao-liu-hu-jian-tui-dong-ju-you-di-yu-te-se-de-zhong-hua-wen-hua-geng-hao-di-zou-xiang-shi-jie-wei-ci-jia-qiang-hu-xiang-wen-hua-de-guo-ji-chuan-bo-neng-li-jian-she-te-bie-shi-yun-yong-xian-dai-shu-ju-fen-xi-he-ji-shu-shou-duan-xi-tong-di-ping-gu-qi-chuan-bo-xiao-guo-ji-ce-lve-ju-you-zhong-yao-de-xian-shi-yi-yi') }}
              <br><br>
              {{ $t('sui-zhuo-xin-mei-ti-ping-tai-he-shu-zi-xin-xi-ji-shu-de-kuai-su-fa-zhan-she-jiao-mei-ti-duan-shi-pin-ping-tai-deng-xin-xing-chuan-bo-qu-dao-tu-po-le-chuan-tong-chuan-bo-lu-jing-de-ju-xian-wei-hu-xiang-wen-hua-zou-xiang-shi-jie-ti-gong-le-xin-de-qi-ji-jin-nian-lai-xue-zhe-men-kai-shi-jiang-ji-qi-xue-xi-zi-ran-yu-yan-chu-li-deng-ji-shu-ying-yong-yu-wen-hua-chuan-bo-de-xiao-guo-ping-gu-zhong-ru-tong-guo-qing-gan-fen-xi-wen-ben-wa-jue-hua-yu-fen-xi-deng-shou-duan-shen-ru-yan-jiu-wen-hua-zai-bu-tong-yu-yan-huan-jing-he-wen-hua-bei-jing-zhong-de-jie-shou-du-ji-chuan-bo-xiao-guo-ran-er-mu-qian-hu-xiang-wen-hua-de-guo-ji-chuan-bo-yan-jiu-zhu-yao-ji-zhong-zai-mou-xie-dan-ge-wen-hua-zuo-pin-huo-xian-xiang-de-fen-xi-shang-que-fa-xi-tong-hua-de-chuan-bo-xiao-guo-ping-gu-mo-xing-nan-yi-quan-mian-fan-ying-hu-xiang-wen-hua-zai-quan-qiu-fan-wei-nei-de-chuan-bo-qing-kuang-wei-ying-dui-zhe-yi-tiao-zhan-ben-xi-tong-ying-yun-er-sheng') }}
            </p>
          </div>
        </el-card>
      </div>

      <!-- 技术路线 -->
      <div v-show="currentTab === 2" class="content-section">
        <el-card class="intro-card" shadow="hover">
          <div class="card-header">
            <h2>{{ $t('ji-shu-lu-xian') }}</h2>
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
import { useI18n } from 'vue-i18n';
import { ref } from 'vue';

export default {
  name: 'BackgroundIntro',
  setup() {
    const { t, locale } = useI18n();

const currentTab = ref(0);
const currentPage = ref(0);

const tabs = locale.value === 'en'
  ? ['Project Introduction', 'Background Introduction', 'Technical Route']
  : ['项目简介', '背景介绍', '技术路线'];
    const techItems= [
        {
          title: locale.value==='en'?'1. Data collection and processing':'1. 数据采集与处理',
          content: locale.value==='en'?'This project adopts a multi-source data collection strategy to obtain data related to Huxiang culture in the following ways: <br><br>(1) Social media data collection: use web crawlers and developer APIs to obtain user comments and interaction data from international mainstream social media platforms (such as Xiaohongshu, Weibo, X, Youtube, etc.), and analyze users concerns and emotional tendencies towards Huxiang culture. <br><br>(2) Integration of official data: Authoritative data such as Huxiang intangible cultural heritage list items and cultural policy documents are obtained from the portal of the Hunan Provincial People\'s Government and the Hunan Provincial Department of Culture and Tourism. <br><br>(3) Encyclopedia data supplement: Obtain structured data such as background knowledge and historical evolution of Huxiang culture through Baidu Encyclopedia, Wikipedia and other platforms. <br><br>(4) WeChat public account content collection: collect official account articles, videos and other content related to Huxiang culture to obtain richer cultural communication materials. <br><br>In terms of data processing, the following technical means are adopted: data cleaning, data standardization, data classification, and data storage.':'本项目采用多源数据采集策略，通过以下方式获取湖湘文化相关数据：<br><br>（1）社交媒体数据采集：利用网络爬虫和开发者API从国际主流社交媒体平台（如小红书、微博、X、Youtube等）获取用户评论、互动数据，分析用户对湖湘文化的关注点和情感倾向。<br><br>（2）官方数据整合：从湖南省人民政府门户网站、湖南省文化和旅游厅等官方渠道获取湖湘非遗名录项目、文化政策文件等权威数据。<br><br>（3）百科类数据补充：通过百度百科、维基百科等平台获取湖湘文化的背景知识、历史沿革等结构化数据。<br><br>（4）微信公众号内容采集：收集湖湘文化相关的公众号文章、视频等内容，获取更丰富的文化传播素材。<br><br>在数据处理方面，采用以下技术手段：数据清洗、数据标准化、数据分类、数据存储。'
        },
        {
          title: locale.value==='en'?'2. Knowledge graph and retrieval enhancement generation':'2. 知识图谱与检索增强生成',
          content: locale.value==='en'?`<div style="display: flex; align-items: start; gap: 20px;">
              <img src="${KgRagImage}" alt="{{ $t('kgrag-jia-gou-tu') }}" style="width: 25%; object-fit: contain;">
              <div>
                <p style="margin-bottom: 15px;">① <strong>Construction of Huxiang cultural knowledge graph</strong><br>
                Through multi-channel acquisition of Huxiang culture-related data, ontology structure design, entity and relationship extraction, construction of high-quality triples, storage in neo4j database, to achieve structured knowledge expression and efficient retrieval.</p>
                
                <p style="margin-bottom: 15px;">② <strong>Retrieval Enhanced Generation (RAG)</strong><br>
                Based on the large language model and combined with the retrieval component, the accuracy and reliability of Q&A are improved. In view of the professional knowledge of Huxiang culture, the professionalism and comprehensiveness of the answers are enhanced through retrieval.</p>
                
                <p>③ <strong>Complement each other's images</strong><br>
               Knowledge graph provides structured storage and logical reasoning, and RAG provides natural language generation and semantic retrieval, which combine to improve the accuracy, coverage, and interpretability of the Q&A system.</p>
              </div>
            </div>`:`
            <div style="display: flex; align-items: start; gap: 20px;">
              <img src="${KgRagImage}" alt="{{ $t('kgrag-jia-gou-tu') }}" style="width: 25%; object-fit: contain;">
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
          title: locale.value==='en'?'3. Multimodal sentiment analysis':'3. 多模态情感分析',
          content: locale.value==='en'?`
            <div style="display: flex; flex-direction: column; gap: 20px;">
              <div style="display: flex; align-items: start; gap: 20px;">
                <div style="width: 90%;">
                  <p style="margin-bottom: 15px;">(1) <strong>Multimodal sentiment analysis model based on ConFEDE</strong><br>
                  Using a framework that combines contrastive learning and feature decomposition, it can process multimodal data such as text, images, and audio simultaneously. Through the optimization of three loss functions, multi-modal prediction loss, unimodal prediction loss and contrast loss, the accurate sentiment analysis of Huxiang culture-related content is realized.</p>
                  
                  <p>(2) <strong>Sentiment analysis based on Qwen2.5-7B-Instruct</strong><br>
                  The high-efficiency fine-tuning scheme of parameters, combined with LoRA low-rank adapter technology, was optimized on the basis of the Qwen2.5-7B-Instruct large model. Experiments show that the fine-tuned model has an accuracy of more than 98% on sentiment analysis tasks, which is significantly better than that of the unfine-tuned model.</p>
                </div>
                <div style="width: 55%; display: flex; flex-direction: column; gap: 10px;margin-top: -40px;">
                  <img src="${ConfedeImage}" alt="{{ $t('confede-jie-gou-tu') }}" style="width: 100%; object-fit: contain;">
                </div>
              </div>
              <div style="background: #f5f5f5; padding: 15px; border-radius: 8px;margin-top: -20px;">
                <p style="margin-top: 0px; margin-bottom: 0;"><strong>Experimental results:</strong> On the weibo_senti_100k dataset, the fine-tuned large models (including Qwen2.5-7B-Instruct, DeepSeek-R1-Distill-Qwen-7B, and Meta-Llama-3.1-8B-Instruct) all performed excellently, with an accuracy of more than 98.3%, which was significantly better than the unfine-tuned baseline model.</p>
              </div>
            </div>`:`
            <div style="display: flex; flex-direction: column; gap: 20px;">
              <div style="display: flex; align-items: start; gap: 20px;">
                <div style="width: 90%;">
                  <p style="margin-bottom: 15px;">① <strong>基于ConFEDE的多模态情感分析模型</strong><br>
                  采用结合对比学习和特征分解的框架，能够同时处理文本、图像和音频等多模态数据。通过多模态预测损失、单模态预测损失和对比损失三种损失函数的优化，实现了对湖湘文化相关内容的精准情感分析。</p>
                  
                  <p>② <strong>基于Qwen2.5-7B-Instruct的情感分析</strong><br>
                  采用参数高效微调方案，结合LoRA低秩适配器技术，在Qwen2.5-7B-Instruct大模型基础上进行优化。实验表明，微调后的模型在情感分析任务上准确率可达98%以上，显著优于未经微调的模型。</p>
                </div>
                <div style="width: 55%; display: flex; flex-direction: column; gap: 10px;margin-top: -40px;">
                  <img src="${ConfedeImage}" alt="{{ $t('confede-jie-gou-tu') }}" style="width: 100%; object-fit: contain;">
                </div>
              </div>
              <div style="background: #f5f5f5; padding: 15px; border-radius: 8px;margin-top: -20px;">
                <p style="margin-top: 0px; margin-bottom: 0;"><strong>实验结果：</strong>在weibo_senti_100k数据集上，经过微调的大模型（包括Qwen2.5-7B-Instruct、DeepSeek-R1-Distill-Qwen-7B、Meta-Llama-3.1-8B-Instruct）均表现出色，准确率达到98.3%以上，显著优于未经微调的基线模型。</p>
              </div>
            </div>`
        },
        {
          title: locale.value==='en'?'4. LDA-based topic extraction model':'4. 基于LDA的主题提取模型',
          content:locale.value==='en'?
`<divstyle="display：flex;flex-direction：column;gap：20px;">
<divstyle="display：flex;align-items：start;gap：20px;">
<divstyle="width：60%;">
Using Leda (Rattente Diriclette Alocation, latent Dirichlet allocation) as the core modeling method, the text data is modeled through probability generation, assuming that each document is composed of a mixture of multiple topics, and each topic is represented by a probability distribution of a set of words, so as to effectively reveal the topic patterns in the document collection. </p>

<pstyle="margin-bottom:15px;"> <strong>Key features:</strong> •Modeling through document-topic distribution and topic-word distribution<br>
• Variational Em algorithm was used for model training and <br>parameter optimization
• Able to effectively identify high-frequency topics in review data<br>
• Can be used for a priori analysis of hot spot tracking and sentiment classification</p>
</div>
<divstyle="width：40%;display：flex;flex-direction：column;gap：10px;">
<imgsrc="${LdaImage}"alt="LDA algorithm model" style="width:100%;object-fit:contain;margin-top:50px;">
<pstyle="text-align:center;margin:0;font-size:14px;color:#666;"> Figure 5 Leida algorithm model</p>
</div>
</div>
<divstyle="background：#f5f5f5;padding：15px;border-radius：8px;">
<pstyle="margin:0;"> <strong>application effect:</strong> The experimental results show that Leda can better distinguish the comment topics with different emotional tendencies on the dataset of this project, which provides strong support for the sentiment analysis task and effectively improves the accuracy of the analysis of the communication effect of Huxiang culture. </p>
</div>
</div>`: `
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
          title:locale.value==='en'? '5. Causal Reasoning and Sentiment Trend Prediction':'5. 因果推理与情感走势预测',
          content:locale.value==='en'?`
<div style="display: flex; align-items: start; gap: 30px;">
<div style="width: 50%;">
<p style="margin-bottom: -10px;">(1) <strong>CausalImpact-based causal inference model</strong></p>
<p style="margin-bottom: -10px;" > CausalImpact was used as the core method to evaluate the impact of propagation events on sentiment trend based on Bayesian structure time series model (BSTS). The model structure contains:</p>
<ul style="list-style-type: none; padding-left: 20px; margin-bottom: 5px;">
<li>• Local Linear Trend Term: Characterizes long-term trends</li>
<li>• Cyclical component: reflects the ups and downs of public opinion on a 7-day cycle</li>
<li>• Covariates: Include factors such as holidays, specific events, and more</li>
<li>• Stochastic perturbation: Uncertainty in the modeled data</li>
</ul>
<p>The MCMC method was used for parameter estimation, and the robust causal effect inference was achieved through 10,000 samples, and the significance of the impact was verified by using the posterior probability. </p>
</div>
<div style="width: 50%;">
<p style="margin-bottom: -10px;">(2) <strong>Sentiment trend prediction model based on LSTM</strong></p>
<p style="margin-bottom: -10px;"> bidirectional LSTM deep time series network is used to realize multi-step prediction and mine the temporal dependence of sentiment data. Key features:</p>
<ul style="list-style-type: none; padding-left: 20px; margin-bottom: 5px;">
<li>• Double-layer LSTM encoder (256 hidden units).</li>
<li>• Temporal attention mechanism enhances feature extraction</li>
<li>• Single-layer LSTM decoder predicts the trend in the next 7 days</li>
<li>• Using the AdamW optimizer, the learning rate is 1e-3</li>
</ul>
<p style="background: #f5f5f5; padding: 10px; border-radius: 5px;">
<strong>Experimental results:</strong> The MAE on the validation set reaches 0.148, which is 37.2% lower than the prediction error of the ARIMA model, showing superior prediction performance.
</p>
</div>
</div>`: `
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
          title:locale.value==='en'? '6. User Portrait and Interest Prediction':'6. 用户画像和兴趣预测',
          content:locale.value==='en'? `
<divstyle="display：flex;flex-direction：column;gap：20px;">
<divstyle="width：50%;text-align：center;margin-bottom：-40px;margin-top：-40px;margin-left：250px;">
<imgsrc="${CfImage}"alt="Collaborative filter diagram"style="width:80%;object-fit:contain;">
</div>
<divstyle="display：flex;flex-direction：column;gap：15px;">
<pstyle="margin:0;" > <strong>collaborative filtering recommendation model</strong><br>
The collaborative filtering (Kolabolativ Feltlin) method was used to construct a hybrid recommendation model by combining user similarity calculation and interest prediction based on scoring data. The core idea is based on the fact that similar users have historically had similar interests and preferences. </p>

<pstyle="margin:0;margin-top:-10px;"> <strong>Technical features:</strong> •Use the Pearson correlation coefficient to calculate user similarity</p>
<ulstyle="list-style-type：none;padding-left：20px;margin-top：-10px;">
<li>• Neighborhood-based scoring prediction method</li>
<li>&;nbsp;&nbsp;&nbsp;•Normalize treatment that takes into account user rating bias</li>
<li>&Bsp;&Embussp;•Weighted to calculate the final referral score</li>
</ul>
<pstyle="margin-top:-30px;margin-bottom:0;"> <strong>application effect:</strong> The method has a significant effect on interest prediction on Huxiang culture-related datasets, and the error is significantly reduced compared with the benchmark model, which can more accurately capture user preferences and provide personalized cultural content recommendations. </p>

</div>
</div>`:`
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
      const handlePageChange = (page) => {
    currentPage.value = page - 1;
  };

  return {
    currentTab,
    currentPage,
    tabs,
    techItems,
    t,
    handlePageChange
  };

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
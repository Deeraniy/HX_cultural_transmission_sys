<template>
  <div class="knowledge-graph-container">
    <div class="left-section">
      <div class="filter-section">
        <el-select
          v-model="selectedTags" 
          multiple 
          collapse-tags-tooltip
          placeholder="选择要显示的人物"
          class="tag-select"
          @change="handleTagsChange"
        >
          <el-option
            v-for="person in availablePersons" 
            :key="person" 
            :label="person"
            :value="person"
          />
        </el-select>
        <el-button type="primary" @click="resetFilter" class="reset-btn">
          重置筛选
        </el-button>
      </div>
    <div class="graph-wrapper">
    <svg ref="svg" :width="width" :height="height"></svg>
      <div class="zoom-controls">
        <button @click="zoomIn" class="zoom-btn">+</button>
        <button @click="zoomOut" class="zoom-btn">-</button>
        <button @click="resetZoom" class="zoom-btn">
          <i class="el-icon-refresh"></i>
        </button>
        </div>
      </div>
    </div>
    <div class="info-panel">
      <div v-if="selectedNode" class="node-details">
        <div class="node-header">
          <img v-if="getNodeImage(selectedNode.id)" :src="getNodeImage(selectedNode.id)" class="node-image" :alt="selectedNode.id">
          <h3>{{ selectedNode.id }}</h3>
        </div>
        <div class="divider"></div>
        <div class="detail-item">
          <span class="label">类型:</span>
          <span class="value">{{ getNodeType(selectedNode.group) }}</span>
        </div>
        <div class="detail-item">
          <span class="label">重要性:</span>
          <span class="value">{{ getImportanceLevel(selectedNode.size) }}</span>
        </div>
        <div class="detail-item">
          <span class="label">关系:</span>
          <div class="relationships">
            <pre class="relation-text">{{ getNodeRelationsText(selectedNode.id) }}</pre>
          </div>
        </div>
        <div class="detail-item">
          <span class="label">简介:</span>
          <p class="description">{{ getNodeDescription(selectedNode.id) }}</p>
        </div>
      </div>
      <div v-else class="empty-state">
        <div class="empty-icon">
          <i class="el-icon-info"></i>
        </div>
        <p>请点击图谱中的节点查看详细信息</p>
      </div>
    </div>
  </div>
</template>

<script>
import * as d3 from "d3";
import 毛泽东图片 from '@/assets/Red/毛泽东.jpg'
import 刘少奇图片 from '@/assets/Red/刘少奇.jpg'
import 贺龙图片 from '@/assets/Red/贺龙.jpg'
import 中国共产党图片 from '@/assets/Red/中国共产党.jpg'
import 八路军图片 from '@/assets/Red/八路军.jpg'
import 中华人民共和国图片 from '@/assets/Red/中华人民共和国.jpg'
import 红军长征图片 from '@/assets/Red/红军长征.jpg'
import 彭德怀图片 from '@/assets/Red/彭德怀.jpg'
import 向警予图片 from '@/assets/Red/向警予.jpg'
import 何叔衡图片 from '@/assets/Red/何叔衡.jpg'
import 任弼时图片 from '@/assets/Red/任弼时.jpg'
import 雷锋图片 from '@/assets/Red/雷锋.jpg'
import 罗荣桓图片 from '@/assets/Red/罗荣桓.jpg'
import 林伯渠图片 from '@/assets/Red/林伯渠.jpg'
import 百团大战图片 from '@/assets/Red/百团大战.jpg'
import 抗美援朝战争图片 from '@/assets/Red/抗美援朝战争.jpg'
import 辽沈战役图片 from '@/assets/Red/辽沈战役.jpg'
import 淮海战役图片 from '@/assets/Red/淮海战役.jpg'
import 西北战役图片 from '@/assets/Red/西北战役.jpg'
import 平江起义图片 from '@/assets/Red/平江起义.jpg'
import 遵义会议图片 from '@/assets/Red/遵义会议.jpg'
import 中华苏维埃共和国图片 from '@/assets/Red/中华苏维埃共和国.jpg'
import 中华人民共和国元帅图片 from '@/assets/Red/中华人民共和国元帅.jpg'
import 中共中央政治局委员图片 from '@/assets/Red/中共中央政治局委员.jpg'
import 国防部部长图片 from '@/assets/Red/国防部部长.jpg'
import 中共中央书记处书记图片 from '@/assets/Red/中共中央书记处书记.jpg'
import 中共中央军委委员图片 from '@/assets/Red/中共中央军委委员.jpg'
import 志愿军司令员图片 from '@/assets/Red/志愿军司令员.jpg'
import 庐山会议图片 from '@/assets/Red/庐山会议.jpg'
import 大跃进图片 from '@/assets/Red/大跃进.jpg'
import 军事系统高干会议图片 from '@/assets/Red/军事系统高干会议.jpg'
import 辛亥革命图片 from '@/assets/Red/辛亥革命.jpg'
import 中共一大图片 from '@/assets/Red/中共一大.jpg'
import 苏维埃革命图片 from '@/assets/Red/苏维埃革命.jpg'
import 反围剿图片 from '@/assets/Red/反围剿.jpg'
import 游击战图片 from '@/assets/Red/游击战.jpg'

export default {
  data() {
    return {
      width: 800,
      height: 600,
      selectedNode: null,
      zoomTransform: null,
      selectedTags: [],
      datajson: {
        nodes: [
          {
            id: "彭德怀",
            group: 1,
            size: 6
          },
          {
            id: "中华人民共和国元帅",
            group: 2,
            size: 4
          },
          {
            id: "中国人民志愿军司令员兼政治委员",
            group: 2,
            size: 4
          },
          {
            id: "中共中央军委副主席",
            group: 2,
            size: 4
          },
          {
            id: "国防部部长",
            group: 2,
            size: 4
          },
          {
            id: "中共中央政治局委员",
            group: 2,
            size: 4
          },
          {
            id: "中共中央书记处书记",
            group: 2,
            size: 4
          },
          {
            id: "中共中央军委委员",
            group: 2,
            size: 4
          },
          {
            id: "百团大战",
            group: 3,
            size: 3
          },
          {
            id: "抗美援朝战争",
            group: 3,
            size: 3
          },
          {
            id: "辽沈战役",
            group: 3,
            size: 3
          },
          {
            id: "淮海战役",
            group: 3,
            size: 3
          },
          {
            id: "西北战役",
            group: 3,
            size: 3
          },
          {
            id: "领导平江起义",
            group: 3,
            size: 3
          },
          {
            id: "参与长征，支持遵义会议确立毛泽东领导地位",
            group: 3,
            size: 3
          },
          {
            id: "指挥抗美援朝战争，取得重大胜利",
            group: 3,
            size: 3
          },
          {
            id: "主持1953年全国军事系统高干会议，推动军队正规化现代化建设",
            group: 3,
            size: 3
          },
          {
            id: "在庐山会议上对\"大跃进\"政策提出批评，后被打压",
            group: 3,
            size: 3
          },
          {
            id: "贺龙",
            group: 1,
            size: 6
          },
          {
            id: "中国人民解放军高级将领",
            group: 2,
            size: 4
          },
          {
            id: "中国共产党高级领导人",
            group: 2,
            size: 4
          },
          {
            id: "中华人民共和国国务院副总理",
            group: 2,
            size: 4
          },
          {
            id: "国家体委主任",
            group: 2,
            size: 4
          },
          {
            id: "国防委员会副主席",
            group: 2,
            size: 4
          },
          {
            id: "西南局第三书记",
            group: 2,
            size: 4
          },
          {
            id: "西南军区司令员",
            group: 2,
            size: 4
          },
          {
            id: "支持抗美援朝战争物资动员",
            group: 3,
            size: 3
          },
          {
            id: "推动国防工业和部队现代化建设",
            group: 3,
            size: 3
          },
          {
            id: "推进军队正规化、技术化、现代化",
            group: 3,
            size: 3
          },
          {
            id: "主持体育事业发展，推动\"发展体育运动，增强人民体质\"",
            group: 3,
            size: 3
          },
          {
            id: "何叔衡",
            group: 1,
            size: 6
          },
          {
            id: "剪辫反封建，带头响应辛亥革命",
            group: 4,
            size: 3
          },
          {
            id: "与毛泽东、蔡和森等共同在湖南组织共产党早期组织",
            group: 4,
            size: 3
          },
          {
            id: "出席中共一大，是党的创始人之一",
            group: 4,
            size: 3
          },
          {
            id: "为研究革命理论，年过五旬赴苏联留学并学会俄语",
            group: 4,
            size: 3
          },
          {
            id: "以\"忘家客\"自称，表达投身革命、无私无悔的志向",
            group: 4,
            size: 3
          },
          {
            id: "影响两个女儿加入革命并从事地下工作",
            group: 4,
            size: 3
          },
          {
            id: "家人多被捕牺牲，仍坚信\"共产党人不应死在病床上\"",
            group: 4,
            size: 3
          },
          {
            id: "提出\"不等群众上访，就先下访\"",
            group: 4,
            size: 3
          },
          {
            id: "调研随身携带布袋子、记事本、手电筒三件宝",
            group: 4,
            size: 3
          },
          {
            id: "第五次反围剿失败后坚守苏区开展游击战",
            group: 4,
            size: 3
          },
          {
            id: "突围失败后为保护同志，跳崖自尽，后被捕壮烈牺牲",
            group: 4,
            size: 3
          },
          {
            id: "誓言：\"要为苏维埃流尽最后一滴血\"",
            group: 4,
            size: 3
          },
          {
            id: "刘少奇",
            group: 1,
            size: 6
          },
          {
            id: "中国共产党和中华人民共和国的主要领导人之一",
            group: 2,
            size: 4
          },
          {
            id: "杰出的革命家",
            group: 2,
            size: 4
          },
          {
            id: "政治家",
            group: 2,
            size: 4
          },
          {
            id: "理论家",
            group: 2,
            size: 4
          },
          {
            id: "任弼时",
            group: 1,
            size: 6
          },
          {
            id: "伟大的马克思主义者",
            group: 2,
            size: 4
          },
          {
            id: "杰出的无产阶级革命家",
            group: 2,
            size: 4
          },
          {
            id: "组织家",
            group: 2,
            size: 4
          },
          {
            id: "中国共产党第一代领导集体成员",
            group: 2,
            size: 4
          },
          {
            id: "原名任培国",
            group: 2,
            size: 4
          },
          {
            id: "字二南",
            group: 2,
            size: 4
          },
          {
            id: "中共中央局副书记",
            group: 2,
            size: 4
          },
          {
            id: "中央组织部长",
            group: 2,
            size: 4
          },
          {
            id: "中共中央党校校长",
            group: 2,
            size: 4
          },
          {
            id: "青年团第一次全国代表大会主持人",
            group: 2,
            size: 4
          },
          {
            id: "两次被捕遭严刑拷打，两次被救",
            group: 3,
            size: 3
          },
          {
            id: "参与筹建中华苏维埃共和国",
            group: 3,
            size: 3
          },
          {
            id: "领导红六军团西征，与红三军会师",
            group: 3,
            size: 3
          },
          {
            id: "率红二、六军团与红四方面军会师并抵制分裂计划",
            group: 3,
            size: 3
          },
          {
            id: "协助毛泽东等指挥三大战役",
            group: 3,
            size: 3
          },
          {
            id: "雷锋",
            group: 1,
            size: 6
          },
          {
            id: "原工程兵工程某团汽车连班长",
            group: 2,
            size: 4
          },
          {
            id: "雷锋班",
            group: 2,
            size: 4
          },
          {
            id: "二等功1次",
            group: 2,
            size: 4
          },
          {
            id: "三等功2次",
            group: 2,
            size: 4
          },
          {
            id: "全军挂像英模",
            group: 2,
            size: 4
          },
          {
            id: "100位新中国成立以来感动中国人物",
            group: 2,
            size: 4
          },
          {
            id: "毛泽东",
            group: 1,
            size: 6
          },
          {
            id: "中国共产党主要缔造者和领导人",
            group: 2,
            size: 4
          },
          {
            id: "中国人民解放军主要缔造者和领导人",
            group: 2,
            size: 4
          },
          {
            id: "中华人民共和国主要缔造者和领导人",
            group: 2,
            size: 4
          },
          {
            id: "毛氏红烧肉",
            group: 5,
            size: 3
          },
          {
            id: "毛泽东故居",
            group: 5,
            size: 3
          },
          {
            id: "向警予",
            group: 1,
            size: 6
          },
          {
            id: "中国共产党唯一的女创始人",
            group: 2,
            size: 4
          },
          {
            id: "中国妇女运动的先驱",
            group: 2,
            size: 4
          },
          {
            id: "无产阶级革命家",
            group: 2,
            size: 4
          },
          {
            id: "教育家",
            group: 2,
            size: 4
          },
          {
            id: "早期女共产主义战士",
            group: 2,
            size: 4
          },
          {
            id: "罗荣桓",
            group: 1,
            size: 6
          },
          {
            id: "中国共产党党员",
            group: 2,
            size: 4
          },
          {
            id: "中华人民共和国开国元勋",
            group: 2,
            size: 4
          },
          {
            id: "中国十大元帅之一",
            group: 2,
            size: 4
          },
          {
            id: "军事家",
            group: 2,
            size: 4
          },
          {
            id: "原名罗慎镇",
            group: 2,
            size: 4
          },
          {
            id: "字雅怀",
            group: 2,
            size: 4
          },
          {
            id: "号宗人",
            group: 2,
            size: 4
          },
          {
            id: "林伯渠",
            group: 1,
            size: 6
          },
          {
            id: "杰出的政治家",
            group: 2,
            size: 4
          },
          {
            id: "延安五老之一",
            group: 2,
            size: 4
          },
          {
            id: "我党早期革命活动参与者",
            group: 2,
            size: 4
          }
        ],
        links: [
          {
            source: "刘少奇",
            target: "理论家",
            label: "人物身份"
          },
          {
            source: "何叔衡",
            target: "为研究革命理论，年过五旬赴苏联留学并学会俄语",
            label: "求学与国际活动"
          },
          {
            source: "任弼时",
            target: "中国共产党第一代领导集体成员",
            label: "人物身份"
          },
          {
            source: "雷锋",
            target: "原工程兵工程某团汽车连班长",
            label: "职务"
          },
          {
            source: "任弼时",
            target: "率红二、六军团与红四方面军会师并抵制分裂计划",
            label: "革命经历"
          },
          {
            source: "何叔衡",
            target: "誓言：\"要为苏维埃流尽最后一滴血\"",
            label: "坚持斗争"
          },
          {
            source: "贺龙",
            target: "国家体委主任",
            label: "职务经历"
          },
          {
            source: "彭德怀",
            target: "主持1953年全国军事系统高干会议，推动军队正规化现代化建设",
            label: "重要事迹"
          },
          {
            source: "彭德怀",
            target: "淮海战役",
            label: "重要战役"
          },
          {
            source: "林伯渠",
            target: "杰出的政治家",
            label: "人物身份"
          },
          {
            source: "何叔衡",
            target: "家人多被捕牺牲，仍坚信\"共产党人不应死在病床上\"",
            label: "家庭影响"
          },
          {
            source: "彭德怀",
            target: "抗美援朝战争",
            label: "重要战役"
          },
          {
            source: "任弼时",
            target: "领导红六军团西征，与红三军会师",
            label: "革命经历"
          },
          {
            source: "任弼时",
            target: "政治家",
            label: "人物身份"
          },
          {
            source: "贺龙",
            target: "中华人民共和国元帅",
            label: "主要身份"
          },
          {
            source: "罗荣桓",
            target: "无产阶级革命家",
            label: "人物身份"
          },
          {
            source: "贺龙",
            target: "中国人民解放军高级将领",
            label: "主要身份"
          },
          {
            source: "任弼时",
            target: "中共中央局副书记",
            label: "主要党政军职务"
          },
          {
            source: "贺龙",
            target: "推动国防工业和部队现代化建设",
            label: "新中国后重要政绩"
          },
          {
            source: "何叔衡",
            target: "第五次反围剿失败后坚守苏区开展游击战",
            label: "坚持斗争"
          },
          {
            source: "何叔衡",
            target: "以\"忘家客\"自称，表达投身革命、无私无悔的志向",
            label: "求学与国际活动"
          },
          {
            source: "贺龙",
            target: "推进军队正规化、技术化、现代化",
            label: "新中国后重要政绩"
          },
          {
            source: "何叔衡",
            target: "提出\"不等群众上访，就先下访\"",
            label: "基层调研"
          },
          {
            source: "雷锋",
            target: "二等功1次",
            label: "荣誉称号"
          },
          {
            source: "贺龙",
            target: "支持抗美援朝战争物资动员",
            label: "新中国后重要政绩"
          },
          {
            source: "林伯渠",
            target: "延安五老之一",
            label: "人物身份"
          },
          {
            source: "罗荣桓",
            target: "军事家",
            label: "人物身份"
          },
          {
            source: "罗荣桓",
            target: "中国十大元帅之一",
            label: "人物身份"
          },
          {
            source: "任弼时",
            target: "字二南",
            label: "别名"
          },
          {
            source: "林伯渠",
            target: "无产阶级革命家",
            label: "人物身份"
          },
          {
            source: "彭德怀",
            target: "中共中央政治局委员",
            label: "党内职务"
          },
          {
            source: "刘少奇",
            target: "杰出的革命家",
            label: "人物身份"
          },
          {
            source: "何叔衡",
            target: "调研随身携带布袋子、记事本、手电筒三件宝",
            label: "基层调研"
          },
          {
            source: "彭德怀",
            target: "百团大战",
            label: "重要战役"
          },
          {
            source: "任弼时",
            target: "中央组织部长",
            label: "主要党政军职务"
          },
          {
            source: "何叔衡",
            target: "影响两个女儿加入革命并从事地下工作",
            label: "家庭影响"
          },
          {
            source: "任弼时",
            target: "杰出的无产阶级革命家",
            label: "人物身份"
          },
          {
            source: "罗荣桓",
            target: "中国共产党党员",
            label: "人物身份"
          },
          {
            source: "彭德怀",
            target: "国防部部长",
            label: "职务"
          },
          {
            source: "彭德怀",
            target: "在庐山会议上对\"大跃进\"政策提出批评，后被打压",
            label: "重要事迹"
          },
          {
            source: "任弼时",
            target: "青年团第一次全国代表大会主持人",
            label: "主要党政军职务"
          },
          {
            source: "何叔衡",
            target: "出席中共一大，是党的创始人之一",
            label: "早期革命"
          },
          {
            source: "彭德怀",
            target: "中共中央书记处书记",
            label: "党内职务"
          },
          {
            source: "雷锋",
            target: "全军挂像英模",
            label: "荣誉称号"
          },
          {
            source: "向警予",
            target: "早期女共产主义战士",
            label: "人物身份"
          },
          {
            source: "毛泽东",
            target: "中国人民解放军主要缔造者和领导人",
            label: "主要身份"
          },
          {
            source: "任弼时",
            target: "两次被捕遭严刑拷打，两次被救",
            label: "革命经历"
          },
          {
            source: "向警予",
            target: "中国共产党唯一的女创始人",
            label: "人物身份"
          },
          {
            source: "贺龙",
            target: "中国共产党高级领导人",
            label: "主要身份"
          },
          {
            source: "彭德怀",
            target: "中共中央军委副主席",
            label: "职务"
          },
          {
            source: "彭德怀",
            target: "辽沈战役",
            label: "重要战役"
          },
          {
            source: "任弼时",
            target: "协助毛泽东等指挥三大战役",
            label: "革命经历"
          },
          {
            source: "毛泽东",
            target: "中华人民共和国主要缔造者和领导人",
            label: "主要身份"
          },
          {
            source: "毛泽东",
            target: "毛氏红烧肉",
            label: "文化印记"
          },
          {
            source: "毛泽东",
            target: "毛泽东故居",
            label: "纪念地"
          },
          {
            source: "向警予",
            target: "无产阶级革命家",
            label: "人物身份"
          },
          {
            source: "彭德怀",
            target: "领导平江起义",
            label: "重要事迹"
          },
          {
            source: "彭德怀",
            target: "参与长征，支持遵义会议确立毛泽东领导地位",
            label: "重要事迹"
          },
          {
            source: "贺龙",
            target: "国防委员会副主席",
            label: "职务经历"
          },
          {
            source: "任弼时",
            target: "参与筹建中华苏维埃共和国",
            label: "革命经历"
          },
          {
            source: "雷锋",
            target: "雷锋班",
            label: "荣誉称号"
          },
          {
            source: "罗荣桓",
            target: "中华人民共和国开国元勋",
            label: "人物身份"
          },
          {
            source: "罗荣桓",
            target: "原名罗慎镇",
            label: "别名"
          },
          {
            source: "贺龙",
            target: "主持体育事业发展，推动\"发展体育运动，增强人民体质\"",
            label: "新中国后重要政绩"
          },
          {
            source: "任弼时",
            target: "伟大的马克思主义者",
            label: "人物身份"
          },
          {
            source: "向警予",
            target: "教育家",
            label: "人物身份"
          },
          {
            source: "罗荣桓",
            target: "号宗人",
            label: "别名"
          },
          {
            source: "雷锋",
            target: "100位新中国成立以来感动中国人物",
            label: "荣誉称号"
          },
          {
            source: "任弼时",
            target: "原名任培国",
            label: "别名"
          },
          {
            source: "彭德怀",
            target: "西北战役",
            label: "重要战役"
          },
          {
            source: "任弼时",
            target: "中共中央党校校长",
            label: "主要党政军职务"
          },
          {
            source: "彭德怀",
            target: "中华人民共和国元帅",
            label: "职务"
          },
          {
            source: "罗荣桓",
            target: "政治家",
            label: "人物身份"
          },
          {
            source: "彭德怀",
            target: "中国人民志愿军司令员兼政治委员",
            label: "职务"
          },
          {
            source: "贺龙",
            target: "西南局第三书记",
            label: "职务经历"
          },
          {
            source: "林伯渠",
            target: "我党早期革命活动参与者",
            label: "人物身份"
          },
          {
            source: "刘少奇",
            target: "中国共产党和中华人民共和国的主要领导人之一",
            label: "人物身份"
          },
          {
            source: "何叔衡",
            target: "剪辫反封建，带头响应辛亥革命",
            label: "早期革命"
          },
          {
            source: "毛泽东",
            target: "中国共产党主要缔造者和领导人",
            label: "主要身份"
          },
          {
            source: "贺龙",
            target: "中共中央军委副主席",
            label: "职务经历"
          },
          {
            source: "何叔衡",
            target: "与毛泽东、蔡和森等共同在湖南组织共产党早期组织",
            label: "早期革命"
          },
          {
            source: "雷锋",
            target: "三等功2次",
            label: "荣誉称号"
          },
          {
            source: "彭德怀",
            target: "指挥抗美援朝战争，取得重大胜利",
            label: "重要事迹"
          },
          {
            source: "何叔衡",
            target: "突围失败后为保护同志，跳崖自尽，后被捕壮烈牺牲",
            label: "坚持斗争"
          },
          {
            source: "向警予",
            target: "中国妇女运动的先驱",
            label: "人物身份"
          },
          {
            source: "刘少奇",
            target: "政治家",
            label: "人物身份"
          },
          {
            source: "贺龙",
            target: "中华人民共和国国务院副总理",
            label: "职务经历"
          },
          {
            source: "罗荣桓",
            target: "字雅怀",
            label: "别名"
          },
          {
            source: "贺龙",
            target: "西南军区司令员",
            label: "职务经历"
          },
          {
            source: "彭德怀",
            target: "中共中央军委委员",
            label: "党内职务"
          },
          {
            source: "任弼时",
            target: "组织家",
            label: "人物身份"
          }
        ]
      },
      availablePersons: [
        "毛泽东",
        "刘少奇",
        "贺龙",
        "彭德怀",
        "向警予",
        "何叔衡",
        "任弼时",
        "雷锋",
        "罗荣桓",
        "林伯渠"
      ],
      filteredData: null,
      nodeDescriptions: {
        '毛泽东': '中国共产党和中华人民共和国的主要缔造者、领导人。',
        '刘少奇': '中国共产党和中华人民共和国主要领导人之一，杰出的革命家、政治家、理论家。',
        '贺龙': '中国人民解放军高级将领，中国共产党高级领导人。',
        '彭德怀': '中华人民共和国元帅，杰出的军事家、政治家。',
        '向警予': '中国共产党唯一的女创始人，中国妇女运动的先驱。',
        '何叔衡': '中国共产党创始人之一，杰出的无产阶级革命家。',
        '任弼时': '中国共产党第一代领导集体重要成员，杰出的革命家、组织家。',
        '雷锋': '全心全意为人民服务的光辉典范，时代楷模。',
        '罗荣桓': '中华人民共和国开国元勋，中国十大元帅之一。',
        '林伯渠': '杰出的政治家，延安五老之一。'
      }
    };
  },
  mounted() {
    this.initGraph();
  },
  methods: {
    handleTagsChange() {
      console.log('Tags changed:', this.selectedTags);
      this.updateGraph();
    },
    resetFilter() {
      this.selectedTags = [];
      this.updateGraph();
    },
    updateGraph() {
      if (this.selectedTags.length === 0) {
        this.filteredData = this.datajson;
      } else {
        // 首先找出所有选中人物的直接关联节点
        const directNodes = new Set();
        const directLinks = new Set();
        
        // 添加选中的人物节点
        this.selectedTags.forEach(personId => {
          directNodes.add(personId);
        });
        
        // 找出所有与选中人物直接相关的节点和连接
        this.datajson.links.forEach(link => {
          const sourceId = typeof link.source === 'object' ? link.source.id : link.source;
          const targetId = typeof link.target === 'object' ? link.target.id : link.target;
          
          if (this.selectedTags.includes(sourceId)) {
            directNodes.add(targetId);
            directLinks.add(link);
          }
          if (this.selectedTags.includes(targetId)) {
            directNodes.add(sourceId);
            directLinks.add(link);
          }
        });
        
        // 如果选择了多个人物，添加人物之间的关联
        if (this.selectedTags.length > 1) {
          this.datajson.links.forEach(link => {
            const sourceId = typeof link.source === 'object' ? link.source.id : link.source;
            const targetId = typeof link.target === 'object' ? link.target.id : link.target;
            
            // 如果连接的两端都在已选节点中，添加这个连接
            if (directNodes.has(sourceId) && directNodes.has(targetId)) {
              directLinks.add(link);
            }
          });
        }

        const filteredNodes = this.datajson.nodes.filter(node => 
          directNodes.has(node.id)
        );

        const filteredLinks = Array.from(directLinks);

        this.filteredData = {
          nodes: filteredNodes,
          links: filteredLinks
        };
      }
      
      this.$nextTick(() => {
        this.renderGraph(this.filteredData);
      });
    },
    initGraph() {
      this.filteredData = this.datajson;
      this.renderGraph(this.filteredData);
    },
    renderGraph(data) {
      d3.select(this.$refs.svg).selectAll("*").remove();
      const svg = d3.select(this.$refs.svg);
      
      // 设置初始缩放比例（相当于点击缩小按钮3次：0.8^3 ≈ 0.512）
      const initialScale = 0.43;
      
      // 设置初始偏移，使图谱居中并稍微向左上偏移
      const initialTransform = d3.zoomIdentity
        .translate(this.width / 2 - 50, this.height / 2 - 40)  // 向左上各偏移100像素
        .scale(initialScale)
        .translate(-this.width / 2, -this.height / 2);
      
      const color = d3.scaleOrdinal(d3.schemeCategory10);
      const nodeRadius = d => d.size * 6;
      
      const svgWidth = this.$refs.svg.clientWidth;
      const svgHeight = this.$refs.svg.clientHeight;
      
      this.width = svgWidth;
      this.height = svgHeight;
      
      svg.append("defs").selectAll("marker")
          .data(["end"])
          .enter().append("marker")
          .attr("id", d => d)
          .attr("viewBox", "0 -5 10 10")
          .attr("refX", 25)
          .attr("refY", 0)
          .attr("markerWidth", 6)
          .attr("markerHeight", 6)
          .attr("orient", "auto")
          .append("path")
          .attr("d", "M0,-5L10,0L0,5")
          .attr("fill", "#999");
      
      const defs = svg.append("defs");
      
      data.nodes.forEach(node => {
        if (node.image) {
          const imgPattern = defs.append("pattern")
              .attr("id", `img-${node.id}`)
              .attr("width", 1)
              .attr("height", 1)
              .attr("patternUnits", "objectBoundingBox");
          
          imgPattern.append("image")
              .attr("xlink:href", this.getNodeImage(node.id))
              .attr("width", nodeRadius(node) * 2)
              .attr("height", nodeRadius(node) * 2)
              .attr("preserveAspectRatio", "xMidYMid slice");
        }
      });

      const simulation = d3.forceSimulation(data.nodes)
          .force("link", d3.forceLink(data.links).id(d => d.id).distance(150))
          .force("charge", d3.forceManyBody().strength(-800))
          .force("collide", d3.forceCollide().radius(d => nodeRadius(d) * 2))
          .force("center", d3.forceCenter(this.width / 2, this.height / 2))
          // 增加一个向心力，使节点更集中
          .force("radial", d3.forceRadial(
            Math.min(this.width, this.height) / 4,
            this.width / 2,
            this.height / 2
          ).strength(0.3));

      const g = svg.append("g")
          .attr("transform", `translate(0, 0)`);
      
      const zoom = d3.zoom()
          .extent([[0, 0], [this.width, this.height]])
          .scaleExtent([0.2, 5])
          .on("zoom", (event) => {
            this.zoomTransform = event.transform;
            g.attr("transform", event.transform);
          });
      
      svg.call(zoom)
         .on("wheel.zoom", null);

      // 设置初始缩放和位置
      svg.call(zoom.transform, initialTransform);

      this.zoom = zoom;

      const link = g.append("g")
          .attr("class", "links")
          .selectAll("path")
          .data(data.links)
          .enter().append("path")
          .attr("stroke", "#999")
          .attr("stroke-width", 1.5)
          .attr("fill", "none")
          .attr("marker-end", "url(#end)");

      const linkText = g.append("g")
          .attr("class", "link-labels")
          .selectAll("text")
          .data(data.links)
          .enter().append("text")
          .attr("dy", -5)
          .attr("text-anchor", "middle")
          .attr("font-size", "12px")
          .attr("fill", "#555")
          .text(d => d.label)
          .attr("pointer-events", "none");

      const node = g.append("g")
          .attr("class", "nodes")
          .selectAll("circle")
          .data(data.nodes)
          .enter().append("circle")
          .attr("r", nodeRadius)
          .style("fill", d => {
            // 检查是否有对应的图片
            const img = this.getNodeImage(d.id);
            if (img) {
              // 创建图片填充模式
              const pattern = defs.append("pattern")
                .attr("id", `pattern-${d.id}`)
                .attr("width", "100%")
                .attr("height", "100%")
                .attr("patternContentUnits", "objectBoundingBox");
              
              pattern.append("image")
                .attr("href", img)
                .attr("width", 1)
                .attr("height", 1)
                .attr("preserveAspectRatio", "xMidYMid slice");
              
              return `url(#pattern-${d.id})`;
            }
            // 没有图片时使用颜色
            return color(d.group);
          })
          .style("stroke", "#fff")
          .style("stroke-width", 2)
          .call(d3.drag()
              .on("start", this.dragstarted)
              .on("drag", this.dragged)
              .on("end", this.dragended))
          .on("click", (event, d) => {
            this.selectedNode = d;
            // 高亮选中的节点
            d3.selectAll("circle")
              .style("stroke", "#fff")
              .style("stroke-width", 2);
            d3.select(event.currentTarget)
              .style("stroke", "#ff0")
              .style("stroke-width", 4);
            // 添加点击效果
            d3.select(event.currentTarget)
              .transition()
              .duration(200)
              .attr("r", nodeRadius(d) * 1.2)
              .transition()
              .duration(200)
              .attr("r", nodeRadius(d));
          });

      // 优化标签显示
      const labels = g.append("g")
          .attr("class", "node-labels")
          .selectAll("text")
          .data(data.nodes)
          .enter().append("text")
          .attr("dy", d => nodeRadius(d) + 15)
          .attr("text-anchor", "middle")
          .attr("font-size", d => d.group === 1 ? "16px" : "14px")
          .attr("font-weight", d => d.group === 1 ? "bold" : "normal")
          .attr("pointer-events", "none")
          .style("fill", d => d.group === 1 ? "#333" : "#666")
          .text(d => d.id);

      simulation.on("tick", () => {
        link.attr("d", d => {
          const dx = d.target.x - d.source.x;
          const dy = d.target.y - d.source.y;
          const dr = Math.sqrt(dx * dx + dy * dy);
          
          const sourceRadius = nodeRadius(d.source);
          const targetRadius = nodeRadius(d.target);
          
          const sourceX = d.source.x + (dx * sourceRadius) / dr;
          const sourceY = d.source.y + (dy * sourceRadius) / dr;
          const targetX = d.target.x - (dx * targetRadius) / dr;
          const targetY = d.target.y - (dy * targetRadius) / dr;
          
          return `M${sourceX},${sourceY}L${targetX},${targetY}`;
        });

        node.attr("cx", d => d.x)
            .attr("cy", d => d.y);

        labels.attr("x", d => d.x)
            .attr("y", d => d.y);

        linkText.attr("x", d => (d.source.x + d.target.x) / 2)
            .attr("y", d => (d.source.y + d.target.y) / 2);
      });

      this.simulation = simulation;
    },
    dragstarted(event, d) {
      if (!event.active) this.simulation.alphaTarget(0.3).restart();
      d.fx = d.x;
      d.fy = d.y;
    },
    dragged(event, d) {
      d.fx = event.x;
      d.fy = event.y;
    },
    dragended(event, d) {
      if (!event.active) this.simulation.alphaTarget(0);
      d.fx = null;
      d.fy = null;
    },
    zoomIn() {
      this.zoom.scaleBy(d3.select(this.$refs.svg), 1.2);
    },
    zoomOut() {
      this.zoom.scaleBy(d3.select(this.$refs.svg), 0.8);
    },
    resetZoom() {
      d3.select(this.$refs.svg)
        .transition()
        .duration(750)
        .call(this.zoom.transform, d3.zoomIdentity);
    },
    getNodeImage(nodeId) {
      const images = {
        '毛泽东': 毛泽东图片,
        '刘少奇': 刘少奇图片,
        '贺龙': 贺龙图片,
        '彭德怀': 彭德怀图片,
        '向警予': 向警予图片,
        '何叔衡': 何叔衡图片,
        '任弼时': 任弼时图片,
        '雷锋': 雷锋图片,
        '罗荣桓': 罗荣桓图片,
        '林伯渠': 林伯渠图片,
        '中国共产党': 中国共产党图片,
        '八路军': 八路军图片,
        '中华人民共和国': 中华人民共和国图片,
        '红军长征': 红军长征图片,
        '百团大战': 百团大战图片,
        '抗美援朝战争': 抗美援朝战争图片,
        '辽沈战役': 辽沈战役图片,
        '淮海战役': 淮海战役图片,
        '西北战役': 西北战役图片,
        '平江起义': 平江起义图片,
        '遵义会议': 遵义会议图片,
        '中华苏维埃共和国': 中华苏维埃共和国图片,
        '中华人民共和国元帅': 中华人民共和国元帅图片,
        '中共中央政治局委员': 中共中央政治局委员图片,
        '国防部部长': 国防部部长图片,
        '中共中央书记处书记': 中共中央书记处书记图片,
        '中共中央军委委员': 中共中央军委委员图片,
        '志愿军司令员': 志愿军司令员图片,
        '庐山会议': 庐山会议图片,
        '大跃进': 大跃进图片,
        '军事系统高干会议': 军事系统高干会议图片,
        '辛亥革命': 辛亥革命图片,
        '中共一大': 中共一大图片,
        '苏维埃革命': 苏维埃革命图片,
        '反围剿': 反围剿图片,
        '游击战': 游击战图片
      };
      return images[nodeId];
    },
    getNodeType(group) {
      const types = {
        1: '重要人物',
        2: '职务身份',
        3: '重要事件',
        4: '个人事迹',
        5: '文化印记'
      };
      return types[group] || '其他';
    },
    getImportanceLevel(size) {
      const levels = {
        6: '核心',
        4: '重要',
        3: '相关',
        2: '一般'
      };
      return levels[size] || '普通';
    },
    getNodeRelations(nodeId) {
      return this.datajson.links.filter(link => 
        link.source === nodeId || link.target === nodeId || 
        (typeof link.source === 'object' && link.source.id === nodeId) || 
        (typeof link.target === 'object' && link.target.id === nodeId)
      );
    },
    getNodeDescription(nodeId) {
      return this.nodeDescriptions[nodeId] || "暂无详细信息";
    },
    getNodeRelationsText(nodeId) {
      const relations = this.getNodeRelations(nodeId);
      let text = '';
      
      relations.forEach(relation => {
        const sourceId = typeof relation.source === 'object' ? relation.source.id : relation.source;
        const targetId = typeof relation.target === 'object' ? relation.target.id : relation.target;
        
        const otherNodeId = sourceId === nodeId ? targetId : sourceId;
        
        text += `${relation.label} ${otherNodeId}\n`;
      });
      
      return text || '暂无关系数据';
    }
  }
};
</script>

<style scoped>
/* 隐藏整个页面的滚动条 */
:deep(body) {
  overflow: hidden;
}

.knowledge-graph-container {
  display: flex;
  width: 99%;
  max-width: 1350px;
  margin: 0 auto;
  height: calc(100vh - 120px);
  border-radius: 8px;
  overflow: hidden !important;
  gap: 20px;

}

.left-section {
  flex: 4;
  display: flex;
  flex-direction: column;
  gap: 20px;
  overflow: hidden;
}

.info-panel {
  flex: 3;
  padding: 20px;
 
  overflow-y: auto;
  /* 自定义滚动条样式 */
  &::-webkit-scrollbar {
    width: 6px;
  }
  &::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 3px;
  }
  &::-webkit-scrollbar-thumb {
    background: #888;
    border-radius: 3px;
  }
  &::-webkit-scrollbar-thumb:hover {
    background: #555;
  }
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

svg {
  width: 100%;
  height: 100%;
  display: block;
  background-color: #fff;
}

.zoom-controls {
  position: absolute;
  bottom: 20px;
  right: 20px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  z-index: 10;
}

.zoom-btn {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background-color: white;
  border: 1px solid #ddd;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.zoom-btn:hover {
  background-color: #f5f5f5;
  transform: scale(1.05);
}

.zoom-btn:active {
  background-color: #e8e8e8;
  transform: scale(0.95);
}

.node-details {
  padding: 10px;
}

.node-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 15px;
}

.node-image {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid #f0f0f0;
  margin-bottom: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.node-details h3 {
  font-size: 22px;
  color: #333;
  margin-top: 0;
  margin-bottom: 5px;
  text-align: center;
  font-weight: bold;
}

.divider {
  height: 2px;
  background-color: #e0e0e0;
  margin: 15px 0;
}

.detail-item {
  margin-bottom: 15px;
}

.label {
  font-weight: bold;
  color: #555;
  display: block;
  margin-bottom: 5px;
}

.value {
  color: #333;
}

.relationships {
  margin-top: 8px;
}

.relation-text {
  font-family: 'Microsoft YaHei', sans-serif;
  white-space: pre-wrap;
  background-color: #f5f5f5;
  padding: 12px;
  border-radius: 4px;
  margin: 8px 0;
  color: #333;
  line-height: 1.6;
  font-size: 14px;
}

.description {
  line-height: 1.6;
  color: #444;
  text-align: justify;
  margin-top: 8px;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #999;
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 20px;
}

.empty-state p {
  font-size: 16px;
}

.filter-section {
  padding: 15px;
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  display: flex;
  gap: 10px;
  align-items: center;
  height: 60px;
}

.tag-select {
  width: 100%;
  max-width: 500px;
}

.reset-btn {
  height: 32px;
  white-space: nowrap;
}

.graph-wrapper {
  flex: 1;
  position: relative;
  overflow: hidden !important;
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}
</style>

<template>
  <div class="knowledge-graph-container">
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

export default {
  data() {
    return {
      width: 800,
      height: 600,
      selectedNode: null,
      zoomTransform: null,
      datajson: {
        nodes: [
          { id: "毛泽东", group: 1, size: 6, image: 毛泽东图片 },
          { id: "刘少奇", group: 2, size: 6, image: 刘少奇图片 },
          { id: "贺龙", group: 3, size: 6, image: 贺龙图片 },
          { id: "中国共产党", group: 4, size: 4, image: 中国共产党图片 },
          { id: "八路军", group: 5, size: 4, image: 八路军图片 },
          { id: "中华人民共和国", group: 6, size: 4, image: 中华人民共和国图片 },
          { id: "红军长征", group: 7, size: 4, image: 红军长征图片 }
        ],
        links: [
          { source: "毛泽东", target: "中国共产党", label: "创立并领导" },
          { source: "毛泽东", target: "中华人民共和国", label: "建立" },
          { source: "毛泽东", target: "八路军", label: "指挥" },
          { source: "毛泽东", target: "红军长征", label: "参与" },
          { source: "刘少奇", target: "中国共产党", label: "领导"},
          {source: "刘少奇", target: "中华人民共和国", label: "国家主席"},
          {source: "刘少奇", target: "红军长征", label: "参与"},
          {source: "贺龙", target: "八路军", label: "指挥"},
          {source: "贺龙", target: "中国共产党", label: "成员"},
          {source: "贺龙", target: "红军长征", label: "参与"},
          {source: "毛泽东", target: "刘少奇", label: "曾是同事"},
          {source: "毛泽东", target: "贺龙", label: "共同领导八路军"},
          {source: "刘少奇", target: "贺龙", label: "战友"}
        ]
      },
      nodeDescriptions: {
        "毛泽东": "中国共产党、中华人民共和国和人民解放军的主要创始人和领导人，马克思主义者，伟大的无产阶级革命家、战略家和理论家。",
        "刘少奇": "中国共产党、中华人民共和国主要领导人之一，杰出的无产阶级革命家、政治家和理论家，中华人民共和国第二任国家主席。",
        "贺龙": "中国共产党的优秀党员，中国人民解放军创建人之一，中华人民共和国元帅，杰出的无产阶级革命家、军事家。",
        "中国共产党": "中国工人阶级的先锋队，同时是中国人民和中华民族的先锋队，是中国特色社会主义事业的领导核心。",
        "八路军": "中国工农红军改编后的名称，是中国共产党在抗日战争时期领导的人民武装力量。",
        "中华人民共和国": "1949年10月1日成立的社会主义国家，由中国共产党领导。",
        "红军长征": "1934年10月至1936年10月，中国工农红军主力从长江南北各苏区向陕甘苏区进行的战略转移。"
      }
    };
  },
  mounted() {
    this.width = this.$el.clientWidth * 0.7;
    this.height = Math.max(600, window.innerHeight - 180);
    this.createGraph();
  },
  methods: {
    createGraph() {
      const svg = d3.select(this.$refs.svg);
      const color = d3.scaleOrdinal(d3.schemeCategory10);
      const nodeRadius = d => d.size * 6;
      
      // 获取实际的 SVG 尺寸
      const svgWidth = this.$refs.svg.clientWidth;
      const svgHeight = this.$refs.svg.clientHeight;
      
      // 更新宽度和高度
      this.width = svgWidth;
      this.height = svgHeight;
      
      svg.selectAll("*").remove();
      
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
      
      this.datajson.nodes.forEach(node => {
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

      const simulation = d3.forceSimulation(this.datajson.nodes)
          .force("link", d3.forceLink(this.datajson.links).id(d => d.id).distance(180))
          .force("charge", d3.forceManyBody().strength(-400))
          // 使用实际的 SVG 尺寸来设置中心点
          .force("center", d3.forceCenter(svgWidth / 2, svgHeight / 2))
          .force("collide", d3.forceCollide().radius(d => nodeRadius(d) + 15).iterations(4));

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

      this.zoom = zoom;

      const link = g.append("g")
          .attr("class", "links")
          .selectAll("path")
          .data(this.datajson.links)
          .enter().append("path")
          .attr("stroke", "#999")
          .attr("stroke-width", 1.5)
          .attr("fill", "none")
          .attr("marker-end", "url(#end)");

      const linkText = g.append("g")
          .attr("class", "link-labels")
          .selectAll("text")
          .data(this.datajson.links)
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
          .data(this.datajson.nodes)
          .enter().append("circle")
          .attr("r", nodeRadius)
          .style("fill", d => d.image ? `url(#img-${d.id})` : color(d.group))
          .style("stroke", "#fff")
          .style("stroke-width", 2)
          .call(d3.drag()
              .on("start", this.dragstarted)
              .on("drag", this.dragged)
              .on("end", this.dragended))
          .on("click", (event, d) => {
            this.selectedNode = d;
            d3.selectAll("circle").style("stroke", "#fff").style("stroke-width", 2);
            d3.select(event.currentTarget).style("stroke", "#ff0").style("stroke-width", 4);
          });

      const labels = g.append("g")
          .attr("class", "node-labels")
          .selectAll("text")
          .data(this.datajson.nodes)
          .enter().append("text")
          .attr("dy", d => nodeRadius(d) + 15)
          .attr("text-anchor", "middle")
          .attr("font-size", "14px")
          .attr("font-weight", "bold")
          .attr("pointer-events", "none")
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
    zoomIn() {
      if (this.zoom) {
        const svg = d3.select(this.$refs.svg);
        const currentScale = this.zoomTransform ? this.zoomTransform.k : 1;
        svg.transition().call(this.zoom.scaleTo, currentScale * 1.3);
      }
    },
    zoomOut() {
      if (this.zoom) {
        const svg = d3.select(this.$refs.svg);
        const currentScale = this.zoomTransform ? this.zoomTransform.k : 1;
        svg.transition().call(this.zoom.scaleTo, currentScale / 1.3);
      }
    },
    resetZoom() {
      if (this.zoom) {
        const svg = d3.select(this.$refs.svg);
        svg.transition().call(this.zoom.transform, d3.zoomIdentity);
      }
    },
    getNodeImage(nodeId) {
      const node = this.datajson.nodes.find(n => n.id === nodeId);
      if (node && node.image) {
        try {
          return node.image;
        } catch (e) {
          console.error(`无法加载图片: ${node.image}`, e);
          return null;
        }
      }
      return null;
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
    getNodeType(group) {
      const types = {
        1: "党和国家领导人",
        2: "党和国家领导人",
        3: "军事领导人",
        4: "政党组织",
        5: "军事组织",
        6: "国家",
        7: "历史事件"
      };
      return types[group] || "未知类型";
    },
    getImportanceLevel(size) {
      if (size >= 6) return "极高";
      if (size >= 4) return "高";
      if (size >= 2) return "中";
      return "一般";
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
.knowledge-graph-container {
  display: flex;
  width: 85%;
  max-width: 1400px;
  margin: 0 auto;
  height: calc(100vh - 140px);
  border-radius: 8px;
  overflow: hidden;
  gap: 40px;
  padding: 15px;
}

.graph-wrapper {
  flex: 7;
  position: relative;
  overflow: hidden;
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  display: flex;
  justify-content: center;
  align-items: center;
}

.info-panel {
  flex: 3;
  padding: 20px;
  overflow-y: auto;
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
</style>

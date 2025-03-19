<template>
  <div>
    <svg ref="svg" :width="width" :height="height"></svg>
  </div>
</template>

<script>
import * as d3 from "d3";

export default {
  data() {
    return {
      width: 800,
      height: 600,
      datajson: {
        nodes: [
          { id: "毛泽东", group: 1, size: 6 },
          { id: "刘少奇", group: 2, size: 6 },
          { id: "贺龙", group: 3, size: 6 },
          { id: "中国共产党", group: 4, size: 4 },
          { id: "八路军", group: 5, size: 4 },
          { id: "中华人民共和国", group: 6, size: 4 },
          { id: "红军长征", group: 7, size: 4 }
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
      }
    };
  },
  mounted() {
    this.createGraph();
  },
  methods: {
    createGraph() {
      const svg = d3.select(this.$refs.svg);
      const color = d3.scaleOrdinal(d3.schemeCategory10);
      const nodeRadius = 20;

      const simulation = d3.forceSimulation(this.datajson.nodes)
          .force("link", d3.forceLink(this.datajson.links).id(d => d.id).distance(120))
          .force("charge", d3.forceManyBody().strength(-200))
          .force("center", d3.forceCenter(this.width / 2, this.height / 2))
          .force("collide", d3.forceCollide().radius(nodeRadius + 2).iterations(4));

      const link = svg.append("g")
          .selectAll("line")
          .data(this.datajson.links)
          .enter().append("line")
          .attr("stroke", "#999")
          .attr("stroke-width", 1.5);

      const linkText = svg.append("g")
          .selectAll("text")
          .data(this.datajson.links)
          .enter().append("text")
          .attr("dx", 5)
          .attr("dy", ".5em")
          .text(d => d.label);

      const node = svg.append("g")
          .selectAll("circle")
          .data(this.datajson.nodes)
          .enter().append("circle")
          .attr("r", d => d.size * 2)
          .style("fill", d => color(d.group))
          .call(d3.drag()
              .on("start", dragstarted)
              .on("drag", dragged)
              .on("end", dragended));

      const labels = svg.append("g")
          .selectAll("text")
          .data(this.datajson.nodes)
          .enter().append("text")
          .attr("dx", 12)
          .attr("dy", ".5em")
          .style("font-size", "13px")
          .text(d => d.id);

      simulation.on("tick", () => {
        link.attr("x1", d => d.source.x)
            .attr("y1", d => d.source.y)
            .attr("x2", d => d.target.x)
            .attr("y2", d => d.target.y);

        node.attr("cx", d => d.x)
            .attr("cy", d => d.y);

        labels.attr("x", d => d.x)
            .attr("y", d => d.y);

        linkText.attr("x", d => (d.source.x + d.target.x) / 2)
            .attr("y", d => (d.source.y + d.target.y) / 2);
      });

      function dragstarted(event, d) {
        if (!event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
      }

      function dragged(event, d) {
        d.fx = event.x;
        d.fy = event.y;
      }

      function dragended(event, d) {
        if (!event.active) simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
      }
    }
  }
};
</script>

<style scoped>
svg {
  border: 1px solid #ccc;
}
</style>

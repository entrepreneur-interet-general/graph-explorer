
<template>
  <div id="graph-container">
    <svg id="svg">
      <defs>
        <marker id="arrowhead" viewBox="-0 -5 10 10" refX="20" refY="0" orient="auto" markerWidth="3" markerHeight="3" xoverflow="visbile">
          <path d="M 0,-5 L 10, 0 L 0, 5" fill="var(--grey)" opacity="0.2" stroke="none;"></path>
        </marker>
      </defs>
      <!-- Main containers for the d3.js force directed graph. 
			They will be populated dynamically by d3.js -->
      <g class="graph">
        <g class="links"></g>
        <g class="edgepaths"></g>
        <g class="edgelabels"></g>
        <g class="nodes"></g>
        <g class="nodelabels"></g>
      </g>
    </svg>
  </div>
</template>


<script>
import * as d3 from "d3";
import api from "../api";
import { getStarCoordinates } from "../utils";
import { UPDATE_FOCUS_NODE, UPDATE_NODES, UPDATE_LINKS } from "../mutation-types";
import { mapState } from 'vuex';

export default {
  computed: mapState({
    focusNodeEntity: state => state.focusNodeEntity,
    nodesData: state => state.nodes,
    linksData: state => state.links 
  }),
  watch: {
    nodesData(){
      this.draw();
    }
  },
  mounted() {
    const vm = this;

    vm.svg = d3.select("svg");
    vm.graph = d3.select(".graph");
    vm.links = d3.select(".links").selectAll(".link");
    vm.edgepaths = d3.select(".edgepaths").selectAll(".edgepath");
    vm.edgelabels = d3.select(".edgelabels").selectAll(".edgelabel");
    vm.circles = d3.select(".nodes").selectAll(".circle");
    vm.stars = d3.select(".nodes").selectAll(".star")
    vm.nodelabels = d3.select('.nodelabels').selectAll(".nodelabel");
    vm.zoom = d3.zoom().scaleExtent([1, 16]).on("zoom", vm.zoomed)
    vm.svg.call(vm.zoom).on("dblclick.zoom", null);
    const { width, height } = vm.getContainerSize();
    vm.simulation = d3.forceSimulation()
      .force("link", d3.forceLink().id(function (d) { return d.id; }).distance(50))
      .force("charge", d3.forceManyBody())
      .force("center", d3.forceCenter(width / 2, height / 2))
      .on("tick", vm.ticked);

    vm.zoomReset();

    vm.$root.$on('zoom-in', () => {
      vm.zoomIn();
    })

    vm.$root.$on('zoom-out', () => {
      vm.zoomOut();
    })

    vm.$root.$on('zoom-reset', () => {
      vm.zoomReset();
    })

  },
  methods: {
    draw() {

      const vm = this;

      vm.simulation.stop();

      const circleNodes = vm.nodesData.filter(function(node) { return !node.star })
      const starNodes = vm.nodesData.filter(function(node) { return node.star })

      const linkKey = (d) => {
        const source = d.source.entity ? d.source.entity : d.source;
        const target = d.target.entity ? d.target.entity : d.target;
        const k = `${source}-${target}`; 
        return k;
      }

      const nodeKey = (d) => {
        return d.entity;
      }

      vm.links = vm.links.data(vm.linksData, linkKey);

      vm.links
        .exit()
        .transition()
        .attr("stroke-opacity", 0)
        .attrTween("x1", function (d) { return function () { return d.source.x; } })
        .attrTween("x2", function (d) { return function () { return d.target.x; } })
        .attrTween("y1", function (d) { return function () { return d.source.y; } })
        .attrTween("y2", function (d) { return function () { return d.target.y; } })
        .remove();

      const newLinks = vm.links.enter()
        .append("line")
        .call(function (link) { link.transition().attr("stroke-opacity", 0.2) })
        .attr("class", "link")
        .on("mouseenter", vm.handleLinkMouseEnter)
        .on("mouseout", vm.handleLinkMouseOut)

      vm.links = newLinks.merge(vm.links);

      vm.edgepaths = vm.edgepaths.data(vm.linksData, linkKey)

      vm.edgepaths.exit().remove();

      vm.edgepaths = vm.edgepaths.enter()
        .append('path')
        .attr('class', 'edgepath')
        .merge(vm.edgepaths)
        .attr('id', function (d, i) { return 'edgepath' + i })

      vm.edgelabels = vm.edgelabels.data(vm.linksData, linkKey);

      vm.edgelabels.exit().remove();

      const newEdgelabels = vm.edgelabels.enter()
        .append('text')
        .attr('class', 'edgelabel')

      newEdgelabels.append('textPath')
        .attr('class', 'label')
        .attr('startOffset', '50%')
        .attr('text-anchor', 'middle')
        .text(function (d) {
          const rounded = Math.round(d.valeur_euro);
          const localized = rounded.toLocaleString('fr-FR');
          return `${localized}€ (${d.transactions.length})`;
        });

      vm.edgelabels = newEdgelabels.merge(vm.edgelabels)
        .attr('id', function (d, i) { return 'edgelabel' + i })

      vm.edgelabels.select("textPath")
        .attr('xlink:href', function (d, i) { return '#edgepath' + i })

      vm.circles = vm.circles.data(circleNodes, nodeKey);

      vm.circles.exit().transition().attr("r", 0).remove();

      const newCircles = vm.circles.enter()
        .append("circle")
        .attr("class", "node")
        .classed("node-focus", d => {
          return d.entity == vm.focusNodeEntity;
        })
        .call(function (node) { node.transition().attr("r", 3); })
        .on("click", vm.handleNodeClicked)
        .on("dblclick", vm.handleNodeDblclick)
        .call(d3.drag()
          .on("start", vm.dragstarted)
          .on("drag", vm.dragged)
          .on("end", vm.dragended));

      vm.circles = newCircles.merge(vm.circles);

      vm.stars = vm.stars.data(starNodes, nodeKey);

      vm.stars.exit().remove();

      const newStars = vm.stars.enter()
        .append("polygon")
        .attr("class", "node")
        .on("click", vm.handleNodeClicked)
        .on("dblclick", vm.handleNodeDblclick)
        .call(d3.drag()
          .on("start", vm.dragstarted)
          .on("drag", vm.dragged)
          .on("end", vm.dragended));

      vm.stars = newStars.merge(vm.stars);

      vm.nodelabels = vm.nodelabels.data(vm.nodesData, nodeKey);

      vm.nodelabels.exit().remove();

      const newNodeLabels = vm.nodelabels 
        .enter()
        .append("g")
        .on("click", vm.handleNodeClicked)
        .on("dblclick", vm.handleNodeDblclick)
        .call(d3.drag()
          .on("start", vm.dragstarted)
          .on("drag", vm.dragged)
          .on("end", vm.dragended));

      newNodeLabels.append("text")
        .attr("class", "label")
        .attr("x", 0)
        .attr("y", 0)
        .style("text-anchor", "middle")
        .text(function (d) {
          return `${d.prenom} ${d.nom} (${d.degree})`;
        })

      vm.nodelabels = newNodeLabels.merge(vm.nodelabels)

      vm.simulation
        .nodes(vm.nodesData)
        .on("tick", vm.ticked);
      vm.simulation.force("link").links(vm.linksData)
      vm.simulation.alpha(1).restart()


    },
    dragstarted: function (d) {
      if (!d3.event.active) this.simulation.alphaTarget(0.3).restart();
      d.fx = d.x;
      d.fy = d.y;
    },
    dragged: function (d) {
      d.fx = d3.event.x;
      d.fy = d3.event.y;
    },
    dragended: function (d) {
      if (!d3.event.active) this.simulation.alphaTarget(0);
      d.fx = null;
      d.fy = null;
    },
    ticked() {
      const vm = this;
      vm.links
        .attr("x1", function (d) { return d.source.x; })
        .attr("y1", function (d) { return d.source.y; })
        .attr("x2", function (d) { return d.target.x; })
        .attr("y2", function (d) { return d.target.y; });

      vm.circles
        .attr("cx", function (d) { return d.x; })
        .attr("cy", function (d) { return d.y; });

      vm.stars
        .attr("points", function(d) {
          var center = { x: d.x, y: d.y };
          var coordinates = getStarCoordinates(center, 2, 5);
          return coordinates.map(function(p){
            return [p.x, p.y].join(",");
          }).join(" ");
        })

      vm.nodelabels
        .attr("transform", function (d) { return "translate(" + d.x + "," + d.y + ")" })

      vm.edgepaths.attr('d', function (d) {
        return 'M ' + d.source.x + ' ' + d.source.y + ' L ' + d.target.x + ' ' + d.target.y;
      });

      vm.edgelabels.attr('transform', function (d) {
        if (d.target.x < d.source.x) {
          const bbox = this.getBBox();
          const rx = bbox.x + bbox.width / 2;
          const ry = bbox.y + bbox.height / 2;
          return 'rotate(180 ' + rx + ' ' + ry + ')';
        }
        else {
          return 'rotate(0)';
        }
      });
    },
    zoomed() {
      if (this.graph) {
        this.graph.attr("transform", d3.event.transform);
      }
    },
    zoomIn: function(){
      this.zoom.scaleBy(this.svg.transition().duration(200), 1.2);
    },
    zoomOut: function(){
      this.zoom.scaleBy(this.svg.transition().duration(200), 1 / 1.2);
    },
    zoomReset: function(){
      this.svg.call(this.zoom.transform, d3.zoomIdentity);
      this.zoom.scaleTo(this.svg.transition(), 2.5);
    },
    handleNodeClicked(node) {
      this.$store.commit(UPDATE_FOCUS_NODE, node.entity)
      this.updateFocusNode();
    },
    handleNodeDblclicked(target){
      console.log("Node double clicked")
    },
    updateFocusNode() {
      const vm = this;
      vm.circles.classed("node-focus", d => {
        return d.entity == vm.focusNodeEntity;
      });
      vm.stars.classed("node-focus", d => {
        return d.entity == vm.focusNodeEntity;
      });
    },
    getContainerSize() {
      const { width, height } = d3.select("#graph-container").node().getBoundingClientRect();
      return { width, height };
    }
  }
};
</script>

<style lang="scss">

@import "../scss/settings.scss";

#graph-container {
  position: fixed;
  height: 100%;
  width: 100%;
}

#svg {
  height: 100%;
  width: 100%;
  z-index: 1;
}

.node, .triangle {
  fill: $peter-river;
  opacity: 0.5;
}

.node, .node-label {
  cursor: pointer;
}

.node-focus {
  opacity: 1;
}

.link {
  marker-end: url(#arrowhead);
  stroke: $asbestos;
  stroke-width: 1;
}

.edgepath {
  fill-opacity: 0;
  stroke-opacity: 0;
  pointer-events: none;
}

.label {
  pointer-events: none;
  font-size: 2px;
  fill: black;
}



</style>


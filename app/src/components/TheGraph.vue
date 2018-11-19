
<template>
  <div id="graph-container">
    <svg id="svg">
      <defs/>
      <!-- Main containers for the d3.js force directed graph.
      They will be populated dynamically by d3.js -->
      <g class="graph">
        <g class="links"/>
        <g class="edgepaths"/>
        <g class="edgelabels"/>
        <g class="nodes"/>
        <g class="flags"/>
        <g class="nodelabels"/>
      </g>
    </svg>
  </div>
</template>


<script>
/* eslint no-underscore-dangle: 0 */
/* eslint no-param-reassign: ["error", { "props": false }] */
/* eslint func-names: ["error", "never"] */

import * as d3 from 'd3';
import { mapState, mapMutations } from 'vuex';
import { getStarCoordinates, array2dict } from '../utils';
import { UPDATE_FOCUS_NODE, HIDE_PROGRESS_SPINNER } from '../mutation-types';
import Worker from '../force.worker';

function importAll(r) {
  const images = {};
  r.keys().forEach((item) => {
    images[item.replace('./', '')] = r(item);
  });
  return images;
}

const flags = importAll(require.context('../flags', false, /\.(svg)$/));

export default {
  data() {
    /* Keep a local copy of nodes and links that will be assigned extra properties by d3 force
    simulation

    For nodes {index, x, y, vx, vy, fx, fy}
    https://github.com/d3/d3-force/blob/master/README.md#simulation_nodes

    For links {source, target, index}
    https://github.com/d3/d3-force/blob/master/README.md#link_links
    */
    return {
      nodes: [],
      links: []
    };
  },
  computed: {
    nodesDict() {
      return array2dict(this.nodes, n => n.entity);
    },
    /**
     * Returns the focusNode with all its properties
     * */
    focusNode() {
      return this.nodesDict[this.focusNodeEntity];
    },
    /**
     * Split the nodes in two lists based on whether or not they are starred
     */
    nodesByType() {
      const starNodes = [];
      const nonStarNodes = [];
      this.nodes.forEach((node) => {
        if (node.star) {
          starNodes.push(node);
        } else {
          nonStarNodes.push(node);
        }
      });
      return [starNodes, nonStarNodes];
    },
    ...mapState(['focusNodeEntity', 'G'])
  },
  watch: {
    /** re-compute the local version of nodes and links
    whenever the underlying graph structure changes by re-running
    the force simulation
    */
    G() {
      const vm = this;
      const { nodes, links } = vm.$store.getters;
      const { nodesDict } = vm;

      // map force layout properties to updated data
      vm.nodes = nodes.map((node) => {
        let n = Object.assign({}, node);
        if (n.entity in nodesDict) {
          n = nodesDict[n.entity];
          if (n.entity === vm.focusNodeEntity) {
            // fix the position of the node under focus
            n.fx = n.x;
            n.fy = n.y;
          }
        }
        return n;
      });
      vm.links = links.map((link) => {
        const l = Object.assign({}, link);
        l.source = l.source in nodesDict ? nodesDict[l.source] : l.source;
        l.target = l.target in nodesDict ? nodesDict[l.target] : l.target;
        return l;
      });

      vm.forceSimulation(() => {
        // release the position of the focus node if exists
        if (vm.focusNode) {
          vm.focusNode.fx = null;
          vm.focusNode.fy = null;
        }
        vm.HIDE_PROGRESS_SPINNER();
        vm.draw();
      });
    }
  },
  mounted() {
    const vm = this;

    vm.select = {
      svg: d3.select('svg'),
      graph: d3.select('.graph'),
      links: d3.select('.links').selectAll('.link'),
      edgepaths: d3.select('.edgepaths').selectAll('.edgepath'),
      edgelabels: d3.select('.edgelabels').selectAll('.edgelabel'),
      circles: d3.select('.nodes').selectAll('.circle'),
      flags: d3.select('.flags').selectAll('.flag'),
      stars: d3.select('.nodes').selectAll('.star'),
      nodelabels: d3.select('.nodelabels').selectAll('.nodelabel'),
      arrowheads: d3.select('defs').selectAll('.arrowhead')
    };

    vm.zoom = d3.zoom().scaleExtent([1, 16]).on('zoom', vm.zoomed);
    vm.select.svg.call(vm.zoom).on('dblclick.zoom', null);

    vm.zoomReset();

    vm.$root.$on('zoom-in', () => {
      vm.zoomIn();
    });

    vm.$root.$on('zoom-out', () => {
      vm.zoomOut();
    });

    vm.$root.$on('zoom-reset', () => {
      vm.zoomReset();
    });
  },
  methods: {
    ...mapMutations([HIDE_PROGRESS_SPINNER]),
    forceSimulation(callback) {
      const vm = this;

      const { width, height } = vm.getContainerSize();
      const center = { x: width / 2, y: height / 2 };

      const worker = Worker();
      worker.postMessage({
        center,
        nodes: vm.nodes,
        links: vm.links
      });

      worker.onmessage = (event) => {
        vm.nodes = event.data.nodes;
        vm.links = event.data.links;
        callback();
      };
    },
    /**
    ** draw (or re-draw) the graph using d3.js
    ** @param {int} transitionDuration - The duration in ms of the transition between two states of the graph
    */
    draw(transitionDuration = 1500) {
      const vm = this;

      const [starNodes, circleNodes] = vm.nodesByType;

      // Defines node and link keys that will be used in data binding
      // see https://bost.ocks.org/mike/constancy/
      const linkKey = (d) => {
        const k = `${d.source.entity}-${d.target.entity}`;
        return k;
      };

      const nodeKey = (d) => {
        const { entity } = d;
        return entity;
      };

      // Create arrow heads used as marker-end to the links
      vm.select.arrowheads = vm.select.arrowheads.data(vm.links, linkKey);

      vm.select.arrowheads
        .exit()
        .transition()
        .duration(transitionDuration)
        .attr('opacity', 0)
        .remove();

      const newArrowHeads = vm.select.arrowheads.enter()
        .append('marker')
        .attr('class', 'arrowhead')
        .attr('viewBox', '-0 -5 10 10')
        .attr('refX', '20')
        .attr('refY', '0')
        .attr('orient', 'auto')
        .attr('markerWidth', '3')
        .attr('markerHeight', '3')
        .attr('xoverflow', 'visible');

      newArrowHeads.append('path')
        .attr('d', 'M 0,-5 L 10, 0 L 0, 5');

      newArrowHeads.attr('opacity', '0')
        .attr('opacity', 0)
        .transition()
        .duration(transitionDuration)
        .attr('opacity', 0.5);

      vm.select.arrowheads = newArrowHeads.merge(vm.select.arrowheads);

      vm.select.arrowheads.attr('id', d => `arrowhead${linkKey(d)}`);

      vm.select.links = vm.select.links.data(vm.links, linkKey);

      vm.select.links
        .exit()
        .transition()
        .duration(transitionDuration)
        .attr('x1', d => ((d.source.entity in vm.nodesDict) ? vm.nodesDict[d.source.entity].x : d.source.x))
        .attr('y1', d => ((d.source.entity in vm.nodesDict) ? vm.nodesDict[d.source.entity].y : d.source.y))
        .attr('x2', d => ((d.target.entity in vm.nodesDict) ? vm.nodesDict[d.target.entity].x : d.target.x))
        .attr('y2', d => ((d.target.entity in vm.nodesDict) ? vm.nodesDict[d.target.entity].y : d.target.y))
        .attr('stroke-opacity', 0)
        .remove();

      const newLinks = vm.select.links.enter()
        .append('line')
        .attr('class', 'link')
        .attr('x1', () => vm.focusNode.x)
        .attr('y1', () => vm.focusNode.y)
        .attr('x2', () => vm.focusNode.x)
        .attr('y2', () => vm.focusNode.y);

      vm.select.links = newLinks.merge(vm.select.links);

      vm.select.links.attr('marker-end', d => `url(#arrowhead${linkKey(d)})`);

      vm.select.links
        .transition()
        .duration(transitionDuration)
        .attr('x1', d => d.source.x)
        .attr('y1', d => d.source.y)
        .attr('x2', d => d.target.x)
        .attr('y2', d => d.target.y)
        .attr('stroke-opacity', 0.2);

      vm.select.edgepaths = vm.select.edgepaths.data(vm.links, linkKey);

      vm.select.edgepaths
        .exit()
        .transition()
        .duration(transitionDuration)
        .attr('d', (d) => {
          const xSource = (d.source.entity in vm.nodesDict)
            ? vm.nodesDict[d.source.entity].x
            : d.source.x;
          const ySource = (d.source.entity in vm.nodesDict)
            ? vm.nodesDict[d.source.entity].y
            : d.source.y;
          const xTarget = (d.target.entity in vm.nodesDict)
            ? vm.nodesDict[d.target.entity].x
            : d.target.x;
          const yTarget = (d.target.entity in vm.nodesDict)
            ? vm.nodesDict[d.target.entity].y
            : d.target.y;
          return `M${xSource} ${ySource}L ${xTarget} ${yTarget}`;
        })
        .remove();

      const newEdgepaths = vm.select.edgepaths.enter()
        .append('path')
        .attr('class', 'edgepath')
        .attr('d', () => `M${vm.focusNode.x} ${vm.focusNode.y}L ${vm.focusNode.x} ${vm.focusNode.y}`);

      vm.select.edgepaths = newEdgepaths.merge(vm.select.edgepaths);
      vm.select.edgepaths.attr('id', d => `edgepath${linkKey(d)}`);

      vm.select.edgepaths
        .transition()
        .duration(transitionDuration)
        .attr('d', d => `M${d.source.x} ${d.source.y}L ${d.target.x} ${d.target.y}`);

      vm.select.edgelabels = vm.select.edgelabels.data(vm.links, linkKey);

      vm.select.edgelabels
        .exit()
        .transition()
        .duration(transitionDuration)
        .style('opacity', 0)
        .attrTween('transform', function (d) {
          const _this = this;
          const xSource = d.source.entity in vm.nodesDict
            ? vm.nodesDict[d.source.entity].x
            : d.source.x;
          const xTarget = d.target.entity in vm.nodesDict
            ? vm.nodesDict[d.target.entity].x
            : d.target.x;
          const f = () => {
            if (xTarget < xSource) {
              const bbox = _this.getBBox();
              const rx = bbox.x + bbox.width / 2;
              const ry = bbox.y + bbox.height / 2;
              return `rotate(180 ${rx} ${ry})`;
            }
            return 'rotate(0)';
          };
          return f;
        })
        .remove();

      vm.select.edgelabels
        .exit()
        .select('textPath')
        .transition()
        .duration(transitionDuration)
        .remove();

      const newEdgelabels = vm.select.edgelabels.enter()
        .append('text')
        .attr('class', 'edgelabel')
        .style('opacity', 0);

      newEdgelabels.append('textPath')
        .attr('class', 'label')
        .attr('startOffset', '50%')
        .attr('text-anchor', 'middle')
        .text((d) => {
          const rounded = Math.round(d.valeur_euro);
          const localized = rounded.toLocaleString('fr-FR');
          return `${localized}€ (${d.number_of_links})`;
        })
        .transition()
        .duration(transitionDuration);

      vm.select.edgelabels = newEdgelabels.merge(vm.select.edgelabels);

      vm.select.edgelabels.select('textPath')
        .attr('xlink:href', d => `#edgepath${linkKey(d)}`);

      vm.select.edgelabels
        .transition()
        .duration(transitionDuration)
        .style('opacity', 1)
        .attrTween('transform', function (d) {
          const _this = this;
          const f = () => {
            if (d.target.x < d.source.x) {
              const bbox = _this.getBBox();
              const rx = bbox.x + bbox.width / 2;
              const ry = bbox.y + bbox.height / 2;
              return `rotate(180 ${rx} ${ry})`;
            }
            return 'rotate(0)';
          };
          return f;
        });

      vm.select.flags = vm.select.flags.data(vm.nodes, nodeKey);

      vm.select.flags
        .exit()
        .transition()
        .duration(transitionDuration)
        .style('opacity', 0)
        .remove();

      const newFlags = vm.select.flags.enter()
        .append('image')
        .attr('class', 'flag')
        .attr('width', 3)
        .attr('height', 2.25)
        .style('opacity', 0)
        .attr('x', () => vm.focusNode.x)
        .attr('y', () => vm.focusNode.y)
        .attr('xlink:href', (d) => {
          if (d.pays_code) {
            const filename = `${d.pays_code.toLowerCase()}.svg`;
            return flags[filename];
          }
          return null;
        });

      newFlags.on('click', vm.handleNodeClicked);

      vm.select.flags = newFlags.merge(vm.select.flags);

      vm.select.flags
        .transition()
        .duration(transitionDuration)
        .attr('x', d => d.x)
        .attr('y', d => d.y + 0.5)
        .style('opacity', 1);

      vm.select.circles = vm.select.circles.data(circleNodes, nodeKey);

      vm.select.circles
        .exit()
        .transition()
        .duration(transitionDuration)
        .style('opacity', 0)
        .remove();

      const newCircles = vm.select.circles.enter()
        .append('circle');

      newCircles
        .attr('class', 'node')
        .attr('cx', () => vm.focusNode.x)
        .attr('cy', () => vm.focusNode.y)
        .attr('r', 3)
        .classed('node-focus', d => d.entity === vm.focusNodeEntity)
        .on('click', vm.handleNodeClicked)
        .call(d3.drag().on('drag', vm.dragged));

      vm.select.circles = newCircles.merge(vm.select.circles);

      vm.select.circles
        .transition()
        .duration(transitionDuration)
        .attr('cx', d => d.x)
        .attr('cy', d => d.y);

      vm.select.stars = vm.select.stars.data(starNodes, nodeKey);

      vm.select.stars
        .exit()
        .transition()
        .duration(transitionDuration)
        .style('opacity', 0)
        .remove();

      const newStars = vm.select.stars.enter()
        .append('polygon')
        .attr('class', 'node')
        .attr('points', () => {
          const center = { x: vm.focusNode.x, y: vm.focusNode.y };
          const coordinates = getStarCoordinates(center, 2, 5);
          return coordinates.map((p) => {
            const coord = [p.x, p.y];
            return coord.join(',');
          }).join(' ');
        })
        .on('click', vm.handleNodeClicked)
        .call(d3.drag().on('drag', vm.dragged));

      vm.select.stars = newStars.merge(vm.select.stars);

      vm.select.stars
        .transition()
        .duration(transitionDuration)
        .attr('points', (d) => {
          const center = { x: d.x, y: d.y };
          const coordinates = getStarCoordinates(center, 2, 5);
          return coordinates.map((p) => {
            const coord = [p.x, p.y];
            return coord.join(',');
          }).join(' ');
        });

      vm.select.nodelabels = vm.select.nodelabels.data(vm.nodes, nodeKey);

      vm.select.nodelabels
        .exit()
        .transition()
        .duration(transitionDuration)
        .remove();

      vm.select.nodelabels
        .exit()
        .select('text')
        .transition()
        .duration(transitionDuration)
        .attr('opacity', 0)
        .remove();

      const newNodeLabels = vm.select.nodelabels
        .enter()
        .append('g')
        .attr('class', 'nodelabel')
        .on('click', vm.handleNodeClicked)
        .call(d3.drag().on('drag', vm.dragged));

      newNodeLabels.append('text')
        .attr('class', 'label')
        .attr('x', () => vm.focusNode.x)
        .attr('y', () => vm.focusNode.y)
        .attr('opacity', 0)
        .style('text-anchor', 'middle')
        .text((d) => {
          const t = `${d.prenom} ${d.nom} (${d.degree})`;
          return t;
        });

      vm.select.nodelabels = newNodeLabels.merge(vm.select.nodelabels);

      vm.select.nodelabels
        .select('text')
        .transition()
        .duration(transitionDuration)
        .attr('x', d => d.x)
        .attr('y', d => d.y)
        .attr('opacity', 1);
    },
    dragged(d) {
      d.x = d3.event.x;
      d.y = d3.event.y;
      this.draw({ transitionDuration: 0 });
    },
    zoomed() {
      if (this.select.graph) {
        this.select.graph.attr('transform', d3.event.transform);
      }
    },
    zoomIn() {
      this.zoom.scaleBy(this.select.svg.transition().duration(200), 1.2);
    },
    zoomOut() {
      this.zoom.scaleBy(this.select.svg.transition().duration(200), 1 / 1.2);
    },
    zoomReset() {
      this.select.svg.call(this.zoom.transform, d3.zoomIdentity);
      this.zoom.scaleTo(this.select.svg.transition(), 2.5);
    },
    handleNodeClicked(node) {
      this.$store.commit(UPDATE_FOCUS_NODE, node.entity);
      this.updateFocusNode();
    },
    handleNodeDblclicked() {
      console.log('Node double clicked');
    },
    updateFocusNode() {
      const vm = this;
      vm.select.circles.classed('node-focus', d => d.entity === vm.focusNodeEntity);
      vm.select.stars.classed('node-focus', d => d.entity === vm.focusNodeEntity);
    },
    getContainerSize() {
      const { width, height } = d3.select('#graph-container').node().getBoundingClientRect();
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

.arrowhead path {
  fill: $asbestos;
}


.node, .triangle {
  fill: $peter-river;
  opacity: 0.5;
}

.node, .node-label, .flag {
  cursor: pointer;
}

.node-focus {
  opacity: 1;
}

.link {
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

var app = new Vue({
  el: '#app',
  data: {
    datasets: [],
    dataset: "default",
    picked: "topBen",
    selected: "default",
    topBeneficiaries: [],
    topDonneurs: [],
    isReady: false,
    isLoading: true,
    nodeHovered: null,
    linkHovered: null
  },
  computed: {
    isNodeHovered: function () { return this.nodeHovered !== null; },
    isLinkHovered: function () { return this.linkHovered !== null; },
    infoBackgroundColor: function () {
      return this.nodeHovered.entity === this.selected ? "var(--pomegranate)" : "var(--peter-river)";
    },
    breakDownLinks: function () {
      var vm = this;
      if (vm.linkHovered === null) {
        return [];
      } else {
        return vm.multiDiGraph.links.filter(function (l) {
          if (vm.source(l) == vm.source(vm.linkHovered) && vm.target(l) == vm.target(vm.linkHovered)) {
            return true;
          }
          return false;
        })
      }
    }
  },
  watch: {
    dataset: function(dataset){

      var vm = this;
      if (dataset == "default") {
        vm.topBeneficiaries = [];
        vm.topDonneurs = [];
      } else {
        // Load top donneurs and top beneficiaires list
        var topBeneficiariesUrl = typeof(getWebAppBackendUrl) === 'undefined' ? 
          "/top_beneficiaries": 
          getWebAppBackendUrl('top_beneficiaries');

        var topDonneursUrl = typeof(getWebAppBackendUrl) === 'undefined' ? 
          "/top_donneurs":
          getWebAppBackendUrl('top_donneurs');

        vm.isLoading = true;

        var promiseTopBen = new Promise(function (resolve) {
          var fullUrl = topBeneficiariesUrl + "?dataset=" + dataset;
          $.getJSON(fullUrl, function (topBen) {
            vm.topBeneficiaries = topBen;
            resolve();
          });
        });

        var promiseTopDon = new Promise(function (resolve) {
          var fullUrl = topDonneursUrl + "?dataset=" + dataset;
          $.getJSON(fullUrl, function (topDon) {
            vm.topDonneurs = topDon;
            resolve();
          });
        })

        Promise.all([promiseTopBen, promiseTopDon]).then(function () {
          vm.isLoading = false;
        });
      }
 
    },
    selected: function (v) {
      // update the data and re-draw the graph
      if (this.selected != "default") {
        if (this.simulation) {
          this.simulation.stop();
        } else {
          var svgSize = this.getSvgSize();
          this.simulation = d3.forceSimulation()
            .force("link", d3.forceLink().id(function (d) { return d.id; }).distance(50))
            .force("charge", d3.forceManyBody())
            .force("center", d3.forceCenter(svgSize.width / 2, svgSize.height / 2))
        }
        var networkUrl = this.getNetworkUrl();
        this.isLoading = true;
        var vm = this;
        vm.diGraph = { links: [], nodes: [] };
        vm.draw();
        $.getJSON(networkUrl, function (response) {

          vm.isLoading = false;
          // de-activate all nodes and links by default
          vm.diGraph = response.data;
          vm.diGraph = vm.collapseAll(vm.diGraph);
          vm.diGraph = vm.expand(vm.diGraph, vm.selected);

          vm.draw();
        })
      }
    }
  },
  created: function () {

    var datasetsUrl = typeof(getWebAppBackendUrl) === 'undefined' ? "/datasets" : getWebAppBackendUrl('datasets');
    var vm = this;

    $.getJSON(datasetsUrl, function(datasets){
      vm.datasets = datasets;
      vm.isReady = true;
      vm.isLoading = false;  
    })

  },
  mounted: function () {
    
    this.svg = d3.select("svg");
    this.graph = d3.select(".graph");
    this.link = d3.select(".links").selectAll(".link");
    this.edgepaths = d3.select(".edgepaths").selectAll(".edgepath");
    this.edgelabels = d3.select(".edgelabels").selectAll(".edgelabel");
    this.node = d3.select(".nodes").selectAll(".node");
    this.text = d3.select('.nodelabels').selectAll(".nodelabel");

    this.svg.call(d3.zoom().scaleExtent([1, 16]).on("zoom", this.zoomed));
  },
  beforeDestroy: function () {
    window.removeEventListener('resize', this.handleResize);
  },
  methods: {
    getSvgSize: function(){
      var svg = document.getElementById("svg")
      var boundingClientRect = svg.getBoundingClientRect() 
      return { width: boundingClientRect.width, height: boundingClientRect.height };
    },
    getNetworkUrl: function () {
      if (this.selected != "default" && this.dataset != "default") {
        var baseUrl = typeof(getWebAppBackendUrl) === 'undefined' ? "/draw_network" : getWebAppBackendUrl('draw_network');
        return baseUrl + "?id=" + this.selected + "&" + "dataset=" + this.dataset;
      }
      return "";
    },
    zoomed: function () {
      if (this.graph) {
        this.graph.attr("transform", d3.event.transform);
      }
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
    ticked: function () {
      var vm = this;
      vm.link
        .attr("x1", function (d) { return d.source.x; })
        .attr("y1", function (d) { return d.source.y; })
        .attr("x2", function (d) { return d.target.x; })
        .attr("y2", function (d) { return d.target.y; });

      vm.node
        .attr("cx", function (d) { return d.x; })
        .attr("cy", function (d) { return d.y; });

      vm.text
        .attr("transform", function (d) { return "translate(" + d.x + "," + d.y + ")" })

      vm.edgepaths.attr('d', function (d) {
        return 'M ' + d.source.x + ' ' + d.source.y + ' L ' + d.target.x + ' ' + d.target.y;
      });

      vm.edgelabels.attr('transform', function (d) {
        if (d.target.x < d.source.x) {
          var bbox = this.getBBox();
          rx = bbox.x + bbox.width / 2;
          ry = bbox.y + bbox.height / 2;
          return 'rotate(180 ' + rx + ' ' + ry + ')';
        }
        else {
          return 'rotate(0)';
        }
      });
    },
    source: function (link) {
      // For some reasons links have either of these two formats
      // 1. { source: 1, target: 2 }
      // 2. { source { entity: 1 }, target: { entity: 2 } }
      return typeof (link.source) === 'object' ? link.source.entity : link.source
    },
    target: function (link) {
      return typeof (link.target) === 'object' ? link.target.entity : link.target
    },
    collapseAll: function (graph) {
      var collapsedGraph = {};
      collapsedGraph.nodes = graph.nodes.map(function (node) {
        node.active = false;
        return node;
      });
      collapsedGraph.links = graph.links.map(function (link) {
        link.active = false;
        return link;
      });
      return collapsedGraph;
    },
    expand: function (graph, node) {
      // expand the graph around a node
      var expandedGraph = {};
      var neighbors = [];
      var vm = this;
      expandedGraph.links = graph.links.map(function (link) {
        if (vm.source(link) === node) {
          link.active = true;
          neighbors.push(vm.target(link));
        } else if (vm.target(link) === node) {
          link.active = true;
          neighbors.push(vm.source(link));
        }
        return link;
      });
      expandedGraph.nodes = graph.nodes.map(function (n) {
        if (neighbors.indexOf(n.entity) > -1) {
          n.active = true;
        } else if (n.entity == node) {
          n.active = true;
          n.expanded = true;
        }
        return n;
      })
      return expandedGraph;
    },
    collapse: function (graph, node) {
      var vm = this;
      var collapsedGraph = {};
    },
    expandOrCollapse: function (n) {
      var vm = this;
      if (n.expanded) {
        // TODO collapse
        console.log("should collapse")
      } else {
        vm.diGraph = vm.expand(vm.diGraph, n.entity);
      }
      vm.draw();
    },
    draw: function () {
      var vm = this;

      var activeLinks = vm.diGraph.links.filter(function (link) { return link.active; });
      var activeNodes = vm.diGraph.nodes.filter(function (node) { return node.active; });

      function linkKey(link) {
        return vm.source(link) + "-" + vm.target(link);
      }

      function nodeKey(node) {
        return node.entity;
      }

      vm.link = vm.link.data(activeLinks, linkKey);

      vm.link
        .exit()
        .transition()
        .attr("stroke-opacity", 0)
        .attrTween("x1", function (d) { return function () { return d.source.x; } })
        .attrTween("x2", function (d) { return function () { return d.target.x; } })
        .attrTween("y1", function (d) { return function () { return d.source.y; } })
        .attrTween("y2", function (d) { return function () { return d.target.y; } })
        .remove();

      var newLinks = vm.link.enter()
        .append("line")
        .call(function (link) { link.transition().attr("stroke-opacity", 0.2) })
        .attr("class", "link")
        .attr("marker-end", "url(#arrowhead)")
        .attr("stroke", "var(--asbestos)")
        .attr("stroke-width", "1")
        .on("mouseenter", vm.handleLinkMouseEnter)
        .on("mouseout", vm.handleLinkMouseOut)

      vm.link = newLinks.merge(vm.link);

      vm.edgepaths = vm.edgepaths.data(activeLinks, linkKey)

      vm.edgepaths.exit().remove();

      vm.edgepaths = vm.edgepaths.enter()
        .append('path')
        .attr('class', 'edgepath')
        .attr('fill-opacity', 0)
        .attr('stroke-opacity', 0)
        .style("pointer-events", "none")
        .merge(vm.edgepaths)
        .attr('id', function (d, i) { return 'edgepath' + i })


      vm.edgelabels = vm.edgelabels.data(activeLinks, linkKey);

      vm.edgelabels.exit().remove();

      var newEdgelabels = vm.edgelabels.enter()
        .append('text')
        .style('pointer-events', 'none')
        .attr('class', 'edgelabel')
        .attr('font-family', 'sans-serif')
        .attr('font-size', "2px")

      newEdgelabels.append('textPath')
        .style('text-anchor', 'middle')
        .style("pointer-events", "none")
        .style('fill', 'black')
        .attr("startOffset", "50%")
        .text(function (d) {
          var rounded = Math.round(d.valeur_euro);
          var localized = rounded.toLocaleString('fr-FR');
          return localized + "€" + " (" + d.transactions.length + ")";
        });

      vm.edgelabels = newEdgelabels.merge(vm.edgelabels)
        .attr('id', function (d, i) { return 'edgelabel' + i })

      vm.edgelabels.select("textPath")
        .attr('xlink:href', function (d, i) { return '#edgepath' + i })

      vm.node = vm.node.data(activeNodes, nodeKey);

      vm.node.exit().transition().attr("r", 0).remove();

      var newNode = vm.node.enter()
        .append("circle")
        .attr("class", "node")
        .attr("fill", function (d) {
          return d.id == app.selected ? "var(--pomegranate)" : "var(--peter-river)";
        })
        .attr("opacity", 0.5)
        .call(function (node) { node.transition().attr("r", 3); })
        .attr("cursor", "grab")
        .on("click", function (n) {
          vm.expandOrCollapse(n);
        })
        .on("mouseenter", vm.handleNodeMouseEnter)
        .on("mouseout", vm.handleNodeMouseOut)
        .call(d3.drag()
          .on("start", vm.dragstarted)
          .on("drag", vm.dragged)
          .on("end", vm.dragended));

      vm.node = newNode.merge(vm.node);

      vm.text = vm.text.data(activeNodes, nodeKey);

      vm.text.exit().remove();

      var newText = vm.text
        .enter()
        .append("g")
        .attr("cursor", "grab")
        .attr("class", "nodelabel")
        .on("click", function (n) {
          vm.expandOrCollapse(n);
        })
        .on("mouseenter", this.handleNodeMouseEnter)
        .on("mouseout", this.handleNodeMouseOut)
        .call(d3.drag()
          .on("start", vm.dragstarted)
          .on("drag", vm.dragged)
          .on("end", vm.dragended))


      newText.append("text")
        .attr("x", 0)
        .attr("y", 0)
        .style("text-anchor", "middle")
        .style("font-family", "sans-serif")
        .style("font-size", "2px")
        .style("fill", "black")
        .text(function (d) {
          var label = d.prenom_nom + " (" + d.degree + ")"
          return label;
        })

      vm.text = newText.merge(vm.text)

      vm.simulation
        .nodes(activeNodes)
        .on("tick", vm.ticked);

      vm.simulation.force("link").links(activeLinks)

      vm.simulation.alpha(1).restart()

    },
    handleNodeMouseEnter: function (n) {
      this.nodeHovered = n;
    },
    handleNodeMouseOut: function (n) {
      this.nodeHovered = null;
    },
    handleLinkMouseEnter: function (l) {
      this.linkHovered = l;
    },
    handleLinkMouseOut: function (l) {
      this.linkHovered = null;
    }
  }
});

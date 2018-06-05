var app = new Vue({
  el: '#app',
  data: {
    datasets: [], /* the list of datasets */
    datasetSelected: { id: "", name: "" },  /* the dataset selected in the dropdown */
    dropdownContentDisplay: "none", /* used to toggle the dropdown  */
    drawerExpanded: true, /* used to expand or collapse the dropdown */
    loaderDisplay: "block", /* used to display or hide the loader */
    detailsModalDisplay: "none", /* used to display or hide the "Details" modal */
    searchPattern: "", /* bind to the content of the search input */
    searchSuggestions: [], /* a list of at most 5 search suggestions matching the searchPattern */
    searchEntity: null, /* this is set when selecting a search suggestion */
    focusNode: null, /* the node under focus. Nodes can be focused with a simple click */
    diGraph: {}, /* all the nodes and links contained in the connected component of searchEntity */
    linkDetail: null /* information used in the "Details" modal */
  },
  computed: {
    // class used in the drawer button to change the direction of the arrow
    arrowClass: function () {
      return this.drawerExpanded ? "arrow-left" : "arrow-right";
    },
    // style of the collapsable drawer
    drawerStyle: function () {
      var drawerWidth = this.drawerExpanded ? "355px" : "0px";
      var drawerDisplay = this.focusNode ? "block" : "none";
      return {
        "display": drawerDisplay,
        "min-width": drawerWidth,
        "max-width": drawerWidth
      }
    },
    // style of the container displaying the name and address of the node under focus 
    identityCardStyle: function () {
      var backgroundColor = this.focusNode ?
        this.focusNode.entity == this.searchEntity ?
          "var(--pomegranate)" :
          "var(--peter-river)" : {};
      return { "background-color": backgroundColor };
    },
    // return all the outbound links of the node under focus 
    outLinks: function () {
      var vm = this;
      if (vm.diGraph && vm.focusNode) {
        var links = vm.diGraph.links.filter(function (link) {
          return vm.source(link) == vm.focusNode.entity;
        });
        return links.map(function (link) {
          link.source = typeof (link.source) === 'object' ? link.source : vm.getNode(link.source);
          link.target = typeof (link.target) === 'object' ? link.target : vm.getNode(link.target);
          return link;
        });
      }
      return [];
    },
    // returns all the inbound links of the node under focus 
    inLinks: function () {
      var vm = this;
      if (vm.diGraph && vm.focusNode) {
        var links = vm.diGraph.links.filter(function (link) {
          return vm.target(link) == vm.focusNode.entity;
        })
        return links.map(function (link) {
          link.source = typeof (link.source) === 'object' ? link.source : vm.getNode(link.source);
          link.target = typeof (link.target) === 'object' ? link.target : vm.getNode(link.target);
          return link;
        });
      }
      return [];
    }
  },
  watch: {
    // call the /search endpoint as the user types.
    // the api calls are debounced (see utils.js) 
    searchPattern: debounce(function () {
      if (document.activeElement.id == "search-input") {
        this.search();
      }
    }, 300),
    // call the /connected_component endpoint when the person were are searching 
    // changes and redraw the graph 
    searchEntity: function (entity) {
      var vm = this;
      this.loaderDisplay = "block";
      
      if (vm.simulation) {
        vm.simulation.stop();
      } else {
        var svgSize = vm.getSvgSize();
        vm.simulation = d3.forceSimulation()
          .force("link", d3.forceLink().id(function (d) { return d.id; }).distance(50))
          .force("charge", d3.forceManyBody())
          .force("center", d3.forceCenter((svgSize.width - 355) / 2, svgSize.height / 2))
      }

      var networkUrl = this.getNetworkUrl();
      vm.diGraph = { links: [], nodes: [] };

      vm.draw();

      $.getJSON(networkUrl, function (response) {
        vm.isLoading = false;
        // de-activate all nodes and links by default
        vm.diGraph = response.data;
        vm.diGraph = vm.collapseAll(vm.diGraph);
        vm.diGraph = vm.expand(vm.diGraph, vm.searchEntity);

        // search the node corresponding to the search entity
        vm.focusNode = vm.diGraph.nodes.find(function (node) {
          return node.entity == entity;
        })

        vm.loaderDisplay = "none";
        
        vm.draw();
      })
    },
    // change the opacity of the nodes when we click a different one
    focusNode: function () {
      var vm = this;
      vm.circles.attr("opacity", function (node) {
        return node.entity == vm.focusNode.entity ? 0.9 : 0.5;
      })
      vm.stars.attr("opacity", function (node) {
        return node.entity == vm.focusNode.entity ? 0.9 : 0.5;
      })
    }
  },
  // this code is executed once Vue.js has mounted <div id="#app">
  mounted: function () {
    var datasetsUrl = typeof (getWebAppBackendUrl) === 'undefined' ? "/datasets" : getWebAppBackendUrl('datasets');
    var vm = this;
    
    /* get a list of available datasets*/
    $.getJSON(datasetsUrl, function (datasets) { 
      vm.datasets = datasets;
      vm.datasetSelected = vm.datasets[0]
      vm.loaderDisplay = "none";
    })
    window.addEventListener("click", this.handleWindowClicked);

    /* bind variables to the graph containers, they are used in the "draw" function */
    this.svg = d3.select("svg");
    this.graph = d3.select(".graph");
    this.links = d3.select(".links").selectAll(".link");
    this.edgepaths = d3.select(".edgepaths").selectAll(".edgepath");
    this.edgelabels = d3.select(".edgelabels").selectAll(".edgelabel");
    this.circles = d3.select(".nodes").selectAll(".circle");
    this.stars = d3.select(".nodes").selectAll(".star")
    this.nodelabels = d3.select('.nodelabels').selectAll(".nodelabel");
    this.zoom = d3.zoom().scaleExtent([1, 16]).on("zoom", this.zoomed)
    this.svg.call(this.zoom).on("dblclick.zoom", null);
  },
  beforeDestroy: function () {
    window.removeEventListener("click", this.handleWindowClicked);
  },
  methods: {
    // returns the size of the svg element
    getSvgSize: function () {
      var svg = document.getElementById("svg")
      var boundingClientRect = svg.getBoundingClientRect()
      return { width: boundingClientRect.width, height: boundingClientRect.height };
    },
    // get the coordinates of a 5 branch stars
    getStarCoordinates: function(center, innerRadius, outerRadius){
      var branches = 5;
      var coordinates = [];
      var theta = 0;
      for (var i = 0; i < 2 * branches; i++) {
        if (i % 2 == 0) {
          // outer circle
          var x = center.x + outerRadius * Math.cos(theta);
          var y = center.y + outerRadius * Math.sin(theta);
        } else {
          // inner circle
          var x = center.x + innerRadius * Math.cos(theta);
          var y = center.y + innerRadius * Math.sin(theta);
        }
        coordinates.push({x: x, y: y})
        theta = theta + Math.PI / branches;
      }
      return coordinates;
    },
    zoomed: function () {
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
    // this method is called by the force directed simulation to change the layout
    ticked: function () {
      var vm = this;
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
          var coordinates = vm.getStarCoordinates(center, 2, 5);
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
    getNetworkUrl: function () {
      var baseUrl = typeof (getWebAppBackendUrl) === 'undefined' ? "/connected_component" : getWebAppBackendUrl('connected_component');
      return baseUrl + "?id=" + this.searchEntity + "&" + "dataset=" + this.datasetSelected.id;
    },
    handleDrawerButtonClicked: function () {
      this.drawerExpanded = !this.drawerExpanded;
    },
    handleWindowClicked: function (event) {
      var detailsModal = document.getElementById('details-modal');
      if (event.target == detailsModal) {
        this.closeModal()
      }
      if (document.activeElement.id != "search-input") {
        this.searchSuggestions = [];
      }
    },
    handleDropdownItemClicked: function (event) {
      this.datasetSelected = { id: event.target.getAttribute("value"), name: event.target.textContent };
      this.closeDropdown();
    },
    handleSearchSuggestionClicked: function (event) {
      this.searchEntity = parseInt(event.target.getAttribute("value"));
      this.searchPattern = event.target.textContent;
      this.searchSuggestions = [];
    },
    clearSearch: function (event) {
      this.searchPattern = "";
      this.searchSuggestions = [];
    },
    handleSearchInputFocus: function () {
      this.search();
    },
    openModal: function (link) {
      this.linkDetail = link;
      this.detailsModalDisplay = "block";
    },
    closeModal: function () {
      this.detailsModalDisplay = "none";
    },
    openDropdown: function () {
      this.dropdownContentDisplay = "block";
    },
    closeDropdown: function () {
      this.dropdownContentDisplay = "none";
    },
    search: function () {
      var searchUrl = typeof (getWebAppBackendUrl) === 'undefined' ? "/search" : getWebAppBackendUrl('search');
      var fullUrl = searchUrl + "?dataset=" + this.datasetSelected.id + "&" + "pattern=" + this.searchPattern;
      var vm = this;
      $.getJSON(fullUrl, function (suggestions) {
        vm.searchSuggestions = suggestions;
      })
    },
    handleNodeClicked: function (n) {
      this.focusNode = n;
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
    getNode: function (entity) {
      return this.diGraph.nodes.find(function (n) {
        return n.entity == entity;
      })
    },
    // Deactivates all nodes 
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
    // expand the graph around a node
    expand: function (graph, node) {
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
    // this function does all the d3 magic. See d3.js update pattern to understand how it works
    draw: function () {

      var vm = this;

      var activeLinks = vm.diGraph.links.filter(function (link) { return link.active; });
      var activeNodes = vm.diGraph.nodes.filter(function (node) { return node.active; });
      var circleNodes = activeNodes.filter(function(node) { return !node.star })
      var starNodes = activeNodes.filter(function(node) { return node.star })

      function linkKey(link) {
        return vm.source(link) + "-" + vm.target(link);
      }

      function nodeKey(node) {
        return node.entity;
      }

      vm.links = vm.links.data(activeLinks, linkKey);

      vm.links
        .exit()
        .transition()
        .attr("stroke-opacity", 0)
        .attrTween("x1", function (d) { return function () { return d.source.x; } })
        .attrTween("x2", function (d) { return function () { return d.target.x; } })
        .attrTween("y1", function (d) { return function () { return d.source.y; } })
        .attrTween("y2", function (d) { return function () { return d.target.y; } })
        .remove();

      var newLinks = vm.links.enter()
        .append("line")
        .call(function (link) { link.transition().attr("stroke-opacity", 0.2) })
        .attr("class", "link")
        .attr("marker-end", "url(#arrowhead)")
        .attr("stroke", "var(--asbestos)")
        .attr("stroke-width", "1")
        .on("mouseenter", vm.handleLinkMouseEnter)
        .on("mouseout", vm.handleLinkMouseOut)

      vm.links = newLinks.merge(vm.links);

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

      vm.circles = vm.circles.data(circleNodes, nodeKey);

      vm.circles.exit().transition().attr("r", 0).remove();

      var newCircles = vm.circles.enter()
        .append("circle")
        .attr("class", "node")
        .attr("fill", function (d) {
          return d.id == vm.searchEntity ? "var(--pomegranate)" : "var(--peter-river)";
        })
        .attr("opacity", function (node) {
          return node.entity == vm.focusNode.entity ? 1.0 : 0.5;
        })
        .call(function (node) { node.transition().attr("r", 3); })
        .on("click", vm.handleNodeClicked)
        .on("dblclick", vm.expandOrCollapse)
        .call(d3.drag()
          .on("start", vm.dragstarted)
          .on("drag", vm.dragged)
          .on("end", vm.dragended));

      vm.circles = newCircles.merge(vm.circles);

      vm.stars = vm.stars.data(starNodes, nodeKey);

      vm.stars.exit().remove();

      var newStars= vm.stars.enter()
        .append("polygon")
        .attr("class", "triangle")
        .attr("fill", function (d) {
          return d.id == vm.searchEntity ? "var(--pomegranate)" : "var(--peter-river)";
        })
        .attr("opacity", function (node) {
          return node.entity == vm.focusNode.entity ? 1.0 : 0.5;
        })
        .on("click", vm.handleNodeClicked)
        .on("dblclick", vm.expandOrCollapse)
        .call(d3.drag()
          .on("start", vm.dragstarted)
          .on("drag", vm.dragged)
          .on("end", vm.dragended));

      vm.stars = newStars.merge(vm.stars);

      vm.nodelabels = vm.nodelabels.data(activeNodes, nodeKey);

      vm.nodelabels .exit().remove();

      var newNodeLabels = vm.nodelabels 
        .enter()
        .append("g")
        .attr("class", "nodelabel")
        .on("click", vm.handleNodeClicked)
        .on("dblclick", vm.expandOrCollapse)
        .call(d3.drag()
          .on("start", vm.dragstarted)
          .on("drag", vm.dragged)
          .on("end", vm.dragended))

      newNodeLabels.append("text")
        .attr("x", 0)
        .attr("y", 0)
        .style("text-anchor", "middle")
        .style("font-size", "2px")
        .style("fill", "black")
        .text(function (d) {
          var label = d.prenom_nom + " (" + d.degree + ")"
          return label;
        })

      vm.nodelabels = newNodeLabels.merge(vm.nodelabels)

      vm.simulation
        .nodes(activeNodes)
        .on("tick", vm.ticked);

      vm.simulation.force("link").links(activeLinks)

      vm.simulation.alpha(1).restart()

    }
  }
})
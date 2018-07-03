import * as d3 from "d3";



onmessage = (event) => {

  let { nodes, links, center } = event.data;

  let simulation = d3.forceSimulation(nodes)
    .force("link", d3.forceLink(links).id(d => d.entity).distance(50))
    .force("charge", d3.forceManyBody())
    .force("center", d3.forceCenter(center.x, center.y))
    .stop();

  for (var i = 0, n = Math.ceil(Math.log(simulation.alphaMin()) / Math.log(1 - simulation.alphaDecay())); i < n; ++i) {
    simulation.tick();
  }

  postMessage({nodes: nodes, links: links});

};
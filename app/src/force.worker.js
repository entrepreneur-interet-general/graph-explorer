import * as d3 from "d3";



onmessage = (event) => {

  let { nodes, links, center } = event.data;

  
  /* For some reasons, disconnected subgraphs are displayed very far apart 
  if we use d3.forceCenter(center.x, center.y). An alternative is to compute 
  the layout in a referential centered around (0, 0) and then to translate 
  all the nodes in the referential centered arround (center.x, center.y)
  */

  function translate(node, tx, ty) {
    if (node.x && node.y) {
      node.x = node.x + tx;
      node.y = node.y + ty;
    }
    if (node.fx && node.fy) {
      node.fx = node.fx + tx;
      node.fy = node.fy + ty;
    }
  }

  // center on (0, 0)
  nodes.forEach(node => {
    translate(node, -center.x, -center.y)
  })

  let simulation = d3.forceSimulation(nodes)
    .force("link", d3.forceLink(links).id(d => d.entity).distance(50))
    .force("charge", d3.forceManyBody().distanceMax(120))
    .force("center", d3.forceCenter(0, 0))
    .stop();

  for (var i = 0, n = Math.ceil(Math.log(simulation.alphaMin()) / Math.log(1 - simulation.alphaDecay())); i < n; ++i) {
    simulation.tick();
  }

  // center on (center.x, center.y) 
  nodes.forEach(node => {
    translate(node, center.x, center.y)
  })

  postMessage({nodes: nodes, links: links});

};
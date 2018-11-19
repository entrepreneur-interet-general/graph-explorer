import * as d3 from 'd3';

onmessage = (event) => {
  const { nodes, links, center } = event.data;


  /* For some reasons, disconnected subgraphs are displayed very far apart
  if we use d3.forceCenter(center.x, center.y). An alternative is to compute
  the layout in a referential centered around (0, 0) and then to translate
  all the nodes in the referential centered arround (center.x, center.y)
  */

  /* eslint no-param-reassign: ["error", { "props": false }] */

  function translate(node, tx, ty) {
    if (node.x && node.y) {
      node.x += tx;
      node.y += ty;
    }
    if (node.fx && node.fy) {
      node.fx += tx;
      node.fy += ty;
    }
  }

  // center on (0, 0)
  nodes.forEach(node => translate(node, -center.x, -center.y));

  const simulation = d3.forceSimulation(nodes)
    .force('link', d3.forceLink(links).id(d => d.entity).distance(50))
    .force('charge', d3.forceManyBody().distanceMax(120))
    .force('center', d3.forceCenter(0, 0))
    .stop();

  const n = Math.ceil(Math.log(simulation.alphaMin()) / Math.log(1 - simulation.alphaDecay()));
  for (let i = 0; i < n; i += 1) {
    simulation.tick();
  }

  // center on (center.x, center.y)
  nodes.forEach(node => translate(node, center.x, center.y));

  postMessage({ nodes, links });
};

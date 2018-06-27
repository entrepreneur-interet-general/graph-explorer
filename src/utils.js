export function getStarCoordinates(center, innerRadius, outerRadius){
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
}


export function array2dict(array, f) {
  return array.reduce((map, obj) => {
    const key = f(obj);
    map[key] = obj
    return map;
  }, {})
}
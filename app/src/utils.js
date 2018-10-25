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

// Taken from https://github.com/bjoerge/debounce-promise 
export function debounce (fn, wait = 0, options = {}) {
  let lastCallAt
  let deferred
  let timer
  let pendingArgs = []
  return function debounced (...args) {
    const currentWait = getWait(wait)
    const currentTime = new Date().getTime()

    const isCold = !lastCallAt || (currentTime - lastCallAt) > currentWait

    lastCallAt = currentTime

    if (isCold && options.leading) {
      return options.accumulate
        ? Promise.resolve(fn.call(this, [args])).then(result => result[0])
        : Promise.resolve(fn.call(this, ...args))
    }

    if (deferred) {
      clearTimeout(timer)
    } else {
      deferred = defer()
    }

    pendingArgs.push(args)
    timer = setTimeout(flush.bind(this), currentWait)

    if (options.accumulate) {
      const argsIndex = pendingArgs.length - 1
      return deferred.promise.then(results => results[argsIndex])
    }

    return deferred.promise
  }

  function flush () {
    const thisDeferred = deferred
    clearTimeout(timer)

    Promise.resolve(
      options.accumulate
        ? fn.call(this, pendingArgs)
        : fn.apply(this, pendingArgs[pendingArgs.length - 1])
    )
      .then(thisDeferred.resolve, thisDeferred.reject)

    pendingArgs = []
    deferred = null
  }
}

function getWait (wait) {
  return (typeof wait === 'function') ? wait() : wait
}

function defer () {
  const deferred = {}
  deferred.promise = new Promise((resolve, reject) => {
    deferred.resolve = resolve
    deferred.reject = reject
  })
  return deferred
}

export function json2csv(items){
  if (items.length === 0 ) {
    return '';
  }
  const replacer = (key, value) => value === null ? '' : value;
  const header = Object.keys(items[0]);
  let csv = items.map(row => {
      return header.map(fieldName =>{
        return JSON.stringify(row[fieldName], replacer)
      }).join(';')
    } 
  )
  csv.unshift(header.map(h => JSON.stringify(h)).join(';'));
  csv = csv.join('\r\n');
  return csv;
}
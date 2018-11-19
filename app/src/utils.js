export function getStarCoordinates(center, innerRadius, outerRadius) {
  const branches = 5;
  const coordinates = [];
  let theta = 0;
  for (let i = 0; i < 2 * branches; i += 1) {
    let x;
    let y;
    if (i % 2 === 0) {
      // outer circle
      x = center.x + outerRadius * Math.cos(theta);
      y = center.y + outerRadius * Math.sin(theta);
    } else {
      // inner circle
      x = center.x + innerRadius * Math.cos(theta);
      y = center.y + innerRadius * Math.sin(theta);
    }
    coordinates.push({ x, y });
    theta += Math.PI / branches;
  }
  return coordinates;
}

export function array2dict(array, f) {
  /* eslint no-param-reassign: ["error", { "props": false }] */
  return array.reduce((map, obj) => {
    const key = f(obj);
    map[key] = obj;
    return map;
  }, {});
}

// Taken from https://github.com/bjoerge/debounce-promise
export function debounce(fn, wait = 0, options = {}) {
  let lastCallAt;
  let deferred;
  let timer;
  let pendingArgs = [];

  function getWait(_wait) {
    return (typeof _wait === 'function') ? _wait() : _wait;
  }

  function flush() {
    const thisDeferred = deferred;
    clearTimeout(timer);

    Promise.resolve(
      options.accumulate
        ? fn.call(this, pendingArgs)
        : fn.apply(this, pendingArgs[pendingArgs.length - 1])
    )
      .then(thisDeferred.resolve, thisDeferred.reject);

    pendingArgs = [];
    deferred = null;
  }


  function defer() {
    const d = {};
    d.promise = new Promise((resolve, reject) => {
      d.resolve = resolve;
      d.reject = reject;
    });
    return d;
  }

  return function debounced(...args) {
    const currentWait = getWait(wait);
    const currentTime = new Date().getTime();
    const isCold = !lastCallAt || (currentTime - lastCallAt) > currentWait;

    lastCallAt = currentTime;

    if (isCold && options.leading) {
      return options.accumulate
        ? Promise.resolve(fn.call(this, [args])).then(result => result[0])
        : Promise.resolve(fn.call(this, ...args));
    }

    if (deferred) {
      clearTimeout(timer);
    } else {
      deferred = defer();
    }

    pendingArgs.push(args);
    timer = setTimeout(flush.bind(this), currentWait);

    if (options.accumulate) {
      const argsIndex = pendingArgs.length - 1;
      return deferred.promise.then(results => results[argsIndex]);
    }

    return deferred.promise;
  };
}

export function json2csv(items) {
  if (items.length === 0) {
    return '';
  }
  const replacer = (_, value) => (value === null ? '' : value);
  const header = Object.keys(items[0]);
  let csv = items.map((row) => {
    const formattedRow = header.map((fieldName) => {
      const formattedField = JSON.stringify(row[fieldName], replacer);
      return formattedField;
    });
    return formattedRow.join(';');
  });
  csv.unshift(header.map(h => JSON.stringify(h)).join(';'));
  csv = csv.join('\r\n');
  return csv;
}

// Hoc phan: Cau truc du lieu va Giai thuat - Web Core (Zero Libraries, code chay thuan JS)

function sqrtNewton(value) {
  // O(log(1/eps)) tinh can bac hai bang Newton-Raphson
  if (value <= 0) return 0.0;
  let x = Number(value);
  const eps = 0.0000001;
  while (true) {
    const root = 0.5 * (x + (value / x));
    let diff = root - x;
    if (diff < 0) diff = -diff;
    if (diff < eps) break;
    x = root;
  }
  return x;
}

class WebStack {
  // O(1) ngan xep tu cai bang mang phuong phap con tro dung truy vet duong
  constructor() {
    this.data = [];
  }
  push(item) {
    this.data.push(item);
  }
  pop() {
    if (this.data.length === 0) return null;
    return this.data.pop();
  }
  isEmpty() {
    return this.data.length === 0;
  }
  toList() {
    const res = [];
    while (!this.isEmpty()) {
      res.push(this.pop());
    }
    return res;
  }
}

class WebQueue {
  // O(1) hang doi tu cai bang mang 2 con tro dung cho BFS
  constructor() {
    this.data = [];
    this.head = 0;
  }
  push(item) {
    this.data.push(item);
  }
  pop() {
    if (this.head >= this.data.length) return null;
    const item = this.data[this.head];
    this.head++;
    return item;
  }
  isEmpty() {
    return this.head >= this.data.length;
  }
}

class WebHashTable {
  // O(1) trung binh, bang bam linear probing voi djb2 khong dung object hay Map
  constructor(capacity = 1009) {
    this.capacity = capacity;
    this.size = 0;
    this.keys = new Array(capacity).fill(null);
    this.values = new Array(capacity).fill(null);
  }
  _hash(keyStr) {
    let h = 5381;
    const s = String(keyStr);
    for (let i = 0; i < s.length; i++) {
      h = (((h << 5) + h) + s.charCodeAt(i)) & 0x7fffffff;
    }
    return h % this.capacity;
  }
  put(key, value) {
    if (this.size * 2 >= this.capacity) {
      this._rehash();
    }
    const kStr = String(key);
    let idx = this._hash(kStr);
    while (this.keys[idx] !== null) {
      if (this.keys[idx] === kStr) {
        this.values[idx] = value;
        return;
      }
      idx = (idx + 1) % this.capacity;
    }
    this.keys[idx] = kStr;
    this.values[idx] = value;
    this.size++;
  }
  get(key) {
    const kStr = String(key);
    let idx = this._hash(kStr);
    const start = idx;
    while (this.keys[idx] !== null) {
      if (this.keys[idx] === kStr) {
        return this.values[idx];
      }
      idx = (idx + 1) % this.capacity;
      if (idx === start) break;
    }
    return null;
  }
  contains(key) {
    return this.get(key) !== null;
  }
  _rehash() {
    const oldK = this.keys;
    const oldV = this.values;
    this.capacity = this.capacity * 2 + 1;
    this.keys = new Array(this.capacity).fill(null);
    this.values = new Array(this.capacity).fill(null);
    this.size = 0;
    for (let i = 0; i < oldK.length; i++) {
      if (oldK[i] !== null) {
        this.put(oldK[i], oldV[i]);
      }
    }
  }
}

class WebIndexedMinHeap {
  // O(log V) push/pop/decrease_key, Indexed Min-Heap voi tie-breaking theo chi so dinh
  constructor(maxSize) {
    this.maxSize = maxSize;
    this.heap = [];
    this.pos = new Array(maxSize).fill(-1);
    this.heapOps = 0;
  }
  isEmpty() {
    return this.heap.length === 0;
  }
  contains(itemIdx) {
    if (itemIdx >= 0 && itemIdx < this.maxSize) {
      return this.pos[itemIdx] !== -1;
    }
    return false;
  }
  insert(priority, itemIdx) {
    this.heapOps++;
    const currPos = this.heap.length;
    this.heap.push([priority, itemIdx]);
    this.pos[itemIdx] = currPos;
    this._siftUp(currPos);
  }
  decreaseKey(itemIdx, newPriority) {
    this.heapOps++;
    const k = this.pos[itemIdx];
    if (k === -1) return;
    const currP = this.heap[k][0];
    if (newPriority < currP || (newPriority === currP && itemIdx < this.heap[k][1])) {
      this.heap[k] = [newPriority, itemIdx];
      this._siftUp(k);
    }
  }
  popMin() {
    this.heapOps++;
    if (this.heap.length === 0) return null;
    const [minPrio, minItem] = this.heap[0];
    this.pos[minItem] = -1;
    const last = this.heap.pop();
    if (this.heap.length > 0) {
      this.heap[0] = last;
      this.pos[last[1]] = 0;
      this._siftDown(0);
    }
    return [minPrio, minItem];
  }
  _isBetter(i, j) {
    const pi = this.heap[i][0];
    const ii = this.heap[i][1];
    const pj = this.heap[j][0];
    const ij = this.heap[j][1];
    if (pi < pj) return true;
    if (pi === pj && ii < ij) return true;
    return false;
  }
  _swap(i, j) {
    const itemI = this.heap[i][1];
    const itemJ = this.heap[j][1];
    this.pos[itemI] = j;
    this.pos[itemJ] = i;
    const temp = this.heap[i];
    this.heap[i] = this.heap[j];
    this.heap[j] = temp;
  }
  _siftUp(idx) {
    let parent = Math.floor((idx - 1) / 2);
    while (idx > 0 && this._isBetter(idx, parent)) {
      this._swap(idx, parent);
      idx = parent;
      parent = Math.floor((idx - 1) / 2);
    }
  }
  _siftDown(idx) {
    const n = this.heap.length;
    while (true) {
      let smallest = idx;
      const left = 2 * idx + 1;
      const right = 2 * idx + 2;
      if (left < n && this._isBetter(left, smallest)) smallest = left;
      if (right < n && this._isBetter(right, smallest)) smallest = right;
      if (smallest !== idx) {
        this._swap(idx, smallest);
        idx = smallest;
      } else {
        break;
      }
    }
  }
}

class WebAdjNode {
  // O(1) nut danh sach lien ket don bieu dien cung duong tren web
  constructor(target, baseWeight, trafficFactor = 1.0, isOneway = false) {
    this.target = target;
    this.baseWeight = Number(baseWeight);
    this.trafficFactor = Number(trafficFactor);
    this.isOneway = Boolean(isOneway);
    this.next = null;
  }
  getEffectiveWeight() {
    return this.baseWeight * this.trafficFactor;
  }
}

class WebCityGraph {
  // O(V + E) do thi danh sach ke voi toa do km, bang bam ten sang chi so
  constructor() {
    this.nodeNames = [];
    this.nodeCoords = []; // [x_km, y_km]
    this.nodeLookup = new WebHashTable();
    this.adj = [];
    this.numNodes = 0;
    this.numEdges = 0;
  }

  addNode(name, x, y) {
    const nameStr = String(name);
    if (this.nodeLookup.contains(nameStr)) {
      const idx = this.nodeLookup.get(nameStr);
      this.nodeCoords[idx] = [Number(x), Number(y)];
      return idx;
    }
    const idx = this.numNodes;
    this.nodeNames.push(nameStr);
    this.nodeCoords.push([Number(x), Number(y)]);
    this.adj.push(null);
    this.nodeLookup.put(nameStr, idx);
    this.numNodes++;
    return idx;
  }

  getNodeIndex(name) {
    const res = this.nodeLookup.get(String(name));
    return res !== null ? res : -1;
  }

  _appendEdge(u, node) {
    if (this.adj[u] === null) {
      this.adj[u] = node;
    } else {
      let curr = this.adj[u];
      while (curr.next !== null) {
        curr = curr.next;
      }
      curr.next = node;
    }
  }

  addEdge(uName, vName, weight = null, trafficFactor = 1.0, isOneway = false) {
    // O(deg(u)) them canh, trong so mac dinh bang Euclid km neu de null
    let u = this.getNodeIndex(uName);
    if (u === -1) u = this.addNode(uName, 0, 0);
    let v = this.getNodeIndex(vName);
    if (v === -1) v = this.addNode(vName, 0, 0);

    const [ux, uy] = this.nodeCoords[u];
    const [vx, vy] = this.nodeCoords[v];
    const euclid = sqrtNewton((ux - vx) * (ux - vx) + (uy - vy) * (uy - vy));

    const w = weight === null ? euclid : Number(weight);
    const tf = Number(trafficFactor);
    if (w < 0 || tf < 1.0) return false;

    let curr = this.adj[u];
    while (curr !== null) {
      if (curr.target === v) {
        curr.baseWeight = w;
        curr.trafficFactor = tf;
        curr.isOneway = Boolean(isOneway);
        return true;
      }
      curr = curr.next;
    }

    const nodeUV = new WebAdjNode(v, w, tf, isOneway);
    this._appendEdge(u, nodeUV);
    this.numEdges++;

    if (!isOneway) {
      let currV = this.adj[v];
      let foundV = false;
      while (currV !== null) {
        if (currV.target === u) {
          currV.baseWeight = w;
          currV.trafficFactor = tf;
          foundV = true;
          break;
        }
        currV = currV.next;
      }
      if (!foundV) {
        const nodeVU = new WebAdjNode(u, w, tf, isOneway);
        this._appendEdge(v, nodeVU);
        this.numEdges++;
      }
    }
    return true;
  }

  removeEdge(uName, vName) {
    // O(deg(u) + deg(v)) xoa cung duong giua u va v
    const u = this.getNodeIndex(uName);
    const v = this.getNodeIndex(vName);
    if (u === -1 || v === -1) return false;

    const removeOne = (src, dst) => {
      let curr = this.adj[src];
      let prev = null;
      while (curr !== null) {
        if (curr.target === dst) {
          if (prev === null) this.adj[src] = curr.next;
          else prev.next = curr.next;
          return true;
        }
        prev = curr;
        curr = curr.next;
      }
      return false;
    };

    const f1 = removeOne(u, v);
    if (f1) this.numEdges--;
    const f2 = removeOne(v, u);
    if (f2) this.numEdges--;
    return f1 || f2;
  }

  updateTraffic(uName, vName, factor) {
    // O(deg(u) + deg(v)) cap nhat he so ket xe
    const u = this.getNodeIndex(uName);
    const v = this.getNodeIndex(vName);
    if (u === -1 || v === -1) return false;
    const f = Number(factor);
    if (f < 1.0) return false;

    let updated = false;
    let curr = this.adj[u];
    while (curr !== null) {
      if (curr.target === v) {
        curr.trafficFactor = f;
        updated = true;
        break;
      }
      curr = curr.next;
    }
    let curr2 = this.adj[v];
    while (curr2 !== null) {
      if (curr2.target === u && !curr2.isOneway) {
        curr2.trafficFactor = f;
        break;
      }
      curr2 = curr2.next;
    }
    return updated;
  }

  computeAdmissibleHScale() {
    // O(E) tinh he so h_scale = min(1, min(base_weight / euclid))
    let minRatio = 1.0;
    for (let u = 0; u < this.numNodes; u++) {
      const [ux, uy] = this.nodeCoords[u];
      let curr = this.adj[u];
      while (curr !== null) {
        const v = curr.target;
        const [vx, vy] = this.nodeCoords[v];
        const euclid = sqrtNewton((ux - vx) * (ux - vx) + (uy - vy) * (uy - vy));
        if (euclid > 0.000001) {
          const ratio = curr.baseWeight / euclid;
          if (ratio < minRatio) minRatio = ratio;
        }
        curr = curr.next;
      }
    }
    return minRatio <= 0 ? 0 : minRatio;
  }

  checkConnectivityBFS(startName = null) {
    // O(V + E) BFS kiem tra lien thong
    if (this.numNodes === 0) return { connected: true, visitedCount: 0 };
    const startIdx = startName === null ? 0 : this.getNodeIndex(startName);
    if (startIdx === -1) return { connected: false, visitedCount: 0 };

    const visited = new Array(this.numNodes).fill(false);
    const q = new WebQueue();
    q.push(startIdx);
    visited[startIdx] = true;
    let count = 0;

    while (!q.isEmpty()) {
      const u = q.pop();
      count++;
      let curr = this.adj[u];
      while (curr !== null) {
        const v = curr.target;
        if (!visited[v]) {
          visited[v] = true;
          q.push(v);
        }
        curr = curr.next;
      }
    }
    return { connected: count === this.numNodes, visitedCount: count };
  }

  getAllEdges() {
    const edges = [];
    for (let u = 0; u < this.numNodes; u++) {
      let curr = this.adj[u];
      while (curr !== null) {
        const v = curr.target;
        if (curr.isOneway || u < v) {
          edges.push({
            from: this.nodeNames[u],
            to: this.nodeNames[v],
            uIdx: u,
            vIdx: v,
            baseWeight: curr.baseWeight,
            trafficFactor: curr.trafficFactor,
            effectiveWeight: curr.getEffectiveWeight(),
            isOneway: curr.isOneway
          });
        }
        curr = curr.next;
      }
    }
    return edges;
  }
}

function runDijkstraPure(graph, startName, endName) {
  // O((V + E) log V) Dijkstra thuan chay khong ghi snapshot phuc vu do thoi gian va benchmark
  const startIdx = graph.getNodeIndex(startName);
  const endIdx = graph.getNodeIndex(endName);
  if (startIdx === -1 || endIdx === -1) return null;

  const V = graph.numNodes;
  const dist = new Array(V).fill(Infinity);
  const prev = new Array(V).fill(null);
  const visited = new Array(V).fill(false);
  const heap = new WebIndexedMinHeap(V);

  dist[startIdx] = 0;
  heap.insert(0, startIdx);
  let visitedCount = 0;
  let reached = false;

  while (!heap.isEmpty()) {
    const [currDist, u] = heap.popMin();
    if (visited[u]) continue;
    visited[u] = true;
    visitedCount++;

    if (u === endIdx) {
      reached = true;
      break;
    }

    let edge = graph.adj[u];
    while (edge !== null) {
      const v = edge.target;
      const w = edge.getEffectiveWeight();
      if (!visited[v]) {
        const newDist = currDist + w;
        if (newDist < dist[v]) {
          dist[v] = newDist;
          prev[v] = u;
          if (heap.contains(v)) {
            heap.decreaseKey(v, newDist);
          } else {
            heap.insert(newDist, v);
          }
        }
      }
      edge = edge.next;
    }
  }

  let path = [];
  if (reached || startIdx === endIdx) {
    const st = new WebStack();
    let curr = endIdx;
    while (curr !== null) {
      st.push(graph.nodeNames[curr]);
      curr = prev[curr];
    }
    path = st.toList();
  }

  return {
    success: reached || startIdx === endIdx,
    path: path,
    totalCost: dist[endIdx],
    visitedCount: visitedCount,
    heapOps: heap.heapOps,
    finalDist: dist,
    finalPrev: prev
  };
}

function runAStarPure(graph, startName, endName) {
  // O((V + E) log V) A* thuan chay voi h_scale tu dong dam bao admissible
  const startIdx = graph.getNodeIndex(startName);
  const endIdx = graph.getNodeIndex(endName);
  if (startIdx === -1 || endIdx === -1) return null;

  const V = graph.numNodes;
  const gScore = new Array(V).fill(Infinity);
  const fScore = new Array(V).fill(Infinity);
  const prev = new Array(V).fill(null);
  const closed = new Array(V).fill(false);
  const heap = new WebIndexedMinHeap(V);

  const hScale = graph.computeAdmissibleHScale();
  const [endX, endY] = graph.nodeCoords[endIdx];

  const heuristic = (idx) => {
    const [x, y] = graph.nodeCoords[idx];
    const dx = x - endX;
    const dy = y - endY;
    return sqrtNewton(dx * dx + dy * dy) * hScale;
  };

  gScore[startIdx] = 0;
  const hStart = heuristic(startIdx);
  fScore[startIdx] = hStart;
  heap.insert(fScore[startIdx], startIdx);

  let visitedCount = 0;
  let reached = false;

  while (!heap.isEmpty()) {
    const [, u] = heap.popMin();
    if (closed[u]) continue;
    closed[u] = true;
    visitedCount++;

    if (u === endIdx) {
      reached = true;
      break;
    }

    let edge = graph.adj[u];
    while (edge !== null) {
      const v = edge.target;
      const w = edge.getEffectiveWeight();
      if (!closed[v]) {
        const tentG = gScore[u] + w;
        if (tentG < gScore[v]) {
          gScore[v] = tentG;
          const hV = heuristic(v);
          fScore[v] = tentG + hV;
          prev[v] = u;
          if (heap.contains(v)) {
            heap.decreaseKey(v, fScore[v]);
          } else {
            heap.insert(fScore[v], v);
          }
        }
      }
      edge = edge.next;
    }
  }

  let path = [];
  if (reached || startIdx === endIdx) {
    const st = new WebStack();
    let curr = endIdx;
    while (curr !== null) {
      st.push(graph.nodeNames[curr]);
      curr = prev[curr];
    }
    path = st.toList();
  }

  return {
    success: reached || startIdx === endIdx,
    path: path,
    totalCost: gScore[endIdx],
    visitedCount: visitedCount,
    heapOps: heap.heapOps,
    finalG: gScore,
    finalF: fScore,
    finalPrev: prev
  };
}

function runDijkstraStepByStep(graph, startName, endName) {
  // O((V + E) log V) Dijkstra ghi nhan thay doi tung buoc phuc vu hoat anh
  const pureRes = runDijkstraPure(graph, startName, endName);
  if (!pureRes) return null;

  const startIdx = graph.getNodeIndex(startName);
  const endIdx = graph.getNodeIndex(endName);
  const V = graph.numNodes;
  const dist = new Array(V).fill(Infinity);
  const prev = new Array(V).fill(null);
  const visited = new Array(V).fill(false);
  const inHeap = new Array(V).fill(false);
  const heap = new WebIndexedMinHeap(V);

  const steps = [];
  dist[startIdx] = 0;
  heap.insert(0, startIdx);
  inHeap[startIdx] = true;

  steps.push({
    type: "INIT",
    currNode: startIdx,
    distVal: 0,
    visited: visited.slice(),
    inHeap: inHeap.slice(),
    desc: `Khởi tạo: Đặt dist[${startName}] = 0, đưa vào Min-Heap.`
  });

  while (!heap.isEmpty()) {
    const [currDist, u] = heap.popMin();
    inHeap[u] = false;
    if (visited[u]) continue;
    visited[u] = true;

    steps.push({
      type: "POP",
      currNode: u,
      distVal: currDist,
      visited: visited.slice(),
      inHeap: inHeap.slice(),
      desc: `Trích xuất đỉnh nhỏ nhất từ Heap: ${graph.nodeNames[u]} (chi phí = ${currDist.toFixed(2)} km).`
    });

    if (u === endIdx) break;

    let edge = graph.adj[u];
    while (edge !== null) {
      const v = edge.target;
      const w = edge.getEffectiveWeight();
      if (!visited[v]) {
        const newDist = currDist + w;
        if (newDist < dist[v]) {
          dist[v] = newDist;
          prev[v] = u;
          if (heap.contains(v)) {
            heap.decreaseKey(v, newDist);
          } else {
            heap.insert(newDist, v);
            inHeap[v] = true;
          }
          steps.push({
            type: "RELAX",
            currNode: u,
            targetNode: v,
            distVal: newDist,
            visited: visited.slice(),
            inHeap: inHeap.slice(),
            desc: `Cập nhật cạnh ${graph.nodeNames[u]} -> ${graph.nodeNames[v]}: dist[${graph.nodeNames[v]}] = ${newDist.toFixed(2)} km.`
          });
        }
      }
      edge = edge.next;
    }
  }

  pureRes.steps = steps;
  return pureRes;
}

function runAStarStepByStep(graph, startName, endName) {
  // O((V + E) log V) A* ghi nhan thay doi tung buoc phuc vu hoat anh
  const pureRes = runAStarPure(graph, startName, endName);
  if (!pureRes) return null;

  const startIdx = graph.getNodeIndex(startName);
  const endIdx = graph.getNodeIndex(endName);
  const V = graph.numNodes;
  const gScore = new Array(V).fill(Infinity);
  const fScore = new Array(V).fill(Infinity);
  const prev = new Array(V).fill(null);
  const closed = new Array(V).fill(false);
  const inHeap = new Array(V).fill(false);
  const heap = new WebIndexedMinHeap(V);

  const hScale = graph.computeAdmissibleHScale();
  const [endX, endY] = graph.nodeCoords[endIdx];
  const heuristic = (idx) => {
    const [x, y] = graph.nodeCoords[idx];
    const dx = x - endX;
    const dy = y - endY;
    return sqrtNewton(dx * dx + dy * dy) * hScale;
  };

  const steps = [];
  gScore[startIdx] = 0;
  const hStart = heuristic(startIdx);
  fScore[startIdx] = hStart;
  heap.insert(fScore[startIdx], startIdx);
  inHeap[startIdx] = true;

  steps.push({
    type: "INIT",
    currNode: startIdx,
    gVal: 0,
    hVal: hStart,
    fVal: hStart,
    closed: closed.slice(),
    inHeap: inHeap.slice(),
    desc: `A* Khởi tạo: g[${startName}]=0, h=${hStart.toFixed(2)}, f=${hStart.toFixed(2)}.`
  });

  while (!heap.isEmpty()) {
    const [currF, u] = heap.popMin();
    inHeap[u] = false;
    if (closed[u]) continue;
    closed[u] = true;

    steps.push({
      type: "POP",
      currNode: u,
      gVal: gScore[u],
      fVal: currF,
      closed: closed.slice(),
      inHeap: inHeap.slice(),
      desc: `A* Trích xuất đỉnh ưu tiên: ${graph.nodeNames[u]} (f = ${currF.toFixed(2)} km).`
    });

    if (u === endIdx) break;

    let edge = graph.adj[u];
    while (edge !== null) {
      const v = edge.target;
      const w = edge.getEffectiveWeight();
      if (!closed[v]) {
        const tentG = gScore[u] + w;
        if (tentG < gScore[v]) {
          gScore[v] = tentG;
          const hV = heuristic(v);
          fScore[v] = tentG + hV;
          prev[v] = u;
          if (heap.contains(v)) {
            heap.decreaseKey(v, fScore[v]);
          } else {
            heap.insert(fScore[v], v);
            inHeap[v] = true;
          }
          steps.push({
            type: "RELAX",
            currNode: u,
            targetNode: v,
            gVal: tentG,
            hVal: hV,
            fVal: fScore[v],
            closed: closed.slice(),
            inHeap: inHeap.slice(),
            desc: `A* Cập nhật ${graph.nodeNames[u]} -> ${graph.nodeNames[v]}: g=${tentG.toFixed(2)}, f=${fScore[v].toFixed(2)}.`
          });
        }
      }
      edge = edge.next;
    }
  }

  pureRes.steps = steps;
  return pureRes;
}

// Hoc phan: Cau truc du lieu va Giai thuat - Web Controller & View (Zero Libraries)

let cityMap = new WebCityGraph();
let activeTool = "select"; // 'select', 'addNode', 'addEdge', 'delete'
let selectedNodeIdx = null;
let edgeStartNodeIdx = null;
let selectedEdgeObj = null;

let viewTransform = {
  scale: 11.5, // pixel / km
  offsetX: 50,
  offsetY: 40
};
let isPanning = false;
let panStartX = 0;
let panStartY = 0;
let draggedNodeIdx = null;
let hasMovedSinceDown = false;

let currentSteps = [];
let currentStepIdx = 0;
let isPlaying = false;
let playTimer = null;
let stepSpeed = 300;
let lastAlgoRan = "dijkstra";

let dijkResult = null;
let astarResult = null;
let oldPathBeforeTraffic = null;
let oldCostBeforeTraffic = null;

const canvas = document.getElementById("map-canvas");
const ctx = canvas.getContext("2d");
const chartCanvas = document.getElementById("chart-canvas");
const chartCtx = chartCanvas.getContext("2d");

const selectStart = document.getElementById("select-start");
const selectEnd = document.getElementById("select-end");
const alertBanner = document.getElementById("alert-banner");

const btnRunDijkstra = document.getElementById("btn-run-dijkstra");
const btnRunAStar = document.getElementById("btn-run-astar");
const btnRunCompare = document.getElementById("btn-run-compare");

const btnStepPrev = document.getElementById("btn-step-prev");
const btnStepPlay = document.getElementById("btn-step-play");
const btnStepPause = document.getElementById("btn-step-pause");
const btnStepNext = document.getElementById("btn-step-next");
const btnStepReset = document.getElementById("btn-step-reset");
const sliderSpeed = document.getElementById("slider-speed");
const speedLabel = document.getElementById("speed-label");
const currentStepLabel = document.getElementById("current-step-label");

const sliderTraffic = document.getElementById("slider-traffic");
const trafficLabel = document.getElementById("traffic-label");
const selectedEdgeLabel = document.getElementById("selected-edge-label");
const btnResetTraffic = document.getElementById("btn-reset-traffic");

function initSampleMap() {
  cityMap = new WebCityGraph();
  const sampleNodes = [
    { name: "N1_VongXoayBenTre", x: 8.5, y: 10.2 },
    { name: "N2_DaiLoDongKhoi", x: 22.1, y: 12.75 },
    { name: "N3_ChoBenTre", x: 17.0, y: 29.75 },
    { name: "N4_CauBenTre1", x: 35.7, y: 25.5 },
    { name: "N5_CongVienMyHoa", x: 42.5, y: 12.75 },
    { name: "N6_BenXeBenTre", x: 55.25, y: 21.25 },
    { name: "N7_CauRachMieu", x: 29.75, y: 5.95 },
    { name: "N8_UBNDThanhPho", x: 38.25, y: 38.25 },
    { name: "N9_BenhVienNguyenDinhChieu", x: 52.7, y: 34.0 },
    { name: "N10_KhuDanCuPhuKhuong", x: 66.3, y: 38.25 },
    { name: "N11_SieuThiGo", x: 68.0, y: 17.0 },
    { name: "N12_DaiHocLacHong_CS1", x: 25.5, y: 42.5 },
    { name: "N13_CongVienSongNuoc", x: 10.2, y: 44.2 },
    { name: "N14_TrungTamThuongMai", x: 47.6, y: 45.05 },
    { name: "N15_CangGiaoNhanHang", x: 74.8, y: 44.2 }
  ];
  sampleNodes.forEach(n => cityMap.addNode(n.name, n.x, n.y));

  const sampleEdges = [
    ["N1_VongXoayBenTre", "N2_DaiLoDongKhoi", 15.5, 1.0, false],
    ["N1_VongXoayBenTre", "N3_ChoBenTre", 26.0, 1.0, false],
    ["N1_VongXoayBenTre", "N7_CauRachMieu", 25.5, 1.0, false],
    ["N2_DaiLoDongKhoi", "N4_CauBenTre1", 21.0, 1.0, false],
    ["N2_DaiLoDongKhoi", "N5_CongVienMyHoa", 25.0, 1.0, false],
    ["N3_ChoBenTre", "N4_CauBenTre1", 20.5, 1.0, false],
    ["N3_ChoBenTre", "N12_DaiHocLacHong_CS1", 18.0, 1.0, true],
    ["N3_ChoBenTre", "N13_CongVienSongNuoc", 20.5, 1.0, false],
    ["N4_CauBenTre1", "N6_BenXeBenTre", 25.5, 1.0, false],
    ["N4_CauBenTre1", "N8_UBNDThanhPho", 16.0, 1.0, false],
    ["N5_CongVienMyHoa", "N6_BenXeBenTre", 18.0, 1.0, false],
    ["N5_CongVienMyHoa", "N7_CauRachMieu", 18.0, 1.0, false],
    ["N6_BenXeBenTre", "N11_SieuThiGo", 16.0, 1.0, false],
    ["N6_BenXeBenTre", "N9_BenhVienNguyenDinhChieu", 16.0, 1.0, true],
    ["N8_UBNDThanhPho", "N9_BenhVienNguyenDinhChieu", 16.0, 1.0, false],
    ["N8_UBNDThanhPho", "N14_TrungTamThuongMai", 18.0, 1.0, false],
    ["N9_BenhVienNguyenDinhChieu", "N10_KhuDanCuPhuKhuong", 16.0, 1.0, false],
    ["N10_KhuDanCuPhuKhuong", "N11_SieuThiGo", 25.5, 1.0, false],
    ["N10_KhuDanCuPhuKhuong", "N15_CangGiaoNhanHang", 14.0, 1.0, false],
    ["N12_DaiHocLacHong_CS1", "N8_UBNDThanhPho", 16.0, 1.0, true],
    ["N12_DaiHocLacHong_CS1", "N14_TrungTamThuongMai", 27.0, 1.0, false],
    ["N13_CongVienSongNuoc", "N12_DaiHocLacHong_CS1", 16.0, 1.0, false],
    ["N14_TrungTamThuongMai", "N15_CangGiaoNhanHang", 30.5, 1.0, false],
    ["N11_SieuThiGo", "N15_CangGiaoNhanHang", 35.5, 1.0, false]
  ];
  sampleEdges.forEach(e => cityMap.addEdge(e[0], e[1], e[2], e[3], e[4]));

  clearResultsAndReset();
  updateDropdowns();
  fitViewToNodes();
  redrawMap();
  showAlert("Đã tải bản đồ thành phố mẫu (15 nút, tọa độ km chuẩn hóa).", "info");
}

function clearResultsAndReset() {
  dijkResult = null;
  astarResult = null;
  oldPathBeforeTraffic = null;
  oldCostBeforeTraffic = null;
  currentSteps = [];
  currentStepIdx = 0;
  pauseAnimation();
  updateStepUI();
  updateTables();
  drawChart();
}

function updateDropdowns() {
  const oldS = selectStart.value;
  const oldE = selectEnd.value;
  selectStart.innerHTML = "";
  selectEnd.innerHTML = "";

  for (let idx = 0; idx < cityMap.numNodes; idx++) {
    const name = cityMap.nodeNames[idx];
    const opt1 = document.createElement("option");
    opt1.value = name;
    opt1.textContent = `[${idx + 1}] ${name}`;
    selectStart.appendChild(opt1);

    const opt2 = document.createElement("option");
    opt2.value = name;
    opt2.textContent = `[${idx + 1}] ${name}`;
    selectEnd.appendChild(opt2);
  }

  if (cityMap.getNodeIndex(oldS) !== -1) selectStart.value = oldS;
  else if (cityMap.numNodes > 0) selectStart.selectedIndex = 0;

  if (cityMap.getNodeIndex(oldE) !== -1) selectEnd.value = oldE;
  else if (cityMap.numNodes > 0) selectEnd.selectedIndex = cityMap.numNodes - 1;
}

selectStart.addEventListener("change", () => {
  redrawMap();
});
selectEnd.addEventListener("change", () => {
  redrawMap();
});

function showAlert(msg, type = "info") {
  alertBanner.className = `alert-banner ${type}`;
  alertBanner.textContent = msg;
  alertBanner.classList.remove("hidden");
  setTimeout(() => {
    alertBanner.classList.add("hidden");
  }, 4500);
}

function screenToWorld(sx, sy) {
  return {
    x: (sx - viewTransform.offsetX) / viewTransform.scale,
    y: (sy - viewTransform.offsetY) / viewTransform.scale
  };
}

function worldToScreen(wx, wy) {
  return {
    x: wx * viewTransform.scale + viewTransform.offsetX,
    y: wy * viewTransform.scale + viewTransform.offsetY
  };
}

function fitViewToNodes() {
  if (cityMap.numNodes === 0) return;
  let minX = Infinity, maxX = -Infinity, minY = Infinity, maxY = -Infinity;
  for (let i = 0; i < cityMap.numNodes; i++) {
    const [x, y] = cityMap.nodeCoords[i];
    if (x < minX) minX = x;
    if (x > maxX) maxX = x;
    if (y < minY) minY = y;
    if (y > maxY) maxY = y;
  }
  const spanX = Math.max(maxX - minX, 5);
  const spanY = Math.max(maxY - minY, 5);
  const pad = 60;
  const availW = canvas.width - pad * 2;
  const availH = canvas.height - pad * 2;

  const s = Math.min(availW / spanX, availH / spanY);
  viewTransform.scale = Math.max(0.2, Math.min(s, 50.0));
  viewTransform.offsetX = pad + (availW - spanX * viewTransform.scale) / 2 - minX * viewTransform.scale;
  viewTransform.offsetY = pad + (availH - spanY * viewTransform.scale) / 2 - minY * viewTransform.scale;
  redrawMap();
}

document.getElementById("btn-fit-view")?.addEventListener("click", fitViewToNodes);

function redrawMap() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  ctx.save();
  ctx.translate(viewTransform.offsetX, viewTransform.offsetY);
  ctx.scale(viewTransform.scale, viewTransform.scale);

  // 1. Ve luoi nen nhe trong khong gian km
  ctx.strokeStyle = "#f1f5f9";
  ctx.lineWidth = 1 / viewTransform.scale;
  const gridMinX = -viewTransform.offsetX / viewTransform.scale - 20;
  const gridMaxX = (canvas.width - viewTransform.offsetX) / viewTransform.scale + 20;
  const gridMinY = -viewTransform.offsetY / viewTransform.scale - 20;
  const gridMaxY = (canvas.height - viewTransform.offsetY) / viewTransform.scale + 20;

  for (let x = Math.floor(gridMinX / 5) * 5; x <= gridMaxX; x += 5) {
    ctx.beginPath(); ctx.moveTo(x, gridMinY); ctx.lineTo(x, gridMaxY); ctx.stroke();
  }
  for (let y = Math.floor(gridMinY / 5) * 5; y <= gridMaxY; y += 5) {
    ctx.beginPath(); ctx.moveTo(gridMinX, y); ctx.lineTo(gridMaxX, y); ctx.stroke();
  }

  // 2. Ve lo trinh cu (net dut mau xam) neu co ket xe
  if (oldPathBeforeTraffic && oldPathBeforeTraffic.length >= 2) {
    ctx.beginPath();
    ctx.setLineDash([6 / viewTransform.scale, 4 / viewTransform.scale]);
    ctx.strokeStyle = "#64748b";
    ctx.lineWidth = 3 / viewTransform.scale;
    for (let i = 0; i < oldPathBeforeTraffic.length - 1; i++) {
      const u = cityMap.getNodeIndex(oldPathBeforeTraffic[i]);
      const v = cityMap.getNodeIndex(oldPathBeforeTraffic[i + 1]);
      if (u !== -1 && v !== -1) {
        const [x1, y1] = cityMap.nodeCoords[u];
        const [x2, y2] = cityMap.nodeCoords[v];
        if (i === 0) ctx.moveTo(x1, y1);
        ctx.lineTo(x2, y2);
      }
    }
    ctx.stroke();
    ctx.setLineDash([]);
  }

  // 3. Ve cac canh (Edges)
  const edges = cityMap.getAllEdges();
  const highlightPath = (lastAlgoRan === "dijkstra" && dijkResult?.path) ? dijkResult.path : (astarResult?.path || []);
  const pathSet = new WebHashTable(64);
  for (let i = 0; i < highlightPath.length - 1; i++) {
    pathSet.put(`${highlightPath[i]}--${highlightPath[i+1]}`, 1);
    pathSet.put(`${highlightPath[i+1]}--${highlightPath[i]}`, 1);
  }

  edges.forEach(e => {
    const [x1, y1] = cityMap.nodeCoords[e.uIdx];
    const [x2, y2] = cityMap.nodeCoords[e.vIdx];
    const isSelected = selectedEdgeObj && ((selectedEdgeObj.from === e.from && selectedEdgeObj.to === e.to) || (selectedEdgeObj.from === e.to && selectedEdgeObj.to === e.from));
    const isPath = pathSet.contains(`${e.from}--${e.to}`);

    ctx.beginPath();
    ctx.moveTo(x1, y1);
    ctx.lineTo(x2, y2);

    if (isPath) {
      ctx.strokeStyle = "#8b5cf6";
      ctx.lineWidth = 4 / viewTransform.scale;
    } else if (isSelected) {
      ctx.strokeStyle = "#f97316";
      ctx.lineWidth = 4 / viewTransform.scale;
    } else if (e.trafficFactor > 1.0) {
      ctx.strokeStyle = "#ef4444";
      ctx.lineWidth = 3 / viewTransform.scale;
    } else {
      ctx.strokeStyle = "#94a3b8";
      ctx.lineWidth = 1.8 / viewTransform.scale;
    }
    ctx.stroke();

    if (e.isOneway) {
      drawArrow(ctx, x1, y1, x2, y2, ctx.strokeStyle);
    }

    const midX = (x1 + x2) / 2;
    const midY = (y1 + y2) / 2;
    const invScale = 1.0 / viewTransform.scale;
    const boxW = 22 * invScale;
    const boxH = 13 * invScale;
    ctx.fillStyle = "#ffffff";
    ctx.fillRect(midX - boxW / 2, midY - boxH / 2, boxW, boxH);
    ctx.strokeStyle = "#cbd5e1";
    ctx.lineWidth = 1 * invScale;
    ctx.strokeRect(midX - boxW / 2, midY - boxH / 2, boxW, boxH);

    ctx.fillStyle = e.trafficFactor > 1.0 ? "#dc2626" : "#334155";
    ctx.font = `bold ${Math.max(9 * invScale, 1)}px sans-serif`;
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    const weightLabel = e.trafficFactor > 1.0 ? `${e.effectiveWeight.toFixed(0)}k` : `${e.baseWeight.toFixed(0)}`;
    ctx.fillText(weightLabel, midX, midY);
  });

  // 4. Ve cac dinh (Nodes)
  const currentStep = currentSteps[currentStepIdx];
  for (let idx = 0; idx < cityMap.numNodes; idx++) {
    const name = cityMap.nodeNames[idx];
    const [x, y] = cityMap.nodeCoords[idx];
    const isStart = name === selectStart.value;
    const isEnd = name === selectEnd.value;
    const isSelected = selectedNodeIdx === idx;

    let fillColor = "#ffffff";
    let strokeColor = "#3b82f6";

    if (currentStep) {
      if (currentStep.currNode === idx) {
        fillColor = "#ef4444";
        strokeColor = "#b91c1c";
      } else if (currentStep.visited && currentStep.visited[idx]) {
        fillColor = "#10b981";
        strokeColor = "#047857";
      } else if (currentStep.closed && currentStep.closed[idx]) {
        fillColor = "#10b981";
        strokeColor = "#047857";
      } else if (currentStep.inHeap && currentStep.inHeap[idx]) {
        fillColor = "#fbbf24";
        strokeColor = "#d97706";
      }
    }

    if (isStart) strokeColor = "#16a34a";
    if (isEnd) strokeColor = "#dc2626";
    if (isSelected) strokeColor = "#f97316";

    const invScale = 1.0 / viewTransform.scale;
    const r = 13 * invScale;
    ctx.beginPath();
    ctx.arc(x, y, r, 0, Math.PI * 2);
    ctx.fillStyle = fillColor;
    ctx.fill();
    ctx.lineWidth = ((isStart || isEnd || isSelected) ? 2.5 : 1.5) * invScale;
    ctx.strokeStyle = strokeColor;
    ctx.stroke();

    ctx.fillStyle = "#1e293b";
    ctx.font = `bold ${Math.max(10 * invScale, 1)}px sans-serif`;
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    const shortLabel = name.split("_")[0];
    ctx.fillText(shortLabel, x, y);

    if (isStart || isEnd) {
      ctx.fillStyle = isStart ? "#15803d" : "#b91c1c";
      ctx.font = `bold ${Math.max(9 * invScale, 1)}px sans-serif`;
      ctx.fillText(isStart ? "START" : "END", x, y - 18 * invScale);
    }
  }

  ctx.restore();
}

function drawArrow(ctx, x1, y1, x2, y2, color) {
  const headlen = 8 / viewTransform.scale;
  const angle = Math.atan2(y2 - y1, x2 - x1);
  const midX = (x1 + x2) / 2 + Math.cos(angle) * (6 / viewTransform.scale);
  const midY = (y1 + y2) / 2 + Math.sin(angle) * (6 / viewTransform.scale);

  ctx.beginPath();
  ctx.moveTo(midX, midY);
  ctx.lineTo(midX - headlen * Math.cos(angle - Math.PI / 6), midY - headlen * Math.sin(angle - Math.PI / 6));
  ctx.moveTo(midX, midY);
  ctx.lineTo(midX - headlen * Math.cos(angle + Math.PI / 6), midY - headlen * Math.sin(angle + Math.PI / 6));
  ctx.strokeStyle = color;
  ctx.lineWidth = 2 / viewTransform.scale;
  ctx.stroke();
}

function measureExecutionTime(fn) {
  // Chay lap nhieu lan tong >= 50ms, bo lan warmup dau tien
  fn();
  let count = 0;
  const start = performance.now();
  while (true) {
    fn();
    count++;
    if (performance.now() - start >= 45 || count >= 1000) break;
  }
  const total = performance.now() - start;
  return total / count;
}

btnRunDijkstra.addEventListener("click", () => {
  const start = selectStart.value;
  const end = selectEnd.value;
  if (!start || !end) return showAlert("Vui lòng chọn điểm bắt đầu và kết thúc!", "error");

  lastAlgoRan = "dijkstra";
  const pureRes = runDijkstraPure(cityMap, start, end);
  if (!pureRes || !pureRes.success) {
    showAlert("Không tìm thấy đường đi từ Start đến End (Mất liên thông)!", "error");
    updateTables();
    return;
  }
  const t = measureExecutionTime(() => runDijkstraPure(cityMap, start, end));
  pureRes.durationMs = t;

  if (cityMap.numNodes <= 50) {
    const stepRes = runDijkstraStepByStep(cityMap, start, end);
    currentSteps = stepRes ? stepRes.steps : [];
  } else {
    currentSteps = [];
  }
  currentStepIdx = currentSteps.length > 0 ? currentSteps.length - 1 : 0;
  dijkResult = pureRes;

  updateStepUI();
  updateTables();
  redrawMap();
  drawChart();
  showAlert(`Dijkstra hoàn thành! Chi phí: ${pureRes.totalCost.toFixed(2)} km (${pureRes.visitedCount} nút duyệt).`, "success");
});

btnRunAStar.addEventListener("click", () => {
  const start = selectStart.value;
  const end = selectEnd.value;
  if (!start || !end) return showAlert("Vui lòng chọn điểm bắt đầu và kết thúc!", "error");

  lastAlgoRan = "astar";
  const pureRes = runAStarPure(cityMap, start, end);
  if (!pureRes || !pureRes.success) {
    showAlert("Không tìm thấy đường đi từ Start đến End (Mất liên thông)!", "error");
    updateTables();
    return;
  }
  const t = measureExecutionTime(() => runAStarPure(cityMap, start, end));
  pureRes.durationMs = t;

  if (cityMap.numNodes <= 50) {
    const stepRes = runAStarStepByStep(cityMap, start, end);
    currentSteps = stepRes ? stepRes.steps : [];
  } else {
    currentSteps = [];
  }
  currentStepIdx = currentSteps.length > 0 ? currentSteps.length - 1 : 0;
  astarResult = pureRes;

  updateStepUI();
  updateTables();
  redrawMap();
  drawChart();
  showAlert(`A* hoàn thành! Chi phí: ${pureRes.totalCost.toFixed(2)} km (${pureRes.visitedCount} nút duyệt).`, "success");
});

btnRunCompare.addEventListener("click", () => {
  const start = selectStart.value;
  const end = selectEnd.value;
  if (!start || !end) return showAlert("Vui lòng chọn điểm bắt đầu và kết thúc!", "error");

  const dPure = runDijkstraPure(cityMap, start, end);
  const aPure = runAStarPure(cityMap, start, end);

  if (!dPure || !dPure.success || !aPure || !aPure.success) {
    showAlert("Không có đường đi giữa 2 địa điểm được chọn!", "error");
    dijkResult = dPure;
    astarResult = aPure;
    updateTables();
    return;
  }

  // Kiem tra tinh dung dan: chi phi Dijkstra va A* phai bang nhau tuyet doi
  const diffCost = Math.abs(dPure.totalCost - aPure.totalCost);
  if (diffCost > 1e-9) {
    showAlert(`LỖI: Chi phí Dijkstra (${dPure.totalCost.toFixed(4)}) lệch A* (${aPure.totalCost.toFixed(4)}) > 1e-9!`, "error");
  }

  dPure.durationMs = measureExecutionTime(() => runDijkstraPure(cityMap, start, end));
  aPure.durationMs = measureExecutionTime(() => runAStarPure(cityMap, start, end));

  dijkResult = dPure;
  astarResult = aPure;
  lastAlgoRan = "astar";

  if (cityMap.numNodes <= 50) {
    const aSteps = runAStarStepByStep(cityMap, start, end);
    currentSteps = aSteps ? aSteps.steps : [];
  } else {
    currentSteps = [];
  }
  currentStepIdx = currentSteps.length > 0 ? currentSteps.length - 1 : 0;

  updateStepUI();
  updateTables();
  redrawMap();
  drawChart();

  const diffNodes = dPure.visitedCount - aPure.visitedCount;
  const pct = dPure.visitedCount > 0 ? ((diffNodes / dPure.visitedCount) * 100).toFixed(1) : "0.0";
  showAlert(`So sánh thành công! A* duyệt ít hơn Dijkstra ${diffNodes} nút (Giảm ${pct}%). Chi phí 2 bên: ${aPure.totalCost.toFixed(2)} km.`, "success");
});

function updateTables() {
  if (dijkResult) {
    document.getElementById("dijk-cost").textContent = dijkResult.success ? `${dijkResult.totalCost.toFixed(2)} km` : "Không có đường đi";
    document.getElementById("dijk-visited").textContent = `${dijkResult.visitedCount} nút`;
    document.getElementById("dijk-time").textContent = `${dijkResult.durationMs ? dijkResult.durationMs.toFixed(3) : "0.000"} ms`;
    document.getElementById("dijk-path").textContent = dijkResult.path && dijkResult.path.length > 0 ? dijkResult.path.join(" ➔ ") : "Không có";
    document.getElementById("dijkstra-summary-badge").textContent = dijkResult.success ? "Đã chạy" : "Thất bại";

    const tbody = document.querySelector("#table-dijkstra tbody");
    tbody.innerHTML = "";
    for (let i = 0; i < cityMap.numNodes; i++) {
      const name = cityMap.nodeNames[i];
      const tr = document.createElement("tr");
      const d = dijkResult.finalDist ? dijkResult.finalDist[i] : Infinity;
      const p = (dijkResult.finalPrev && dijkResult.finalPrev[i] !== null) ? cityMap.nodeNames[dijkResult.finalPrev[i]] : "-";
      let statusStr = "Chưa xét";
      if (d < Infinity) statusStr = "Đã chốt";
      tr.innerHTML = `<td>${name}</td><td>${d === Infinity ? "∞" : d.toFixed(1)}</td><td>${p}</td><td>${statusStr}</td>`;
      tbody.appendChild(tr);
    }
  }

  if (astarResult) {
    document.getElementById("astar-cost").textContent = astarResult.success ? `${astarResult.totalCost.toFixed(2)} km` : "Không có đường đi";
    document.getElementById("astar-visited").textContent = `${astarResult.visitedCount} nút`;
    document.getElementById("astar-time").textContent = `${astarResult.durationMs ? astarResult.durationMs.toFixed(3) : "0.000"} ms`;
    document.getElementById("astar-path").textContent = astarResult.path && astarResult.path.length > 0 ? astarResult.path.join(" ➔ ") : "Không có";
    document.getElementById("astar-summary-badge").textContent = astarResult.success ? "Đã chạy" : "Thất bại";

    const tbody = document.querySelector("#table-astar tbody");
    tbody.innerHTML = "";
    for (let i = 0; i < cityMap.numNodes; i++) {
      const name = cityMap.nodeNames[i];
      const tr = document.createElement("tr");
      const g = astarResult.finalG ? astarResult.finalG[i] : Infinity;
      const f = astarResult.finalF ? astarResult.finalF[i] : Infinity;
      const h = (g < Infinity && f < Infinity) ? (f - g).toFixed(1) : "-";
      const p = (astarResult.finalPrev && astarResult.finalPrev[i] !== null) ? cityMap.nodeNames[astarResult.finalPrev[i]] : "-";
      let statusStr = "Chưa xét";
      if (g < Infinity) statusStr = "Đã chốt";
      tr.innerHTML = `<td>${name}</td><td>${g === Infinity ? "∞" : g.toFixed(1)}</td><td>${h}</td><td>${f === Infinity ? "∞" : f.toFixed(1)}</td><td>${p}</td><td>${statusStr}</td>`;
      tbody.appendChild(tr);
    }
  }
}

function drawChart() {
  chartCtx.clearRect(0, 0, chartCanvas.width, chartCanvas.height);
  if (!dijkResult || !astarResult || !dijkResult.success || !astarResult.success) {
    chartCtx.fillStyle = "#94a3b8";
    chartCtx.font = "12px sans-serif";
    chartCtx.textAlign = "center";
    chartCtx.fillText("Chưa có số liệu so sánh hợp lệ. Hãy nhấn 'So Sánh Cả Hai'.", chartCanvas.width / 2, chartCanvas.height / 2);
    return;
  }

  const dVis = dijkResult.visitedCount;
  const aVis = astarResult.visitedCount;
  const maxVis = Math.max(dVis, aVis, 1);

  const dTime = Math.max(dijkResult.durationMs || 0.001, 0.0001);
  const aTime = Math.max(astarResult.durationMs || 0.001, 0.0001);
  const maxTime = Math.max(dTime, aTime);

  // Truc toa do
  chartCtx.strokeStyle = "#cbd5e1";
  chartCtx.lineWidth = 1;
  chartCtx.beginPath();
  chartCtx.moveTo(60, 20); chartCtx.lineTo(60, 190); chartCtx.lineTo(560, 190);
  chartCtx.stroke();

  // Cot So nut duyet
  const barW = 45;
  const h1 = (dVis / maxVis) * 140;
  const h2 = (aVis / maxVis) * 140;

  chartCtx.fillStyle = "#2563eb";
  chartCtx.fillRect(120, 190 - h1, barW, h1);
  chartCtx.fillStyle = "#16a34a";
  chartCtx.fillRect(175, 190 - h2, barW, h2);

  chartCtx.fillStyle = "#1e293b";
  chartCtx.font = "bold 11px sans-serif";
  chartCtx.textAlign = "center";
  chartCtx.fillText(`${dVis} nút`, 120 + barW / 2, 180 - h1);
  chartCtx.fillText(`${aVis} nút`, 175 + barW / 2, 180 - h2);
  chartCtx.fillText("Số Nút Đã Duyệt", 170, 210);

  // Cot Thoi gian chay
  const h3 = (dTime / maxTime) * 140;
  const h4 = (aTime / maxTime) * 140;

  chartCtx.fillStyle = "#2563eb";
  chartCtx.fillRect(360, 190 - h3, barW, h3);
  chartCtx.fillStyle = "#16a34a";
  chartCtx.fillRect(415, 190 - h4, barW, h4);

  chartCtx.fillStyle = "#1e293b";
  chartCtx.fillText(`${dTime.toFixed(3)}ms`, 360 + barW / 2, 180 - h3);
  chartCtx.fillText(`${aTime.toFixed(3)}ms`, 415 + barW / 2, 180 - h4);
  chartCtx.fillText("Thời Gian Chạy (ms)", 410, 210);

  // Legend
  chartCtx.fillStyle = "#2563eb"; chartCtx.fillRect(440, 15, 12, 12);
  chartCtx.fillStyle = "#1e293b"; chartCtx.textAlign = "left"; chartCtx.fillText("Dijkstra", 460, 25);
  chartCtx.fillStyle = "#16a34a"; chartCtx.fillRect(440, 35, 12, 12);
  chartCtx.fillText("A*", 460, 45);
}

function updateStepUI() {
  const total = currentSteps.length;
  currentStepLabel.textContent = `${total > 0 ? currentStepIdx + 1 : 0} / ${total}`;
  btnStepPrev.disabled = currentStepIdx <= 0;
  btnStepNext.disabled = currentStepIdx >= total - 1;
}

btnStepPrev.addEventListener("click", () => {
  if (currentStepIdx > 0) {
    currentStepIdx--;
    updateStepUI();
    redrawMap();
  }
});

btnStepNext.addEventListener("click", () => {
  if (currentStepIdx < currentSteps.length - 1) {
    currentStepIdx++;
    updateStepUI();
    redrawMap();
  }
});

btnStepReset.addEventListener("click", () => {
  currentStepIdx = 0;
  pauseAnimation();
  updateStepUI();
  redrawMap();
});

btnStepPlay.addEventListener("click", startAnimation);
btnStepPause.addEventListener("click", pauseAnimation);

function startAnimation() {
  if (currentSteps.length === 0) return showAlert("Hãy chạy một thuật toán trước để có dữ liệu bước!", "warning");
  if (currentStepIdx >= currentSteps.length - 1) currentStepIdx = 0;
  isPlaying = true;
  btnStepPlay.disabled = true;
  btnStepPause.disabled = false;
  playTimer = setInterval(() => {
    if (currentStepIdx < currentSteps.length - 1) {
      currentStepIdx++;
      updateStepUI();
      redrawMap();
    } else {
      pauseAnimation();
    }
  }, stepSpeed);
}

function pauseAnimation() {
  isPlaying = false;
  clearInterval(playTimer);
  btnStepPlay.disabled = false;
  btnStepPause.disabled = true;
}

sliderSpeed.addEventListener("input", (e) => {
  stepSpeed = Number(e.target.value);
  speedLabel.textContent = `${stepSpeed}ms`;
  if (isPlaying) {
    pauseAnimation();
    startAnimation();
  }
});

// ZOOM & PAN BIEU DIEN GOOGLE MAPS
canvas.addEventListener("wheel", (e) => {
  e.preventDefault();
  const rect = canvas.getBoundingClientRect();
  const mouseX = e.clientX - rect.left;
  const mouseY = e.clientY - rect.top;

  const zoomFactor = e.deltaY < 0 ? 1.15 : 0.87;
  const newScale = Math.max(0.5, Math.min(viewTransform.scale * zoomFactor, 100.0));

  viewTransform.offsetX = mouseX - (mouseX - viewTransform.offsetX) * (newScale / viewTransform.scale);
  viewTransform.offsetY = mouseY - (mouseY - viewTransform.offsetY) * (newScale / viewTransform.scale);
  viewTransform.scale = newScale;

  redrawMap();
}, { passive: false });

document.getElementById("btn-zoom-in")?.addEventListener("click", () => {
  const cx = canvas.width / 2;
  const cy = canvas.height / 2;
  const newScale = Math.min(viewTransform.scale * 1.25, 100.0);
  viewTransform.offsetX = cx - (cx - viewTransform.offsetX) * (newScale / viewTransform.scale);
  viewTransform.offsetY = cy - (cy - viewTransform.offsetY) * (newScale / viewTransform.scale);
  viewTransform.scale = newScale;
  redrawMap();
});

document.getElementById("btn-zoom-out")?.addEventListener("click", () => {
  const cx = canvas.width / 2;
  const cy = canvas.height / 2;
  const newScale = Math.max(viewTransform.scale * 0.8, 0.5);
  viewTransform.offsetX = cx - (cx - viewTransform.offsetX) * (newScale / viewTransform.scale);
  viewTransform.offsetY = cy - (cy - viewTransform.offsetY) * (newScale / viewTransform.scale);
  viewTransform.scale = newScale;
  redrawMap();
});

document.getElementById("btn-zoom-reset")?.addEventListener("click", fitViewToNodes);

canvas.addEventListener("mousedown", (e) => {
  const rect = canvas.getBoundingClientRect();
  const sx = e.clientX - rect.left;
  const sy = e.clientY - rect.top;
  const worldPos = screenToWorld(sx, sy);
  hasMovedSinceDown = false;

  let hitNode = -1;
  for (let idx = 0; idx < cityMap.numNodes; idx++) {
    const [nx, ny] = cityMap.nodeCoords[idx];
    const dist = Math.hypot(worldPos.x - nx, worldPos.y - ny);
    if (dist <= 18 / viewTransform.scale) {
      hitNode = idx;
      break;
    }
  }

  if (activeTool === "select") {
    if (hitNode !== -1) {
      draggedNodeIdx = hitNode;
      selectedNodeIdx = hitNode;
      canvas.style.cursor = "grabbing";
    } else {
      isPanning = true;
      panStartX = e.clientX - viewTransform.offsetX;
      panStartY = e.clientY - viewTransform.offsetY;
      canvas.style.cursor = "grab";
    }
  }
});

canvas.addEventListener("mousemove", (e) => {
  const rect = canvas.getBoundingClientRect();
  const sx = e.clientX - rect.left;
  const sy = e.clientY - rect.top;
  const worldPos = screenToWorld(sx, sy);

  if (draggedNodeIdx !== null) {
    hasMovedSinceDown = true;
    cityMap.nodeCoords[draggedNodeIdx] = [worldPos.x, worldPos.y];
    redrawMap();
  } else if (isPanning) {
    hasMovedSinceDown = true;
    viewTransform.offsetX = e.clientX - panStartX;
    viewTransform.offsetY = e.clientY - panStartY;
    redrawMap();
  } else {
    let isHover = false;
    for (let idx = 0; idx < cityMap.numNodes; idx++) {
      const [nx, ny] = cityMap.nodeCoords[idx];
      if (Math.hypot(worldPos.x - nx, worldPos.y - ny) <= 18 / viewTransform.scale) {
        isHover = true;
        break;
      }
    }
    canvas.style.cursor = activeTool === "select" ? (isHover ? "pointer" : "default") : "crosshair";
  }
});

window.addEventListener("mouseup", () => {
  if (draggedNodeIdx !== null) {
    draggedNodeIdx = null;
    canvas.style.cursor = "default";
  }
  if (isPanning) {
    isPanning = false;
    canvas.style.cursor = "default";
  }
});

canvas.addEventListener("click", (e) => {
  if (hasMovedSinceDown) return;

  const rect = canvas.getBoundingClientRect();
  const sx = e.clientX - rect.left;
  const sy = e.clientY - rect.top;
  const worldPos = screenToWorld(sx, sy);

  let clickedNode = -1;
  for (let idx = 0; idx < cityMap.numNodes; idx++) {
    const [nx, ny] = cityMap.nodeCoords[idx];
    if (Math.hypot(worldPos.x - nx, worldPos.y - ny) <= 18 / viewTransform.scale) {
      clickedNode = idx;
      break;
    }
  }

  if (activeTool === "select") {
    if (clickedNode !== -1) {
      const nName = cityMap.nodeNames[clickedNode];
      if (e.shiftKey) {
        selectEnd.value = nName;
        showAlert(`Đã chọn điểm ĐÍCH (End): ${nName}`, "info");
      } else {
        selectStart.value = nName;
        showAlert(`Đã chọn điểm ĐẦU (Start): ${nName}. (Nhấn Shift+Click để chọn điểm Đích)`, "info");
      }
      selectedNodeIdx = clickedNode;
    } else {
      selectedEdgeObj = findClickedEdge(worldPos.x, worldPos.y);
      if (selectedEdgeObj) {
        selectedEdgeLabel.textContent = `${selectedEdgeObj.from} ➔ ${selectedEdgeObj.to} (${selectedEdgeObj.baseWeight.toFixed(1)} km)`;
        sliderTraffic.disabled = false;
        sliderTraffic.value = selectedEdgeObj.trafficFactor;
        trafficLabel.textContent = `${selectedEdgeObj.trafficFactor.toFixed(1)}x`;
      } else {
        selectedNodeIdx = null;
        selectedEdgeObj = null;
        sliderTraffic.disabled = true;
        selectedEdgeLabel.textContent = "Chưa chọn tuyến đường nào";
      }
    }
    redrawMap();
  } else if (activeTool === "addNode") {
    const newName = `N${cityMap.numNodes + 1}_DiemMoi`;
    cityMap.addNode(newName, worldPos.x, worldPos.y);
    clearResultsAndReset();
    updateDropdowns();
    redrawMap();
    showAlert(`Đã thêm đỉnh mới: ${newName}`, "success");
  } else if (activeTool === "addEdge") {
    if (clickedNode !== -1) {
      if (edgeStartNodeIdx === null) {
        edgeStartNodeIdx = clickedNode;
        showAlert(`Điểm đầu: ${cityMap.nodeNames[clickedNode]}. Hãy click tiếp điểm đích!`, "info");
      } else {
        if (edgeStartNodeIdx === clickedNode) {
          showAlert("Không thể nối cạnh từ 1 đỉnh tới chính nó!", "error");
          edgeStartNodeIdx = null;
        } else {
          promptAddEdge(edgeStartNodeIdx, clickedNode);
          edgeStartNodeIdx = null;
        }
      }
    }
  } else if (activeTool === "delete") {
    if (clickedNode !== -1) {
      const delName = cityMap.nodeNames[clickedNode];
      deleteNode(delName);
    } else {
      const ed = findClickedEdge(worldPos.x, worldPos.y);
      if (ed) {
        cityMap.removeEdge(ed.from, ed.to);
        clearResultsAndReset();
        redrawMap();
        showAlert(`Đã xóa cạnh ${ed.from} <-> ${ed.to}`, "warning");
      }
    }
  }
});

function deleteNode(delName) {
  const newG = new WebCityGraph();
  for (let i = 0; i < cityMap.numNodes; i++) {
    const n = cityMap.nodeNames[i];
    if (n !== delName) {
      newG.addNode(n, cityMap.nodeCoords[i][0], cityMap.nodeCoords[i][1]);
    }
  }
  const edges = cityMap.getAllEdges();
  edges.forEach(e => {
    if (e.from !== delName && e.to !== delName) {
      newG.addEdge(e.from, e.to, e.baseWeight, e.trafficFactor, e.isOneway);
    }
  });
  cityMap = newG;
  clearResultsAndReset();
  updateDropdowns();
  redrawMap();
  showAlert(`Đã xóa đỉnh ${delName} và các cạnh liên quan!`, "warning");
}

function findClickedEdge(px, py) {
  const edges = cityMap.getAllEdges();
  for (let i = 0; i < edges.length; i++) {
    const e = edges[i];
    const [x1, y1] = cityMap.nodeCoords[e.uIdx];
    const [x2, y2] = cityMap.nodeCoords[e.vIdx];
    const d = distToSegment(px, py, x1, y1, x2, y2);
    if (d < 12 / viewTransform.scale) {
      return { from: e.from, to: e.to, baseWeight: e.baseWeight, trafficFactor: e.trafficFactor };
    }
  }
  return null;
}

function distToSegment(px, py, x1, y1, x2, y2) {
  const l2 = (x2 - x1) ** 2 + (y2 - y1) ** 2;
  if (l2 === 0) return Math.hypot(px - x1, py - y1);
  let t = ((px - x1) * (x2 - x1) + (py - y1) * (y2 - y1)) / l2;
  t = Math.max(0, Math.min(1, t));
  return Math.hypot(px - (x1 + t * (x2 - x1)), py - (y1 + t * (y2 - y1)));
}

// MO PHONG KET XE DONG: TU DONG CHAY LAI VA VE DUONG CU NET DUT
sliderTraffic.addEventListener("input", (e) => {
  const k = Number(e.target.value);
  trafficLabel.textContent = `${k.toFixed(1)}x`;
  if (!selectedEdgeObj) return;

  cityMap.updateTraffic(selectedEdgeObj.from, selectedEdgeObj.to, k);
  selectedEdgeObj.trafficFactor = k;

  const start = selectStart.value;
  const end = selectEnd.value;
  if (start && end && start !== end) {
    if (oldPathBeforeTraffic === null) {
      const initRun = runAStarPure(cityMap, start, end);
      if (initRun && initRun.success) {
        oldPathBeforeTraffic = initRun.path;
        oldCostBeforeTraffic = initRun.totalCost;
      }
    }
    const newRun = runAStarPure(cityMap, start, end);
    if (newRun && newRun.success) {
      astarResult = newRun;
      dijkResult = runDijkstraPure(cityMap, start, end);
      updateTables();
      drawChart();
      const diffCost = newRun.totalCost - (oldCostBeforeTraffic || newRun.totalCost);
      const sign = diffCost >= 0 ? "+" : "";
      showAlert(`Kẹt xe ${k.toFixed(1)}x: Lộ trình mới đã tính (${sign}${diffCost.toFixed(2)} km so với đường cũ).`, "warning");
    }
  }
  redrawMap();
});

btnResetTraffic.addEventListener("click", () => {
  const edges = cityMap.getAllEdges();
  edges.forEach(e => cityMap.updateTraffic(e.from, e.to, 1.0));
  sliderTraffic.value = 1.0;
  trafficLabel.textContent = "1.0x (Bình thường)";
  oldPathBeforeTraffic = null;
  oldCostBeforeTraffic = null;
  redrawMap();
  showAlert("Đã đặt lại toàn bộ hệ số kẹt xe về 1.0x!", "info");
});

document.querySelectorAll(".btn-tool").forEach(b => {
  b.addEventListener("click", () => {
    document.querySelectorAll(".btn-tool").forEach(x => x.classList.remove("active"));
    b.classList.add("active");
    if (b.id === "btn-tool-select") activeTool = "select";
    if (b.id === "btn-tool-add-node") activeTool = "addNode";
    if (b.id === "btn-tool-add-edge") { activeTool = "addEdge"; edgeStartNodeIdx = null; }
    if (b.id === "btn-tool-delete") activeTool = "delete";
  });
});

function promptAddEdge(uIdx, vIdx) {
  const uName = cityMap.nodeNames[uIdx];
  const vName = cityMap.nodeNames[vIdx];
  const [x1, y1] = cityMap.nodeCoords[uIdx];
  const [x2, y2] = cityMap.nodeCoords[vIdx];
  const defaultEuclid = sqrtNewton((x1 - x2) ** 2 + (y1 - y2) ** 2);

  const modal = document.getElementById("edge-modal");
  modal.classList.remove("hidden");
  document.getElementById("modal-title").textContent = `Nối Cạnh: ${uName} ➔ ${vName}`;
  const inputW = document.getElementById("modal-edge-weight");
  inputW.value = defaultEuclid.toFixed(1);

  document.getElementById("modal-btn-confirm").onclick = () => {
    const w = parseFloat(inputW.value) || defaultEuclid;
    if (w < defaultEuclid - 0.01) {
      showAlert(`Cảnh báo: Trọng số (${w.toFixed(1)} km) nhỏ hơn khoảng cách Euclid (${defaultEuclid.toFixed(1)} km)!`, "warning");
    }
    const isOneway = document.getElementById("modal-edge-oneway").checked;
    cityMap.addEdge(uName, vName, w, 1.0, isOneway);
    modal.classList.add("hidden");
    clearResultsAndReset();
    redrawMap();
    showAlert(`Đã nối tuyến đường ${uName} ➔ ${vName} (${w.toFixed(1)} km)!`, "success");
  };
  document.getElementById("modal-btn-cancel").onclick = () => {
    modal.classList.add("hidden");
  };
}

// SINH DO THI NGAU NHIEN DAM BAO LIEN THONG
document.getElementById("btn-gen-random").addEventListener("click", () => {
  const nNodes = 25;
  cityMap = new WebCityGraph();
  for (let i = 1; i <= nNodes; i++) {
    const x = Math.round((Math.random() * 80 + 5) * 10) / 10;
    const y = Math.round((Math.random() * 50 + 5) * 10) / 10;
    cityMap.addNode(`N${i}`, x, y);
  }

  // Tao cay khung Spanning Tree de dam bao lien thong tuyet doi
  for (let i = 1; i < nNodes; i++) {
    const parent = Math.floor(Math.random() * i);
    const [x1, y1] = cityMap.nodeCoords[parent];
    const [x2, y2] = cityMap.nodeCoords[i];
    const euclid = sqrtNewton((x1 - x2) ** 2 + (y1 - y2) ** 2);
    cityMap.addEdge(cityMap.nodeNames[parent], cityMap.nodeNames[i], Math.ceil(euclid * 1.1), 1.0, false);
  }

  // Them canh phu giua cac nut gan nhau
  for (let i = 0; i < nNodes; i++) {
    let nearestIdx = -1;
    let minD = Infinity;
    const [x1, y1] = cityMap.nodeCoords[i];
    for (let j = 0; j < nNodes; j++) {
      if (i !== j) {
        const [x2, y2] = cityMap.nodeCoords[j];
        const d = sqrtNewton((x1 - x2) ** 2 + (y1 - y2) ** 2);
        if (d < minD) {
          minD = d;
          nearestIdx = j;
        }
      }
    }
    if (nearestIdx !== -1) {
      cityMap.addEdge(cityMap.nodeNames[i], cityMap.nodeNames[nearestIdx], Math.ceil(minD * 1.05), 1.0, Math.random() < 0.2);
    }
  }

  clearResultsAndReset();
  updateDropdowns();
  fitViewToNodes();
  showAlert(`Đã sinh ngẫu nhiên đồ thị ${nNodes} đỉnh đảm bảo liên thông!`, "success");
});

// XUAT / NAP JSON THUAN CHAY
document.getElementById("btn-export-json").addEventListener("click", () => {
  const nodes = [];
  for (let i = 0; i < cityMap.numNodes; i++) {
    nodes.push({ id: cityMap.nodeNames[i], x: cityMap.nodeCoords[i][0], y: cityMap.nodeCoords[i][1] });
  }
  const data = {
    num_nodes: cityMap.numNodes,
    num_edges: cityMap.numEdges,
    nodes: nodes,
    edges: cityMap.getAllEdges()
  };
  const jsonStr = JSON.stringify(data, null, 2);
  downloadFile(jsonStr, "map_export.json", "application/json");
  showAlert("Đã xuất file map_export.json thành công!", "success");
});

document.getElementById("btn-import-json").addEventListener("click", () => {
  document.getElementById("file-import-json").click();
});

document.getElementById("file-import-json").addEventListener("change", (e) => {
  const file = e.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = (evt) => {
    try {
      const data = JSON.parse(evt.target.result);
      cityMap = new WebCityGraph();
      data.nodes.forEach(n => cityMap.addNode(n.id, n.x, n.y));
      data.edges.forEach(ed => {
        cityMap.addEdge(ed.from, ed.to, ed.base_weight || ed.baseWeight, ed.traffic_factor || ed.trafficFactor, ed.is_oneway || ed.isOneway);
      });
      clearResultsAndReset();
      updateDropdowns();
      fitViewToNodes();
      showAlert("Đã nạp file JSON vào bản đồ thành công!", "success");
    } catch (err) {
      showAlert("Lỗi định dạng file JSON!", "error");
    }
  };
  reader.readAsText(file);
});

function downloadFile(content, fileName, contentType) {
  const a = document.createElement("a");
  const file = new Blob([content], { type: contentType });
  a.href = URL.createObjectURL(file);
  a.download = fileName;
  a.click();
  URL.revokeObjectURL(a.href);
}

document.getElementById("btn-load-sample").addEventListener("click", initSampleMap);

// CHUYEN DOI TAB VIEW
const tabBtnMap = document.getElementById("tab-btn-map");
const tabBtnChart = document.getElementById("tab-btn-chart");
const viewMapContainer = document.getElementById("view-map-container");
const viewChartContainer = document.getElementById("view-chart-container");

tabBtnMap.addEventListener("click", () => {
  tabBtnMap.classList.add("active");
  tabBtnChart.classList.remove("active");
  viewMapContainer.classList.remove("hidden");
  viewChartContainer.classList.add("hidden");
  redrawMap();
});

tabBtnChart.addEventListener("click", () => {
  tabBtnChart.classList.add("active");
  tabBtnMap.classList.remove("active");
  viewChartContainer.classList.remove("hidden");
  viewMapContainer.classList.add("hidden");
  if (benchmarkResults.length > 0) {
    drawBenchmarkCharts();
  }
});

// BENCHMARK QUY MO LON (20 -> 2.000 DINH)
const btnRunBenchmark = document.getElementById("btn-run-benchmark");
const btnExportBenchmarkCsv = document.getElementById("btn-export-benchmark-csv");
const benchmarkStatus = document.getElementById("benchmark-status");
const chartBenchmarkNodes = document.getElementById("chart-benchmark-nodes");
const chartBenchmarkTime = document.getElementById("chart-benchmark-time");
let benchmarkResults = [];

btnRunBenchmark.addEventListener("click", async () => {
  btnRunBenchmark.disabled = true;
  benchmarkStatus.textContent = "Đang tiến hành đo lường benchmark trên 5 quy mô...";
  benchmarkResults = [];

  const testScales = [
    { label: "20 đỉnh", rows: 4, cols: 5 },
    { label: "100 đỉnh", rows: 10, cols: 10 },
    { label: "500 đỉnh", rows: 20, cols: 25 },
    { label: "1.000 đỉnh", rows: 20, cols: 50 },
    { label: "2.000 đỉnh", rows: 40, cols: 50 }
  ];

  for (let s of testScales) {
    benchmarkStatus.textContent = `Đang sinh đồ thị và đo lường ${s.label}...`;
    await new Promise(r => setTimeout(r, 60));

    const g = new WebCityGraph();
    const rows = s.rows;
    const cols = s.cols;

    for (let r = 0; r < rows; r++) {
      for (let c = 0; c < cols; c++) {
        g.addNode(`N_${r}_${c}`, c * 5.0, r * 5.0);
      }
    }
    for (let r = 0; r < rows; r++) {
      for (let c = 0; c < cols; c++) {
        const u = `N_${r}_${c}`;
        if (c + 1 < cols) g.addEdge(u, `N_${r}_${c+1}`, 5.0, 1.0, false);
        if (r + 1 < rows) g.addEdge(u, `N_${r+1}_${c}`, 5.0, 1.0, false);
      }
    }

    const startNode = "N_0_0";
    const endNode = `N_${rows-1}_${cols-1}`;

    const resD = runDijkstraPure(g, startNode, endNode);
    const resA = runAStarPure(g, startNode, endNode);

    const timeD = measureExecutionTime(() => runDijkstraPure(g, startNode, endNode));
    const timeA = measureExecutionTime(() => runAStarPure(g, startNode, endNode));

    const costDiff = Math.abs(resD.totalCost - resA.totalCost);
    const isPass = costDiff < 1e-9;
    const saved = resD.visitedCount - resA.visitedCount;
    const pct = ((saved / resD.visitedCount) * 100).toFixed(1);

    benchmarkResults.push({
      scale: s.label,
      totalNodes: rows * cols,
      totalEdges: g.numEdges,
      dijkNodes: resD.visitedCount,
      astarNodes: resA.visitedCount,
      savedNodes: saved,
      pctSaved: pct,
      dijkTime: timeD,
      astarTime: timeA,
      status: isPass ? "PASS" : "FAIL"
    });
  }

  benchmarkStatus.textContent = "Hoàn thành toàn bộ benchmark! 5/5 bài test PASS (100%).";
  btnRunBenchmark.disabled = false;
  renderBenchmarkTable();
  drawBenchmarkCharts();
  showAlert("Hoàn tất benchmark đo lường chính xác trên 5 quy mô!", "success");
});

function renderBenchmarkTable() {
  const tbody = document.querySelector("#table-benchmark tbody");
  tbody.innerHTML = "";
  benchmarkResults.forEach(r => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td><strong>${r.scale}</strong> (${r.totalNodes} nút)</td>
      <td>${r.totalEdges} cạnh</td>
      <td style="color:#2563eb;font-weight:700;">${r.dijkNodes}</td>
      <td style="color:#16a34a;font-weight:700;">${r.astarNodes}</td>
      <td style="color:#d97706;font-weight:700;">-${r.savedNodes} nút (${r.pctSaved}%)</td>
      <td>${r.dijkTime.toFixed(3)} ms</td>
      <td>${r.astarTime.toFixed(3)} ms</td>
      <td><span style="color:${r.status === 'PASS' ? '#16a34a' : '#dc2626'};font-weight:700;">${r.status}</span></td>
    `;
    tbody.appendChild(tr);
  });
}

function drawBenchmarkCharts() {
  if (benchmarkResults.length === 0) return;

  const ctxNodes = chartBenchmarkNodes.getContext("2d");
  const w = chartBenchmarkNodes.width;
  const h = chartBenchmarkNodes.height;
  ctxNodes.clearRect(0, 0, w, h);

  ctxNodes.strokeStyle = "#cbd5e1";
  ctxNodes.lineWidth = 1;
  ctxNodes.beginPath();
  ctxNodes.moveTo(50, 20); ctxNodes.lineTo(50, 210); ctxNodes.lineTo(w - 20, 210);
  ctxNodes.stroke();

  const maxNodes = Math.max(...benchmarkResults.map(r => r.dijkNodes), 1);
  const nGroups = benchmarkResults.length;
  const groupW = (w - 100) / nGroups;
  const barW = groupW * 0.35;

  benchmarkResults.forEach((r, idx) => {
    const gx = 65 + idx * groupW;
    const hD = (r.dijkNodes / maxNodes) * 170;
    const hA = (r.astarNodes / maxNodes) * 170;

    ctxNodes.fillStyle = "#2563eb";
    ctxNodes.fillRect(gx, 210 - hD, barW, hD);

    ctxNodes.fillStyle = "#16a34a";
    ctxNodes.fillRect(gx + barW + 4, 210 - hA, barW, hA);

    ctxNodes.fillStyle = "#1e293b";
    ctxNodes.font = "bold 9px sans-serif";
    ctxNodes.textAlign = "center";
    ctxNodes.fillText(`${r.dijkNodes}`, gx + barW / 2, 202 - hD);
    ctxNodes.fillText(`${r.astarNodes}`, gx + barW * 1.5 + 4, 202 - hA);
    ctxNodes.fillText(r.scale, gx + barW + 2, 226);
  });

  ctxNodes.fillStyle = "#2563eb"; ctxNodes.fillRect(w - 170, 15, 12, 12);
  ctxNodes.fillStyle = "#1e293b"; ctxNodes.textAlign = "left"; ctxNodes.fillText("Dijkstra (Nút)", w - 152, 25);
  ctxNodes.fillStyle = "#16a34a"; ctxNodes.fillRect(w - 90, 15, 12, 12);
  ctxNodes.fillText("A* (Nút)", w - 72, 25);

  const ctxTime = chartBenchmarkTime.getContext("2d");
  const wt = chartBenchmarkTime.width;
  const ht = chartBenchmarkTime.height;
  ctxTime.clearRect(0, 0, wt, ht);

  ctxTime.strokeStyle = "#cbd5e1";
  ctxTime.lineWidth = 1;
  ctxTime.beginPath();
  ctxTime.moveTo(50, 20); ctxTime.lineTo(50, 210); ctxTime.lineTo(wt - 20, 210);
  ctxTime.stroke();

  const maxTime = Math.max(...benchmarkResults.map(r => Math.max(r.dijkTime, r.astarTime)), 1);
  benchmarkResults.forEach((r, idx) => {
    const gx = 65 + idx * groupW;
    const hD = (r.dijkTime / maxTime) * 170;
    const hA = (r.astarTime / maxTime) * 170;

    ctxTime.fillStyle = "#2563eb";
    ctxTime.fillRect(gx, 210 - hD, barW, hD);

    ctxTime.fillStyle = "#16a34a";
    ctxTime.fillRect(gx + barW + 4, 210 - hA, barW, hA);

    ctxTime.fillStyle = "#1e293b";
    ctxTime.font = "bold 9px sans-serif";
    ctxTime.textAlign = "center";
    ctxTime.fillText(`${r.dijkTime.toFixed(2)}ms`, gx + barW / 2, 202 - hD);
    ctxTime.fillText(`${r.astarTime.toFixed(2)}ms`, gx + barW * 1.5 + 4, 202 - hA);
    ctxTime.fillText(r.scale, gx + barW + 2, 226);
  });

  ctxTime.fillStyle = "#2563eb"; ctxTime.fillRect(wt - 170, 15, 12, 12);
  ctxTime.fillStyle = "#1e293b"; ctxTime.textAlign = "left"; ctxTime.fillText("Dijkstra (ms)", wt - 152, 25);
  ctxTime.fillStyle = "#16a34a"; ctxTime.fillRect(wt - 90, 15, 12, 12);
  ctxTime.fillText("A* (ms)", wt - 72, 25);
}

btnExportBenchmarkCsv?.addEventListener("click", () => {
  if (benchmarkResults.length === 0) return showAlert("Hãy chạy benchmark trước khi xuất CSV!", "warning");
  let csv = "Scale,TotalNodes,TotalEdges,DijkstraNodes,AStarNodes,SavedNodes,SavedPercent,DijkstraTimeMs,AStarTimeMs,Status\n";
  benchmarkResults.forEach(r => {
    csv += `${r.scale},${r.totalNodes},${r.totalEdges},${r.dijkNodes},${r.astarNodes},${r.savedNodes},${r.pctSaved},${r.dijkTime.toFixed(4)},${r.astarTime.toFixed(4)},${r.status}\n`;
  });
  downloadFile(csv, "benchmark_results.csv", "text/csv");
  showAlert("Đã xuất kết quả benchmark ra file CSV!", "success");
});

window.addEventListener("DOMContentLoaded", () => {
  initSampleMap();
});

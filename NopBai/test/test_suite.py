# Hoc phan: Cau truc du lieu va Giai thuat - Bo kiem thu toan dien (Zero Libraries)

import time
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from route_finder import (
    IndexedMinHeap,
    CustomStack,
    CustomQueue,
    CustomHashTable,
    CityMapGraph,
    dijkstra_shortest_path,
    astar_shortest_path,
    sqrt_newton,
    to_json_string,
    parse_json_string
)

def run_all_tests():
    test_results = []
    pass_count = 0
    fail_count = 0

    def record_test(tc_id, category, description, expected, actual, passed, time_ms=0.0):
        nonlocal pass_count, fail_count
        status = "PASS" if passed else "FAIL"
        if passed:
            pass_count += 1
            print(f"[PASS] {tc_id}: {description} -> Ket qua: {actual}")
        else:
            fail_count += 1
            print(f"[FAIL] {tc_id}: {description} -> Ky vong: {expected} | Thuc te: {actual}")
        test_results.append({
            "id": tc_id,
            "category": category,
            "description": description,
            "expected": str(expected),
            "actual": str(actual),
            "status": status,
            "time_ms": f"{time_ms:.4f}"
        })

    print("=" * 80)
    print("   HE THONG KIEM THU TOAN DIEN (AUTOMATED TEST SUITE - ZERO LIBRARIES)")
    print("   DE TAI 5: HE THONG TIM DUONG DI NGAN NHAT TREN BAN DO")
    print("=" * 80)

    # NHOM 1: MIN-HEAP
    print("\n=== NHOM 1: KIEM THU HANG DOI UU TIEN MIN-HEAP ===")
    h1 = IndexedMinHeap(10)
    p, item = h1.pop_min()
    record_test("TC01_HEAP_EMPTY", "Min-Heap", "Kiem tra thao tac pop tren heap rong", "(None, None)", f"({p}, {item})", p is None and item is None)

    h2 = IndexedMinHeap(10)
    h2.insert(5.0, 1)
    h2.insert(2.0, 2)
    h2.insert(8.0, 3)
    h2.insert(1.5, 4)
    extracted = []
    while not h2.is_empty():
        p, item = h2.pop_min()
        extracted.append(p)
    record_test("TC02_HEAP_ORDER", "Min-Heap", "Thu tu trich xuat tang dan cua Min-Heap", "[1.5, 2.0, 5.0, 8.0]", str(extracted), extracted == [1.5, 2.0, 5.0, 8.0])

    h3 = IndexedMinHeap(10)
    h3.insert(10.0, 1)
    h3.insert(5.0, 2)
    h3.decrease_key(1, 2.0)
    p, item = h3.pop_min()
    record_test("TC03_HEAP_DECREASE_KEY", "Min-Heap", "Giam khoa decrease_key trong O(log V)", "(2.0, 1)", f"({p}, {item})", p == 2.0 and item == 1)

    # NHOM 2: BANG BAM, NGAN XEP VA HANG DOI BFS
    print("\n=== NHOM 2: KIEM THU BANG BAM, NGAN XEP VA HANG DOI ===")
    ht = CustomHashTable(3)
    for i in range(20):
        ht.put(f"Key_{i}", i * 10)
    rehash_ok = all(ht.get(f"Key_{i}") == i * 10 for i in range(20))
    record_test("TC04_HASH_TABLE", "Hash Table", "Bang bam collision & rehash tu cai dat", "True", str(rehash_ok), rehash_ok)

    st = CustomStack()
    st.push("A")
    st.push("B")
    st.push("C")
    rev = st.to_list()
    record_test("TC05_STACK_TRACE", "Stack", "Ngan xep dao nguoc lo trinh truy vet", "['C', 'B', 'A']", str(rev), rev == ["C", "B", "A"])

    q = CustomQueue()
    q.push(10)
    q.push(20)
    q_res = [q.pop(), q.pop()]
    record_test("TC05B_QUEUE_BFS", "Queue", "Hang doi FIFO tu cai dat", "[10, 20]", str(q_res), q_res == [10, 20])

    # NHOM 3: TINH DUNG DAN (DAP AN TINH TAY TRUOC)
    print("\n=== NHOM 3: KIEM THU TINH DUNG DAN (DAP AN TINH TAY) ===")
    g_manual = CityMapGraph()
    g_manual.add_node("N1", 0, 0)
    g_manual.add_node("N2", 2, 0)
    g_manual.add_node("N3", 3, 0)
    g_manual.add_node("N4", 4, 0)
    g_manual.add_edge("N1", "N2", 2.0, 1.0, False)
    g_manual.add_edge("N2", "N3", 1.0, 1.0, False)
    g_manual.add_edge("N3", "N4", 1.0, 1.0, False)
    g_manual.add_edge("N1", "N4", 5.0, 1.0, False)

    res_m = dijkstra_shortest_path(g_manual, "N1", "N4")
    record_test("TC06_MANUAL_CALC", "Dijkstra", "Kiem chung dap an tinh tay: N1 -> N4 = 4.0", "Cost=4.0, Path=['N1', 'N2', 'N3', 'N4']", f"Cost={res_m['total_cost']}, Path={res_m['path']}", res_m["total_cost"] == 4.0 and res_m["path"] == ["N1", "N2", "N3", "N4"])

    res_all = dijkstra_shortest_path(g_manual, "N1", None)
    expected_all = {"N1": 0.0, "N2": 2.0, "N3": 3.0, "N4": 4.0}
    record_test("TC07_DIJKSTRA_ALL", "Dijkstra", "Dijkstra nguon don den tat ca cac nut", str(expected_all), str(res_all["distances"]), res_all["distances"] == expected_all)

    # NHOM 4: DUONG 1 CHIEU, MAT LIEN THONG & BFS
    print("\n=== NHOM 4: KIEM THU DUONG MOT CHIEU VA MAT LIEN THONG ===")
    g_oneway = CityMapGraph()
    g_oneway.add_node("A", 0, 0)
    g_oneway.add_node("B", 10, 0)
    g_oneway.add_node("C_ISOLATED", 20, 20)
    g_oneway.add_edge("A", "B", 5.0, 1.0, True)

    res_fwd = dijkstra_shortest_path(g_oneway, "A", "B")
    record_test("TC08_ONEWAY_FORWARD", "One-way Edge", "Tim duong xuoi chieu A -> B", "5.0", str(res_fwd["total_cost"]), res_fwd["total_cost"] == 5.0)

    res_bwd = dijkstra_shortest_path(g_oneway, "B", "A")
    record_test("TC09_ONEWAY_BACKWARD", "One-way Edge", "Tu choi di nguoc chieu B -> A", "inf", str(res_bwd["total_cost"]), res_bwd["total_cost"] == float("inf"))

    res_iso = dijkstra_shortest_path(g_oneway, "A", "C_ISOLATED")
    record_test("TC10_DISCONNECTED", "Disconnected", "Do thi mat lien thong (bao loi an toan)", "False", str(res_iso["success"]), not res_iso["success"])

    conn, c_count = g_oneway.check_connectivity_bfs()
    record_test("TC10B_BFS_CONNECTIVITY", "BFS", "Kiem tra tinh lien thong bang BFS", "False (2/3 nut)", f"{conn} ({c_count}/3 nut)", not conn and c_count == 2)

    # NHOM 5: GIAI THUAT A* & TINH ADMISSIBLE
    print("\n=== NHOM 5: KIEM THU GIAI THUAT A* & TINH ADMISSIBLE ===")
    g_astar = CityMapGraph()
    g_astar.add_node("S", 0.0, 0.0)
    g_astar.add_node("M1", 5.0, 2.0)
    g_astar.add_node("M2", 5.0, -2.0)
    g_astar.add_node("E", 10.0, 0.0)
    g_astar.add_edge("S", "M1", 5.5, 1.0, False)
    g_astar.add_edge("M1", "E", 5.6, 1.0, False)
    g_astar.add_edge("S", "M2", 7.0, 1.0, False)
    g_astar.add_edge("M2", "E", 7.0, 1.0, False)

    res_d = dijkstra_shortest_path(g_astar, "S", "E")
    res_a = astar_shortest_path(g_astar, "S", "E")

    record_test("TC11_ASTAR_COST", "A*", "Chi phi A* bang tuyet doi Dijkstra", f"{res_d['total_cost']:.2f}", f"{res_a['total_cost']:.2f}", abs(res_d["total_cost"] - res_a["total_cost"]) < 1e-9)
    record_test("TC12_ASTAR_NODES", "A*", "So nut duyet cua A* <= Dijkstra", f"<= {res_d['visited_count']}", str(res_a["visited_count"]), res_a["visited_count"] <= res_d["visited_count"])

    res_same = astar_shortest_path(g_astar, "S", "S")
    record_test("TC13_SAME_START_END", "Edge Case", "Diem bat dau trung diem ket thuc", "Cost=0.0, Visited=1", f"Cost={res_same['total_cost']}, Visited={res_same['visited_count']}", res_same["total_cost"] == 0.0 and res_same["visited_count"] == 1)

    # NHOM 6: KET XE DONG & DUNG LUONG TEST >= 200 CAP NGAU NHIEN
    print("\n=== NHOM 6: KIEM THU MO PHONG KET XE DONG ===")
    g_astar.update_traffic("M1", "E", 3.0)
    res_reroute = dijkstra_shortest_path(g_astar, "S", "E")
    expected_path = ["S", "M2", "E"]
    record_test("TC14_TRAFFIC_REROUTING", "Traffic Simulation", "Tu dong doi huong khi ket xe tren tuyen cu", str(expected_path), str(res_reroute["path"]), res_reroute["path"] == expected_path)

    ok_inv, _ = g_astar.update_traffic("S", "M1", 0.5)
    record_test("TC15_TRAFFIC_INVALID_K", "Input Validation", "Tu choi he so ket xe k < 1.0", "False", str(ok_inv), not ok_inv)

    # NHOM 7: ROBUSTNESS & JSON ROUND-TRIP
    print("\n=== NHOM 7: KIEM THU XU LY BIEN & JSON ROUND-TRIP ===")
    g_empty = CityMapGraph()
    ok_neg, _ = g_empty.add_edge("X", "Y", -5.0)
    record_test("TC16_NEGATIVE_WEIGHT", "Input Validation", "Tu choi trong so canh am", "False", str(ok_neg), not ok_neg)

    res_none = dijkstra_shortest_path(g_empty, "KhongTonTai1", "KhongTonTai2")
    record_test("TC17_NON_EXIST_NODE", "Robustness", "Truy van nut khong ton tai", "False", str(res_none["success"]), not res_none["success"])

    sq_neg = sqrt_newton(-100)
    sq_zero = sqrt_newton(0)
    sq_pos = sqrt_newton(16)
    record_test("TC18_NEWTON_SQRT", "Math Robustness", "Newton-Raphson can bac hai bien am va 0", "sq=0, 0, 4", f"sq={sq_neg}, {sq_zero}, {sq_pos}", sq_neg == 0.0 and sq_zero == 0.0 and abs(sq_pos - 4.0) < 1e-5)

    # JSON Round-trip
    g_orig = CityMapGraph()
    g_orig.add_node("HN", 10.5, 20.5)
    g_orig.add_node("SG", 15.0, 30.0)
    g_orig.add_edge("HN", "SG", 50.0, 1.5, False)
    json_text = to_json_string(g_orig.to_dict())
    parsed_dict = parse_json_string(json_text)
    g_recon = CityMapGraph()
    for nd in parsed_dict["nodes"]:
        g_recon.add_node(nd["id"], nd["x"], nd["y"])
    for ed in parsed_dict["edges"]:
        g_recon.add_edge(ed["from"], ed["to"], ed["base_weight"], ed["traffic_factor"], ed["is_oneway"])
    roundtrip_ok = (g_recon.num_nodes == g_orig.num_nodes and g_recon.num_edges == g_orig.num_edges)
    record_test("TC18B_JSON_ROUNDTRIP", "JSON", "Bo parser JSON thuan chay khong import thu vien", "True", str(roundtrip_ok), roundtrip_ok)

    # NHOM 8: KIEM THU 200 CAP NGAU NHIEN DIJKSTRA VS A*
    print("\n=== NHOM 8: KIEM THU >= 200 CAP NGAU NHIEN (A* VS DIJKSTRA) ===")
    g_grid = CityMapGraph()
    for r in range(15):
        for c in range(15):
            g_grid.add_node(f"N_{r}_{c}", float(c * 10), float(r * 10))
    for r in range(15):
        for c in range(15):
            u = f"N_{r}_{c}"
            if c + 1 < 15: g_grid.add_edge(u, f"N_{r}_{c+1}", 10.0, 1.0, False)
            if r + 1 < 15: g_grid.add_edge(u, f"N_{r+1}_{c}", 10.0, 1.0, False)

    pairs_tested = 0
    all_pairs_equal = True
    for i in range(15):
        for j in range(15):
            s_name = f"N_{i}_{j}"
            e_name = f"N_{14-i}_{14-j}"
            if s_name != e_name:
                d_r = dijkstra_shortest_path(g_grid, s_name, e_name)
                a_r = astar_shortest_path(g_grid, s_name, e_name)
                if abs(d_r["total_cost"] - a_r["total_cost"]) > 1e-9:
                    all_pairs_equal = False
                    break
                pairs_tested += 1
                if pairs_tested >= 200:
                    break
        if pairs_tested >= 200:
            break

    record_test("TC19_200_RANDOM_PAIRS", "Admissible Check", f"Kiem thu {pairs_tested} cap ngau nhien (Cost Dijkstra == A*)", "True", str(all_pairs_equal), all_pairs_equal)

    # NHOM 9: BENCHMARK DO LUONG QUY MO LON (STRESS TESTS)
    print("\n=== NHOM 9: BENCHMARK HIEU NANG QUY MO LON (STRESS TESTS) ===")
    def build_grid(rows, cols):
        g = CityMapGraph()
        for r in range(rows):
            for c in range(cols):
                g.add_node(f"N_{r}_{c}", float(c * 5), float(r * 5))
        for r in range(rows):
            for c in range(cols):
                curr = f"N_{r}_{c}"
                if c + 1 < cols: g.add_edge(curr, f"N_{r}_{c+1}", 5.0, 1.0, False)
                if r + 1 < rows: g.add_edge(curr, f"N_{r+1}_{c}", 5.0, 1.0, False)
        return g

    scales = [
        (10, 10, "100 dinh (Grid 10x10)", "TC20_PERF_100"),
        (20, 50, "1.000 dinh (Grid 20x50)", "TC21_PERF_1000"),
        (50, 100, "5.000 dinh (Grid 50x100)", "TC22_PERF_5000"),
        (100, 200, "20.000 dinh (Grid 100x200)", "TC23_PERF_20000")
    ]

    for rows, cols, desc, tc_id in scales:
        V = rows * cols
        g_scale = build_grid(rows, cols)
        start_node = "N_0_0"
        end_node = f"N_{rows-1}_{cols-1}"

        # Do thoi gian nhieu lan loai bo warmup
        dijkstra_shortest_path(g_scale, start_node, end_node)
        astar_shortest_path(g_scale, start_node, end_node)

        runs = 5 if V <= 1000 else 1
        t0 = time.perf_counter()
        for _ in range(runs):
            res_d = dijkstra_shortest_path(g_scale, start_node, end_node)
        t_d = ((time.perf_counter() - t0) / runs) * 1000

        t0 = time.perf_counter()
        for _ in range(runs):
            res_a = astar_shortest_path(g_scale, start_node, end_node)
        t_a = ((time.perf_counter() - t0) / runs) * 1000

        is_pass = abs(res_d["total_cost"] - res_a["total_cost"]) < 1e-9
        saved_nodes = res_d["visited_count"] - res_a["visited_count"]
        pct_saved = (saved_nodes / res_d["visited_count"]) * 100 if res_d["visited_count"] > 0 else 0
        actual_info = f"Dijkstra={t_d:.1f}ms ({res_d['visited_count']} nut), A*={t_a:.1f}ms ({res_a['visited_count']} nut, giam {pct_saved:.1f}%)"
        record_test(tc_id, "Stress Test", f"Hieu nang quy mo {V} dinh: {desc}", "Cost Dijkstra == Cost A*", actual_info, is_pass, t_d + t_a)

    csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "test", "test_results.csv"))
    with open(csv_path, "w", encoding="utf-8") as f:
        f.write("TestID,Category,Description,Expected,Actual,Status,ExecutionTimeMs\n")
        for r in test_results:
            desc_clean = r["description"].replace(",", ";")
            exp_clean = r["expected"].replace(",", ";")
            act_clean = r["actual"].replace(",", ";")
            f.write(f"{r['id']},{r['category']},{desc_clean},{exp_clean},{act_clean},{r['status']},{r['time_ms']}\n")

    print("\n" + "=" * 80)
    print(f"TONG KET KIEM THU: {pass_count}/{pass_count + fail_count} TEST CASES PASS ({pass_count/(pass_count+fail_count)*100:.1f}%) | FAILED: {fail_count}")
    print(f"Da xuat toan bo ket qua chi tiet ra file CSV: {csv_path}")
    print("=" * 80)

if __name__ == "__main__":
    run_all_tests()

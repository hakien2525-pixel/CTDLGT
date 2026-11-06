# Hoc phan: Cau truc du lieu va Giai thuat - Do thoi gian va thu nghiem hieu nang benchmark

import time
from typing import Callable, Any, Dict
from .sinhdothi import sinh_do_thi_luoi

def do_thoi_gian_thuc_thi(ham_thuc_thi: Callable[[], Any], min_tong_ms: float = 45.0) -> float:
    # O(N) do thoi gian lặp nhieu lan loai bo warmup CPU dat thoi gian chay chinh xac
    ham_thuc_thi() # Warmup
    dem = 0
    bat_dau = time.perf_counter()
    while True:
        ham_thuc_thi()
        dem += 1
        tong_ms = (time.perf_counter() - bat_dau) * 1000.0
        if tong_ms >= min_tong_ms or dem >= 1000:
            break
    tong_ms = (time.perf_counter() - bat_dau) * 1000.0
    return tong_ms / dem

def chay_benchmark_mot_quy_mo(quy_mo_ten: str, rows: int, cols: int) -> Dict[str, Any]:
    # O((V + E) log V) chay va so sanh chi tiet giua Dijkstra va A* tren do thi luoi
    from ..thuattoan.dijkstra import dijkstra_shortest_path
    from ..thuattoan.astar import astar_shortest_path

    g = sinh_do_thi_luoi(rows, cols, cell_dist=5.0)
    start_node = "N_0_0"
    end_node = f"N_{rows-1}_{cols-1}"

    res_d = dijkstra_shortest_path(g, start_node, end_node)
    res_a = astar_shortest_path(g, start_node, end_node)

    t_d = do_thoi_gian_thuc_thi(lambda: dijkstra_shortest_path(g, start_node, end_node))
    t_a = do_thoi_gian_thuc_thi(lambda: astar_shortest_path(g, start_node, end_node))

    cost_diff = abs(res_d.total_cost - res_a.total_cost)
    is_pass = cost_diff < 1e-9
    saved_nodes = res_d.visited_count - res_a.visited_count
    pct = (saved_nodes / res_d.visited_count * 100.0) if res_d.visited_count > 0 else 0.0

    return {
        "quy_mo": quy_mo_ten,
        "so_dinh": rows * cols,
        "so_canh": g.num_edges,
        "dijk_nut": res_d.visited_count,
        "astar_nut": res_a.visited_count,
        "nut_tiet_kiem": saved_nodes,
        "ti_le_tiet_kiem": pct,
        "dijk_time_ms": t_d,
        "astar_time_ms": t_a,
        "trang_thai": "PASS" if is_pass else "FAIL"
    }

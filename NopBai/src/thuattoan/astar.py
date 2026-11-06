# Hoc phan: Cau truc du lieu va Giai thuat - Giai thuat A* voi Euclidean Heuristic Admissible

from typing import Any
from ..cautruc.minheap import IndexedMinHeap
from ..tienich.toan import tinh_khoang_cach_euclid
from .duongdi import KetQuaTimDuong, phuc_hoi_duong_di

def astar_shortest_path(dothi: Any, start_name: Any, end_name: Any, heuristic_weight: float = 1.0) -> KetQuaTimDuong:
    # O((V + E) log V) A* voi heuristic Euclid tinh h_scale tu dong dam bao admissible va consistent
    start_idx, end_idx = dothi.get_node_index(start_name), dothi.get_node_index(end_name)
    if start_idx is None or end_idx is None:
        loi = f"Diem {'bat dau' if start_idx is None else 'ket thuc'} khong ton tai!"
        return KetQuaTimDuong(success=False, message=loi)

    if start_idx == end_idx:
        ten = dothi.get_node_name(start_idx)
        return KetQuaTimDuong(success=True, path=[ten], total_cost=0.0, visited_count=1, heap_ops=1, visited_order=[ten])

    h_scale = dothi.compute_admissible_h_scale() * float(heuristic_weight)
    end_x, end_y = dothi.node_coords[end_idx]

    def heuristic(idx: int) -> float:
        x, y = dothi.node_coords[idx]
        return tinh_khoang_cach_euclid(x, y, end_x, end_y) * h_scale

    V = dothi.num_nodes
    inf = float("inf")
    g_score, f_score, prev, closed_set = [inf] * V, [inf] * V, [None] * V, [False] * V
    visited_order = []
    heap = IndexedMinHeap(V)

    g_score[start_idx] = 0.0
    h_start = heuristic(start_idx)
    f_score[start_idx] = h_start
    heap.insert(f_score[start_idx], start_idx)
    nodes_visited_count = 0

    while not heap.is_empty():
        _, u = heap.pop_min()
        if closed_set[u]:
            continue
        closed_set[u] = True
        nodes_visited_count += 1
        visited_order.append(dothi.get_node_name(u))
        if u == end_idx:
            break

        curr_edge = dothi.adj[u]
        while curr_edge is not None:
            v, w = curr_edge.target_idx, curr_edge.get_effective_weight()
            if not closed_set[v]:
                tent_g = g_score[u] + w
                if tent_g < g_score[v]:
                    g_score[v], prev[v] = tent_g, u
                    f_score[v] = tent_g + heuristic(v)
                    if heap.contains(v): heap.decrease_key(v, f_score[v])
                    else: heap.insert(f_score[v], v)
            curr_edge = curr_edge.next

    if g_score[end_idx] == inf:
        return KetQuaTimDuong(success=False, message=f"Khong co duong di tu '{start_name}' den '{end_name}'!", visited_count=nodes_visited_count, heap_ops=heap.heap_ops)

    duong_di = phuc_hoi_duong_di(prev, end_idx, dothi)
    return KetQuaTimDuong(success=True, path=duong_di, total_cost=g_score[end_idx], visited_count=nodes_visited_count, heap_ops=heap.heap_ops, visited_order=visited_order)

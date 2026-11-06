# Hoc phan: Cau truc du lieu va Giai thuat - Giai thuat Dijkstra nguon don va diem-den-diem

from typing import Optional, List, Any
from ..cautruc.minheap import IndexedMinHeap
from .duongdi import KetQuaTimDuong, phuc_hoi_duong_di

def dijkstra_shortest_path(dothi: Any, start_name: Any, end_name: Optional[Any] = None) -> KetQuaTimDuong:
    # O((V + E) log V) Dijkstra tim duong ngan nhat dung som khi gap end_name
    start_idx = dothi.get_node_index(start_name)
    if start_idx is None:
        return KetQuaTimDuong(success=False, message=f"Diem bat dau '{start_name}' khong ton tai!")
    end_idx = dothi.get_node_index(end_name) if end_name is not None else None
    if end_name is not None and end_idx is None:
        return KetQuaTimDuong(success=False, message=f"Diem ket thuc '{end_name}' khong ton tai!")

    if end_idx is not None and start_idx == end_idx:
        ten = dothi.get_node_name(start_idx)
        return KetQuaTimDuong(success=True, path=[ten], total_cost=0.0, visited_count=1, heap_ops=1, visited_order=[ten], distances={ten: 0.0})

    V = dothi.num_nodes
    inf = float("inf")
    dist: List[float] = [inf] * V
    prev: List[Optional[int]] = [None] * V
    visited: List[bool] = [False] * V
    visited_order: List[str] = []
    heap = IndexedMinHeap(V)

    dist[start_idx] = 0.0
    heap.insert(0.0, start_idx)
    nodes_visited_count = 0

    while not heap.is_empty():
        curr_dist, u = heap.pop_min()
        if visited[u]:
            continue
        visited[u] = True
        nodes_visited_count += 1
        visited_order.append(dothi.get_node_name(u))
        if end_idx is not None and u == end_idx:
            break

        curr_edge = dothi.adj[u]
        while curr_edge is not None:
            v, w = curr_edge.target_idx, curr_edge.get_effective_weight()
            if not visited[v]:
                new_dist = curr_dist + w
                if new_dist < dist[v]:
                    dist[v], prev[v] = new_dist, u
                    if heap.contains(v): heap.decrease_key(v, new_dist)
                    else: heap.insert(new_dist, v)
            curr_edge = curr_edge.next

    if end_idx is None:
        return KetQuaTimDuong(success=True, distances={dothi.get_node_name(i): dist[i] for i in range(V)}, visited_count=nodes_visited_count, heap_ops=heap.heap_ops, visited_order=visited_order)

    if dist[end_idx] == inf:
        return KetQuaTimDuong(success=False, message=f"Khong co duong di tu '{start_name}' den '{end_name}'!", visited_count=nodes_visited_count, heap_ops=heap.heap_ops)

    duong_di = phuc_hoi_duong_di(prev, end_idx, dothi)
    return KetQuaTimDuong(success=True, path=duong_di, total_cost=dist[end_idx], visited_count=nodes_visited_count, heap_ops=heap.heap_ops, visited_order=visited_order)

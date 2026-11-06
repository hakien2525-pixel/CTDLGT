# Hoc phan: Cau truc du lieu va Giai thuat - Kiem tra tinh lien thong bang BFS

from typing import Tuple, Optional, Any
from ..cautruc.queue_ import CustomQueue

def kiem_tra_lien_thong_bfs(dothi: Any, start_name: Optional[str] = None) -> Tuple[bool, int]:
    # O(V + E) BFS kiem tra tinh lien thong bang hang doi CustomQueue
    if dothi.num_nodes == 0:
        return True, 0
    start_idx = 0 if start_name is None else dothi.get_node_index(start_name)
    if start_idx is None:
        return False, 0
    visited = [False] * dothi.num_nodes
    q = CustomQueue()
    q.push(start_idx)
    visited[start_idx] = True
    count = 0
    while not q.is_empty():
        u = q.pop()
        count += 1
        curr = dothi.adj[u]
        while curr is not None:
            v = curr.target_idx
            if not visited[v]:
                visited[v] = True
                q.push(v)
            curr = curr.next
    return (count == dothi.num_nodes), count

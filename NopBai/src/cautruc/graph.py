# Hoc phan: Cau truc du lieu va Giai thuat - Do thi danh sach ke voi toa do km

from typing import List, Tuple, Optional, Dict, Any
from .hashtable import CustomHashTable

class AdjListNode:
    # O(1) nut danh sach lien ket don bieu dien cung duong
    def __init__(self, target_idx: int, base_weight: float, traffic_factor: float = 1.0, is_oneway: bool = False) -> None:
        self.target_idx: int = target_idx
        self.base_weight: float = float(base_weight)
        self.traffic_factor: float = float(traffic_factor)
        self.is_oneway: bool = bool(is_oneway)
        self.next: Optional["AdjListNode"] = None

    def get_effective_weight(self) -> float:
        return self.base_weight * self.traffic_factor

class CityMapGraph:
    # O(V + E) do thi danh sach ke ho tro toa do km, 1/2 chieu va he so ket xe dong
    def __init__(self) -> None:
        self.node_names: List[str] = []
        self.node_coords: List[Tuple[float, float]] = []
        self.node_lookup: CustomHashTable = CustomHashTable()
        self.adj: List[Optional[AdjListNode]] = []
        self.num_nodes: int = 0
        self.num_edges: int = 0

    def add_node(self, name: Any, x: Optional[float] = None, y: Optional[float] = None) -> int:
        name_str = str(name)
        if self.node_lookup.contains(name_str):
            idx = self.node_lookup.get(name_str)
            if x is not None and y is not None:
                self.node_coords[idx] = (float(x), float(y))
            return idx
        idx = self.num_nodes
        self.node_names.append(name_str)
        cx = float(x) if x is not None else 0.0
        cy = float(y) if y is not None else 0.0
        self.node_coords.append((cx, cy))
        self.adj.append(None)
        self.node_lookup.put(name_str, idx)
        self.num_nodes += 1
        return idx

    def get_node_index(self, name: Any) -> Optional[int]:
        return self.node_lookup.get(str(name))

    def get_node_name(self, idx: int) -> Optional[str]:
        return self.node_names[idx] if 0 <= idx < self.num_nodes else None

    def _append_edge_node(self, u: int, node: AdjListNode) -> None:
        if self.adj[u] is None:
            self.adj[u] = node
        else:
            curr = self.adj[u]
            while curr.next is not None:
                curr = curr.next
            curr.next = node

    def add_edge(self, u_name: Any, v_name: Any, base_weight: float, traffic_factor: float = 1.0, is_oneway: bool = False) -> Tuple[bool, str]:
        if base_weight < 0:
            return False, "Trong so canh khong duoc am!"
        u, v = self.add_node(u_name), self.add_node(v_name)
        self._append_edge_node(u, AdjListNode(v, base_weight, traffic_factor, is_oneway))
        self.num_edges += 1
        if not is_oneway:
            self._append_edge_node(v, AdjListNode(u, base_weight, traffic_factor, is_oneway))
            self.num_edges += 1
        return True, "Thanh cong"

    def remove_edge(self, u_name: Any, v_name: Any) -> Tuple[bool, str]:
        u, v = self.get_node_index(u_name), self.get_node_index(v_name)
        if u is None or v is None:
            return False, "Dinh khong ton tai!"
        def _rem(src: int, dst: int) -> bool:
            curr, prev, removed = self.adj[src], None, False
            while curr is not None:
                if curr.target_idx == dst:
                    if prev is None: self.adj[src] = curr.next
                    else: prev.next = curr.next
                    self.num_edges -= 1
                    removed = True
                    break
                prev, curr = curr, curr.next
            return removed
        r1 = _rem(u, v)
        r2 = _rem(v, u)
        return (r1 or r2), "Thanh cong" if (r1 or r2) else "Khong tim thay canh!"

    def update_traffic(self, u_name: Any, v_name: Any, traffic_factor: float) -> Tuple[bool, str]:
        if traffic_factor < 1.0:
            return False, "He so ket xe k phai >= 1.0!"
        u, v = self.get_node_index(u_name), self.get_node_index(v_name)
        if u is None or v is None:
            return False, "Dinh khong ton tai!"
        updated = False
        for src, dst in ((u, v), (v, u)):
            curr = self.adj[src]
            while curr is not None:
                if curr.target_idx == dst:
                    curr.traffic_factor = float(traffic_factor)
                    updated = True
                curr = curr.next
        return updated, "Thanh cong" if updated else "Khong tim thay canh!"

    def reset_all_traffic(self) -> None:
        for u in range(self.num_nodes):
            curr = self.adj[u]
            while curr is not None:
                curr.traffic_factor = 1.0
                curr = curr.next

    def compute_admissible_h_scale(self) -> float:
        min_ratio = 1.0
        for u in range(self.num_nodes):
            ux, uy = self.node_coords[u]
            curr = self.adj[u]
            while curr is not None:
                vx, vy = self.node_coords[curr.target_idx]
                dx, dy = ux - vx, uy - vy
                # Tinh can bac hai newton tai cho de khong gay circular import
                sq = dx * dx + dy * dy
                if sq > 0.0:
                    x = float(sq)
                    while True:
                        can = 0.5 * (x + sq / x)
                        if abs(can - x) < 1e-7:
                            euclid = can
                            break
                        x = can
                else:
                    euclid = 0.0

                if euclid > 1e-6:
                    ratio = curr.base_weight / euclid
                    if ratio < min_ratio:
                        min_ratio = ratio
                curr = curr.next
        return max(0.0, min_ratio)

    def check_connectivity_bfs(self, start_name: Optional[Any] = None) -> Tuple[bool, int]:
        # O(V + E) BFS kiem tra tinh lien thong su dung hang doi
        if self.num_nodes == 0:
            return True, 0
        start_idx = 0 if start_name is None else self.get_node_index(start_name)
        if start_idx is None:
            return False, 0
        visited = [False] * self.num_nodes
        q: List[int] = [start_idx]
        head = 0
        visited[start_idx] = True
        count = 0
        while head < len(q):
            u = q[head]
            head += 1
            count += 1
            curr = self.adj[u]
            while curr is not None:
                v = curr.target_idx
                if not visited[v]:
                    visited[v] = True
                    q.append(v)
                curr = curr.next
        return (count == self.num_nodes), count

    def get_all_edges_info(self) -> List[Dict[str, Any]]:
        edges = []
        for u in range(self.num_nodes):
            curr = self.adj[u]
            while curr is not None:
                v = curr.target_idx
                if curr.is_oneway or (u < v):
                    edges.append({
                        "from": self.node_names[u], "to": self.node_names[v],
                        "base_weight": curr.base_weight, "traffic_factor": curr.traffic_factor,
                        "effective_weight": curr.get_effective_weight(), "is_oneway": curr.is_oneway
                    })
                curr = curr.next
        return edges

    def to_dict(self) -> Dict[str, Any]:
        return {
            "num_nodes": self.num_nodes, "num_edges": self.num_edges,
            "nodes": [{"id": self.node_names[i], "x": self.node_coords[i][0], "y": self.node_coords[i][1]} for i in range(self.num_nodes)],
            "edges": self.get_all_edges_info()
        }

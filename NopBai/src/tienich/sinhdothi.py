# Hoc phan: Cau truc du lieu va Giai thuat - Sinh do thi luoi va do thi ngau nhien co seed

from typing import List, Tuple
from ..cautruc.graph import CityMapGraph

class BoSinhSoNgauNhien:
    # O(1) bo sinh so gia ngau nhien Linear Congruential Generator (LCG) co seed tai lap duoc
    def __init__(self, seed: int = 123456789) -> None:
        self.state: int = seed

    def next_int(self, min_val: int, max_val: int) -> int:
        self.state = (self.state * 1103515245 + 12345) & 0x7FFFFFFF
        return min_val + (self.state % (max_val - min_val + 1))

    def next_float(self, min_val: float, max_val: float) -> float:
        self.state = (self.state * 1103515245 + 12345) & 0x7FFFFFFF
        ti_le = self.state / 0x7FFFFFFF
        return min_val + ti_le * (max_val - min_val)

def sinh_do_thi_luoi(rows: int, cols: int, cell_dist: float = 5.0) -> CityMapGraph:
    # O(rows * cols) sinh do thi luoi toa do km khop tuyet doi khoang cach Euclid
    g = CityMapGraph()
    for r in range(rows):
        for c in range(cols):
            g.add_node(f"N_{r}_{c}", c * cell_dist, r * cell_dist)

    for r in range(rows):
        for c in range(cols):
            u = f"N_{r}_{c}"
            if c + 1 < cols:
                g.add_edge(u, f"N_{r}_{c+1}", cell_dist, 1.0, False)
            if r + 1 < rows:
                g.add_edge(u, f"N_{r+1}_{c}", cell_dist, 1.0, False)
    return g

def sinh_do_thi_ngau_nhien_lien_thong(num_nodes: int, extra_edges: int = 0, seed: int = 42) -> CityMapGraph:
    # O(V + E) sinh do thi ngau nhien dam bao lien thong bang cay khung Spanning Tree
    rng = BoSinhSoNgauNhien(seed)
    g = CityMapGraph()

    for i in range(num_nodes):
        x = rng.next_float(0.0, 100.0)
        y = rng.next_float(0.0, 100.0)
        g.add_node(f"Node_{i+1}", x, y)

    # Tao cay khung lien thong (Spanning Tree)
    for i in range(1, num_nodes):
        u_idx = rng.next_int(0, i - 1)
        u_name = f"Node_{u_idx+1}"
        v_name = f"Node_{i+1}"
        ux, uy = g.node_coords[u_idx]
        vx, vy = g.node_coords[i]
        khoang_cach = max(1.0, ((ux - vx)**2 + (uy - vy)**2)**0.5)
        g.add_edge(u_name, v_name, round(khoang_cach, 1), 1.0, False)

    # Them cac canh ngau nhien
    for _ in range(extra_edges):
        u_idx = rng.next_int(0, num_nodes - 1)
        v_idx = rng.next_int(0, num_nodes - 1)
        if u_idx != v_idx:
            u_name = f"Node_{u_idx+1}"
            v_name = f"Node_{v_idx+1}"
            ux, uy = g.node_coords[u_idx]
            vx, vy = g.node_coords[v_idx]
            khoang_cach = max(1.0, ((ux - vx)**2 + (uy - vy)**2)**0.5)
            is_oneway = rng.next_int(1, 10) <= 3
            g.add_edge(u_name, v_name, round(khoang_cach, 1), 1.0, is_oneway)

    return g

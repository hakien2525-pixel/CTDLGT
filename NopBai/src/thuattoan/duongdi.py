# Hoc phan: Cau truc du lieu va Giai thuat - Kieu du lieu va truy vet duong di

from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from ..cautruc.stack import CustomStack

@dataclass
class KetQuaTimDuong:
    # Kieu du lieu dong goi ket qua thong nhat cho ca Dijkstra va A*
    success: bool
    path: Optional[List[str]] = None
    total_cost: float = float("inf")
    visited_count: int = 0
    heap_ops: int = 0
    visited_order: Optional[List[str]] = None
    message: str = ""
    distances: Optional[Dict[str, float]] = None

    def __getitem__(self, item: str) -> Any:
        return getattr(self, item)

    def get(self, item: str, default: Any = None) -> Any:
        return getattr(self, item, default)

def phuc_hoi_duong_di(prev: List[Optional[int]], end_idx: int, dothi: Any) -> List[str]:
    # O(V) phuc hoi va dao nguoc thu tu duong di tu prev[] bang CustomStack
    stack = CustomStack()
    curr: Optional[int] = end_idx
    while curr is not None:
        stack.push(dothi.get_node_name(curr))
        curr = prev[curr]
    return stack.to_list()

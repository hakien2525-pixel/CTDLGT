# Hoc phan: Cau truc du lieu va Giai thuat - Hang doi uu tien Min-Heap co mang chi muc

from typing import List, Tuple, Optional

class IndexedMinHeap:
    # O(log V) Min-Heap co mang chi muc pos[] giup decrease_key dat O(log V)
    def __init__(self, capacity: int) -> None:
        self.heap: List[Tuple[float, int]] = []
        self.pos: List[int] = [-1] * capacity
        self.heap_ops: int = 0

    def is_empty(self) -> bool:
        return len(self.heap) == 0

    def contains(self, item: int) -> bool:
        return 0 <= item < len(self.pos) and self.pos[item] != -1

    def insert(self, priority: float, item: int) -> None:
        self.heap_ops += 1
        idx = len(self.heap)
        self.heap.append((priority, item))
        self.pos[item] = idx
        self._sift_up(idx)

    def decrease_key(self, item: int, new_priority: float) -> None:
        self.heap_ops += 1
        idx = self.pos[item]
        if idx != -1 and new_priority < self.heap[idx][0]:
            self.heap[idx] = (new_priority, item)
            self._sift_up(idx)

    def pop_min(self) -> Tuple[Optional[float], Optional[int]]:
        self.heap_ops += 1
        if not self.heap:
            return None, None
        min_prio, min_item = self.heap[0]
        self.pos[min_item] = -1
        last_prio, last_item = self.heap.pop()
        if self.heap:
            self.heap[0] = (last_prio, last_item)
            self.pos[last_item] = 0
            self._sift_down(0)
        return min_prio, min_item

    def _better(self, i: int, j: int) -> bool:
        pi, ii = self.heap[i]
        pj, ij = self.heap[j]
        return pi < pj or (pi == pj and ii < ij)

    def _swap(self, i: int, j: int) -> None:
        self.pos[self.heap[i][1]], self.pos[self.heap[j][1]] = j, i
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def _sift_up(self, idx: int) -> None:
        cha = (idx - 1) // 2
        while idx > 0 and self._better(idx, cha):
            self._swap(idx, cha)
            idx, cha = cha, (cha - 1) // 2

    def _sift_down(self, idx: int) -> None:
        n = len(self.heap)
        while True:
            sm, trai, phai = idx, 2 * idx + 1, 2 * idx + 2
            if trai < n and self._better(trai, sm):
                sm = trai
            if phai < n and self._better(phai, sm):
                sm = phai
            if sm == idx:
                break
            self._swap(idx, sm)
            idx = sm

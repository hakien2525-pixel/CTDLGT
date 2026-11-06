# Hoc phan: Cau truc du lieu va Giai thuat - Ngan xep tu cai dat

from typing import Any, List, Optional

class CustomStack:
    # O(1) ngan xep tu cai dat bang mang phuc vu dao nguoc va truy vet lo trinh
    def __init__(self) -> None:
        self.data: List[Any] = []

    def push(self, phan_tu: Any) -> None:
        self.data.append(phan_tu)

    def pop(self) -> Optional[Any]:
        return self.data.pop() if self.data else None

    def is_empty(self) -> bool:
        return len(self.data) == 0

    def size(self) -> int:
        return len(self.data)

    def to_list(self) -> List[Any]:
        danh_sach: List[Any] = []
        while not self.is_empty():
            danh_sach.append(self.pop())
        return danh_sach

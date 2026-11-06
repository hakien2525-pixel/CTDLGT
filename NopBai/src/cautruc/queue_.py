# Hoc phan: Cau truc du lieu va Giai thuat - Hang doi FIFO tu cai dat

from typing import Any, Optional

class CustomQueue:
    # O(1) hang doi FIFO tu cai dat bang mang 2 con tro dung cho duyet BFS
    def __init__(self) -> None:
        self.data = []
        self.head: int = 0

    def push(self, phan_tu: Any) -> None:
        self.data.append(phan_tu)

    def pop(self) -> Optional[Any]:
        if self.head >= len(self.data):
            return None
        phan_tu = self.data[self.head]
        self.head += 1
        return phan_tu

    def is_empty(self) -> bool:
        return self.head >= len(self.data)

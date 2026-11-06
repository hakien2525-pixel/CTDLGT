# Hoc phan: Cau truc du lieu va Giai thuat - Bang bam djb2 Linear Probing

from typing import Any, Optional

class CustomHashTable:
    # O(1) trung binh, bang bam linear probing voi giai thuat djb2 anh xa ten sang chi so
    def __init__(self, capacity: int = 1009) -> None:
        self.capacity: int = capacity
        self.size: int = 0
        self.keys = [None] * capacity
        self.values = [None] * capacity

    def _hash(self, khoa_chuoi: Any) -> int:
        h = 5381
        for ky_tu in str(khoa_chuoi):
            h = ((h * 33) + ord(ky_tu)) & 0xFFFFFFFF
        return h % self.capacity

    def put(self, khoa: Any, gia_tri: Any) -> None:
        if self.size * 2 >= self.capacity:
            self._rehash()
        idx = self._hash(khoa)
        while self.keys[idx] is not None:
            if self.keys[idx] == khoa:
                self.values[idx] = gia_tri
                return
            idx = (idx + 1) % self.capacity
        self.keys[idx] = khoa
        self.values[idx] = gia_tri
        self.size += 1

    def get(self, khoa: Any) -> Optional[Any]:
        idx = self._hash(khoa)
        bat_dau = idx
        while self.keys[idx] is not None:
            if self.keys[idx] == khoa:
                return self.values[idx]
            idx = (idx + 1) % self.capacity
            if idx == bat_dau:
                break
        return None

    def contains(self, khoa: Any) -> bool:
        return self.get(khoa) is not None

    def _rehash(self) -> None:
        khoa_cu, gia_tri_cu = self.keys, self.values
        self.capacity = self.capacity * 2 + 1
        self.size = 0
        self.keys = [None] * self.capacity
        self.values = [None] * self.capacity
        for i in range(len(khoa_cu)):
            if khoa_cu[i] is not None:
                self.put(khoa_cu[i], gia_tri_cu[i])

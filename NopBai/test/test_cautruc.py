# Hoc phan: Cau truc du lieu va Giai thuat - Kiem thu cau truc du lieu

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.cautruc.minheap import IndexedMinHeap
from src.cautruc.hashtable import CustomHashTable
from src.cautruc.stack import CustomStack
from src.cautruc.queue_ import CustomQueue
from src.cautruc.graph import CityMapGraph

def test_heap_rong():
    heap = IndexedMinHeap(10)
    prio, item = heap.pop_min()
    assert prio is None and item is None, "Heap rong phai tra ve None, None"

def test_heap_thu_tu():
    heap = IndexedMinHeap(10)
    heap.insert(5.0, 0)
    heap.insert(2.0, 1)
    heap.insert(8.0, 2)
    heap.insert(1.5, 3)
    kq = []
    while not heap.is_empty():
        prio, _ = heap.pop_min()
        kq.append(prio)
    assert kq == [1.5, 2.0, 5.0, 8.0], "Thu tu trich xuat phai tang dan"

def test_heap_decrease_key():
    heap = IndexedMinHeap(10)
    heap.insert(10.0, 1)
    heap.insert(5.0, 2)
    heap.decrease_key(1, 2.0)
    prio, item = heap.pop_min()
    assert prio == 2.0 and item == 1, "decrease_key phai dua phan tu len dau heap"

def test_bang_bam():
    ht = CustomHashTable(capacity=5)
    for i in range(20):
        ht.put(f"Key_{i}", i * 10)
    for i in range(20):
        assert ht.get(f"Key_{i}") == i * 10, f"Gia tri cua Key_{i} phai bang {i * 10}"

def test_ngan_xep():
    st = CustomStack()
    st.push("A"); st.push("B"); st.push("C")
    assert st.to_list() == ["C", "B", "A"], "Ngan xep phai dao nguoc thu tu LIFO"

def test_hang_doi():
    q = CustomQueue()
    q.push(10); q.push(20)
    assert q.pop() == 10 and q.pop() == 20, "Hang doi phai tuan thu FIFO"

def chay_kiem_thu_cautruc():
    test_heap_rong()
    test_heap_thu_tu()
    test_heap_decrease_key()
    test_bang_bam()
    test_ngan_xep()
    test_hang_doi()
    print("[PASS] Toan bo kiem thu cau truc du lieu (Heap, Hash Table, Stack, Queue) thanh cong!")

if __name__ == "__main__":
    chay_kiem_thu_cautruc()

# Hoc phan: Cau truc du lieu va Giai thuat - Thuat toan sap xep va tim kiem tu cai dat

from typing import List, Tuple, Any

def quicksort_khoang_cach(arr: List[Tuple[str, float]], low: int = 0, high: int = -1) -> None:
    # O(N log N) sap xep nhanh quicksort tu cai dat phan hoach Hoare/Lomuto
    if high == -1:
        high = len(arr) - 1
    if low < high:
        pi = _partition(arr, low, high)
        quicksort_khoang_cach(arr, low, pi - 1)
        quicksort_khoang_cach(arr, pi + 1, high)

def _partition(arr: List[Tuple[str, float]], low: int, high: int) -> int:
    pivot = arr[high][1]
    i = low - 1
    for j in range(low, high):
        if arr[j][1] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

def tim_kiem_nhi_phan(arr: List[Tuple[str, float]], gia_tri_muc_tieu: float) -> int:
    # O(log N) tim kiem nhi phan phan tu tren mang da sap xep
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if abs(arr[mid][1] - gia_tri_muc_tieu) < 1e-6:
            return mid
        elif arr[mid][1] < gia_tri_muc_tieu:
            left = mid + 1
        else:
            right = mid - 1
    return -1

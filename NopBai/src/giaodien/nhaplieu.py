# Hoc phan: Cau truc du lieu va Giai thuat - Nhap va kiem tra tinh hop le cua du lieu

from typing import Optional, Any

def nhap_so_nguyen(thong_bao: str, min_val: Optional[int] = None, max_val: Optional[int] = None) -> int:
    # O(1) nhap so nguyen an toan khong crash khi nhap sai kieu
    while True:
        try:
            chuoi = input(thong_bao).strip()
            val = int(chuoi)
            if min_val is not None and val < min_val:
                print(f"[!] Gia tri phai lon hon hoac bang {min_val}!")
                continue
            if max_val is not None and val > max_val:
                print(f"[!] Gia tri phai nho hon hoac bang {max_val}!")
                continue
            return val
        except ValueError:
            print("[!] Vui long nhap so nguyen hop le!")

def nhap_so_thuc(thong_bao: str, min_val: Optional[float] = None) -> float:
    # O(1) nhap so thuc an toan tu choi gia tri am
    while True:
        try:
            chuoi = input(thong_bao).strip()
            val = float(chuoi)
            if min_val is not None and val < min_val:
                print(f"[!] Gia tri phai lon hon hoac bang {min_val}!")
                continue
            return val
        except ValueError:
            print("[!] Vui long nhap so thuc hop le!")

def nhap_ten_dinh(thong_bao: str, dothi: Any) -> str:
    # O(1) nhap ten dinh hoac so thu tu, tra ve ten chuan xac trong do thi
    while True:
        chuoi = input(thong_bao).strip()
        if not chuoi:
            print("[!] Ten dinh khong duoc de trong!")
            continue
        if chuoi.isdigit():
            idx = int(chuoi) - 1
            ten = dothi.get_node_name(idx)
            if ten is not None:
                return ten
        if dothi.get_node_index(chuoi) is not None:
            return chuoi
        print(f"[!] Dinh '{chuoi}' khong ton tai trong ban do! Vui long nhap lai.")

# Hoc phan: Cau truc du lieu va Giai thuat - Diem vao chuong trinh chinh (Main Entry Point)

import sys
import os

# Dam bao import duong dan dung bat ke chay tu dau
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.tienich.dulieu import khoi_tao_ban_do_mau_15_nut, to_json_string
from src.giaodien.nhaplieu import nhap_so_nguyen
from src.giaodien.menu import (
    xem_thong_tin_ban_do,
    tim_duong_dijkstra_mot_nguon,
    tim_duong_hai_diem,
    so_sanh_hai_thuat_toan,
    mo_phong_ket_xe,
    chay_benchmark_tu_dong
)

def in_menu_chinh() -> None:
    print("\n" + "=" * 65)
    print("   HE THONG TIM DUONG DI NGAN NHAT TREN BAN DO (DIJKSTRA & A*)")
    print("   Hoc phan: Cau truc du lieu va Giai thuat | DH Lac Hong")
    print("=" * 65)
    print(" 1. Xem thong tin ban do va danh sach dia diem")
    print(" 2. Tim duong tu 1 diem den tat ca dia diem (Dijkstra mot nguon)")
    print(" 3. Tim duong giua 2 dia diem (Chon Dijkstra hoac A*)")
    print(" 4. So sanh hieu nang Dijkstra vs A* tren cung cap dia diem")
    print(" 5. Mo phong ket xe dong (Nhan he so k tren tuyen duong)")
    print(" 6. Dat lai tat ca he so ket xe ve 1.0x (Binh thuong)")
    print(" 7. Kiem thu hieu nang tu dong (Benchmark 20 -> 2.000 dinh)")
    print(" 8. Xuat ban do ra chuoi JSON (Dong bo cho ung dung Web)")
    print(" 0. Thoat chuong trinh")
    print("=" * 65)

def dieu_phoi_chuong_trinh() -> None:
    # O(1) vong lap dieu phoi goi cac ham chuc nang rieng biet
    dothi = khoi_tao_ban_do_mau_15_nut()
    while True:
        in_menu_chinh()
        chon = nhap_so_nguyen("Chon chuc nang [0-8]: ", 0, 8)
        if chon == 1: xem_thong_tin_ban_do(dothi)
        elif chon == 2: tim_duong_dijkstra_mot_nguon(dothi)
        elif chon == 3: tim_duong_hai_diem(dothi)
        elif chon == 4: so_sanh_hai_thuat_toan(dothi)
        elif chon == 5: mo_phong_ket_xe(dothi)
        elif chon == 6:
            dothi.reset_all_traffic()
            print("[+] Da dat lai toan bo he so ket xe ve 1.0x!")
        elif chon == 7: chay_benchmark_tu_dong()
        elif chon == 8:
            print("\n--- CHUOI DU LIEU JSON CUA BAN DO ---")
            print(to_json_string(dothi.to_dict()))
        elif chon == 0:
            print("\nCam on ban da su dung chuong trinh! Tam biet.")
            break

if __name__ == "__main__":
    dieu_phoi_chuong_trinh()

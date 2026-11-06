# Hoc phan: Cau truc du lieu va Giai thuat - Cac chuc nang va vong lap Menu Console

from typing import Any
from ..thuattoan.dijkstra import dijkstra_shortest_path
from ..thuattoan.astar import astar_shortest_path
from ..thuattoan.lienthong import kiem_tra_lien_thong_bfs
from ..thuattoan.sapxep_timkiem import quicksort_khoang_cach
from ..tienich.dohieunang import do_thoi_gian_thuc_thi, chay_benchmark_mot_quy_mo
from ..tienich.dulieu import to_json_string, parse_json_string, khoi_tao_ban_do_mau_15_nut
from .nhaplieu import nhap_so_nguyen, nhap_so_thuc, nhap_ten_dinh
from .hienthi import in_tieu_de, in_lo_trinh_chi_tiet, in_bang_so_sanh_hai_thuat_toan

def xem_thong_tin_ban_do(dothi: Any) -> None:
    # O(V + E) in danh sach dinh va canh
    in_tieu_de("THONG TIN BAN DO THANH PHO")
    print(f"* Tong so dia diem (dinh): {dothi.num_nodes}")
    print(f"* Tong so tuyen duong (canh): {dothi.num_edges}")
    print("\n--- DANH SACH DIA DIEM ---")
    for i in range(dothi.num_nodes):
        ten = dothi.node_names[i]
        x, y = dothi.node_coords[i]
        print(f"[{i+1:02d}] {ten:<28} (x={x:5.1f} km, y={y:5.1f} km)")

def tim_duong_dijkstra_mot_nguon(dothi: Any) -> None:
    # O((V + E) log V) tim duong tu 1 diem den tat ca cac diem
    in_tieu_de("DIJKSTRA MOT NGUON DEN TAT CA CAC DIEM")
    start = nhap_ten_dinh("Nhap diem bat dau: ", dothi)
    res = dijkstra_shortest_path(dothi, start)
    if not res.success or not res.distances:
        print(f"[!] {res.message}")
        return
    arr = [(k, v) for k, v in res.distances.items()]
    quicksort_khoang_cach(arr)
    print(f"\nBang khoang cach tu '{start}' (Sap xep tang dan bang Quicksort):")
    for k, v in arr:
        val_str = "Khong the toi (inf)" if v == float("inf") else f"{v:.2f} km"
        print(f"  -> {k:<28}: {val_str}")

def tim_duong_hai_diem(dothi: Any) -> None:
    # O((V + E) log V) tim duong giua 2 diem bat ky bang Dijkstra hoac A*
    in_tieu_de("TIM DUONG DI NGAN NHAT GIUA HAI DIA DIEM")
    start = nhap_ten_dinh("Nhap diem bat dau: ", dothi)
    end = nhap_ten_dinh("Nhap diem ket thuc: ", dothi)
    chon = nhap_so_nguyen("Chon thuat toan (1: Dijkstra, 2: A*): ", 1, 2)
    if chon == 1:
        res = dijkstra_shortest_path(dothi, start, end)
        in_lo_trinh_chi_tiet("Dijkstra", res)
    else:
        res = astar_shortest_path(dothi, start, end)
        in_lo_trinh_chi_tiet("A*", res)

def so_sanh_hai_thuat_toan(dothi: Any) -> None:
    # O((V + E) log V) chay va so sanh chi tiet giua Dijkstra va A* tren cung cap nut
    in_tieu_de("SO SANH HIEU NANG DIJKSTRA VA A*")
    start = nhap_ten_dinh("Nhap diem bat dau: ", dothi)
    end = nhap_ten_dinh("Nhap diem ket thuc: ", dothi)

    res_d = dijkstra_shortest_path(dothi, start, end)
    res_a = astar_shortest_path(dothi, start, end)
    if not res_d.success or not res_a.success:
        print("[!] Khong the so sanh vi khong co duong di giua hai diem nay!")
        return

    t_d = do_thoi_gian_thuc_thi(lambda: dijkstra_shortest_path(dothi, start, end))
    t_a = do_thoi_gian_thuc_thi(lambda: astar_shortest_path(dothi, start, end))
    in_bang_so_sanh_hai_thuat_toan(res_d, res_a, t_d, t_a)

def mo_phong_ket_xe(dothi: Any) -> None:
    # O(E + (V+E)log V) tang trong so canh gia lap ket xe va tu dong doi huong
    in_tieu_de("MO PHONG KET XE DONG VA TU DONG DOI HUONG")
    u = nhap_ten_dinh("Nhap diem dau cua tuyen duong bi ket: ", dothi)
    v = nhap_ten_dinh("Nhap diem cuoi cua tuyen duong bi ket: ", dothi)
    k = nhap_so_thuc("Nhap he so ket xe k (k >= 1.0, vd 2.5): ", min_val=1.0)

    ok, msg = dothi.update_traffic(u, v, k)
    if not ok:
        print(f"[!] {msg}")
        return
    print(f"[+] Da cap nhat k={k:.1f}x tren tuyen duong {u} <-> {v}!")
    print("Moi ban chon chuc nang 3 hoac 4 de kiem tra lo trinh moi sau khi ket xe.")

def chay_benchmark_tu_dong() -> None:
    # O((V+E)log V) kiem thu stress-test tren 5 quy mo
    in_tieu_de("KIEM THU HIEU NANG TU DONG TREN NHIEU QUY MO")
    cac_quy_mo = [
        ("20 dinh", 4, 5),
        ("100 dinh", 10, 10),
        ("500 dinh", 20, 25),
        ("1.000 dinh", 20, 50),
        ("2.000 dinh", 40, 50)
    ]
    print(f"{'QUY MO':<12} | {'SO CANH':<8} | {'DIJKSTRA (NUT)':<15} | {'A* (NUT)':<12} | {'TIET KIEM':<12} | {'DIJK (ms)':<10} | {'A* (ms)':<10} | {'TRANG THAI'}")
    print("-" * 105)
    for ten, r, c in cac_quy_mo:
        res = chay_benchmark_mot_quy_mo(ten, r, c)
        print(f"{res['quy_mo']:<12} | {res['so_canh']:<8} | {res['dijk_nut']:<15} | {res['astar_nut']:<12} | -{res['nut_tiet_kiem']} ({res['ti_le_tiet_kiem']:.1f}%) | {res['dijk_time_ms']:<10.3f} | {res['astar_time_ms']:<10.3f} | {res['trang_thai']}")

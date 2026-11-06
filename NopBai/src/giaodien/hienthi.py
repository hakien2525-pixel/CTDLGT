# Hoc phan: Cau truc du lieu va Giai thuat - Dinh dang va in ket qua

from typing import List, Any
from ..thuattoan.duongdi import KetQuaTimDuong

def in_tieu_de(noi_dung: str) -> None:
    print("\n" + "=" * 70)
    print(f"   {noi_dung.upper()}")
    print("=" * 70)

def in_lo_trinh_chi_tiet(ten_giai_thuat: str, ket_qua: KetQuaTimDuong) -> None:
    # O(V) in chi tiet lo trinh chi phi va so thao tac
    print(f"\n--- KET QUA {ten_giai_thuat.upper()} ---")
    if not ket_qua.success:
        print(f"[!] {ket_qua.message}")
        return
    print(f"* Tong chi phi   : {ket_qua.total_cost:.2f} km")
    print(f"* So nut da duyet: {ket_qua.visited_count} nut")
    print(f"* So thao tac Heap: {ket_qua.heap_ops} lan")
    if ket_qua.path:
        print(f"* Lo trinh di qua: {' -> '.join(ket_qua.path)}")

def in_bang_so_sanh_hai_thuat_toan(res_d: KetQuaTimDuong, res_a: KetQuaTimDuong, t_d_ms: float, t_a_ms: float) -> None:
    # O(1) in bang so sanh chi tiet hai thuat toan
    print("\n" + "-" * 75)
    print(f"{'TIEU CHI SO SANH':<28} | {'DIJKSTRA':<20} | {'A* (EUCLID)':<20}")
    print("-" * 75)
    print(f"{'Tong chi phi (km)':<28} | {res_d.total_cost:<20.2f} | {res_a.total_cost:<20.2f}")
    print(f"{'So nut da duyet':<28} | {res_d.visited_count:<20} | {res_a.visited_count:<20}")
    print(f"{'So thao tac Heap':<28} | {res_d.heap_ops:<20} | {res_a.heap_ops:<20}")
    print(f"{'Thoi gian chay (ms)':<28} | {t_d_ms:<20.3f} | {t_a_ms:<20.3f}")
    print("-" * 75)

    lech_phi = abs(res_d.total_cost - res_a.total_cost)
    if lech_phi > 1e-9:
        print(f"[CANH BAO] Chi phi hai giai thuat khong khop! (Lech: {lech_phi:.6f})")
    else:
        print("[XAC NHAN] Chi phi toi uu cua Dijkstra va A* TRUNG KHOP 100%.")

    tiet_kiem = res_d.visited_count - res_a.visited_count
    pct = (tiet_kiem / res_d.visited_count * 100.0) if res_d.visited_count > 0 else 0.0
    print(f"[KET LUAN] A* tiet kiem duoc {tiet_kiem} nut duyet so voi Dijkstra (Giam {pct:.1f}%).")

# Hoc phan: Cau truc du lieu va Giai thuat - Kiem thu hieu nang quy mo lon (Stress Tests)

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.tienich.dohieunang import chay_benchmark_mot_quy_mo

def chay_kiem_thu_hieunang():
    print("Dang chay kiem thu hieu nang tren cac quy mo...")
    cac_quy_mo = [
        ("100 dinh", 10, 10),
        ("1.000 dinh", 20, 50),
        ("5.000 dinh", 50, 100),
        ("20.000 dinh", 100, 200)
    ]
    for ten, r, c in cac_quy_mo:
        res = chay_benchmark_mot_quy_mo(ten, r, c)
        print(f"[{res['trang_thai']}] {res['quy_mo']}: Dijkstra={res['dijk_time_ms']:.2f}ms ({res['dijk_nut']} nut), A*={res['astar_time_ms']:.2f}ms ({res['astar_nut']} nut)")
        assert res["trang_thai"] == "PASS", f"Benchmark {ten} that bai!"
    print("[PASS] Toan bo stress test hieu nang tu 100 den 20.000 dinh thanh cong!")

if __name__ == "__main__":
    chay_kiem_thu_hieunang()

# Hoc phan: Cau truc du lieu va Giai thuat - Kiem thu giai thuat Dijkstra va A*

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.cautruc.graph import CityMapGraph
from src.thuattoan.dijkstra import dijkstra_shortest_path
from src.thuattoan.astar import astar_shortest_path
from src.tienich.dulieu import khoi_tao_ban_do_mau_15_nut
from src.tienich.sinhdothi import sinh_do_thi_ngau_nhien_lien_thong, BoSinhSoNgauNhien

def test_tinh_tay():
    g = CityMapGraph()
    g.add_node("A", 0, 0); g.add_node("B", 2, 0); g.add_node("C", 3, 0); g.add_node("D", 4, 0)
    g.add_edge("A", "B", 2.0); g.add_edge("B", "C", 1.0); g.add_edge("C", "D", 1.0); g.add_edge("A", "D", 10.0)
    res = dijkstra_shortest_path(g, "A", "D")
    assert res.total_cost == 4.0 and res.path == ["A", "B", "C", "D"], "Chi phi tinh tay phai la 4.0"

def test_duong_mot_chieu():
    g = CityMapGraph()
    g.add_node("A", 0, 0); g.add_node("B", 5, 0)
    g.add_edge("A", "B", 5.0, 1.0, is_oneway=True)
    res_fw = dijkstra_shortest_path(g, "A", "B")
    res_bw = dijkstra_shortest_path(g, "B", "A")
    assert res_fw.total_cost == 5.0, "Di xuoi chieu thanh cong"
    assert not res_bw.success, "Di nguoc chieu bi tu choi an toan"

def test_dijkstra_vs_astar_admissible():
    g = khoi_tao_ban_do_mau_15_nut()
    res_d = dijkstra_shortest_path(g, "N1_VongXoayBenTre", "N15_CangGiaoNhanHang")
    res_a = astar_shortest_path(g, "N1_VongXoayBenTre", "N15_CangGiaoNhanHang")
    assert abs(res_d.total_cost - res_a.total_cost) < 1e-9, "Chi phi A* phai bang tuyet doi Dijkstra"
    assert res_a.visited_count <= res_d.visited_count, "A* khong duoc duyet nhieu nut hon Dijkstra"

def test_200_cap_ngau_nhien():
    g = sinh_do_thi_ngau_nhien_lien_thong(num_nodes=50, extra_edges=80, seed=123)
    rng = BoSinhSoNgauNhien(999)
    for _ in range(200):
        u = f"Node_{rng.next_int(1, 50)}"
        v = f"Node_{rng.next_int(1, 50)}"
        res_d = dijkstra_shortest_path(g, u, v)
        res_a = astar_shortest_path(g, u, v)
        assert abs(res_d.total_cost - res_a.total_cost) < 1e-9, f"Cap ({u}, {v}) bi lech chi phi!"

def chay_kiem_thu_thuattoan():
    test_tinh_tay()
    test_duong_mot_chieu()
    test_dijkstra_vs_astar_admissible()
    test_200_cap_ngau_nhien()
    print("[PASS] Toan bo kiem thu giai thuat (Dijkstra, A*, 1 chieu, 200 cap) thanh cong!")

if __name__ == "__main__":
    chay_kiem_thu_thuattoan()

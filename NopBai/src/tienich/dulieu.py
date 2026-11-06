# Hoc phan: Cau truc du lieu va Giai thuat - Nap va xuat ban do JSON / CSV

from typing import Any, Dict, List
from ..cautruc.graph import CityMapGraph

def to_json_string(obj: Any, indent: int = 2) -> str:
    # O(N) bo sinh chuoi JSON thuan khong import thu vien
    def _ser(o: Any, lvl: int) -> str:
        sp, spi = " " * (lvl * indent), " " * ((lvl + 1) * indent)
        if o is None: return "null"
        if isinstance(o, bool): return "true" if o else "false"
        if isinstance(o, float): return f"{o:.4f}"
        if isinstance(o, int): return str(o)
        if isinstance(o, str):
            return '"' + o.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n") + '"'
        if isinstance(o, list):
            if not o: return "[]"
            if all(isinstance(x, (int, float, str, bool)) for x in o) and len(o) <= 8:
                return "[" + ", ".join(_ser(x, 0) for x in o) + "]"
            return "[\n" + ",\n".join(spi + _ser(x, lvl + 1) for x in o) + "\n" + sp + "]"
        if isinstance(o, dict):
            if not o: return "{}"
            return "{\n" + ",\n".join(spi + f'"{k}": ' + _ser(v, lvl + 1) for k, v in o.items()) + "\n" + sp + "}"
        return f'"{str(o)}"'
    return _ser(obj, 0)

def parse_json_string(s: str) -> Any:
    # O(N) bo phan tich cu phap JSON thuan chay khong import thu vien
    idx, n = 0, len(s)
    def skip() -> None:
        nonlocal idx
        while idx < n and s[idx] in " \t\r\n": idx += 1
    def p_val() -> Any:
        skip()
        if idx >= n: return None
        c = s[idx]
        if c == '{': return p_obj()
        if c == '[': return p_arr()
        if c == '"': return p_str()
        if c in "0123456789-": return p_num()
        if s.startswith("true", idx): idx_adv(4); return True
        if s.startswith("false", idx): idx_adv(5); return False
        if s.startswith("null", idx): idx_adv(4); return None
        return None
    def idx_adv(k: int) -> None: nonlocal idx; idx += k
    def p_str() -> str:
        nonlocal idx
        idx += 1
        res = []
        while idx < n:
            c = s[idx]
            if c == '"': idx += 1; return "".join(res)
            if c == '\\':
                idx += 1
                if idx < n:
                    esc = s[idx]
                    res.append('\n' if esc == 'n' else '\r' if esc == 'r' else '\t' if esc == 't' else esc)
            else: res.append(c)
            idx += 1
        return "".join(res)
    def p_num() -> Any:
        nonlocal idx
        st = idx
        if s[idx] == '-': idx += 1
        while idx < n and s[idx] in "0123456789.eE+-": idx += 1
        v = s[st:idx]
        return float(v) if ('.' in v or 'e' in v or 'E' in v) else int(v)
    def p_arr() -> List[Any]:
        nonlocal idx
        idx += 1
        arr = []
        skip()
        if idx < n and s[idx] == ']': idx += 1; return arr
        while idx < n:
            arr.append(p_val())
            skip()
            if idx < n and s[idx] == ',': idx += 1
            elif idx < n and s[idx] == ']': idx += 1; break
        return arr
    def p_obj() -> Dict[str, Any]:
        nonlocal idx
        idx += 1
        obj: Dict[str, Any] = {}
        skip()
        if idx < n and s[idx] == '}': idx += 1; return obj
        while idx < n:
            skip()
            if s[idx] != '"': break
            k = p_str()
            skip()
            if idx < n and s[idx] == ':': idx += 1
            obj[k] = p_val()
            skip()
            if idx < n and s[idx] == ',': idx += 1
            elif idx < n and s[idx] == '}': idx += 1; break
        return obj
    return p_val()

def khoi_tao_ban_do_mau_15_nut() -> CityMapGraph:
    # O(V + E) khoi tao ban do thanh pho mau 15 giao lo voi toa do km chuan hoa
    g = CityMapGraph()
    nodes = [
        ("N1_VongXoayBenTre", 8.5, 10.2), ("N2_DaiLoDongKhoi", 22.1, 12.75), ("N3_ChoBenTre", 17.0, 29.75),
        ("N4_CauBenTre1", 35.7, 25.5), ("N5_CongVienMyHoa", 42.5, 12.75), ("N6_BenXeBenTre", 55.25, 21.25),
        ("N7_CauRachMieu", 29.75, 5.95), ("N8_UBNDThanhPho", 38.25, 38.25), ("N9_BenhVienNguyenDinhChieu", 52.7, 34.0),
        ("N10_KhuDanCuPhuKhuong", 66.3, 38.25), ("N11_SieuThiGo", 68.0, 17.0), ("N12_DaiHocLacHong_CS1", 25.5, 42.5),
        ("N13_CongVienSongNuoc", 10.2, 44.2), ("N14_TrungTamThuongMai", 47.6, 45.05), ("N15_CangGiaoNhanHang", 74.8, 44.2)
    ]
    for name, x, y in nodes: g.add_node(name, x, y)
    edges = [
        ("N1_VongXoayBenTre", "N2_DaiLoDongKhoi", 15.5, 1.0, False), ("N1_VongXoayBenTre", "N3_ChoBenTre", 26.0, 1.0, False),
        ("N1_VongXoayBenTre", "N7_CauRachMieu", 25.5, 1.0, False), ("N2_DaiLoDongKhoi", "N4_CauBenTre1", 21.0, 1.0, False),
        ("N2_DaiLoDongKhoi", "N5_CongVienMyHoa", 25.0, 1.0, False), ("N3_ChoBenTre", "N4_CauBenTre1", 20.5, 1.0, False),
        ("N3_ChoBenTre", "N12_DaiHocLacHong_CS1", 18.0, 1.0, True), ("N3_ChoBenTre", "N13_CongVienSongNuoc", 20.5, 1.0, False),
        ("N4_CauBenTre1", "N6_BenXeBenTre", 25.5, 1.0, False), ("N4_CauBenTre1", "N8_UBNDThanhPho", 16.0, 1.0, False),
        ("N5_CongVienMyHoa", "N6_BenXeBenTre", 18.0, 1.0, False), ("N5_CongVienMyHoa", "N7_CauRachMieu", 18.0, 1.0, False),
        ("N6_BenXeBenTre", "N11_SieuThiGo", 16.0, 1.0, False), ("N6_BenXeBenTre", "N9_BenhVienNguyenDinhChieu", 16.0, 1.0, True),
        ("N8_UBNDThanhPho", "N9_BenhVienNguyenDinhChieu", 16.0, 1.0, False), ("N8_UBNDThanhPho", "N14_TrungTamThuongMai", 18.0, 1.0, False),
        ("N9_BenhVienNguyenDinhChieu", "N10_KhuDanCuPhuKhuong", 16.0, 1.0, False), ("N10_KhuDanCuPhuKhuong", "N11_SieuThiGo", 25.5, 1.0, False),
        ("N10_KhuDanCuPhuKhuong", "N15_CangGiaoNhanHang", 14.0, 1.0, False), ("N12_DaiHocLacHong_CS1", "N8_UBNDThanhPho", 16.0, 1.0, True),
        ("N12_DaiHocLacHong_CS1", "N14_TrungTamThuongMai", 27.0, 1.0, False), ("N13_CongVienSongNuoc", "N12_DaiHocLacHong_CS1", 16.0, 1.0, False),
        ("N14_TrungTamThuongMai", "N15_CangGiaoNhanHang", 30.5, 1.0, False), ("N11_SieuThiGo", "N15_CangGiaoNhanHang", 35.5, 1.0, False)
    ]
    for u, v, w, tf, oneway in edges: g.add_edge(u, v, w, tf, oneway)
    return g

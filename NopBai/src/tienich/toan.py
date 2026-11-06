# Hoc phan: Cau truc du lieu va Giai thuat - Tien ich tinh toan so hoc

def tinh_can_bac_hai_newton(gia_tri: float) -> float:
    # O(log(1/eps)) tinh can bac hai bang phuong phap lap tiep tuyen Newton-Raphson
    if gia_tri <= 0.0:
        return 0.0
    x, eps = float(gia_tri), 1e-7
    while True:
        can = 0.5 * (x + gia_tri / x)
        if abs(can - x) < eps:
            return can
        x = can

def tinh_khoang_cach_euclid(x1: float, y1: float, x2: float, y2: float) -> float:
    # O(1) tinh khoang cach hinh hoc giua 2 toa do tren mat phang
    dx = x1 - x2
    dy = y1 - y2
    return tinh_can_bac_hai_newton(dx * dx + dy * dy)

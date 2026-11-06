# Hoc phan: Cau truc du lieu va Giai thuat - Chay toan bo bo kiem thu va xuat CSV

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from test.test_cautruc import chay_kiem_thu_cautruc
from test.test_thuattoan import chay_kiem_thu_thuattoan
from test.test_hieunang import chay_kiem_thu_hieunang
from test.test_suite import run_all_tests

if __name__ == "__main__":
    print("================================================================================")
    print("   CHAY TOAN BO BO KIEM THU MO-DUL HOA (REFACTORED AUTOMATED TEST SUITE)")
    print("================================================================================")
    chay_kiem_thu_cautruc()
    chay_kiem_thu_thuattoan()
    chay_kiem_thu_hieunang()
    print("\n--- CHAY BO KIEM THU TEST_SUITE GOC (26 TEST CASES) ---")
    run_all_tests()

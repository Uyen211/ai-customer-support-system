"""
Test Runner tổng hợp thực thi toàn bộ Test Suite cho Khối 1:
- TestCustomerAuth (Use Case 1.1: Đăng ký, Đăng nhập, Brute-force lockout, Profile)
- TestConversationManagement (Use Case 1.2: Quản lý phiên, Lời chào tự động, Lịch sử 50 tin nhắn, Đóng phiên)
- TestRAGPipeline (Use Case 1.3: RAG KH-06 Decomposer, SQL Retriever, Vector HNSW, OutOfDomain, SSE Stream)
"""

import unittest
import sys
import os

# Add backend directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tests.test_customer_auth import TestCustomerAuth
from tests.test_conversation import TestConversationManagement
from tests.test_staff_management import TestStaffAuth, TestStaffManagement

# Lưu ý: test_rag_pipeline.py phụ thuộc pytest (chưa có trong requirements.txt).
# Import có điều kiện nhằm không chặn toàn bộ Test Suite nếu thiếu pytest.
try:
    from tests.test_rag_pipeline import TestRAGPipeline
    HAS_RAG_TESTS = True
except (ImportError, NameError):
    HAS_RAG_TESTS = False

def suite():
    test_suite = unittest.TestSuite()
    
    # 1. Khối 1 - Use Case 1.1: Quản lý tài khoản khách hàng
    test_suite.addTest(unittest.makeSuite(TestCustomerAuth))
    
    # 2. Khối 1 - Use Case 1.2: Quản lý phiên trò chuyện
    test_suite.addTest(unittest.makeSuite(TestConversationManagement))
    
    # 3. Khối 1 - Use Case 1.3: Trợ lý RAG Chatbot KH-06 (nếu pytest khả dụng)
    if HAS_RAG_TESTS:
        test_suite.addTest(unittest.makeSuite(TestRAGPipeline))
    else:
        print("[SKIP] TestRAGPipeline bị bỏ qua do thiếu pytest (chỉ hiển thị khi chạy trực tiếp).")

    # 4. Khối 3 - Use Case 3.1 & 3.2: Tài khoản nhân viên & trạng thái làm việc
    test_suite.addTest(unittest.makeSuite(TestStaffAuth))
    test_suite.addTest(unittest.makeSuite(TestStaffManagement))
    
    return test_suite

if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite())
    if not result.wasSuccessful():
        sys.exit(1)

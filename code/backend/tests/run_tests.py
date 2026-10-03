"""
Test Runner tổng hợp thực thi toàn bộ Test Suite:
- TestCustomerAuth (Use Case 1.1: Đăng ký, Đăng nhập, Brute-force lockout, Profile)
- TestConversationManagement (Use Case 1.2 & 1.4: Quản lý phiên, Lời chào tự động, Lịch sử 50 tin nhắn, Đóng & Xóa phiên)
- TestRAGPipeline (Use Case 1.3: RAG KH-06 Decomposer, SQL Retriever, Vector HNSW, OutOfDomain, SSE Stream)
- TestStaffAuth & TestStaffManagement (Use Case 3.1 & 3.2: Quản trị nhân viên & Trạng thái làm việc)
- TestAgentConversations (Use Case 3.3: Hàng đợi & Tiếp quản hội thoại)
- TestCannedResponses (Use Case 3.4: Mẫu phản hồi nhanh)
"""

import unittest
import sys
import os

# Add backend directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tests.test_customer_auth import TestCustomerAuth
from tests.test_conversation import TestConversationManagement
from tests.test_rag_pipeline import TestRAGPipeline
from tests.test_staff_management import TestStaffAuth, TestStaffManagement
from tests.test_agent_conversations import TestAgentConversations
from tests.test_canned_responses import TestCannedResponses

def suite():
    test_suite = unittest.TestSuite()
    
    # 1. Khối 1 - Use Case 1.1: Quản lý tài khoản khách hàng
    test_suite.addTest(unittest.makeSuite(TestCustomerAuth))
    
    # 2. Khối 1 - Use Case 1.2 & 1.4: Quản lý & Xóa phiên trò chuyện
    test_suite.addTest(unittest.makeSuite(TestConversationManagement))
    
    # 3. Khối 1 - Use Case 1.3: Trợ lý RAG Chatbot KH-06
    test_suite.addTest(unittest.makeSuite(TestRAGPipeline))

    # 4. Khối 3 - Use Case 3.1 & 3.2: Tài khoản nhân viên & trạng thái làm việc
    test_suite.addTest(unittest.makeSuite(TestStaffAuth))
    test_suite.addTest(unittest.makeSuite(TestStaffManagement))

    # 5. Khối 3 - Use Case 3.3: Hàng đợi & tiếp quản cuộc trò chuyện
    test_suite.addTest(unittest.makeSuite(TestAgentConversations))

    # 6. Khối 3 - Use Case 3.4: Mẫu phản hồi nhanh
    test_suite.addTest(unittest.makeSuite(TestCannedResponses))

    return test_suite

if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite())
    if not result.wasSuccessful():
        sys.exit(1)

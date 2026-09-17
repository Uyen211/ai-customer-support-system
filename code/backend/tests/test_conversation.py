"""
Unit & Integration Tests for Conversation Management (Use Case 1.2).
Covers: Conversation List, New Conversation + Greeting, Message History (Lazy loading), and Closing Conversation.
"""

import unittest
import asyncio
import sys
import os
import uuid
from datetime import datetime, timezone
from unittest.mock import MagicMock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import httpx
from app.main import app
from app.models.customer import Customer
from app.models.conversation import Conversation
from app.models.message import Message
from app.core.security import create_access_token
from app.api.deps import get_db

class TestConversationManagement(unittest.TestCase):

    def setUp(self):
        self.customer_id = uuid.uuid4()
        self.customer = Customer(
            id=self.customer_id,
            email="chatuser@pethome.vn",
            full_name="Khách Hàng Chat",
            is_active=True
        )
        self.auth_token = create_access_token({
            "sub": str(self.customer_id),
            "email": "chatuser@pethome.vn",
            "role": "CUSTOMER"
        })
        self.headers = {"Authorization": f"Bearer {self.auth_token}"}

    def test_01_create_conversation_and_auto_greeting(self):
        """SPEC-1.4: Tạo cuộc trò chuyện mới và tự động gửi tin nhắn chào mừng mặc định của Bot."""
        mock_db = MagicMock()
        mock_db.query.return_value.filter.return_value.first.return_value = self.customer
        
        async def run():
            app.dependency_overrides[get_db] = lambda: mock_db
            try:
                async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
                    response = await ac.post("/api/conversations", headers=self.headers)
                    self.assertEqual(response.status_code, 201)
                    data = response.json()
                    
                    self.assertIn("conversation", data)
                    self.assertIn("initial_message", data)
                    self.assertEqual(data["conversation"]["mode"], "BOT")
                    self.assertEqual(data["initial_message"]["sender_type"], "BOT")
                    self.assertIn("Xin chào! Mình là Trợ lý tư vấn PetHome", data["initial_message"]["content"])
            finally:
                app.dependency_overrides.clear()

        asyncio.run(run())

    def test_02_list_conversations_with_snippets(self):
        """SPEC-1.5: Lấy danh sách phiên chat kèm tóm tắt tin nhắn cuối và trạng thái."""
        conv_id = uuid.uuid4()
        conv = Conversation(
            id=conv_id,
            customer_id=self.customer_id,
            mode="BOT",
            is_flagged=False,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        
        msg = Message(
            id=uuid.uuid4(),
            conversation_id=conv_id,
            sender_type="BOT",
            content="PetHome xin chào quý khách!",
            created_at=datetime.now(timezone.utc)
        )

        mock_db = MagicMock()
        # Mock auth customer query
        def query_side_effect(model):
            mock_q = MagicMock()
            if model == Customer:
                mock_q.filter.return_value.first.return_value = self.customer
            elif model == Conversation:
                mock_q.filter.return_value.order_by.return_value.all.return_value = [conv]
            elif model == Message:
                mock_q.filter.return_value.order_by.return_value.first.return_value = msg
            return mock_q

        mock_db.query.side_effect = query_side_effect

        async def run():
            app.dependency_overrides[get_db] = lambda: mock_db
            try:
                async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
                    response = await ac.get("/api/conversations", headers=self.headers)
                    self.assertEqual(response.status_code, 200)
                    data = response.json()
                    self.assertEqual(len(data), 1)
                    self.assertEqual(data[0]["mode"], "BOT")
                    self.assertEqual(data[0]["last_message_content"], "PetHome xin chào quý khách!")
            finally:
                app.dependency_overrides.clear()

        asyncio.run(run())

    def test_03_get_conversation_messages_lazy_loading(self):
        """SPEC-1.6: Lấy 50 tin nhắn của phiên chat (Lazy Loading) kèm trích dẫn."""
        conv_id = uuid.uuid4()
        conv = Conversation(
            id=conv_id,
            customer_id=self.customer_id,
            mode="BOT",
            is_flagged=False
        )

        messages = [
            Message(
                id=uuid.uuid4(),
                conversation_id=conv_id,
                sender_type="CUSTOMER",
                content=f"Câu hỏi số {i}",
                created_at=datetime.now(timezone.utc)
            ) for i in range(10)
        ]

        mock_db = MagicMock()
        def query_side_effect(model):
            mock_q = MagicMock()
            if model == Customer:
                mock_q.filter.return_value.first.return_value = self.customer
            elif model == Conversation:
                mock_q.filter.return_value.first.return_value = conv
            elif model == Message:
                mock_q.filter.return_value.count.return_value = 10
                mock_q.filter.return_value.order_by.return_value.limit.return_value.all.return_value = list(reversed(messages))
            return mock_q

        mock_db.query.side_effect = query_side_effect

        async def run():
            app.dependency_overrides[get_db] = lambda: mock_db
            try:
                async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
                    response = await ac.get(f"/api/conversations/{conv_id}/messages?limit=50", headers=self.headers)
                    self.assertEqual(response.status_code, 200)
                    data = response.json()
                    self.assertEqual(data["total"], 10)
                    self.assertEqual(len(data["messages"]), 10)
                    self.assertFalse(data["has_more"])
            finally:
                app.dependency_overrides.clear()

        asyncio.run(run())

    def test_04_close_conversation(self):
        """SPEC-1.7: Đóng phiên trò chuyện chuyển mode sang CLOSED."""
        conv_id = uuid.uuid4()
        conv = Conversation(
            id=conv_id,
            customer_id=self.customer_id,
            mode="BOT",
            is_flagged=False
        )

        mock_db = MagicMock()
        def query_side_effect(model):
            mock_q = MagicMock()
            if model == Customer:
                mock_q.filter.return_value.first.return_value = self.customer
            elif model == Conversation:
                mock_q.filter.return_value.first.return_value = conv
            return mock_q

        mock_db.query.side_effect = query_side_effect

        async def run():
            app.dependency_overrides[get_db] = lambda: mock_db
            try:
                async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
                    response = await ac.post(f"/api/conversations/{conv_id}/close", headers=self.headers)
                    self.assertEqual(response.status_code, 200)
                    data = response.json()
                    self.assertEqual(data["status"], "success")
                    self.assertEqual(data["mode"], "CLOSED")
                    self.assertEqual(conv.mode, "CLOSED")
            finally:
                app.dependency_overrides.clear()

        asyncio.run(run())

if __name__ == "__main__":
    unittest.main()

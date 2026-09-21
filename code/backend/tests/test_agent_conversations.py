"""
Integration & Unit Tests for UC 3.3 — Agent Live Console:
Hàng đợi hội thoại, tiếp quản cuộc trò chuyện (khóa FOR UPDATE, 409 conflict),
xem lịch sử tin nhắn trước/sau tiếp quản, gửi tin nhắn AGENT.
"""

import unittest
import asyncio
import sys
import os
import uuid
from datetime import datetime, timezone
from unittest.mock import patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import httpx
from fastapi import HTTPException

from app.main import app
from app.models.user import User
from app.core.security import get_password_hash, create_access_token
from app.api.deps import get_db
from app.schemas.conversation import (
    ConversationQueueItemSchema,
    ConversationDetailSchema,
    ConversationMessagesListResponse,
    MessageItemSchema,
    AgentSendMessageResponse,
)
from app.services.conversation_service import ConversationService


def _make_user(role="AGENT", id=None):
    return User(
        id=id or uuid.uuid4(),
        email=f"{role.lower()}@{role.lower()}.vn",
        password_hash=get_password_hash("Password1"),
        full_name="Nhân Viên Test",
        phone="0912345678",
        role=role,
        status="ONLINE",
        skills=["ALL"] if role in ("ADMIN", "MANAGER") else ["Đổi trả"],
        is_active=True,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )


def _db_returns(user):
    """MagicMock cho get_current_user: query(User).filter().first() trả về user."""
    mock_db = unittest.mock.MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = user
    return mock_db


def _run_with_auth(assert_fn, user):
    mock_db = _db_returns(user)

    async def _runner():
        app.dependency_overrides[get_db] = lambda: mock_db
        try:
            async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
                await assert_fn(ac)
        finally:
            app.dependency_overrides.clear()

    asyncio.run(_runner())


def _make_queue_item(**kwargs):
    now = datetime.now(timezone.utc)
    data = {
        "id": uuid.uuid4(),
        "customer_id": uuid.uuid4(),
        "mode": "WAITING_HUMAN",
        "is_flagged": True,
        "created_at": now,
        "updated_at": now,
    }
    data.update(kwargs)
    return ConversationQueueItemSchema(**data)


def _make_detail(conversation_id=None, **kwargs):
    now = datetime.now(timezone.utc)
    data = {
        "id": conversation_id or uuid.uuid4(),
        "customer_id": uuid.uuid4(),
        "mode": "HUMAN",
        "is_flagged": False,
        "created_at": now,
        "updated_at": now,
    }
    data.update(kwargs)
    return ConversationDetailSchema(**data)


class TestAgentConversations(unittest.TestCase):

    def test_01_queue_requires_auth(self):
        """UC 3.3 E: Không có token -> 401."""
        async def run():
            async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
                res = await ac.get("/api/agent/conversations/queue")
                self.assertEqual(res.status_code, 401)
        asyncio.run(run())

    def test_02_customer_cannot_access_queue(self):
        """UC 3.3 Quyền: Token CUSTOMER bị từ chối -> 401."""
        customer_token = create_access_token({"sub": str(uuid.uuid4()), "email": "khach@pethome.vn", "role": "CUSTOMER"})

        async def run():
            async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
                res = await ac.get("/api/agent/conversations/queue", headers={"Authorization": f"Bearer {customer_token}"})
                self.assertEqual(res.status_code, 401)
        asyncio.run(run())

    def test_03_queue_returns_flagged_items(self):
        """UC 3.3 B-1/B-2: Nhân viên xem hàng đợi -> danh sách hội thoại cờ đỏ/WAITING_HUMAN."""
        agent = _make_user("AGENT")
        token = create_access_token({"sub": str(agent.id), "email": agent.email, "role": "STAFF"})
        items = [_make_queue_item(customer_name="Nguyễn Văn A", last_message_content="Xin lỗi bạn...")]

        with patch.object(ConversationService, "get_agent_queue", return_value=items):
            async def assert_fn(ac):
                res = await ac.get("/api/agent/conversations/queue", headers={"Authorization": f"Bearer {token}"})
                self.assertEqual(res.status_code, 200)
                data = res.json()
                self.assertIsInstance(data, list)
                self.assertEqual(len(data), 1)
                self.assertEqual(data[0]["mode"], "WAITING_HUMAN")
                self.assertTrue(data[0]["is_flagged"])

            _run_with_auth(assert_fn, agent)

    def test_04_takeover_conflict_409(self):
        """UC 3.3 E-1: Hội thoại đã bị nhân viên khác tiếp quản -> 409."""
        agent = _make_user("AGENT")
        token = create_access_token({"sub": str(agent.id), "email": agent.email, "role": "STAFF"})
        conv_id = uuid.uuid4()

        def _conflict(*args, **kwargs):
            raise HTTPException(status_code=409, detail="Cuộc trò chuyện này đã được nhân viên Nguyễn Văn A tiếp quản.")

        with patch.object(ConversationService, "take_over_conversation", new=_conflict):
            async def assert_fn(ac):
                res = await ac.post(
                    f"/api/agent/conversations/{conv_id}/takeover",
                    headers={"Authorization": f"Bearer {token}"},
                )
                self.assertEqual(res.status_code, 409)
                self.assertIn("Nguyễn Văn A", res.json()["detail"])

            _run_with_auth(assert_fn, agent)

    def test_05_takeover_success(self):
        """UC 3.3 B-3 → C-3: Tiếp quản thành công -> mode HUMAN + thông tin nhân viên."""
        agent = _make_user("AGENT")
        token = create_access_token({"sub": str(agent.id), "email": agent.email, "role": "STAFF"})
        conv = _make_detail(mode="HUMAN", assigned_agent_id=agent.id)

        with patch.object(ConversationService, "take_over_conversation", return_value=conv):
            async def assert_fn(ac):
                res = await ac.post(
                    f"/api/agent/conversations/{conv.id}/takeover",
                    headers={"Authorization": f"Bearer {token}"},
                )
                self.assertEqual(res.status_code, 200)
                data = res.json()
                self.assertEqual(data["mode"], "HUMAN")
                self.assertEqual(data["assigned_agent_id"], str(agent.id))

            _run_with_auth(assert_fn, agent)

    def test_06_messages_endpoint(self):
        """UC 3.3 C-1: Nhân viên xem lịch sử tin nhắn trước khi tiếp quản."""
        agent = _make_user("AGENT")
        token = create_access_token({"sub": str(agent.id), "email": agent.email, "role": "STAFF"})
        conv_id = uuid.uuid4()
        now = datetime.now(timezone.utc)
        payload = ConversationMessagesListResponse(
            conversation_id=conv_id,
            mode="WAITING_HUMAN",
            is_flagged=True,
            messages=[
                MessageItemSchema(id=uuid.uuid4(), conversation_id=conv_id, sender_type="CUSTOMER", content="Tôi cần hỗ trợ", created_at=now),
                MessageItemSchema(id=uuid.uuid4(), conversation_id=conv_id, sender_type="BOT", content="Xin lỗi bạn...", created_at=now),
            ],
            total=2,
            has_more=False,
        )

        with patch.object(ConversationService, "get_conversation_messages_for_agent", return_value=payload):
            async def assert_fn(ac):
                res = await ac.get(
                    f"/api/agent/conversations/{conv_id}/messages",
                    headers={"Authorization": f"Bearer {token}"},
                )
                self.assertEqual(res.status_code, 200)
                data = res.json()
                self.assertEqual(data["total"], 2)
                self.assertEqual(data["messages"][0]["sender_type"], "CUSTOMER")

            _run_with_auth(assert_fn, agent)

    def test_07_send_agent_message(self):
        """UC 3.3 D-1: Nhân viên gửi tin nhắn -> lưu sender_type=AGENT."""
        agent = _make_user("AGENT")
        token = create_access_token({"sub": str(agent.id), "email": agent.email, "role": "STAFF"})
        conv_id = uuid.uuid4()
        now = datetime.now(timezone.utc)
        payload = AgentSendMessageResponse(
            message=MessageItemSchema(
                id=uuid.uuid4(),
                conversation_id=conv_id,
                sender_type="AGENT",
                sender_id=agent.id,
                content="Chào bạn, tôi sẽ hỗ trợ bạn ngay.",
                created_at=now,
            )
        )

        with patch.object(ConversationService, "send_agent_message", return_value=payload):
            async def assert_fn(ac):
                res = await ac.post(
                    f"/api/agent/conversations/{conv_id}/messages",
                    headers={"Authorization": f"Bearer {token}"},
                    json={"content": "Chào bạn, tôi sẽ hỗ trợ bạn ngay."},
                )
                self.assertEqual(res.status_code, 201)
                data = res.json()
                self.assertEqual(data["message"]["sender_type"], "AGENT")

            _run_with_auth(assert_fn, agent)

    def test_08_send_message_empty_content_422(self):
        """UC 3.3 E: Nội dung rỗng -> 422."""
        agent = _make_user("AGENT")
        token = create_access_token({"sub": str(agent.id), "email": agent.email, "role": "STAFF"})
        conv_id = uuid.uuid4()

        async def assert_fn(ac):
            res = await ac.post(
                f"/api/agent/conversations/{conv_id}/messages",
                headers={"Authorization": f"Bearer {token}"},
                json={"content": ""},
            )
            self.assertEqual(res.status_code, 422)

        _run_with_auth(assert_fn, agent)

    def test_09_service_takeover_conflict_logic(self):
        """UC 3.3 E-1 (logic service): với_for_update + chặn tranh chấp -> 409."""
        db = unittest.mock.MagicMock()
        conversation = unittest.mock.MagicMock()
        conversation.id = uuid.uuid4()
        conversation.assigned_agent_id = uuid.uuid4()  # đã có nhân viên khác
        db.query.return_value.filter.return_value.with_for_update.return_value.first.return_value = conversation

        agent = _make_user("AGENT")
        with self.assertRaises(HTTPException) as ctx:
            ConversationService.take_over_conversation(db=db, conversation_id=conversation.id, user=agent)
        self.assertEqual(ctx.exception.status_code, 409)

    def test_11_service_takeover_conflict_detail_has_agent_name(self):
        """UC 3.3 E-1: 409 detail phải chứa họ tên nhân viên đã tiếp quản phiên."""
        from app.models.conversation import Conversation

        conversation = unittest.mock.MagicMock()
        conversation.id = uuid.uuid4()
        conversation.assigned_agent_id = uuid.uuid4()

        conv_query = unittest.mock.MagicMock()
        conv_query.filter.return_value.with_for_update.return_value.first.return_value = conversation

        assigned_user = _make_user("AGENT", id=conversation.assigned_agent_id)
        assigned_user.full_name = "Trần Thị Khác"
        user_query = unittest.mock.MagicMock()
        user_query.filter.return_value.first.return_value = assigned_user

        db = unittest.mock.MagicMock()

        def _side_effect(entity):
            if entity is Conversation:
                return conv_query
            return user_query

        db.query.side_effect = _side_effect

        agent = _make_user("AGENT")
        with self.assertRaises(HTTPException) as ctx:
            ConversationService.take_over_conversation(db=db, conversation_id=conversation.id, user=agent)
        self.assertEqual(ctx.exception.status_code, 409)
        self.assertIn("Trần Thị Khác", ctx.exception.detail)

    def test_10_service_agent_can_access_rules(self):
        """UC 3.3 Quyền (logic service): AGENT chỉ truy cập phiên của mình / phiên chưa nhận trong hàng đợi."""
        agent = _make_user("AGENT")
        other = _make_user("AGENT")

        conv_my = unittest.mock.MagicMock(assigned_agent_id=agent.id, is_flagged=False, mode="HUMAN")
        conv_free = unittest.mock.MagicMock(assigned_agent_id=None, is_flagged=True, mode="WAITING_HUMAN")
        conv_other = unittest.mock.MagicMock(assigned_agent_id=other.id, is_flagged=True, mode="HUMAN")

        self.assertTrue(ConversationService._agent_can_access(conv_my, agent))
        self.assertTrue(ConversationService._agent_can_access(conv_free, agent))
        self.assertFalse(ConversationService._agent_can_access(conv_other, agent))
        self.assertFalse(ConversationService._agent_can_access(None, agent))


if __name__ == "__main__":
    unittest.main()
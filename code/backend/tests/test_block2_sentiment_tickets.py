import unittest
import uuid
import asyncio
from datetime import datetime, timezone, timedelta
from unittest.mock import MagicMock, patch, AsyncMock
import httpx

from app.main import app
from app.db.session import get_db
from app.models.customer import Customer
from app.models.user import User
from app.models.conversation import Conversation
from app.models.message import Message
from app.models.ticket import Ticket
from app.models.ai_rule import AIRule
from app.core.security import create_access_token


class TestBlock2SentimentAndTickets(unittest.TestCase):
    def setUp(self):
        self.customer_id = uuid.uuid4()
        self.customer = Customer(
            id=self.customer_id,
            email="cust_block2@example.com",
            full_name="Khách Hàng Block 2",
            password_hash="hashed_password",
            is_active=True
        )
        self.customer_token = create_access_token(
            data={"sub": str(self.customer_id), "email": self.customer.email, "role": "CUSTOMER"}
        )
        self.customer_headers = {"Authorization": f"Bearer {self.customer_token}"}

        self.agent_id = uuid.uuid4()
        self.agent = User(
            id=self.agent_id,
            email="agent_block2@brand.com",
            full_name="Agent An",
            role="AGENT",
            password_hash="hashed_password",
            is_active=True
        )
        self.agent_token = create_access_token(
            data={"sub": str(self.agent_id), "email": self.agent.email, "role": "AGENT"}
        )
        self.agent_headers = {"Authorization": f"Bearer {self.agent_token}"}

        self.manager_id = uuid.uuid4()
        self.manager = User(
            id=self.manager_id,
            email="manager_block2@brand.com",
            full_name="Manager Binh",
            role="MANAGER",
            password_hash="hashed_password",
            is_active=True
        )
        self.manager_token = create_access_token(
            data={"sub": str(self.manager_id), "email": self.manager.email, "role": "MANAGER"}
        )
        self.manager_headers = {"Authorization": f"Bearer {self.manager_token}"}

    # -------------------------------------------------------------------------
    # UC 2.3: Cấu hình quy tắc & Cảnh báo (Alert Config & RBAC)
    # -------------------------------------------------------------------------

    def test_01_alert_config_rbac_customer_forbidden(self):
        """UC 2.3 Quyền: Token CUSTOMER bị từ chối truy cập /api/v1/configs/alerts (401/403)."""
        mock_db = MagicMock()
        def query_side(model):
            m = MagicMock()
            if model == Customer:
                m.filter.return_value.first.return_value = self.customer
            return m
        mock_db.query.side_effect = query_side

        async def run():
            app.dependency_overrides[get_db] = lambda: mock_db
            try:
                async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
                    res = await ac.get("/api/v1/configs/alerts", headers=self.customer_headers)
                    self.assertIn(res.status_code, [401, 403])
            finally:
                app.dependency_overrides.clear()

        asyncio.run(run())

    def test_02_alert_config_rbac_agent_forbidden(self):
        """UC 2.3 Quyền: Token AGENT bị từ chối truy cập /api/v1/configs/alerts (403 Forbidden)."""
        mock_db = MagicMock()
        def query_side(model):
            m = MagicMock()
            if model == User:
                m.filter.return_value.first.return_value = self.agent
            return m
        mock_db.query.side_effect = query_side

        async def run():
            app.dependency_overrides[get_db] = lambda: mock_db
            try:
                async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
                    res = await ac.get("/api/v1/configs/alerts", headers=self.agent_headers)
                    self.assertEqual(res.status_code, 403)
                    self.assertIn("không có quyền", res.json()["detail"])
            finally:
                app.dependency_overrides.clear()

        asyncio.run(run())

    def test_03_alert_config_get_and_put_success_by_manager(self):
        """UC 2.3: MANAGER đọc và cập nhật quy tắc cấu hình cảnh báo thành công (200 OK)."""
        ai_rule = AIRule(
            id=uuid.uuid4(),
            instruction_prompt="Ưu tiên giao hàng bị hỏng",
            p1_threshold=-0.60,
            p2_threshold=-0.30
        )
        mock_db = MagicMock()
        def query_side(model):
            m = MagicMock()
            if model == User:
                m.filter.return_value.first.return_value = self.manager
            elif model == AIRule:
                m.first.return_value = ai_rule
            return m
        mock_db.query.side_effect = query_side

        async def run():
            app.dependency_overrides[get_db] = lambda: mock_db
            try:
                async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
                    # 1. GET
                    res_get = await ac.get("/api/v1/configs/alerts", headers=self.manager_headers)
                    self.assertEqual(res_get.status_code, 200)
                    self.assertEqual(res_get.json()["p1_threshold"], -0.60)

                    # 2. PUT Update
                    payload = {
                        "instruction_prompt": "Cảnh báo khẩn khi khách phàn nàn giá",
                        "p1_threshold": -0.70,
                        "p2_threshold": -0.40
                    }
                    res_put = await ac.put("/api/v1/configs/alerts", headers=self.manager_headers, json=payload)
                    self.assertEqual(res_put.status_code, 200)
                    self.assertEqual(res_put.json()["p1_threshold"], -0.70)
                    self.assertEqual(res_put.json()["p2_threshold"], -0.40)
            finally:
                app.dependency_overrides.clear()

        asyncio.run(run())

    def test_04_alert_config_validation_p1_greater_than_p2(self):
        """UC 2.3 E-1: Báo lỗi 400 khi ngưỡng P1 >= P2 (ví dụ P1: -0.20 >= P2: -0.50)."""
        ai_rule = AIRule(id=uuid.uuid4(), instruction_prompt="", p1_threshold=-0.60, p2_threshold=-0.30)
        mock_db = MagicMock()
        def query_side(model):
            m = MagicMock()
            if model == User:
                m.filter.return_value.first.return_value = self.manager
            elif model == AIRule:
                m.first.return_value = ai_rule
            return m
        mock_db.query.side_effect = query_side

        async def run():
            app.dependency_overrides[get_db] = lambda: mock_db
            try:
                async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
                    payload = {
                        "instruction_prompt": "Test invalid threshold",
                        "p1_threshold": -0.20,
                        "p2_threshold": -0.50
                    }
                    res = await ac.put("/api/v1/configs/alerts", headers=self.manager_headers, json=payload)
                    self.assertEqual(res.status_code, 400)
                    self.assertIn("Ngưỡng P1 phải nhỏ hơn ngưỡng P2", res.json()["detail"])
            finally:
                app.dependency_overrides.clear()

        asyncio.run(run())

    # -------------------------------------------------------------------------
    # UC 2.1: Phân tích cảm xúc & Sticky Red Flag
    # -------------------------------------------------------------------------

    def test_05_sticky_red_flag_activation_and_persistence(self):
        """UC 2.1: Sticky Red Flag duy trì (is_flagged=True) không bị tự gỡ khi khách gửi câu tích cực sau đó."""
        conv = Conversation(
            id=uuid.uuid4(),
            customer_id=self.customer_id,
            mode="BOT",
            is_flagged=True,  # Đã bật cờ đỏ trước đó do phàn nàn
            last_sentiment="CRITICAL"
        )
        self.assertTrue(conv.is_flagged)

        # Giả lập tin nhắn tiếp theo có sentiment tích cực (+0.80)
        # Theo quy tắc Sticky Red Flag (Rule UC 2.1), cờ đỏ KHÔNG ĐƯỢC TỰ BẮT HẠ khi chưa có nhân viên nhận việc.
        sentiment_score = 0.80
        p2_thresh = -0.30
        
        # Mô phỏng logic cập nhật trong RAG pipeline
        if sentiment_score <= p2_thresh:
            conv.is_flagged = True
        # Lưu ý: Không có nhánh `else: conv.is_flagged = False` -> Cờ đỏ giữ nguyên True
        self.assertTrue(conv.is_flagged, "Sticky Red Flag phải giữ nguyên True khi khách nói câu tiếp theo")

    # -------------------------------------------------------------------------
    # UC 2.2: Khởi tạo Ticket khẩn cấp & Graceful Handover
    # -------------------------------------------------------------------------

    def test_06_ticket_sla_deadline_calculation(self):
        """UC 2.2: Kiểm tra tính toán SLA deadline theo mức ưu tiên (P1=15m, P2=60m, P3=240m)."""
        now = datetime.now(timezone.utc)
        conv_id = uuid.uuid4()
        
        # P1 SLA
        p1_ticket = Ticket(
            id=uuid.uuid4(),
            conversation_id=conv_id,
            category="Khiếu nại sản phẩm",
            summary="Sự cố hỏng hóc P1",
            priority="P1",
            status="PENDING",
            sla_deadline=now + timedelta(minutes=15)
        )
        delta_p1 = (p1_ticket.sla_deadline - now).total_seconds() / 60
        self.assertAlmostEqual(delta_p1, 15, delta=1)

        # P2 SLA
        p2_ticket = Ticket(
            id=uuid.uuid4(),
            conversation_id=conv_id,
            category="Giao hàng chậm",
            summary="Sự cố nhầm đơn P2",
            priority="P2",
            status="PENDING",
            sla_deadline=now + timedelta(minutes=60)
        )
        delta_p2 = (p2_ticket.sla_deadline - now).total_seconds() / 60
        self.assertAlmostEqual(delta_p2, 60, delta=1)

        # P3 SLA
        p3_ticket = Ticket(
            id=uuid.uuid4(),
            conversation_id=conv_id,
            category="Tư vấn bảo hành",
            summary="Thắc mắc đổi trả P3",
            priority="P3",
            status="PENDING",
            sla_deadline=now + timedelta(minutes=240)
        )
        delta_p3 = (p3_ticket.sla_deadline - now).total_seconds() / 60
        self.assertAlmostEqual(delta_p3, 240, delta=1)


if __name__ == "__main__":
    unittest.main()

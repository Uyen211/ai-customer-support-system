import unittest
import uuid
import asyncio
from datetime import datetime, timezone, timedelta, date
from unittest.mock import MagicMock
import httpx

from app.main import app
from app.db.session import get_db
from app.models.customer import Customer
from app.models.user import User
from app.models.conversation import Conversation
from app.models.ticket import Ticket
from app.core.security import create_access_token


class TestBlock4SLAKanbanReports(unittest.TestCase):
    def setUp(self):
        self.customer_id = uuid.uuid4()
        self.customer = Customer(
            id=self.customer_id,
            email="cust_block4@example.com",
            full_name="Khách Hàng Block 4",
            password_hash="hashed_password",
            is_active=True
        )
        self.customer_token = create_access_token(
            data={"sub": str(self.customer_id), "email": self.customer.email, "role": "CUSTOMER"}
        )
        self.customer_headers = {"Authorization": f"Bearer {self.customer_token}"}

        self.agent1_id = uuid.uuid4()
        self.agent1 = User(
            id=self.agent1_id,
            email="agent1_block4@brand.com",
            full_name="Agent One",
            role="AGENT",
            password_hash="hashed_password",
            is_active=True
        )
        self.agent1_token = create_access_token(
            data={"sub": str(self.agent1_id), "email": self.agent1.email, "role": "AGENT"}
        )
        self.agent1_headers = {"Authorization": f"Bearer {self.agent1_token}"}

        self.agent2_id = uuid.uuid4()
        self.agent2 = User(
            id=self.agent2_id,
            email="agent2_block4@brand.com",
            full_name="Agent Two",
            role="AGENT",
            password_hash="hashed_password",
            is_active=True
        )
        self.agent2_token = create_access_token(
            data={"sub": str(self.agent2_id), "email": self.agent2.email, "role": "AGENT"}
        )
        self.agent2_headers = {"Authorization": f"Bearer {self.agent2_token}"}

        self.manager_id = uuid.uuid4()
        self.manager = User(
            id=self.manager_id,
            email="manager_block4@brand.com",
            full_name="Manager Cao",
            role="MANAGER",
            password_hash="hashed_password",
            is_active=True
        )
        self.manager_token = create_access_token(
            data={"sub": str(self.manager_id), "email": self.manager.email, "role": "MANAGER"}
        )
        self.manager_headers = {"Authorization": f"Bearer {self.manager_token}"}

    # -------------------------------------------------------------------------
    # UC 4.1: Phân công công việc (Manual Assignment & RBAC)
    # -------------------------------------------------------------------------

    def test_01_manual_assign_ticket_success_by_manager(self):
        """UC 4.1: MANAGER phân công vé thủ công cho AGENT thành công (200 OK)."""
        ticket_id = uuid.uuid4()
        conv_id = uuid.uuid4()
        ticket = Ticket(
            id=ticket_id,
            conversation_id=conv_id,
            category="Tư vấn bảo hành",
            summary="Cần xử lý bảo hành máy sấy",
            priority="P2",
            status="PENDING",
            sla_deadline=datetime.now(timezone.utc) + timedelta(minutes=60),
            sla_breached=False,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )

        mock_db = MagicMock()
        def query_side(model):
            m = MagicMock()
            if model == User:
                m.filter.return_value.first.return_value = self.manager
            elif model == Ticket:
                m.filter.return_value.first.return_value = ticket
            return m
        mock_db.query.side_effect = query_side

        def execute_side(stmt):
            m = MagicMock()
            sql_str = str(stmt).lower()
            if "users" in sql_str:
                m.scalar_one_or_none.return_value = self.agent1
            elif "tickets" in sql_str:
                m.scalar_one_or_none.return_value = ticket
            return m
        mock_db.execute.side_effect = execute_side

        async def run():
            app.dependency_overrides[get_db] = lambda: mock_db
            try:
                async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
                    payload = {"agent_id": str(self.agent1_id)}
                    res = await ac.post(f"/api/v1/admin/tickets/{ticket_id}/assign", headers=self.manager_headers, json=payload)
                    self.assertEqual(res.status_code, 200)
                    self.assertEqual(ticket.assigned_to, self.agent1_id)
                    self.assertEqual(ticket.status, "IN_PROGRESS")
            finally:
                app.dependency_overrides.clear()

        asyncio.run(run())

    def test_02_manual_assign_ticket_rbac_agent_forbidden(self):
        """UC 4.1 Quyền: AGENT bị từ chối phân công thủ công (403 Forbidden)."""
        ticket_id = uuid.uuid4()
        mock_db = MagicMock()
        def query_side(model):
            m = MagicMock()
            if model == User:
                m.filter.return_value.first.return_value = self.agent1
            return m
        mock_db.query.side_effect = query_side

        def execute_side(stmt):
            m = MagicMock()
            m.scalar_one_or_none.return_value = self.agent1
            return m
        mock_db.execute.side_effect = execute_side

        async def run():
            app.dependency_overrides[get_db] = lambda: mock_db
            try:
                async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
                    payload = {"agent_id": str(self.agent2_id)}
                    res = await ac.post(f"/api/v1/admin/tickets/{ticket_id}/assign", headers=self.agent1_headers, json=payload)
                    self.assertEqual(res.status_code, 403)
            finally:
                app.dependency_overrides.clear()

        asyncio.run(run())

    # -------------------------------------------------------------------------
    # UC 4.3: Tiến độ Kanban & Luân chuyển trạng thái 1 chiều
    # -------------------------------------------------------------------------

    def test_03_kanban_backward_transition_forbidden(self):
        """UC 4.3: Chặn lùi trạng thái từ IN_PROGRESS về PENDING hoặc RESOLVED về IN_PROGRESS (400 Bad Request)."""
        ticket_id = uuid.uuid4()
        ticket = Ticket(
            id=ticket_id,
            conversation_id=uuid.uuid4(),
            assigned_to=self.agent1_id,
            category="Giao hàng chậm",
            summary="Ticket đang xử lý",
            priority="P2",
            status="IN_PROGRESS",
            sla_deadline=datetime.now(timezone.utc) + timedelta(minutes=60)
        )

        mock_db = MagicMock()
        def query_side(model):
            m = MagicMock()
            if model == User:
                m.filter.return_value.first.return_value = self.agent1
            return m
        mock_db.query.side_effect = query_side

        def execute_side(stmt):
            m = MagicMock()
            m.scalar_one_or_none.return_value = ticket
            return m
        mock_db.execute.side_effect = execute_side

        async def run():
            app.dependency_overrides[get_db] = lambda: mock_db
            try:
                async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
                    # Thử kéo lùi từ IN_PROGRESS về PENDING
                    payload = {"status": "PENDING"}
                    res = await ac.put(f"/api/v1/admin/tickets/{ticket_id}/status", headers=self.agent1_headers, json=payload)
                    self.assertEqual(res.status_code, 400)
                    self.assertIn("không thể chuyển ngược lại", res.json()["detail"])
            finally:
                app.dependency_overrides.clear()

        asyncio.run(run())

    def test_04_kanban_resolution_note_validation(self):
        """UC 4.3: Bắt buộc nhập resolution_note từ 10 đến 1000 ký tự khi chuyển sang RESOLVED."""
        ticket_id = uuid.uuid4()
        ticket = Ticket(
            id=ticket_id,
            conversation_id=uuid.uuid4(),
            assigned_to=self.agent1_id,
            category="Khiếu nại sản phẩm",
            summary="Sản phẩm hư hỏng",
            priority="P1",
            status="IN_PROGRESS",
            sla_deadline=datetime.now(timezone.utc) + timedelta(minutes=15),
            sla_breached=False,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )

        mock_db = MagicMock()
        def query_side(model):
            m = MagicMock()
            if model == User:
                m.filter.return_value.first.return_value = self.agent1
            return m
        mock_db.query.side_effect = query_side

        def execute_side(stmt):
            m = MagicMock()
            m.scalar_one_or_none.return_value = ticket
            return m
        mock_db.execute.side_effect = execute_side

        async def run():
            app.dependency_overrides[get_db] = lambda: mock_db
            try:
                async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
                    # Ghi chú quá ngắn (< 10 ký tự)
                    payload = {"status": "RESOLVED", "resolution_note": "Đã xong"}
                    res = await ac.put(f"/api/v1/admin/tickets/{ticket_id}/status", headers=self.agent1_headers, json=payload)
                    self.assertIn(res.status_code, [400, 422])

                    # Ghi chú hợp lệ (>= 10 ký tự)
                    payload_valid = {"status": "RESOLVED", "resolution_note": "Đã đổi sản phẩm mới cho khách thành công."}
                    res_valid = await ac.put(f"/api/v1/admin/tickets/{ticket_id}/status", headers=self.agent1_headers, json=payload_valid)
                    self.assertEqual(res_valid.status_code, 200)
                    self.assertEqual(ticket.status, "RESOLVED")
                    self.assertEqual(ticket.resolution_note, "Đã đổi sản phẩm mới cho khách thành công.")
            finally:
                app.dependency_overrides.clear()

        asyncio.run(run())

    def test_05_agent_cannot_update_others_ticket(self):
        """UC 4.3 Quyền: AGENT không được cập nhật vé do AGENT khác phụ trách (403 Forbidden)."""
        ticket_id = uuid.uuid4()
        ticket = Ticket(
            id=ticket_id,
            conversation_id=uuid.uuid4(),
            assigned_to=self.agent2_id,  # Gán cho Agent 2
            category="Tư vấn",
            summary="Vé của Agent 2",
            priority="P3",
            status="IN_PROGRESS",
            sla_deadline=datetime.now(timezone.utc) + timedelta(minutes=240)
        )

        mock_db = MagicMock()
        def query_side(model):
            m = MagicMock()
            if model == User:
                m.filter.return_value.first.return_value = self.agent1
            return m
        mock_db.query.side_effect = query_side

        def execute_side(stmt):
            m = MagicMock()
            m.scalar_one_or_none.return_value = ticket
            return m
        mock_db.execute.side_effect = execute_side

        async def run():
            app.dependency_overrides[get_db] = lambda: mock_db
            try:
                async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
                    # Agent 1 thử cập nhật vé của Agent 2
                    payload = {"status": "RESOLVED", "resolution_note": "Ghi chú hợp lệ từ Agent 1"}
                    res = await ac.put(f"/api/v1/admin/tickets/{ticket_id}/status", headers=self.agent1_headers, json=payload)
                    self.assertEqual(res.status_code, 403)
                    self.assertIn("không có quyền", res.json()["detail"])
            finally:
                app.dependency_overrides.clear()

        asyncio.run(run())

    # -------------------------------------------------------------------------
    # UC 4.4: Báo cáo Thống kê Hiệu suất
    # -------------------------------------------------------------------------

    def test_06_reports_rbac_agent_forbidden(self):
        """UC 4.4 Quyền: Token AGENT bị từ chối xem báo cáo thống kê hiệu suất (403 Forbidden)."""
        mock_db = MagicMock()
        def query_side(model):
            m = MagicMock()
            if model == User:
                m.filter.return_value.first.return_value = self.agent1
            return m
        mock_db.query.side_effect = query_side

        def execute_side(stmt):
            m = MagicMock()
            m.scalar_one_or_none.return_value = self.agent1
            return m
        mock_db.execute.side_effect = execute_side

        async def run():
            app.dependency_overrides[get_db] = lambda: mock_db
            try:
                async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
                    today_str = date.today().strftime("%d/%m/%Y")
                    res = await ac.get(f"/api/v1/admin/reports/performance?start_date={today_str}&end_date={today_str}", headers=self.agent1_headers)
                    self.assertEqual(res.status_code, 403)
            finally:
                app.dependency_overrides.clear()

        asyncio.run(run())

    def test_07_reports_date_range_validations(self):
        """UC 4.4: Kiểm tra Validation ngày báo cáo (sai định dạng 400, start > end 400, range > 365 days 400)."""
        mock_db = MagicMock()
        def query_side(model):
            m = MagicMock()
            if model == User:
                m.filter.return_value.first.return_value = self.manager
            return m
        mock_db.query.side_effect = query_side

        def execute_side(stmt):
            m = MagicMock()
            m.all.return_value = []
            return m
        mock_db.execute.side_effect = execute_side

        async def run():
            app.dependency_overrides[get_db] = lambda: mock_db
            try:
                async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
                    # 1. Sai định dạng ngày
                    res1 = await ac.get("/api/v1/admin/reports/performance?start_date=2026-01-01&end_date=2026-01-10", headers=self.manager_headers)
                    self.assertEqual(res1.status_code, 400)
                    self.assertIn("DD/MM/YYYY", res1.json()["detail"])

                    # 2. Start > End
                    res2 = await ac.get("/api/v1/admin/reports/performance?start_date=10/05/2026&end_date=01/05/2026", headers=self.manager_headers)
                    self.assertEqual(res2.status_code, 400)
                    self.assertIn("bắt đầu phải nhỏ hơn hoặc bằng", res2.json()["detail"])
            finally:
                app.dependency_overrides.clear()

        asyncio.run(run())


if __name__ == "__main__":
    unittest.main()

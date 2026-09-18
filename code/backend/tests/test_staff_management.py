"""
Unit & Integration Tests for Staff Accounts & Work Status (Use Case 3.1 & 3.2).
Covers: Login, Token, /me, RBAC (AGENT/MANAGER/ADMIN), Create Staff, Validation, and Status Updates.
"""

import unittest
import asyncio
import sys
import os
import uuid
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import httpx
from app.main import app
from app.models.user import User
from app.core.security import get_password_hash, create_access_token
from app.api.deps import get_db


def _make_user(role="AGENT", status="OFFLINE", skills=None, email=None, password="Password1"):
    user = User(
        id=uuid.uuid4(),
        email=email or f"{role.lower()}@{role.lower()}.vn",
        password_hash=get_password_hash(password),
        full_name="Nhân Viên Test",
        phone="0912345678",
        role=role,
        status=status,
        skills=skills or (["ALL"] if role in ("ADMIN", "MANAGER") else ["Đổi trả"]),
        is_active=True,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    return user


def make_db(*first_values):
    """MagicMock có .query().filter().first() trả theo thứ tự giá trị truyền vào.
    Giá trị cuối được lặp lại cho các lệnh gọi tiếp theo."""
    mock_db = unittest.mock.MagicMock()
    if len(first_values) == 1:
        mock_db.query.return_value.filter.return_value.first.return_value = first_values[0]
    else:

        def side_effect(_=None):
            value = first_values[min(len(first_values) - 1, side_effect.calls)]
            side_effect.calls += 1
            return value

        side_effect.calls = 0
        mock_db.query.return_value.filter.return_value.first.side_effect = side_effect
    return mock_db


class TestStaffAuth(unittest.TestCase):

    def test_01_login_success(self):
        """Use Case 3.1: Đăng nhập nhân viên thành công -> trả JWT và thông tin user."""
        mock_db = unittest.mock.MagicMock()
        mock_db.query.return_value.filter.return_value.first.return_value = _make_user(role="ADMIN")

        async def run():
            app.dependency_overrides[get_db] = lambda: mock_db
            try:
                async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
                    res = await ac.post("/api/auth/agent/login", json={
                        "email": "admin@brand.com", "password": "Password1"
                    })
                    self.assertEqual(res.status_code, 200)
                    data = res.json()
                    self.assertIn("access_token", data)
                    self.assertEqual(data["token_type"], "bearer")
                    self.assertEqual(data["user"]["role"], "ADMIN")
            finally:
                app.dependency_overrides.clear()

        asyncio.run(run())

    def test_02_login_wrong_password(self):
        """Use Case 3.1 E: Sai mật khẩu -> 401 Unauthorized."""
        mock_db = unittest.mock.MagicMock()
        mock_db.query.return_value.filter.return_value.first.return_value = _make_user()

        async def run():
            app.dependency_overrides[get_db] = lambda: mock_db
            try:
                async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
                    res = await ac.post("/api/auth/agent/login", json={
                        "email": "agent@agent.vn", "password": "WrongPass1"
                    })
                    self.assertEqual(res.status_code, 401)
            finally:
                app.dependency_overrides.clear()

        asyncio.run(run())

    def test_03_login_inactive_account_forbidden(self):
        """Use Case 3.1 E: Tài khoản bị khóa (is_active=False) -> 403."""
        mock_db = unittest.mock.MagicMock()
        inactive = _make_user()
        inactive.is_active = False
        mock_db.query.return_value.filter.return_value.first.return_value = inactive

        async def run():
            app.dependency_overrides[get_db] = lambda: mock_db
            try:
                async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
                    res = await ac.post("/api/auth/agent/login", json={
                        "email": "agent@agent.vn", "password": "Password1"
                    })
                    self.assertEqual(res.status_code, 403)
            finally:
                app.dependency_overrides.clear()

        asyncio.run(run())

    def test_04_me_endpoint(self):
        """Use Case 3.1: GET /auth/agent/me trả thông tin nhân viên phân biệt token STAFF/CUSTOMER."""
        staff_user = _make_user(role="MANAGER")
        staff_token = create_access_token({"sub": str(staff_user.id), "email": staff_user.email, "role": "STAFF"})
        customer_token = create_access_token({"sub": str(uuid.uuid4()), "email": "khach@pethome.vn", "role": "CUSTOMER"})

        mock_db = unittest.mock.MagicMock()
        mock_db.query.return_value.filter.return_value.first.return_value = staff_user

        async def run():
            app.dependency_overrides[get_db] = lambda: mock_db
            try:
                async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
                    res = await ac.get("/api/auth/agent/me", headers={"Authorization": f"Bearer {staff_token}"})
                    self.assertEqual(res.status_code, 200)
                    self.assertEqual(res.json()["email"], staff_user.email)

                    res_no_auth = await ac.get("/api/auth/agent/me")
                    self.assertEqual(res_no_auth.status_code, 401)

                    res_customer = await ac.get("/api/auth/agent/me", headers={"Authorization": f"Bearer {customer_token}"})
                    self.assertEqual(res_customer.status_code, 401)
            finally:
                app.dependency_overrides.clear()

        asyncio.run(run())


class TestStaffManagement(unittest.TestCase):

    def test_01_create_agent_success(self):
        """Use Case 3.1: Tạo tài khoản AGENT hợp lệ -> 201 Created."""
        admin = _make_user(role="ADMIN")
        mock_db = make_db(admin, None)  # auth lookup -> admin; duplicate check -> None

        def capture_add(user):
            if user.id is None:
                user.id = uuid.uuid4()
            if user.created_at is None:
                user.created_at = datetime.now(timezone.utc)
            if user.updated_at is None:
                user.updated_at = datetime.now(timezone.utc)

        mock_db.add.side_effect = capture_add
        admin_token = create_access_token({"sub": str(admin.id), "email": admin.email, "role": "STAFF"})

        async def run():
            app.dependency_overrides[get_db] = lambda: mock_db
            try:
                async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
                    res = await ac.post("/api/admin/users", headers={"Authorization": f"Bearer {admin_token}"}, json={
                        "full_name": "Phạm Thị Mới",
                        "email": "agent.moi@brand.com",
                        "password": "Moi@123456",
                        "phone": "0987654321",
                        "role": "AGENT",
                        "skills": ["Đổi trả", "Giao hàng"],
                    })
                    self.assertEqual(res.status_code, 201)
            finally:
                app.dependency_overrides.clear()

        asyncio.run(run())

    def test_02_create_duplicate_email(self):
        """Use Case 3.1 E-1: Email trùng -> 400."""
        existing = _make_user()
        admin = _make_user(role="ADMIN")
        mock_db = make_db(admin, existing)  # auth lookup -> admin; duplicate check -> existing
        admin_token = create_access_token({"sub": str(admin.id), "email": admin.email, "role": "STAFF"})

        async def run():
            app.dependency_overrides[get_db] = lambda: mock_db
            try:
                async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
                    res = await ac.post("/api/admin/users", headers={"Authorization": f"Bearer {admin_token}"}, json={
                        "full_name": "Trùng Email", "email": "agent@agent.vn",
                        "password": "Moi@123456", "role": "AGENT", "skills": ["Đổi trả"],
                    })
                    self.assertEqual(res.status_code, 400)
            finally:
                app.dependency_overrides.clear()

        asyncio.run(run())

    def test_03_create_agent_without_skills(self):
        """Use Case 3.1 E: Agent bắt buộc có >= 1 kỹ năng -> 422."""
        admin = _make_user(role="ADMIN")
        mock_db = make_db(admin)
        admin_token = create_access_token({"sub": str(admin.id), "email": admin.email, "role": "STAFF"})

        async def run():
            app.dependency_overrides[get_db] = lambda: mock_db
            try:
                async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
                    res = await ac.post("/api/admin/users", headers={"Authorization": f"Bearer {admin_token}"}, json={
                        "full_name": "Không Kỹ Năng", "email": "noskill@brand.com",
                        "password": "Moi@123456", "role": "AGENT", "skills": [],
                    })
                    self.assertEqual(res.status_code, 422)
            finally:
                app.dependency_overrides.clear()

        asyncio.run(run())

    def test_04_create_weak_password(self):
        """Use Case 3.1 E: Mật khẩu chỉ số -> 422."""
        admin = _make_user(role="ADMIN")
        mock_db = make_db(admin)
        admin_token = create_access_token({"sub": str(admin.id), "email": admin.email, "role": "STAFF"})

        async def run():
            app.dependency_overrides[get_db] = lambda: mock_db
            try:
                async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
                    res = await ac.post("/api/admin/users", headers={"Authorization": f"Bearer {admin_token}"}, json={
                        "full_name": "Pass Yếu", "email": "weak@brand.com",
                        "password": "12345678", "role": "AGENT", "skills": ["Đổi trả"],
                    })
                    self.assertEqual(res.status_code, 422)
            finally:
                app.dependency_overrides.clear()

        asyncio.run(run())

    def test_05_agent_cannot_manage_users(self):
        """Use Case 3.1 Quyền: AGENT không được quản lý tài khoản -> 403."""
        agent = _make_user(role="AGENT")
        mock_db = make_db(agent)
        agent_token = create_access_token({"sub": str(agent.id), "email": agent.email, "role": "STAFF"})

        async def run():
            app.dependency_overrides[get_db] = lambda: mock_db
            try:
                async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
                    res = await ac.post("/api/admin/users", headers={"Authorization": f"Bearer {agent_token}"}, json={
                        "full_name": "X", "email": "x@brand.com",
                        "password": "Moi@123456", "role": "AGENT", "skills": ["Đổi trả"],
                    })
                    self.assertEqual(res.status_code, 403)
            finally:
                app.dependency_overrides.clear()

        asyncio.run(run())

    def test_06_status_update_valid(self):
        """Use Case 3.2: Đổi trạng thái ONLINE/BUSY/OFFLINE thành công."""
        user = _make_user(role="AGENT", status="OFFLINE")
        token = create_access_token({"sub": str(user.id), "email": user.email, "role": "STAFF"})

        mock_db = unittest.mock.MagicMock()
        mock_db.query.return_value.filter.return_value.first.return_value = user

        async def run():
            app.dependency_overrides[get_db] = lambda: mock_db
            try:
                async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
                    for s in ["ONLINE", "BUSY", "OFFLINE"]:
                        res = await ac.put("/api/agent/status", headers={"Authorization": f"Bearer {token}"}, json={"status": s})
                        self.assertEqual(res.status_code, 200)
                        self.assertEqual(res.json()["status"], s)
            finally:
                app.dependency_overrides.clear()

        asyncio.run(run())

    def test_07_status_update_invalid(self):
        """Use Case 3.2 E: Trạng thái không hợp lệ -> 422."""
        user = _make_user(role="AGENT")
        token = create_access_token({"sub": str(user.id), "email": user.email, "role": "STAFF"})

        mock_db = unittest.mock.MagicMock()
        mock_db.query.return_value.filter.return_value.first.return_value = user

        async def run():
            app.dependency_overrides[get_db] = lambda: mock_db
            try:
                async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
                    res = await ac.put("/api/agent/status", headers={"Authorization": f"Bearer {token}"}, json={"status": "AWAY"})
                    self.assertEqual(res.status_code, 422)
            finally:
                app.dependency_overrides.clear()

        asyncio.run(run())


if __name__ == "__main__":
    unittest.main()
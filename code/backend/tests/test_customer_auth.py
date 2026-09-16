"""
Unit & Integration Tests for Customer Authentication (Use Case 1.1).
Covers: Registration, Validation, Login, JWT Token, Brute-Force Lockout, and Profile Endpoint.
"""

import unittest
import asyncio
import sys
import os
import uuid
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import httpx
from app.main import app
from app.models.customer import Customer
from app.core.security import get_password_hash, create_access_token, _failed_login_attempts, _account_lockouts
from app.api.deps import get_db

class TestCustomerAuth(unittest.TestCase):

    def setUp(self):
        # Reset brute force caches trước mỗi test
        _failed_login_attempts.clear()
        _account_lockouts.clear()

    def test_01_customer_registration_success(self):
        """SPEC-1.1: Khách hàng đăng ký tài khoản thành công với thông tin hợp lệ."""
        mock_db = MagicMock()
        mock_db.query.return_value.filter.return_value.first.return_value = None  # Email chưa tồn tại
        
        async def run():
            app.dependency_overrides[get_db] = lambda: mock_db
            try:
                async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
                    payload = {
                        "full_name": "Nguyễn Văn Khách",
                        "email": "khachhang@pethome.vn",
                        "password": "Password123",
                        "phone": "0987654321"
                    }
                    response = await ac.post("/api/auth/customer/register", json=payload)
                    self.assertEqual(response.status_code, 201)
                    data = response.json()
                    self.assertIn("access_token", data)
                    self.assertEqual(data["token_type"], "bearer")
                    self.assertEqual(data["customer"]["email"], "khachhang@pethome.vn")
                    self.assertEqual(data["customer"]["full_name"], "Nguyễn Văn Khách")
            finally:
                app.dependency_overrides.clear()

        asyncio.run(run())

    def test_02_customer_registration_duplicate_email(self):
        """SPEC-1.1 E-4: Báo lỗi 400 nếu email đã được sử dụng."""
        mock_db = MagicMock()
        existing_customer = MagicMock(spec=Customer)
        existing_customer.email = "duplicate@pethome.vn"
        mock_db.query.return_value.filter.return_value.first.return_value = existing_customer
        
        async def run():
            app.dependency_overrides[get_db] = lambda: mock_db
            try:
                async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
                    payload = {
                        "full_name": "Trần Thị Trùng",
                        "email": "duplicate@pethome.vn",
                        "password": "Password123"
                    }
                    response = await ac.post("/api/auth/customer/register", json=payload)
                    self.assertEqual(response.status_code, 400)
                    self.assertIn("Địa chỉ email này đã được sử dụng", response.json()["detail"])
            finally:
                app.dependency_overrides.clear()

        asyncio.run(run())

    def test_03_customer_registration_weak_password_validation(self):
        """SPEC-1.1 E-2: Kiểm tra mật khẩu quá ngắn hoặc thiếu chữ/số."""
        async def run():
            async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
                # Password chỉ toàn số
                res1 = await ac.post("/api/auth/customer/register", json={
                    "full_name": "Lê Văn A",
                    "email": "test1@pethome.vn",
                    "password": "12345678"
                })
                self.assertEqual(res1.status_code, 422)

                # Password < 8 ký tự
                res2 = await ac.post("/api/auth/customer/register", json={
                    "full_name": "Lê Văn B",
                    "email": "test2@pethome.vn",
                    "password": "Abc1"
                })
                self.assertEqual(res2.status_code, 422)

        asyncio.run(run())

    def test_04_customer_login_success(self):
        """SPEC-1.2: Đăng nhập thành công với email và mật khẩu chính xác."""
        mock_db = MagicMock()
        customer_id = uuid.uuid4()
        mock_customer = Customer(
            id=customer_id,
            email="valid@pethome.vn",
            password_hash=get_password_hash("Password123"),
            full_name="Khách Hàng Chuẩn",
            phone="0912345678",
            is_active=True
        )
        mock_db.query.return_value.filter.return_value.first.return_value = mock_customer

        async def run():
            app.dependency_overrides[get_db] = lambda: mock_db
            try:
                async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
                    response = await ac.post("/api/auth/customer/login", json={
                        "email": "valid@pethome.vn",
                        "password": "Password123"
                    })
                    self.assertEqual(response.status_code, 200)
                    data = response.json()
                    self.assertIn("access_token", data)
                    self.assertEqual(data["customer"]["email"], "valid@pethome.vn")
            finally:
                app.dependency_overrides.clear()

        asyncio.run(run())

    def test_05_customer_login_brute_force_lockout(self):
        """SPEC-1.2 E-7 & E-6: Nhập sai mật khẩu 5 lần liên tiếp kích hoạt khóa tài khoản 15 phút (423 Locked)."""
        mock_db = MagicMock()
        mock_customer = Customer(
            id=uuid.uuid4(),
            email="victim@pethome.vn",
            password_hash=get_password_hash("CorrectPassword123"),
            full_name="Nạn Nhân Brute Force",
            is_active=True
        )
        mock_db.query.return_value.filter.return_value.first.return_value = mock_customer

        async def run():
            app.dependency_overrides[get_db] = lambda: mock_db
            try:
                async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
                    # 4 lần thử đầu tiên -> 401 Unauthorized
                    for i in range(4):
                        res = await ac.post("/api/auth/customer/login", json={
                            "email": "victim@pethome.vn",
                            "password": "WrongPassword"
                        })
                        self.assertEqual(res.status_code, 401)
                        self.assertIn(f"Bạn còn {4 - i} lần thử", res.json()["detail"])

                    # Lần thứ 5 -> 423 Locked
                    res5 = await ac.post("/api/auth/customer/login", json={
                        "email": "victim@pethome.vn",
                        "password": "WrongPassword"
                    })
                    self.assertEqual(res5.status_code, 423)
                    self.assertIn("tạm khóa trong 15 phút", res5.json()["detail"])

                    # Thử lại ngay sau khi bị khóa dù gõ đúng mật khẩu -> Vẫn 423 Locked
                    res_locked = await ac.post("/api/auth/customer/login", json={
                        "email": "victim@pethome.vn",
                        "password": "CorrectPassword123"
                    })
                    self.assertEqual(res_locked.status_code, 423)
            finally:
                app.dependency_overrides.clear()

        asyncio.run(run())

    def test_06_customer_profile_me_endpoint(self):
        """SPEC-1.3: Lấy thông tin cá nhân qua Bearer Token."""
        customer_id = uuid.uuid4()
        token = create_access_token({"sub": str(customer_id), "email": "me@pethome.vn", "role": "CUSTOMER"})
        
        mock_db = MagicMock()
        mock_customer = Customer(
            id=customer_id,
            email="me@pethome.vn",
            full_name="Khách Hàng Tôi",
            phone="0909090909",
            is_active=True
        )
        mock_db.query.return_value.filter.return_value.first.return_value = mock_customer

        async def run():
            app.dependency_overrides[get_db] = lambda: mock_db
            try:
                async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
                    # Có token hợp lệ
                    res = await ac.get("/api/auth/customer/me", headers={"Authorization": f"Bearer {token}"})
                    self.assertEqual(res.status_code, 200)
                    data = res.json()
                    self.assertEqual(data["email"], "me@pethome.vn")
                    self.assertEqual(data["full_name"], "Khách Hàng Tôi")

                    # Không có token -> 401
                    res_no_auth = await ac.get("/api/auth/customer/me")
                    self.assertEqual(res_no_auth.status_code, 401)
            finally:
                app.dependency_overrides.clear()

        asyncio.run(run())

if __name__ == "__main__":
    unittest.main()

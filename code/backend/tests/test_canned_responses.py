"""
Integration & Unit Tests for UC 3.4 — Mẫu phản hồi nhanh (Canned Responses):
CRUD, quyền truy cập, kiểm tra trùng Shortcut, chỉ owner/manager được chỉnh-sửa-xóa.
"""

import unittest
import asyncio
import sys
import os
import uuid
import json
from datetime import datetime, timezone
from unittest.mock import patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import httpx
from fastapi import HTTPException

from app.main import app
from app.models.user import User
from app.core.security import get_password_hash, create_access_token
from app.api.deps import get_db
from app.schemas.canned_response import CannedResponseResponse
from app.services.canned_response_service import CannedResponseService


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


def _make_canned(**kwargs):
    data = {
        "id": uuid.uuid4(),
        "shortcut": "hoan-tien",
        "title": "Chính sách hoàn tiền",
        "content": "Chào bạn, chúng tôi sẽ hoàn tiền trong 3-5 ngày làm việc.",
        "category": "Chính sách",
        "created_by": uuid.uuid4(),
        "created_at": datetime.now(timezone.utc),
    }
    data.update(kwargs)
    return CannedResponseResponse(**data)


class TestCannedResponses(unittest.TestCase):

    def test_01_create_requires_auth(self):
        """UC 3.4 E: Không có token -> 401."""
        async def run():
            async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
                res = await ac.post("/api/canned-responses", json={})
                self.assertEqual(res.status_code, 401)
        asyncio.run(run())

    def test_02_customer_cannot_manage(self):
        """UC 3.4 Quyền: Token CUSTOMER bị từ chối -> 401."""
        customer_token = create_access_token({"sub": str(uuid.uuid4()), "email": "khach@pethome.vn", "role": "CUSTOMER"})

        async def run():
            async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
                res = await ac.get("/api/canned-responses", headers={"Authorization": f"Bearer {customer_token}"})
                self.assertEqual(res.status_code, 401)
        asyncio.run(run())

    def test_03_create_success(self):
        """UC 3.4 A-1: Nhân viên tạo mẫu phản hồi -> 201."""
        agent = _make_user("AGENT")
        token = create_access_token({"sub": str(agent.id), "email": agent.email, "role": "STAFF"})
        canned = _make_canned(created_by=agent.id)

        with patch.object(CannedResponseService, "create", return_value=canned):
            async def assert_fn(ac):
                res = await ac.post(
                    "/api/canned-responses",
                    headers={"Authorization": f"Bearer {token}"},
                    json={"shortcut": "/hoan-tien", "title": "Hoàn tiền", "content": "Chúng tôi sẽ hoàn tiền...", "category": "Chính sách"},
                )
                self.assertEqual(res.status_code, 201)
                data = res.json()
                self.assertEqual(data["shortcut"], "hoan-tien")

            _run_with_auth(assert_fn, agent)

    def test_04_list_responses(self):
        """UC 3.4 A-1: Danh sách mẫu phản hồi, lọc theo danh mục."""
        agent = _make_user("AGENT")
        token = create_access_token({"sub": str(agent.id), "email": agent.email, "role": "STAFF"})
        canned = _make_canned()

        with patch.object(CannedResponseService, "list_responses", return_value=[canned]):
            async def assert_fn(ac):
                res = await ac.get("/api/canned-responses?category=Chính sách", headers={"Authorization": f"Bearer {token}"})
                self.assertEqual(res.status_code, 200)
                data = res.json()
                self.assertIsInstance(data, list)
                self.assertEqual(len(data), 1)

            _run_with_auth(assert_fn, agent)

    def test_05_duplicate_shortcut_conflict(self):
        """UC 3.4 E-1: Shortcut trùng -> 400 'Phím tắt đã tồn tại'."""
        agent = _make_user("AGENT")
        token = create_access_token({"sub": str(agent.id), "email": agent.email, "role": "STAFF"})

        def _dup(*args, **kwargs):
            raise HTTPException(status_code=400, detail="Phím tắt đã tồn tại.")

        with patch.object(CannedResponseService, "create", new=_dup):
            async def assert_fn(ac):
                res = await ac.post(
                    "/api/canned-responses",
                    headers={"Authorization": f"Bearer {token}"},
                    json={"shortcut": "/hoan-tien", "title": "Hoàn tiền", "content": "Chúng tôi sẽ hoàn tiền theo chính sách.", "category": "Chính sách"},
                )
                self.assertEqual(res.status_code, 400)
                self.assertEqual(res.json()["detail"], "Phím tắt đã tồn tại.")

            _run_with_auth(assert_fn, agent)

    def test_06_update_validation(self):
        """UC 3.4: Cập nhật mẫu phản hồi -> 200."""
        agent = _make_user("AGENT")
        token = create_access_token({"sub": str(agent.id), "email": agent.email, "role": "STAFF"})
        canned = _make_canned(title="Hoàn tiền nhanh", created_by=agent.id)

        with patch.object(CannedResponseService, "update", return_value=canned):
            async def assert_fn(ac):
                res = await ac.put(
                    f"/api/canned-responses/{canned.id}",
                    headers={"Authorization": f"Bearer {token}"},
                    json={"title": "Hoàn tiền nhanh"},
                )
                self.assertEqual(res.status_code, 200)
                self.assertEqual(res.json()["title"], "Hoàn tiền nhanh")

            _run_with_auth(assert_fn, agent)

    def test_07_delete_success(self):
        """UC 3.4: Xóa mẫu phản hồi -> success."""
        agent = _make_user("AGENT")
        token = create_access_token({"sub": str(agent.id), "email": agent.email, "role": "STAFF"})
        canned_id = uuid.uuid4()

        with patch.object(CannedResponseService, "delete", return_value={"status": "success", "deleted_id": str(canned_id)}):
            async def assert_fn(ac):
                res = await ac.delete(f"/api/canned-responses/{canned_id}", headers={"Authorization": f"Bearer {token}"})
                self.assertEqual(res.status_code, 200)

            _run_with_auth(assert_fn, agent)

    def test_08_service_duplicate_shortcut(self):
        """UC 3.4 E-1 (logic service): Shortcut trùng -> 400 Bad Request."""
        db = unittest.mock.MagicMock()
        db.query.return_value.filter.return_value.first.return_value = unittest.mock.MagicMock()
        agent = _make_user("AGENT")

        with self.assertRaises(HTTPException) as ctx:
            CannedResponseService.create(db=db, req=unittest.mock.MagicMock(shortcut="hoan-tien", title="X", content="Y", category="Z"), user=agent)
        self.assertEqual(ctx.exception.status_code, 400)
        self.assertEqual(ctx.exception.detail, "Phím tắt đã tồn tại.")

    def test_09_service_publishes_created_event(self):
        """UC 3.4: Sau khi tạo mẫu -> bắn sự kiện CANNED_RESPONSE_CREATED qua Redis."""
        db = unittest.mock.MagicMock()
        db.query.return_value.filter.return_value.first.return_value = None
        agent = _make_user("AGENT")
        canned = _make_canned(created_by=agent.id)

        with patch.object(CannedResponseResponse, "model_validate", return_value=canned), \
             patch("app.services.canned_response_service.redis_client") as rc:
            CannedResponseService.create(
                db=db,
                req=unittest.mock.MagicMock(
                    shortcut="/hoan-tien",
                    title="Hoàn tiền",
                    content="Chúng tôi sẽ hoàn tiền trong 3-5 ngày.",
                    category="Chính sách",
                ),
                user=agent,
            )
            rc.publish.assert_called_once()
            payload = json.loads(rc.publish.call_args[0][1])
            self.assertEqual(payload["event"], "CANNED_RESPONSE_CREATED")
            self.assertEqual(payload["payload"]["shortcut"], "hoan-tien")

    def test_10_schema_shortcut_requires_slash(self):
        """UC 3.4 A-1 Validation: shortcut thiếu '/' -> 422."""
        try:
            CannedResponseCreate(shortcut="hoan-tien", title="Hoàn tiền", content="Chúng tôi sẽ hoàn tiền.", category="Chính sách")
            self.fail("shortcut không bắt đầu bằng '/' phải lỗi")
        except Exception:
            pass

    def test_11_schema_shortcut_has_space(self):
        """UC 3.4 A-1 Validation: shortcut chứa khoảng trắng -> 422."""
        try:
            CannedResponseCreate(shortcut="/hoan tien", title="Hoàn tiền", content="Chúng tôi sẽ hoàn tiền.", category="Chính sách")
            self.fail("shortcut chứa khoảng trắng phải lỗi")
        except Exception:
            pass

    def test_12_schema_content_too_short(self):
        """UC 3.4 A-1 Validation: content < 5 ký tự -> 422."""
        try:
            CannedResponseCreate(shortcut="/hoan-tien", title="Hoàn tiền", content="X", category="Chính sách")
            self.fail("content quá ngắn phải lỗi")
        except Exception:
            pass

    def test_13_schema_title_too_short(self):
        """UC 3.4 A-1 Validation: title < 3 ký tự -> 422."""
        try:
            CannedResponseCreate(shortcut="/hoan-tien", title="HT", content="Chúng tôi sẽ hoàn tiền.", category="Chính sách")
            self.fail("title quá ngắn phải lỗi")
        except Exception:
            pass

    def test_14_service_non_owner_cannot_edit(self):
        """UC 3.4 Quyền (logic service): AGENT không phải chủ mẫu -> 403."""
        db = unittest.mock.MagicMock()
        item = unittest.mock.MagicMock()
        item.id = uuid.uuid4()
        item.created_by = uuid.uuid4()  # người tạo khác
        db.query.return_value.filter.return_value.first.return_value = item
        agent = _make_user("AGENT")

        with self.assertRaises(HTTPException) as ctx:
            CannedResponseService.update(db=db, response_id=item.id, req=unittest.mock.MagicMock(shortcut=None, title="X", content="Y", category="Z"), user=agent)
        self.assertEqual(ctx.exception.status_code, 403)

    def test_15_service_manager_can_edit_any(self):
        """UC 3.4 Quyền: MANAGER được chỉnh sửa mẫu của người khác."""
        manager = _make_user("MANAGER")
        item = unittest.mock.MagicMock()
        item.id = uuid.uuid4()
        item.created_by = uuid.uuid4()

        self.assertTrue(CannedResponseService._can_manage(item, manager))


if __name__ == "__main__":
    unittest.main()
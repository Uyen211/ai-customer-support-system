from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.redis import redis_client
from app.core.security import create_access_token, get_password_hash, verify_password
from app.models.user import User
from app.schemas.user import (
    StaffCreateRequest,
    StaffLoginRequest,
    StaffStatusUpdateRequest,
    StaffTokenResponse,
    UserResponse,
)


class UserService:
    @staticmethod
    def _to_response(user: User) -> UserResponse:
        data = {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "phone": user.phone,
            "role": user.role,
            "status": user.status,
            "skills": user.skills or [],
            "is_active": user.is_active,
            "created_at": user.created_at,
        }
        return UserResponse.model_validate(data)

    @staticmethod
    def login_staff(db: Session, req: StaffLoginRequest) -> StaffTokenResponse:
        normalized_email = req.email.lower().strip()
        user = db.query(User).filter(User.email == normalized_email).first()

        if not user or not verify_password(req.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Địa chỉ email hoặc mật khẩu không chính xác."
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Tài khoản hiện đang bị khóa hoặc ngừng kích hoạt."
            )

        user.status = "OFFLINE"
        db.commit()
        db.refresh(user)
        UserService._sync_agent_status(user.id, user.status)

        token_data = {"sub": str(user.id), "email": user.email, "role": user.role, "type": "STAFF"}
        access_token = create_access_token(token_data)
        return StaffTokenResponse(access_token=access_token, user=UserService._to_response(user))

    @staticmethod
    def create_staff(db: Session, req: StaffCreateRequest) -> UserResponse:
        try:
            req.validate_business_rules()
        except ValueError as exc:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc))

        normalized_email = req.email.lower().strip()
        existing = db.query(User).filter(User.email == normalized_email).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Địa chỉ email này đã được sử dụng."
            )

        user = User(
            email=normalized_email,
            password_hash=get_password_hash(req.password),
            full_name=req.full_name.strip(),
            phone=req.phone,
            role=req.role,
            status="OFFLINE",
            skills=req.skills,
            is_active=True,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return UserService._to_response(user)

    @staticmethod
    def list_staff(db: Session) -> list[UserResponse]:
        users = db.query(User).order_by(User.created_at.desc()).all()
        return [UserService._to_response(user) for user in users]

    @staticmethod
    def update_status(db: Session, user: User, req: StaffStatusUpdateRequest) -> UserResponse:
        user.status = req.status
        db.commit()
        db.refresh(user)
        UserService._sync_agent_status(user.id, user.status)
        return UserService._to_response(user)

    @staticmethod
    def _sync_agent_status(user_id, new_status: str) -> None:
        try:
            redis_client.set(f"agent:status:{user_id}", new_status)
            redis_client.publish(
                "agent:status:events",
                f'{{"event":"AGENT_STATUS_CHANGED","user_id":"{user_id}","status":"{new_status}"}}'
            )
        except Exception:
            pass

from typing import Optional
from uuid import UUID
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.security import decode_access_token
from app.models.customer import Customer

# Sử dụng HTTPBearer để hỗ trợ Header: Authorization: Bearer <token>
security_scheme = HTTPBearer(auto_error=False)

def get_current_customer(
    auth: Optional[HTTPAuthorizationCredentials] = Depends(security_scheme),
    db: Session = Depends(get_db)
) -> Customer:
    """
    Dependency xác thực token của khách hàng. Yêu cầu token hợp lệ và tài khoản đang kích hoạt.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Phiên đăng nhập không hợp lệ hoặc đã hết hạn. Vui lòng đăng nhập lại.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    if not auth or not auth.credentials:
        raise credentials_exception
    
    payload = decode_access_token(auth.credentials)
    if not payload:
        raise credentials_exception
    
    customer_id_str = payload.get("sub") or payload.get("customer_id")
    if not customer_id_str:
        raise credentials_exception
    
    try:
        customer_id = UUID(customer_id_str)
    except (ValueError, TypeError):
        raise credentials_exception
    
    customer = db.query(Customer).filter(Customer.id == customer_id, Customer.is_active == True).first()
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tài khoản khách hàng không tồn tại hoặc đã bị khóa.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return customer

def get_optional_current_customer(
    auth: Optional[HTTPAuthorizationCredentials] = Depends(security_scheme),
    db: Session = Depends(get_db)
) -> Optional[Customer]:
    """
    Dependency lấy khách hàng tùy chọn (cho phép khách vãng lai hoặc khách đã đăng nhập).
    """
    if not auth or not auth.credentials:
        return None
    
    payload = decode_access_token(auth.credentials)
    if not payload:
        return None
    
    customer_id_str = payload.get("sub") or payload.get("customer_id")
    if not customer_id_str:
        return None
    
    try:
        customer_id = UUID(customer_id_str)
        return db.query(Customer).filter(Customer.id == customer_id, Customer.is_active == True).first()
    except Exception:
        return None

__all__ = ["get_db", "get_current_customer", "get_optional_current_customer"]

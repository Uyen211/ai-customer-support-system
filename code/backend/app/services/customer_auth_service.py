from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.customer import Customer
from app.models.user import User
from app.schemas.customer import CustomerRegisterRequest, CustomerLoginRequest, TokenResponse, CustomerResponse
from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    check_login_lockout,
    record_failed_login,
    record_successful_login
)

class CustomerAuthService:
    @staticmethod
    def register_customer(db: Session, req: CustomerRegisterRequest) -> TokenResponse:
        """
        Đăng ký tài khoản khách hàng mới (Use Case 1.1).
        """
        normalized_email = req.email.lower().strip()
        
        # E-4: Kiểm tra sự tồn tại của email
        existing = db.query(Customer).filter(Customer.email == normalized_email).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Địa chỉ email này đã được sử dụng. Vui lòng chọn Đăng nhập."
            )
        
        # Băm mật khẩu và lưu vào CSDL
        hashed_pwd = get_password_hash(req.password)
        new_customer = Customer(
            email=normalized_email,
            password_hash=hashed_pwd,
            full_name=req.full_name.strip(),
            phone=req.phone.strip() if req.phone else None,
            is_active=True
        )
        db.add(new_customer)
        db.commit()
        db.refresh(new_customer)
        
        # Sinh Access Token tự động đăng nhập
        token_data = {"sub": str(new_customer.id), "email": new_customer.email, "role": "CUSTOMER"}
        access_token = create_access_token(token_data)
        
        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            customer=CustomerResponse.model_validate(new_customer)
        )

    @staticmethod
    def login_customer(db: Session, req: CustomerLoginRequest) -> TokenResponse:
        """
        Đăng nhập tài khoản khách hàng (Use Case 1.1 A-1 & bảo vệ Brute Force).
        """
        normalized_email = req.email.lower().strip()
        
        # E-6 / Rule 2: Kiểm tra khóa tài khoản do brute force 5 lần
        is_locked, remaining_sec = check_login_lockout(normalized_email)
        if is_locked:
            minutes = max(1, (remaining_sec + 59) // 60)
            raise HTTPException(
                status_code=status.HTTP_423_LOCKED,
                detail=f"Tài khoản hiện đang bị tạm khóa do nhập sai mật khẩu 5 lần liên tiếp. Vui lòng thử lại sau {minutes} phút ({remaining_sec}s)."
            )
        
        # E-5: Kiểm tra email có tồn tại không
        customer = db.query(Customer).filter(Customer.email == normalized_email).first()
        if not customer:
            # Email có thể là tài khoản nhân viên (Use Case 3.1) -> chỉ dẫn đúng cổng đăng nhập
            staff_account = db.query(User).filter(User.email == normalized_email).first()
            if staff_account:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Email này là tài khoản nhân viên. Vui lòng đăng nhập qua Cổng Nhân Viên."
                )
            record_failed_login(normalized_email)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Thông tin tài khoản hoặc mật khẩu không chính xác."
            )
        
        # E-6: Kiểm tra tài khoản bị vô hiệu hóa
        if not customer.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Tài khoản hiện đang bị tạm khóa. Vui lòng quay lại sau hoặc liên hệ bộ phận hỗ trợ."
            )
        
        # E-7: So khớp mật khẩu
        if not verify_password(req.password, customer.password_hash):
            fail_count, is_now_locked = record_failed_login(normalized_email)
            if is_now_locked:
                raise HTTPException(
                    status_code=status.HTTP_423_LOCKED,
                    detail="Bạn đã nhập sai mật khẩu 5 lần liên tiếp. Tài khoản đã bị tạm khóa trong 15 phút để bảo đảm an toàn."
                )
            remaining_attempts = max(0, 5 - fail_count)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Thông tin tài khoản hoặc mật khẩu không chính xác. (Bạn còn {remaining_attempts} lần thử trước khi bị khóa tạm thời)"
            )
        
        # Đăng nhập thành công -> Xóa cờ sai
        record_successful_login(normalized_email)
        
        token_data = {"sub": str(customer.id), "email": customer.email, "role": "CUSTOMER"}
        access_token = create_access_token(token_data)
        
        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            customer=CustomerResponse.model_validate(customer)
        )

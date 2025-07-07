from sqlalchemy.orm import Session
from fastapi import status
from app.exceptions import raise_http_exception
from app.user.models.user_models import User
from app.user.utils.hash_utils import HashUtils
from app.user.utils.token_utils import TokenUtils
from app.user.schemas import AuthLogin, AuthSignup, AuthResponse
from app.config.config import Settings, settings


class UserService:
    def __init__(self, session: Session) -> None:
        self.session = session

    def signup(self, signup_data: AuthSignup) -> User:
        if self.user_exist_by_email(email=signup_data.email):
            raise raise_http_exception(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User with email {signup_data.email} already exists",
                error_code="DUPLICATE_USER_EMAIL"
            )
            
        hashed_password = HashUtils.hash_password(
            password=signup_data.password)
        signup_data.password = hashed_password

        new_user = User(**signup_data.dict())

        self.session.add(instance=new_user)
        self.session.commit()
        self.session.refresh(instance=new_user)

        return new_user

    def login(self, login_data: AuthLogin) -> AuthResponse:
        user = self.get_user_by_email(email=login_data.email)
        if user is None or not HashUtils.check_password(password=login_data.password, hashed_password=user.password):
            raise 

        token = TokenUtils.generate_token(user_id=user.id)
        return AuthResponse(access_token=token, token_type="bearer")

    def user_exist_by_email(self, email: str) -> bool:
        return self.session.query(User).filter_by(email=email).first() is not None

    def get_user_by_email(self, email: str) -> User:
        return self.session.query(User).filter_by(email=email).first()

    def get_user_by_id(self, user_id: int) -> User:
        return self.session.query(User).filter_by(id=user_id).first()
    
    def add_shop_to_user(self, user_id: int, shop_id: int) -> User:
        user = self.get_user_by_id(user_id=user_id)
        user.shop_id = shop_id
        self.session.commit()
        self.session.refresh(instance=user)
        return user

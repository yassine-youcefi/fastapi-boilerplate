from sqlalchemy.ext.asyncio import AsyncSession
from app.user.models.user_models import User
from app.auth.utils.hash_utils import HashUtils
from app.auth.utils.token_utils import TokenUtils
from app.auth.schemas.auth_schemas import (
    AuthLoginRequest, AuthLoginResponse, AuthRegisterRequest, AuthRegisterResponse
)
from app.user.schemas import UserResponse
from app.user.services.user_services import UserService
from app.exceptions import raise_predefined_http_exception
from app.auth.exceptions import DuplicateUserEmailException, InvalidCredentialsException

class AuthService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.user_service = UserService(session)

    async def signup(self, signup_data: AuthRegisterRequest) -> AuthRegisterResponse:
        if await self.user_service.user_exists_by_email(email=signup_data.email):
            raise_predefined_http_exception(DuplicateUserEmailException(signup_data.email))
        hashed_password = await HashUtils.hash_password(password=signup_data.password)
        signup_data.password = hashed_password
        new_user = User(**signup_data.dict())
        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)
        return AuthRegisterResponse(
            id=new_user.id,
            full_name=new_user.full_name,
            email=new_user.email
        )

    async def login(self, login_data: AuthLoginRequest) -> AuthLoginResponse:
        user = await self.user_service.get_user_by_email(email=login_data.email)
        if user is None or not await HashUtils.check_password(password=login_data.password, hashed_password=user.password):
            raise_predefined_http_exception(InvalidCredentialsException())
        token = await TokenUtils.generate_token(user_id=user.id)
        return AuthLoginResponse(
            user=UserResponse(id=user.id, full_name=user.full_name, email=user.email),
            access_token=token,
            token_type="bearer"
        )

from fastapi import Depends, HTTPException, status, APIRouter

from src.schemas.auth import UserRegister, Token, UserLogin
from src.core.jwt_utils import create_access_token
from src.core.database import AsyncSessionLocal
from src.models.models import User
from src.core.database import get_db
from src.crud.user import get_user_by_email
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from passlib.context import CryptContext
import uuid

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/register", response_model=Token)
async def register_user(user_data: UserRegister):
    async with AsyncSessionLocal() as session:
        #проверка email
        result = await session.execute(select(User).where(User.email == user_data.email))
        existing_user = result.scalar_one_or_none()

        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        hashed_password = pwd_context.hash(user_data.password)

        new_user = User(
            id=uuid.uuid4(),
            username=user_data.username,
            email=user_data.email,
            description=user_data.description,
            password=hashed_password,
            created_at = datetime.utcnow(),
            last_updated_at = datetime.utcnow()
        )

        session.add(new_user)
        await session.commit()

        access_token = create_access_token(data={"sub": str(new_user.id)})

        return Token(access_token=access_token)

@router.post("/login", response_model=Token)
async def login_user(
    login_data: UserLogin,
    session: AsyncSession = Depends(get_db)
):
    user = await get_user_by_email(session, login_data.email)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email")

    if not pwd_context.verify(login_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")

    access_token = create_access_token(data={"sub": str(user.id)})
    return Token(access_token=access_token)
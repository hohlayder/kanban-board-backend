from uuid import UUID, uuid4
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext
from datetime import datetime

from src.models.models import User
from src.schemas.user import UserCreate, UserUpdate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def get_user_by_id(user_id: UUID, session: AsyncSession) -> User | None:
    result = await session.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def get_user_by_email(session: AsyncSession, email: str) -> User | None:
    result = await session.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def create_user(session: AsyncSession, user_data: UserCreate) -> User:
    hashed_password = pwd_context.hash(user_data.password)

    new_user = User(
        id=uuid4(),
        username=user_data.username,
        description=user_data.description,
        email=user_data.email,
        password=hashed_password,
        created_at=datetime.utcnow()
    )

    session.add(new_user)
    try:
        await session.commit()
        await session.refresh(new_user)
        return new_user
    except IntegrityError:
        await session.rollback()
        raise


async def update_user(
    user_id: UUID,
    user_data: UserUpdate,
    session: AsyncSession
) -> User | None:
    user = await get_user_by_id(user_id, session)
    if not user:
        return None

    update_data = user_data.model_dump(exclude_unset=True)

    if "password" in update_data:
        update_data["password"] = pwd_context.hash(update_data["password"])

    for key, value in update_data.items():
        setattr(user, key, value)

    user.last_updated_at = datetime.utcnow()
    await session.commit()
    await session.refresh(user)
    return user


async def delete_user(user_id: UUID, session: AsyncSession) -> bool:
    user = await get_user_by_id(user_id, session)
    if not user:
        return False

    await session.delete(user)
    await session.commit()
    return True


async def get_all_users(session: AsyncSession) -> list[User]:
    result = await session.execute(select(User))
    return result.scalars().all()

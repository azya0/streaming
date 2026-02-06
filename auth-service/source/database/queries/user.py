from enum import Enum

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from utils.expected import *

from ..engine import AsyncSession
from ..models import User


class CreateStatus(int, Enum):
    AlreadyExists = 1


async def create_user(session: AsyncSession, username: str, password_hash: str) -> Expected[User, CreateStatus]:
    user = User(
        username=username,
        password_hash=password_hash,
    )
    
    try:
        session.add(user)
        
        await session.commit()
        await session.refresh(user)
    except IntegrityError:
        return Error(CreateStatus.AlreadyExists)
    
    return Ok(user)


async def get_user(session: AsyncSession, id: int, actual: bool = False) -> User | None:
    if not actual:
        return await session.get(User, id)

    query = select(User).where(
        User.id == id,
        User.is_active == True
    )

    return (await session.execute(query)).scalar_one_or_none()


class DeleteStatus(Enum):
    Ok = 0
    NotFound = 1


async def delete_user(session: AsyncSession, id: int) -> Expected[None, DeleteStatus]:
    user: User | None = await get_user(session, id, actual=True)

    if user is None:
        return Error(DeleteStatus.NotFound)
    
    user.is_active = False
    
    session.add(user)
    await session.commit()
    await session.refresh(user)

    return Ok(None, DeleteStatus.Ok)


async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    query = select(User).where(
        User.username == username,
    )

    return (await session.execute(query)).scalar_one_or_none()
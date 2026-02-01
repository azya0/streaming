from enum import Enum

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from ..engine import AsyncSession
from ..models import User


class CreateStatus(Enum):
    Ok = 0
    AlreadyExists = 1


async def create_user(session: AsyncSession, user: User) -> CreateStatus:
    try:
        session.add(user)
        
        await session.commit()
        await session.refresh(user)
    except IntegrityError:
        return CreateStatus.AlreadyExists
    
    return CreateStatus.Ok


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


async def delete_user(session: AsyncSession, id: int) -> DeleteStatus:
    user: User | None = await get_user(session, id, actual=True)

    if user is None:
        return DeleteStatus.NotFound
    
    user.is_active = False
    
    session.add(user)
    await session.commit()
    await session.refresh(user)

    return DeleteStatus.Ok

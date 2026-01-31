from enum import Enum

from sqlalchemy.exc import IntegrityError

from ..engine import get_session
from ..models import User


class CreateStatus(Enum):
    Ok = 0
    AlreadyExists = 1


async def create_user(user: User) -> CreateStatus:
    try:
        async with get_session() as session:
            session.add(user)
            
            await session.commit()
            await session.refresh(user)
    except IntegrityError:
        return CreateStatus.AlreadyExists
    
    return CreateStatus.Ok

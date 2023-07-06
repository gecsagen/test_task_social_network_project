from typing import Union
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from fastapi import HTTPException
from starlette import status
from jose import JWTError
import settings
from .schemas import ShowUser
from .schemas import UserCreate
from .dals import UserDAL
from .hashing import Hasher
from session import get_db
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from .models import User


#  создание пользователя
async def _create_new_user(body: UserCreate, session) -> ShowUser:
    async with session.begin():
        user_dal = UserDAL(session)
        user = await user_dal.create_user(
            name=body.name,
            surname=body.surname,
            email=body.email,
            hashed_password=Hasher.get_password_hash(body.password),
        )
        return ShowUser(
            user_id=user.user_id,
            name=user.name,
            surname=user.surname,
            email=user.email,
            is_active=user.is_active,
        )
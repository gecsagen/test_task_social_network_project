from logging import getLogger
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from session import get_db
from user.models import User
from user.services import get_current_user_from_token

from .schemas import (
    PostCreate,
    PostDeleteResponse,
    ShowPost,
    UpdatedPostResponse,
    UpdatePostReuest,
)
from .services import (
    _create_new_post,
    _delete_post,
    _like_post,
    _remove_like_post,
    _get_post_by_id,
    _dislike_post,
    _remove_dislike_post,
    _update_post,
)

logger = getLogger(__name__)

post_router = APIRouter()


#  создание нового поста
@post_router.post("/create-post", response_model=ShowPost)
async def create_post(
    body: PostCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
) -> ShowPost:
    try:
        #  вызывается функция создания нового поста
        return await _create_new_post(body, current_user.user_id, db)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")

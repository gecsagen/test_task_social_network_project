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


#  удаление поста
@post_router.delete("/", response_model=PostDeleteResponse)
async def delete_post(
    post_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
) -> PostDeleteResponse:
    #  вызывается функция удаления поста
    deleted_post_id = await _delete_post(post_id, current_user.user_id, db)
    if deleted_post_id is None:
        raise HTTPException(
            status_code=404, detail=f"Post with id {post_id} not found."
        )
    return PostDeleteResponse(deleted_post_id=deleted_post_id)


#  получение поста по id
@post_router.get("/", response_model=ShowPost)
async def get_post_by_id(
    post_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
) -> ShowPost:
    #  вызывается функция получения поста по id
    post = await _get_post_by_id(post_id, db)
    if post is None:
        raise HTTPException(
            status_code=404, detail=f"Post with id {post_id} not found."
        )
    return post


#  обновление поста
@post_router.patch("/", response_model=UpdatedPostResponse)
async def update_post_by_id(
    post_id: UUID,
    body: UpdatePostReuest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
) -> UpdatedPostResponse:
    updated_post_params = body.dict(exclude_none=True)
    #  проверка переданы ли какие-то параметры для изменения поста
    if updated_post_params == {}:
        raise HTTPException(
            status_code=422,
            detail="At least one parameter for post update info should be provided",
        )
    #  вызывается функция получения поста по id и затем проверка наличия поста
    post = await _get_post_by_id(post_id, db)
    if post is None:
        raise HTTPException(
            status_code=404, detail=f"Post with id {post_id} not found."
        )
    try:
        #  вызывается функция обновления поста
        updated_post_id = await _update_post(
            updated_post_params=updated_post_params,
            post_id=post_id,
            author_id=current_user.user_id,
            session=db,
        )
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
    return UpdatedPostResponse(updated_post_id=updated_post_id)

from typing import Union
from uuid import UUID

from .dals import PostDAL
from .schemas import PostCreate, ShowPost


#  создание поста
async def _create_new_post(body: PostCreate, user_id: UUID, session) -> ShowPost:
    async with session.begin():
        post_dal = PostDAL(session)
        post = await post_dal.create_post(
            user_id=user_id, title=body.title, text=body.text
        )
        return ShowPost(
            id=post.id,
            user_id=post.user_id,
            title=post.title,
            text=post.text,
            time_created=post.time_created,
            time_updated=post.time_updated,
        )


#  удаление поста
async def _delete_post(post_id: UUID, author_id: UUID, session) -> Union[UUID, None]:
    async with session.begin():
        post_dal = PostDAL(session)
        deleted_post_id = await post_dal.delete_post(
            post_id=post_id, author_id=author_id
        )
        return deleted_post_id


#  обновление поста
async def _update_post(
    updated_post_params: dict, post_id: UUID, author_id: UUID, session
) -> Union[UUID, None]:
    async with session.begin():
        post_dal = PostDAL(session)
        updated_post_id = await post_dal.update_post(
            post_id=post_id, author_id=author_id, **updated_post_params
        )
        return updated_post_id


#  получение поста
async def _get_post_by_id(post_id, session) -> Union[ShowPost, None]:
    async with session.begin():
        post_dal = PostDAL(session)
        post = await post_dal.get_post_by_id(
            post_id=post_id,
        )
        if post is not None:
            return ShowPost(
                id=post.id,
                user_id=post.user_id,
                title=post.title,
                text=post.text,
                time_created=post.time_created,
                time_updated=post.time_updated,
            )


# лайк посту
async def _like_post(post_id: UUID, user_id: int, session) -> bool:
    async with session.begin():
        post_dal = PostDAL(session)
        post = await post_dal.add_like_to_post(post_id=post_id, user_id=user_id)
        return post


# убрать лайк посту
async def _remove_like_post(post_id: UUID, user_id: int, session) -> bool:
    async with session.begin():
        post_dal = PostDAL(session)
        post = await post_dal.remove_like_from_post(post_id=post_id, user_id=user_id)
        return post


# дизлайк посту
async def _dislike_post(post_id: UUID, user_id: int, session) -> bool:
    async with session.begin():
        post_dal = PostDAL(session)
        post = await post_dal.add_dislike_to_post(post_id=post_id, user_id=user_id)
        return post


# убрать дизлайк посту
async def _remove_dislike_post(post_id: UUID, user_id: int, session) -> bool:
    async with session.begin():
        post_dal = PostDAL(session)
        post = await post_dal.remove_dislike_from_post(post_id=post_id, user_id=user_id)
        return post

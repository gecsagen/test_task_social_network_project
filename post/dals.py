from typing import Union
from uuid import UUID

from sqlalchemy import and_, delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Post, post_like_table, post_dislike_table


class PostDAL:
    """Data Access Layer for operating post info"""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    # Создание поста
    async def create_post(self, user_id: int, title: str, text: str) -> Post:
        new_post = Post(user_id=user_id, title=title, text=text)
        self.db_session.add(new_post)
        await self.db_session.flush()
        return new_post

    # Удаление поста
    async def delete_post(self, post_id: UUID, author_id: UUID) -> Union[UUID, dict]:
        query = select(Post).where(Post.id == post_id)
        result = await self.db_session.execute(query)
        post = result.scalar_one_or_none()
        if post is None:
            return {"error": f"Post with id {post_id} does not exist"}

        if post.user_id != author_id:
            return {"error": "Only the author can modify the post"}

        query = update(Post).where(and_(Post.id == post_id)).returning(Post.id)
        result = await self.db_session.execute(query)
        deleted_post_id_row = result.fetchone()
        if deleted_post_id_row is not None:
            return deleted_post_id_row[0]

    # Получение поста по id
    async def get_post_by_id(self, post_id: UUID) -> Union[Post, None]:
        query = select(Post).where(Post.id == post_id)
        res = await self.db_session.execute(query)
        post_row = res.fetchone()
        if post_row is not None:
            return post_row[0]

    async def update_post(
        self, post_id: UUID, author_id: UUID, **kwargs
    ) -> Union[UUID, dict]:
        query = select(Post).where(Post.id == post_id)
        result = await self.db_session.execute(query)
        post = result.scalar_one_or_none()
        if post is None:
            return {"error": f"Post with id {post_id} does not exist"}

        if post.user_id != author_id:
            return {"error": "Only the author can modify the post"}

        query = (
            update(Post)
            .where(and_(Post.id == post_id))
            .values(kwargs)
            .returning(Post.id)
        )
        res = await self.db_session.execute(query)
        update_post_id_row = res.fetchone()
        if update_post_id_row is not None:
            return update_post_id_row[0]

    # Пример добавления лайка к посту
    async def add_like_to_post(self, post_id, user_id) -> bool:
        query = select(Post).where(Post.id == post_id)
        result = await self.db_session.execute(query)
        #  проверка не является ли пост собственным
        post = result.scalar_one_or_none()
        if post is None or post.user_id == user_id:
            return False
        # Проверяем, существует ли запись о лайке данного пользователя на указанный пост
        query = select(post_like_table).where(
            (post_like_table.c.post_id == post_id)
            & (post_like_table.c.user_id == user_id)
        )
        result = await self.db_session.execute(query)
        existing_like = result.scalar_one_or_none()

        if existing_like is None:
            await self.db_session.execute(
                post_like_table.insert().values(post_id=post_id, user_id=user_id)
            )
            await self.db_session.commit()  # Commit the changes
            return True
        return False

        # Пример удаления лайка из поста

    async def remove_like_from_post(self, post_id, user_id) -> bool:
        # Проверяем, существует ли запись о лайке данного пользователя на указанный пост
        query = select(post_like_table).where(
            (post_like_table.c.post_id == post_id)
            & (post_like_table.c.user_id == user_id)
        )
        result = await self.db_session.execute(query)
        existing_like = result.scalar_one_or_none()
        print(f"Результат: {existing_like}")

        if existing_like is not None:
            await self.db_session.execute(
                post_like_table.delete().where(
                    (post_like_table.c.post_id == post_id)
                    & (post_like_table.c.user_id == user_id)
                )
            )
            await self.db_session.commit()  # Commit the changes
            return True
        return False

    # Пример добавления дизлайка к посту
    async def add_dislike_to_post(self, post_id, user_id) -> bool:
        query = select(Post).where(Post.id == post_id)
        result = await self.db_session.execute(query)
        # проверка не является ли пост собственным
        post = result.scalar_one_or_none()
        if post is None or post.user_id == user_id:
            return False
        # Проверяем, существует ли запись о дизлайке данного пользователя на указанный пост
        query = select(post_dislike_table).where(
            (post_dislike_table.c.post_id == post_id)
            & (post_dislike_table.c.user_id == user_id)
        )
        result = await self.db_session.execute(query)
        existing_dislike = result.scalar_one_or_none()

        if existing_dislike is None:
            await self.db_session.execute(
                post_dislike_table.insert().values(post_id=post_id, user_id=user_id)
            )
            await self.db_session.commit()  # Commit the changes
            return True
        return False

    # Пример удаления дизлайка из поста
    async def remove_dislike_from_post(self, post_id, user_id) -> bool:
        # Проверяем, существует ли запись о дизлайке данного пользователя на указанный пост
        query = select(post_dislike_table).where(
            (post_dislike_table.c.post_id == post_id)
            & (post_dislike_table.c.user_id == user_id)
        )
        result = await self.db_session.execute(query)
        existing_dislike = result.scalar_one_or_none()

        if existing_dislike is not None:
            await self.db_session.execute(
                post_dislike_table.delete().where(
                    (post_dislike_table.c.post_id == post_id)
                    & (post_dislike_table.c.user_id == user_id)
                )
            )
            await self.db_session.commit()  # Commit the changes
            return True
        return False

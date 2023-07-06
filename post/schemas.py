import datetime
import uuid

from pydantic import BaseModel
from typing import Optional
from pydantic import BaseModel
from pydantic import constr


class TunedModel(BaseModel):
    class Config:
        """tells pydantic to convert even non dict obj to json"""

        orm_mode = True


class ShowPost(TunedModel):
    """Модель отображения поста"""

    id: uuid.UUID
    user_id: int
    title: str
    text: str
    time_created: datetime.datetime
    time_updated: Optional[datetime.datetime]


class PostCreate(BaseModel):
    """Модель создания поста"""

    title: str
    text: str


class PostDeleteResponse(BaseModel):
    """Модель удаления поста"""

    deleted_post_id: uuid.UUID


class UpdatePostReuest(BaseModel):
    """Модель обновления поста"""

    title: Optional[constr(min_length=1)]
    text: Optional[constr(min_length=1)]


class UpdatedPostResponse(BaseModel):
    """Модель ответа обновления поста"""

    updated_post_id: uuid.UUID
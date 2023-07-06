import uuid
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy import Text, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, ForeignKey, Integer, Table
from user.models import User
from sqlalchemy.orm import declarative_base

Base = declarative_base()

post_like_table = Table(
    "post_like",
    Base.metadata,
    Column("post_id", UUID, ForeignKey("posts.id")),
    Column("user_id", UUID, ForeignKey(User.user_id)),
)

post_dislike_table = Table(
    "post_dislike",
    Base.metadata,
    Column("post_id", UUID, ForeignKey("posts.id")),
    Column("user_id", UUID, ForeignKey(User.user_id)),
)


class Post(Base):
    """Модель поста"""

    __tablename__ = "posts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey(User.user_id))
    title = Column(String)
    text = Column(Text, nullable=False)
    time_created = Column(DateTime(timezone=True), default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

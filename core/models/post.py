from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from core.models.mixins import UserRelationMixin

from .base import Base


class Post(Base, UserRelationMixin):
    _user_back_populates = 'posts'

    title: Mapped[str] = mapped_column(String(100), unique=False)
    text: Mapped[str] = mapped_column(
        Text,
        default='',
        server_default=''
    )

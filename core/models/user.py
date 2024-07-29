from typing import TYPE_CHECKING, List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    # импортируем только при проверке типов, а при реальном
    # выполнении кода этого импорта не происходит
    from .post import Post
    from .profile import Profile


class User(Base):
    username: Mapped[str] = mapped_column(String(30), unique=True)
    posts: Mapped[List['Post']] = relationship(back_populates='user')
    profile: Mapped['Profile'] = relationship(back_populates='user')

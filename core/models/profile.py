from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from core.models.mixins import UserRelationMixin

from .base import Base


class Profile(Base, UserRelationMixin):
    _user_id_unique: bool = True
    _user_back_populates = 'profile'

    first_name: Mapped[str | None] = mapped_column(String(30))
    last_name: Mapped[str | None] = mapped_column(String(30))
    bio: Mapped[str | None]

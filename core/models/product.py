from typing import TYPE_CHECKING, List
from sqlalchemy.orm import Mapped, relationship

from .base import Base
from .order_product_ass import order_product_association

if TYPE_CHECKING:
    # импортируем только при проверке типов, а при реальном
    # выполнении кода этого импорта не происходит
    from .order import Order


class Product(Base):
    name: Mapped[str]
    price: Mapped[int]
    description: Mapped[str]

    orders: Mapped[List["Order"]] = relationship(
        secondary=order_product_association, back_populates="products"
    )

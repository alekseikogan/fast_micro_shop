from datetime import datetime
from typing import TYPE_CHECKING, List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import func

from core.models.base import Base

if TYPE_CHECKING:
    # импортируем только при проверке типов, а при реальном
    # выполнении кода этого импорта не происходит
    from .product import Product
    from .order_product_ass import OrderProductAssociation


class Order(Base):
    promocode: Mapped[str | None]
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        default=datetime.now,
    )
    # products: Mapped[List["Product"]] = relationship(
    #     secondary="order_product_association",
    #     back_populates="orders",
    # )

    products_details: Mapped[List["OrderProductAssociation"]] = relationship(
        back_populates="order"
    )

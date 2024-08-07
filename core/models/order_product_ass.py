from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

from .base import Base

if TYPE_CHECKING:
    from .order import Order
    from .product import Product


class OrderProductAssociation(Base):
    __tablename__ = "order_product_association"
    __table_args__ = (
        UniqueConstraint("order_id", "product_id", name="idx_unique_order_product"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    count: Mapped[int] = mapped_column(default=1, server_default="1")
    current_price: Mapped[int] = mapped_column(default=0, server_default="0")

    # ассоциация между текущим классом и Order
    order: Mapped["Order"] = relationship(back_populates="products_details")
    # ассоциация между текущим классом и Product
    product: Mapped["Product"] = relationship(back_populates="orders_details")


# order_product_association = Table(
#     "order_product_association",
#     Base.metadata,
#     Column("id", Integer, primary_key=True),
#     Column("order_id", ForeignKey("orders.id"), nullable=False),
#     Column("product_id", ForeignKey("products.id"), nullable=False),
#     UniqueConstraint("order_id", "product_id", name="index_unique_orders_product"),
# )


# так можно оставить, но если расширить с id, то
# лучше сделать иначе
# order_product_association = Table(
#     "order_product_association",
#     Base.metadata,
#     Column("order_id", ForeignKey("orders.id"), primary_key=True),
#     Column("product_id", ForeignKey("products.id"), primary_key=True),
# )

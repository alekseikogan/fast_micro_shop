from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class OrderProductAssociation(Base):
    __tablename__ = "order_product_association"
    __table_args__ = (
        UniqueConstraint("order_id", "product_id", name="idx_unique_order_product"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))


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

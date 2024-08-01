from sqlalchemy import Column, Table, ForeignKey, Integer, UniqueConstraint

from .base import Base


order_product_association = Table(
    "order_product_association",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("order_id", ForeignKey("orders.id"), nullable=False),
    Column("product_id", ForeignKey("products.id"), nullable=False),
    UniqueConstraint("order_id", "product_id", name="index_unique_orders_product"),
)


# так можно оставить, но если расширить с id, то
# лучше сделать иначе
# order_product_association = Table(
#     "order_product_association",
#     Base.metadata,
#     Column("order_id", ForeignKey("orders.id"), primary_key=True),
#     Column("product_id", ForeignKey("products.id"), primary_key=True),
# )

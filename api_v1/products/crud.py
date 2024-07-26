from typing import List
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.products.schemas import ProductCreate
from core.models import Product


async def get_products(session: AsyncSession) -> List[Product]:
    """Получение всех продуктов."""

    stmt = select(Product).order_by(Product.id)
    result: Result = await session.execute(stmt)
    products = result.mappings().all()
    return list(products)


async def get_product(session: AsyncSession, product_id: int) -> Product | None:
    """Получение продукта по id."""

    return await session.get(Product, product_id)


async def create_product(session: AsyncSession, product_in: ProductCreate) -> Product:
    """Создание продукта."""

    product = Product(**product_in.model_dump())
    session.add(product)
    await session.commit()
    return product

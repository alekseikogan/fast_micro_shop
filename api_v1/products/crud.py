from typing import List
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.products.schemas import ProductCreate, ProductPartialUpdate, ProductUpdate
from core.models import Product


async def get_products(session: AsyncSession) -> List[Product]:
    """GET - Получение всех продуктов."""

    stmt = select(Product).order_by(Product.id)
    result: Result = await session.execute(stmt)
    products = result.scalars().all()
    return list(products)


async def get_product(
        session: AsyncSession,
        product_id: int
) -> Product | None:
    """RETRIEVE - Получение продукта по id."""

    return await session.get(Product, product_id)


async def create_product(
        session: AsyncSession,
        product_in: ProductCreate
) -> Product:
    """CREATE - Создание продукта."""

    product = Product(**product_in.model_dump())
    session.add(product)
    await session.commit()
    return product


async def update_product(
        session: AsyncSession,
        product: Product,
        product_update: ProductUpdate | ProductPartialUpdate,
        partial: bool = False,
) -> Product:
    """PUT / PATCH - Обновление продукта."""

    for name, value in product_update.model_dump(exclude_unset=partial).items():
        setattr(product, name, value)
    await session.commit()
    return product


async def delete_product(
        session: AsyncSession,
        product: Product
) -> Product:
    """DELETE - Удаление продукта."""

    await session.delete(product)
    await session.commit()

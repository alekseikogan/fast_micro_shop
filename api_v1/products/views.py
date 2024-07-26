from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper

from . import crud
from .dependencies import product_by_id
from .schemas import Product, ProductCreate

router = APIRouter(
    prefix='/products',
    tags=['Products'],
)


@router.get('', response_model=List[Product])
async def get_products(session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    """GET - Получение всех продуктов."""

    return await crud.get_products(session=session)


@router.get('/{product_id}', response_model=Product)
async def get_product(product: Product = Depends(product_by_id)) -> Product:
    """RETRIEVE - Получение продукта по id."""

    return product


@router.post('', response_model=Product)
async def create_product(
    product_in: ProductCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    """CREATE - Создание продукта."""
    return await crud.create_product(session=session, product_in=product_in)


@router.put('/{product_id}', response_model=Product)
async def update_product(
    product: Product = Depends(product_by_id)
):
    """PUT - Обновление продукта."""
    return await crud.update_product(
        session=product.session,
        product=product,
        product_update=product,
        partial=False)


@router.put('/{product_id}', response_model=Product)
async def partial_update_product(
    product: Product = Depends(product_by_id)
):
    """PATCH - Обновление продукта."""
    return await crud.update_product(
        session=product.session,
        product=product,
        product_update=product,
        partial=True)

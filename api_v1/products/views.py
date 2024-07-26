from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper

from . import crud
from .schemas import Product, ProductCreate

router = APIRouter(
    prefix='/products',
    tags=['Products'],
)


@router.get('', response_model=List[Product])
async def get_products(session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    """Получение всех продуктов."""

    return await crud.get_products(session=session)


@router.get('/{product_id}', response_model=Product)
async def get_product(
    product_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    """Получение продукта по id."""
    product = await crud.get_product(session=session, product_id=product_id)
    if product is not None:
        return product
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'Продукт {product_id} не найден!'
    )


@router.post('', response_model=Product)
async def create_product(
    product_in: ProductCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    """Создание продукта."""
    return await crud.create_product(session=session, product_in=product_in)

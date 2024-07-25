from fastapi import Path, APIRouter
from typing import Annotated


router = APIRouter(
    prefix='/items',
    tags=['Items']
)


@router.get('')
def list_items():
    return [
        'item_1',
        'item_2',
        'item_3'
    ]


@router.get('/{item_id}')
def get_item_by_id(item_id: Annotated[int, Path(ge=1, lt=1_000_000)]):
    return {
        'id': item_id
    }

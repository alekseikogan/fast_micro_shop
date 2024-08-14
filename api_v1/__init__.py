from fastapi import APIRouter

from .products.views import router as products_router
from .auth.jwt_auth import router as jwt_auth_router

router = APIRouter()

router.include_router(router=products_router)
router.include_router(router=jwt_auth_router)

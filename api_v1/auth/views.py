from fastapi import APIRouter, Depends
from typing import Annotated
from fastapi.security import HTTPBasic, HTTPBasicCredentials

router = APIRouter(prefix="/auth", tags=["Auth"])

security = HTTPBasic()


@router.get("/basic")
def basic_auth(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
):
    return {
        "message": "Успехно получилось!",
        "username": credentials.username,
        "password": credentials.password,
    }


# username_to_password = {"admin": "admin", "alex": "StelsDelta200"}


# def get_auth_user_username(
#     credentials: Annotated[HTTPBasicCredentials, Depends(security)],
# ):
#     pass


# @router.get("/basic")
# def basic_auth_username(
#     credentials: Annotated[HTTPBasicCredentials, Depends(security)],
#     auth_username: str = Depends(...),
# ):
#     return {
#         "message": "Успехно получилось!",
#         "username": credentials.username,
#         "password": credentials.password,
#     }

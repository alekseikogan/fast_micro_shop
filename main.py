from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from api_v1 import router as router_v1
from core.config import settings
from core.models import Base, db_helper
from items_views import router as items_router
from users.views import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title='MicroShop',
    lifespan=lifespan
)

app.include_router(items_router)
app.include_router(users_router)
app.include_router(router_v1, prefix=settings.api_v1_prefix)


@app.get('/')
def index():
    return {
        'message': 'Hello index!'
    }


@app.get('/hello')
def hello(name: str = 'world'):
    name = name.strip().title()
    return {
        'message': f'Hello, {name}!'
    }


@app.post('/calc')
def calc(a: int, b: int):
    return {
        'a': a,
        'b': b,
        'sum': a + b
    }


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)

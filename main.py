import uvicorn
from fastapi import FastAPI

from items_views import router as items_router
from users.views import router as users_router

app = FastAPI()
app.include_router(items_router)
app.include_router(users_router)


@app.get('')
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


@app.get('/kalkulator')
def kalk(a: int, b: int):
    return {
        'a': a,
        'b': b,
        'sum': a + b
    }


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)

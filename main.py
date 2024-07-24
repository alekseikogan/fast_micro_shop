import uvicorn
from fastapi import FastAPI
from pydantic import EmailStr, BaseModel

app = FastAPI()


class CreateUser(BaseModel):
    email: EmailStr


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


@app.get('/items')
def list_items():
    return [
        'item_1',
        'item_2',
        'item_3'
    ]


@app.get('/items/{item_id}')
def get_item_by_id(item_id: int):
    return {
        'id': item_id
    }


@app.post('/users')
def create_user(user: CreateUser):
    return {
        'status': 'HTTP_201_CREATED',
        'email': user.email
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

from pydantic import BaseModel, ConfigDict


class ProductBase(BaseModel):
    """Для пользователя, чтобы не вводил id."""
    name: str
    price: int
    description: str


class ProductCreate(ProductBase):
    """Добавление продукта в БД."""
    pass


class ProductUpdate(ProductCreate):
    """Добавление продукта в БД."""
    pass


class ProductPartialUpdate(ProductCreate):
    """Добавление продукта в БД."""
    name: str | None = None
    price: int | None = None
    description: str | None = None


class Product(ProductBase):
    """Для админов, чтобы могли изменять id."""
    model_config = ConfigDict(from_attributes=True)
    id: int

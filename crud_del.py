import asyncio
from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from core.models import Post, Profile, User, db_helper
from core.models.order import Order
from core.models.product import Product


async def create_user(session: AsyncSession, username: str) -> User:
    user = User(username=username)
    session.add(user)
    await session.commit()
    print(f"user= {user}")
    return user


async def get_user_by_username(session: AsyncSession, username: str) -> User:
    stmt = select(User).where(User.username == username)
    user: User | None = await session.scalar(stmt)
    print(f"user = {user}")
    return user


async def create_user_profile(
    session: AsyncSession,
    user_id: int,
    first_name: str | None = None,
    last_name: str | None = None,
) -> Profile:
    profile = Profile(user_id=user_id, first_name=first_name, last_name=last_name)
    session.add(profile)
    print(f"Создан профиль для user_id = {user_id}")
    await session.commit()
    return profile


async def show_users_with_profiles(session: AsyncSession) -> List[User]:
    stmt = select(User).options((User.profile)).order_by(User.id)
    users = await session.scalars(stmt)
    i = 1
    for user in users:
        print(f"{i}.", end="")
        print(f"user = {user}")
        if user.profile:
            print(f"first_name = {user.profile.first_name}")
        i += 1


async def create_post(
    session: AsyncSession, user_id: int, title: str, text: str
) -> Post:
    post = Post(user_id=user_id, title=title, text=text)
    session.add(post)
    print(f"Создан пост для user_id = {user_id}")
    print(f"title={title}")
    print(f"text={text}")
    await session.commit()
    return post


async def get_users_with_posts(session: AsyncSession):
    stmt = select(User).options(selectinload(User.posts)).order_by(User.id)
    users = await session.scalars(stmt)

    for user in users:
        print("**" * 15)
        print(user)
        for post in user.posts:
            print(post.title)
            print(post.text)


async def get_posts_with_authors(session: AsyncSession):
    stmt = select(Post).options(joinedload(Post.user)).order_by(Post.id)
    posts = await session.scalars(stmt)

    i = 1
    for post in posts:
        print("**" * 15)
        print(f"Пост № {i}:")
        print(post.title, post.text, sep="\n")
        i += 1


async def main_relations(session: AsyncSession):
    # await create_user(session=session, username='Mark ')
    # await create_user(session=session, username='Anna')
    # await get_user_by_username(session=session, username="Mark")
    # await get_user_by_username(session=session, username="Tanya")
    # user = await get_user_by_username(session=session, username="Mark")
    # await create_user_profile(
    #     session=session,
    #     user_id=user.id,
    #     first_name="Kogan",
    #     last_name='Mark'
    # )
    # await show_users_with_profiles(session=session)
    # title = 'Пост 4'
    # text = 'Заинтересован в публикации ВАК'
    # await create_post(session=session, user_id=3, title=title, text=text)
    # await get_users_with_posts(session=session)
    # await get_posts_with_authors(session=session)
    pass


async def create_order(session: AsyncSession, promocode: str | None = None) -> Order:
    order = Order(promocode=promocode)
    session.add(order)
    await session.commit()
    return order


async def create_product(
    session: AsyncSession,
    name: str,
    price: int,
    description: str,
) -> Product:

    product = Product(
        name=name,
        price=price,
        description=description,
    )

    session.add(product)
    await session.commit()
    return product


async def create_orders_and_products(session: AsyncSession):
    order_one = await create_order(session)
    order_promo = await create_order(session, promocode="promo")

    bread = await create_product(
        session, name="Хлеб", price=40, description="Бородинский хлеб"
    )
    meat = await create_product(
        session, name="Колбаса", price=150, description="Колбаса для хлеба"
    )
    cheese = await create_product(
        session, name="Кыр сосичка", price=100, description="Чеддыр"
    )

    order_one = await session.scalar(
        select(Order)
        .where(Order.id == order_one.id)
        .options(selectinload(Order.products)),
    )
    order_promo = await session.scalar(
        select(Order)
        .where(Order.id == order_promo.id)
        .options(selectinload(Order.products)),
    )

    order_one.products.append(bread)
    order_one.products.append(meat)
    order_promo.products.append(bread)
    order_promo.products.append(cheese)

    order_promo.products = [bread, cheese]
    print("Заказы добавлены")
    await session.commit()


async def get_orders_with_products(session: AsyncSession) -> list[Order]:
    stmt = (
        select(Order)
        .options(
            selectinload(Order.products),
        )
        .order_by(Order.id)
    )
    orders = await session.scalars(stmt)

    return list(orders)


async def get_orders_with_products_through_secondary(session: AsyncSession):
    orders = await get_orders_with_products(session)
    for order in orders:
        print(order.id, order.promocode, order.created_at, "products:")
        for product in order.products:
            print("-", product.id, product.name, product.price)


async def demo_m2m(session: AsyncSession):
    orders = await get_orders_with_products(session)
    for order in orders:
        print(order.id, order.promocode, order.created_at, "products:")
        for product in order.products:
            print("-", product.id, product.name, product.price)


async def main():
    async with db_helper.session_factory() as session:
        await demo_m2m(session)


if __name__ == "__main__":
    asyncio.run(main())

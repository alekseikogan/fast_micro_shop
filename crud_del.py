import asyncio
from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from core.models import Post, Profile, User, db_helper


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
    print(f'Создан профиль для user_id = {user_id}')
    await session.commit()
    return profile


async def show_users_with_profiles(session: AsyncSession) -> List[User]:
    stmt = select(User).options(joinedload(User.profile)).order_by(User.id)
    users = await session.scalars(stmt)
    i = 1
    for user in users:
        print(f'{i}.', end='')
        print(f'user = {user}')
        if user.profile:
            print(f'first_name = {user.profile.first_name}')
        i += 1


async def create_post(session: AsyncSession, user_id: int, title: str, text: str) -> Post:
    post = Post(user_id=user_id, title=title, text=text)
    session.add(post)
    print(f'Создан пост для user_id = {user_id}')
    print(f'title={title}')
    print(f'text={text}')
    await session.commit()
    return post


async def get_users_with_posts(session: AsyncSession):
    stmt = select(User).options(joinedload(User.posts)).order_by(User.id)
    users = await session.scalars(stmt)

    for user in users.unique():
        print('*' * 15)
        print(user)
        for post in user.posts:
            print(post.title)
            print(post.text)


async def main():
    async with db_helper.session_factory() as session:
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
        await get_users_with_posts(session=session)

if __name__ == "__main__":
    asyncio.run(main())

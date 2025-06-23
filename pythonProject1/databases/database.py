from sqlalchemy import select, update
from databases.connect import async_session
from databases.models import User


async def insert_data(user_id:int, name:str):
    async with async_session() as session:
        description = select(User).where(User.user_id == user_id)
        request = await session.execute(description)
        user = request.scalars().first()
        if not user:
            work_data = User(
                user_id = int(user_id),
                user_name = name

            )
            session.add(work_data)
            await session.commit()
            return True
        else:
            return False

async def select_user(user_id:int = None, much = False):
    async with async_session() as session:
        if not much:
            description = select(User).where(User.user_id == user_id)
            request = await session.execute(description)
            return request.scalars().first()
        else:
            description = select(User)
            request = await session.execute(description)
            return request.scalars().all()

async def update_user(user_id, column: str, value: int):
    async with async_session() as session:
        descript = update(User).where(User.user_id == user_id).values({column: value})
        await session.execute(descript)
        await session.commit()
        return True
import asyncio

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean, DateTime, NullPool, Float, BigInteger, Text
from sqlalchemy.ext.asyncio import AsyncAttrs, create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import sessionmaker, relationship, DeclarativeBase
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import select
from sqlalchemy.orm import joinedload

# Настройка базы данных
# engine = create_engine('sqlite:///Data.db')
engine = create_async_engine('postgresql+asyncpg://', poolclass=NullPool, connect_args={'timeout': 15})
async_session = async_sessionmaker(engine, expire_on_commit=False)
async_session_2 = AsyncSession(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class FanslyAccount(Base):
    __tablename__ = 'fansly_accounts'
    id = Column(String, primary_key=True)
    fansly_id = Column(String)

    auth_token = Column(String)
    ct0 = Column(String)
    proxy = Column(String)
    user_agent = Column(String)

    status = Column(String)

    authorization_token = Column(String)

    username = Column(String)
    password = Column(String)
    follows = Column(Integer)
    max_follows = Column(Integer)

    warming_days = Column(Integer, default=0)




async def async_main():

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == '__main__':

    asyncio.run(async_main())
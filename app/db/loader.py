from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.config_reader import config
from app.db.models import Base, Shop, Product

engine = create_async_engine(config.postgres.dsn, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


async def fill_database() -> None:
    async with async_session() as session:
        shop = Shop(
            id=1,
            name="XXX",
            description="XXX",
            latitude=43.3,
            longitude=32.42,
            products=[
                Product(
                    id=i,
                    name="XXX",
                    description="XXX",
                ) for i in range(20)
            ],
        )
        await session.merge(shop)
        await session.commit()


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    # await fill_database()

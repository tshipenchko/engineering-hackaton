
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.data import SHOPS, PRODUCTS
from app.utils import (
    generate_random_place_in_astana,
    random_int_from_string,
    random_dict,
)
from app.config_reader import config
from app.db.models import Base, Shop, Product

engine = create_async_engine(config.postgres.dsn, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


async def fill_database() -> None:
    async with async_session() as session:
        for name, description in SHOPS.items():
            # Выбор случайного элемента из словаря
            # https://picsum.photos/seed/123/1000/1000
            latitude, longitude = generate_random_place_in_astana()

            shop = Shop(
                name=name,
                description=description,
                latitude=latitude,
                longitude=longitude,
                products=[
                    Product(
                        name=name,
                        category=category,
                        description=description,
                        image_url=f"https://picsum.photos/seed/{random_int_from_string(name)}/1000/1000",
                    )
                    for name, (category, description) in random_dict(PRODUCTS).items()
                ],
            )
            await session.merge(shop)
            await session.commit()


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    await fill_database()

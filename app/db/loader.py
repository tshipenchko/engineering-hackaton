import random

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.data import SHOPS, PRODUCTS
from app.utils import generate_random_place_in_astana
from app.config_reader import config
from app.db.models import Base, Shop, Product

engine = create_async_engine(config.postgres.dsn, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


async def fill_database() -> None:
    async with async_session() as session:
        shop_info = SHOPS
        for name, description in shop_info.items():
            product_info = PRODUCTS
            # Выбор случайного элемента из словаря
            # https://picsum.photos/seed/123/1000/1000
            for _ in range(40):
                rnd_key = random.choice(list(product_info))
                random_photo = random.randint(0, 100000)
                image_url = f"https://picsum.photos/seed/{random_photo}/1000/1000"
                latitude, longtitude = generate_random_place_in_astana()
                shop = Shop(
                    name=name,
                    description=description,
                    latitude=latitude,
                    longitude=longtitude,
                    products=[
                        Product(
                            name=rnd_key,
                            description=product_info[rnd_key][1],
                            category=product_info[rnd_key][0],
                            image_url=image_url
                        )
                    ],
                )
                await session.merge(shop)
                await session.commit()


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    # await fill_database()

from fastapi import APIRouter, Depends, Response

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.db.loader import get_session
from app.db.models import Shop

router = APIRouter(prefix="/shop")


@router.get("/")
async def get_all_shops(session: AsyncSession = Depends(get_session)):
    return (
        (await session.scalars(select(Shop).options(joinedload(Shop.products))))
        .unique()
        .all()
    )


@router.get("/{shop_id}")
async def get_shop(shop_id: int, session: AsyncSession = Depends(get_session)):
    return (
        (
            await session.scalars(
                select(Shop)
                .options(joinedload(Shop.products))
                .where(Shop.id == shop_id)
            )
        )
        .unique()
        .all()
    ) or Response(status_code=404)

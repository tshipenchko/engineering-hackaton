from fastapi import APIRouter, Depends

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.db.loader import get_session
from app.db.models import Shop

router = APIRouter(prefix="/shop")


@router.get("/")
async def get_all_shops(session: AsyncSession = Depends(get_session)):
    return (
        await session.scalars(
            select(Shop).options(joinedload(Shop.products))
        )
    ).unique().all()


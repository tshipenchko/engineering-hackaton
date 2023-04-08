from fastapi import FastAPI

from app.db.loader import create_tables
from app.routers import shop

app = FastAPI()
app.include_router(shop.router)


@app.on_event("startup")
async def on_startup():
    await create_tables()

import asyncio
from sqlalchemy import text
from src.core.database import engine

async def drop_table():
    async with engine.begin() as conn:
        # Оборачиваем SQL-запрос в text()
        await conn.execute(text("DROP TABLE IF EXISTS alembic_version"))

if __name__ == "__main__":
    asyncio.run(drop_table())
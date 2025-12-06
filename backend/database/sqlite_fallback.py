import aiosqlite
from pathlib import Path

DB_PATH = Path("backend/data/pampeano.db")

async def init_sqlite():
    DB_PATH.parent.mkdir(exist_ok=True)
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS organizaciones (
                id TEXT PRIMARY KEY,
                nombre TEXT NOT NULL,
                tipo TEXT,
                localidad TEXT,
                created_at TEXT
            )
        """)
        await db.commit()

async def get_db():
    return await aiosqlite.connect(DB_PATH)

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# DATABASE_URL = "postgresql+asyncpg://username:Password@localhost/users"
DATABASE_URL = "postgresql+asyncpg://username:Password@host.docker.internal:5432/users"

engine = create_async_engine(DATABASE_URL)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
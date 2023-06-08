from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from .config import DATABASE_URL
from sqlalchemy import inspect
from sqlalchemy.ext.declarative import declarative_base

def _declarative_constructor(self, **kwargs):
    """Don't raise a TypeError for unknown attribute names."""
    cls_ = type(self)
    for k in kwargs:
        if not hasattr(cls_, k):
            continue
        setattr(self, k, kwargs[k])

engine = create_async_engine(DATABASE_URL, echo=True)
Base = declarative_base(constructor=_declarative_constructor)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session

async def init_models():
    def get_table_names(conn):
        inspector = inspect(conn)
        return inspector.get_table_names()
    
    async with engine.begin() as conn:
        table_names = await conn.run_sync(get_table_names)
        print(table_names)
        if not table_names:
            print("Creating models...")
            await conn.run_sync(Base.metadata.create_all)
            return
        print("Tables already exist. Skipping model creation.")
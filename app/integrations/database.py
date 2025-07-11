from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config.config import settings

# Create async engine with connection pooling and performance best practices
engine = create_async_engine(
    settings.ASYNC_DATABASE_URL,
    pool_size=10,  # Number of persistent connections
    max_overflow=20,  # Extra connections allowed temporarily
    pool_timeout=30,  # Seconds to wait for a connection
    pool_recycle=1800,  # Recycle connections every 30 min
    pool_pre_ping=True,  # Check connection health
)

# Create async session factory
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, autocommit=False, autoflush=False)

# Create base class for models
Base = declarative_base()


# Dependency to get DB session
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

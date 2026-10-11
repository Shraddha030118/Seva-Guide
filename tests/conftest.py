import pytest_asyncio
from app.database import connect_to_mongo, close_mongo_connection, get_database
from app.seed import seed_database


@pytest_asyncio.fixture(autouse=True)
async def setup_test_database():
    """Connect to MongoDB on the current test event loop, seed data, and teardown cleanly."""
    await connect_to_mongo()
    db = get_database()
    await seed_database(db, force=False)
    yield
    await close_mongo_connection()

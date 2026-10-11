import logging
from typing import Any, Dict, List, Optional

try:
    from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
except ModuleNotFoundError:  # pragma: no cover - optional dependency in offline mode
    AsyncIOMotorClient = None
    AsyncIOMotorDatabase = Any

from app.config import settings

logger = logging.getLogger("sevaguide.database")


class InMemoryCollection:
    def __init__(self, name: str):
        self.name = name
        self._documents: List[Dict[str, Any]] = []

    def _matches(self, doc: Dict[str, Any], query: Optional[Dict[str, Any]]) -> bool:
        if not query:
            return True
        for key, expected in query.items():
            if key == "$and":
                if not all(self._matches(doc, part) for part in expected):
                    return False
                continue
            if key == "$or":
                if not any(self._matches(doc, part) for part in expected):
                    return False
                continue
            if key not in doc:
                return False
            actual = doc.get(key)
            if isinstance(expected, dict):
                if "$in" in expected and actual not in expected["$in"]:
                    return False
                if "$ne" in expected and actual == expected["$ne"]:
                    return False
                continue
            if actual != expected:
                return False
        return True

    async def count_documents(self, query: Optional[Dict[str, Any]] = None) -> int:
        return sum(1 for doc in self._documents if self._matches(doc, query))

    async def find_one(self, query: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        for doc in self._documents:
            if self._matches(doc, query):
                return doc
        return None

    async def create_index(self, field: str, unique: bool = False):
        return None

    async def update_one(self, query: Dict[str, Any], update: Dict[str, Any], upsert: bool = False):
        existing = await self.find_one(query)
        if existing is None:
            if not upsert:
                return type("Result", (), {"matched_count": 0, "modified_count": 0})()
            payload = dict(existing) if existing else {}
            set_fields = update.get("$set", {})
            payload.update(set_fields)
            self._documents.append(payload)
            return type("Result", (), {"matched_count": 1, "modified_count": 0, "upserted_id": payload.get("_id")})()

        set_fields = update.get("$set", {})
        existing.update(set_fields)
        return type("Result", (), {"matched_count": 1, "modified_count": 1})()


class InMemoryDatabase:
    def __init__(self, name: str):
        self.name = name
        self.collections: Dict[str, InMemoryCollection] = {}

    def __getitem__(self, name: str) -> InMemoryCollection:
        if name not in self.collections:
            self.collections[name] = InMemoryCollection(name)
        return self.collections[name]


class InMemoryMongoClient:
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.admin = type("Admin", (), {"command": lambda self, *args, **kwargs: {"ok": 1}})()

    def __getitem__(self, name: str) -> InMemoryDatabase:
        return InMemoryDatabase(name)

    def close(self):
        return None


class DatabaseManager:
    client: Optional[Any] = None
    db: Optional[Any] = None


db_manager = DatabaseManager()


async def connect_to_mongo():
    """Establish connection to MongoDB and ensure indexes."""
    logger.info(f"Connecting to MongoDB at {settings.MONGODB_URL}...")
    try:
        if AsyncIOMotorClient is None:
            raise RuntimeError("motor is not installed")

        db_manager.client = AsyncIOMotorClient(settings.MONGODB_URL)
        db_manager.db = db_manager.client[settings.DATABASE_NAME]

        await db_manager.client.admin.command('ping')
        logger.info(f"Successfully connected to MongoDB database: '{settings.DATABASE_NAME}'")
        await create_indexes()
        return
    except Exception as e:
        logger.warning(f"MongoDB not available. Falling back to in-memory database: {e}")
        db_manager.client = InMemoryMongoClient(settings.DATABASE_NAME)
        db_manager.db = db_manager.client[settings.DATABASE_NAME]
        await create_indexes()


async def close_mongo_connection():
    """Close MongoDB connection gracefully."""
    if db_manager.client:
        logger.info("Closing database connection...")
        try:
            db_manager.client.close()
        except Exception:
            pass
        logger.info("Database connection closed.")


async def create_indexes():
    """Create necessary database indexes for fast query performance."""
    if db_manager.db is None:
        return

    services_col = db_manager.db["services"]
    checklists_col = db_manager.db["checklists"]

    await services_col.create_index("slug", unique=True)
    await services_col.create_index("category")
    await checklists_col.create_index("service_slug", unique=True)
    logger.info("Database indexes ensured successfully.")


def get_database() -> Any:
    """Dependency / Helper to retrieve active database instance."""
    if db_manager.db is None:
        raise RuntimeError("Database connection has not been initialized.")
    return db_manager.db

import asyncio
import logging
import sys
import os
from datetime import datetime

# Allow running directly as a script: python app/seed.py
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from motor.motor_asyncio import AsyncIOMotorDatabase
from app.database import get_database, connect_to_mongo, close_mongo_connection
from app.seed_data import SERVICES_SEED, CHECKLISTS_SEED

logger = logging.getLogger("sevaguide.seed")


async def seed_database(db: AsyncIOMotorDatabase, force: bool = False):
    """
    Seeds initial service information and checklist data into MongoDB.
    If force=True, updates or overwrites existing seed entries.
    """
    services_col = db["services"]
    checklists_col = db["checklists"]

    count_services = await services_col.count_documents({})
    count_checklists = await checklists_col.count_documents({})

    if count_services > 0 and not force:
        logger.info(f"Database already contains {count_services} services. Skipping seed.")
        return

    logger.info("Seeding initial certificate services and checklists into MongoDB...")

    now = datetime.utcnow()

    # 1. Seed Services
    for s_data in SERVICES_SEED:
        existing = await services_col.find_one({"slug": s_data["slug"]})
        if not existing or force:
            doc = s_data.copy()
            doc["updated_at"] = now
            if not existing:
                doc["created_at"] = now

            await services_col.update_one(
                {"slug": s_data["slug"]},
                {"$set": doc},
                upsert=True
            )
            logger.info(f"Seeded Service: {s_data['slug']}")

    # 2. Seed Checklists
    for c_data in CHECKLISTS_SEED:
        existing = await checklists_col.find_one({"service_slug": c_data["service_slug"]})
        if not existing or force:
            doc = c_data.copy()
            doc["updated_at"] = now
            if not existing:
                doc["created_at"] = now

            await checklists_col.update_one(
                {"service_slug": c_data["service_slug"]},
                {"$set": doc},
                upsert=True
            )
            logger.info(f"Seeded Checklist for: {c_data['service_slug']}")

    logger.info("Database seeding completed successfully.")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    async def main():
        await connect_to_mongo()
        db = get_database()
        await seed_database(db, force=True)
        await close_mongo_connection()

    asyncio.run(main())

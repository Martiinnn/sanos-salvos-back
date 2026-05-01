"""
Sanos y Salvos — Match Repository (MongoDB)
"""

from typing import List, Optional
from bson import ObjectId
from app.config import matches_collection, reports_cache


class MatchRepository:
    """Repository for Match CRUD operations on MongoDB."""

    @staticmethod
    async def save_match(match_data: dict) -> str:
        result = await matches_collection.insert_one(match_data)
        return str(result.inserted_id)

    @staticmethod
    async def get_by_id(match_id: str) -> Optional[dict]:
        result = await matches_collection.find_one({"_id": ObjectId(match_id)})
        if result:
            result["_id"] = str(result["_id"])
        return result

    @staticmethod
    async def get_all(skip: int = 0, limit: int = 50) -> List[dict]:
        cursor = matches_collection.find().sort("created_at", -1).skip(skip).limit(limit)
        results = []
        async for doc in cursor:
            doc["_id"] = str(doc["_id"])
            results.append(doc)
        return results

    @staticmethod
    async def get_by_report(report_id: int) -> List[dict]:
        cursor = matches_collection.find({
            "$or": [
                {"report_lost_id": report_id},
                {"report_found_id": report_id},
            ]
        }).sort("score", -1)
        results = []
        async for doc in cursor:
            doc["_id"] = str(doc["_id"])
            results.append(doc)
        return results

    @staticmethod
    async def update_status(match_id: str, status: str) -> bool:
        result = await matches_collection.update_one(
            {"_id": ObjectId(match_id)},
            {"$set": {"status": status}},
        )
        return result.modified_count > 0

    @staticmethod
    async def cache_report(report_data: dict):
        """Cache report data in MongoDB for matching."""
        await reports_cache.update_one(
            {"report_id": report_data["report_id"]},
            {"$set": report_data},
            upsert=True,
        )

    @staticmethod
    async def get_active_reports(report_type: str) -> List[dict]:
        """Get cached reports by type for matching."""
        cursor = reports_cache.find({"report_type": report_type})
        results = []
        async for doc in cursor:
            doc["_id"] = str(doc["_id"])
            results.append(doc)
        return results

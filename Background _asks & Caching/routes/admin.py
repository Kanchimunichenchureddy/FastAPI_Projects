# routes/admin.py
from fastapi import APIRouter
from tasks import task_store, TaskStatus
from utils import redis_client

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/dashboard")
async def admin_dashboard():
    """
    Aggregation dashboard showing stats for background tasks and caching performance.
    """
    tasks = list(task_store.values())
    task_stats = {
        "total": len(tasks),
        "pending": sum(1 for t in tasks if t["status"] == TaskStatus.PENDING),
        "running": sum(1 for t in tasks if t["status"] == TaskStatus.RUNNING),
        "completed": sum(1 for t in tasks if t["status"] == TaskStatus.COMPLETED),
        "failed": sum(1 for t in tasks if t["status"] == TaskStatus.FAILED),
    }
    
    # Safely get Redis info
    try:
        info = await redis_client.info("stats")
        cache_stats = {
            "hits": info.get("keyspace_hits", 0),
            "misses": info.get("keyspace_misses", 0),
            "hit_rate": round(
                info.get("keyspace_hits", 0) /
                max(info.get("keyspace_hits", 0) + info.get("keyspace_misses", 0), 1) * 100,
                2
            ),
            "total_keys": await redis_client.dbsize()
        }
    except Exception:
        cache_stats = {"error": "Could not fetch Redis stats"}
    
    return {
        "tasks": task_stats,
        "cache": cache_stats,
        "recent_tasks": sorted(tasks, key=lambda t: t.get("created_at", ""), reverse=True)[:10]
    }
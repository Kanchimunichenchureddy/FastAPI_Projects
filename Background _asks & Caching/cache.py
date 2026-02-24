# cache.py (now functioning as a router)
from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy import select, func
from database import get_db, Order
from utils import cache_response

router = APIRouter(tags=["caching"])

@router.get("/expensive-query")
@cache_response(ttl=600)
async def expensive_query(request: Request, response: Response, db=Depends(get_db)):
    """
    Simulates an expensive database query that is cached in Redis.
    Note: 'request' and 'response' are required for the decorator.
    """
    result = await db.execute(select(func.count()).select_from(Order))
    return {"total_orders": result.scalar()}

@router.post("/orders/seed")
async def seed_orders(db=Depends(get_db)):
    """Seed some data for testing"""
    import random
    names = ["Laptop", "Smartphone", "Headphones", "Coffee Maker", "Keyboard"]
    for _ in range(10):
        order = Order(item_name=random.choice(names), amount=random.randint(50, 2000))
        db.add(order)
    await db.commit()
    return {"message": "10 orders seeded"}
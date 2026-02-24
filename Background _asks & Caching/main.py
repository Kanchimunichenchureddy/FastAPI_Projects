# main.py
from fastapi import FastAPI
from database import init_db
from tasks import router as tasks_router
from cache import router as cache_router
from routes.admin import router as admin_router

app = FastAPI(title="Background Tasks & Caching API")

@app.on_event("startup")
async def startup_event():
    """Initialize the database tables on startup"""
    await init_db()

# Register Routers
app.include_router(tasks_router)
app.include_router(cache_router)
app.include_router(admin_router)

@app.get("/")
def root():
    return {"message": "Hello! The Background Tasks & Caching API is running."}

@app.get("/api/status")
def status():
    return {
        "status": "running",
        "framework": "FastAPI",
        "features": ["Background Tasks", "Redis Caching", "Admin Dashboard"],
        "database": "MySQL (Async)",
        "cache_store": "Redis",
        "docs": "/docs"
    }

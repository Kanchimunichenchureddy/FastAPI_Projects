# tasks.py
import uuid
from datetime import datetime
from fastapi import APIRouter, BackgroundTasks, HTTPException
from typing import Dict, Any

router = APIRouter(tags=["background-tasks"])

# Shared task store
task_store: dict = {}

class TaskStatus:
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

async def generate_report(task_id: str, params: dict):
    """Simulate a long-running report generation."""
    task_store[task_id]["status"] = TaskStatus.RUNNING
    task_store[task_id]["started_at"] = datetime.utcnow().isoformat()
    
    try:
        import asyncio
        await asyncio.sleep(10)  # Simulate expensive work
        
        task_store[task_id]["status"] = TaskStatus.COMPLETED
        task_store[task_id]["result"] = {
            "report_url": f"/reports/{task_id}.pdf",
            "rows_processed": 15000,
            "params": params
        }
    except Exception as e:
        task_store[task_id]["status"] = TaskStatus.FAILED
        task_store[task_id]["error"] = str(e)
    
    task_store[task_id]["finished_at"] = datetime.utcnow().isoformat()

@router.post("/tasks/report")
async def create_report(params: dict, background_tasks: BackgroundTasks):
    task_id = str(uuid.uuid4())
    task_store[task_id] = {
        "id": task_id,
        "type": "report",
        "status": TaskStatus.PENDING,
        "created_at": datetime.utcnow().isoformat()
    }
    background_tasks.add_task(generate_report, task_id, params)
    return {"task_id": task_id, "status": "pending"}

@router.get("/tasks/{task_id}")
async def get_task_status(task_id: str):
    if task_id not in task_store:
        raise HTTPException(404, "Task not found")
    return task_store[task_id]
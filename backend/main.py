from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from planner import plan_task
from browser import execute_plan

app=FastAPI(title="Web Navigator AI", version="0.1.0")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173"], allow_methods=["*"], allow_headers=["*"])

class Task(BaseModel):
    instruction: str = Field(min_length=3, max_length=1000)

@app.get("/health")
def health(): return {"status":"ok"}

@app.post("/api/run")
async def run_task(task:Task):
    try:
        plan=await plan_task(task.instruction)
        results=await execute_plan(plan)
        return {"goal":plan.get("goal",task.instruction),"plan":plan,"results":results,"status":"completed"}
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))

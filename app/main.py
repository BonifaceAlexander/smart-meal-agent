from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from app.orchestrator import Orchestrator

app = FastAPI(title="smart-meal-agent")
orchestrator = Orchestrator()

class Preference(BaseModel):
    budget_cents: Optional[int] = None
    max_calories: Optional[int] = None
    macros: Optional[dict] = None  # {"p": grams, "c": grams, "f": grams}
    time_minutes: Optional[int] = None
    dietary_restrictions: Optional[List[str]] = None

class RecommendRequest(BaseModel):
    user_id: int
    pref: Preference
    limit: int = 5

class OrderRequest(BaseModel):
    user_id: int
    provider: str
    restaurant_id: str
    items: List[dict]
    address: dict

@app.get("/")
def root():
    return {"status":"ok","service":"smart-meal-agent"}

@app.post("/recommend")
async def recommend(req: RecommendRequest):
    recs = orchestrator.recommend_meals(user_id=req.user_id, pref=req.pref, limit=req.limit)
    return recs

@app.post("/order")
async def order(req: OrderRequest, background_tasks: BackgroundTasks):
    try:
        order_info = orchestrator.place_order(
            user_id=req.user_id,
            provider=req.provider,
            restaurant_id=req.restaurant_id,
            items=req.items,
            address=req.address
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    background_tasks.add_task(orchestrator.post_order_tasks, order_info)
    return order_info

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

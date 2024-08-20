from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import random

app = FastAPI()

class ResponseData(BaseModel):
    id: int
    title: str
    completed: bool

@app.get("/api/data", response_model=ResponseData)
async def get_data():
    response_data = {
        'id': random.randint(1, 100),
        'title': random.choice(['Sample Todo', 'Another Task', 'Random Activity']),
        'completed': random.choice([True, False])
    }
    return response_data

# Unauthorized and sensitive endpoint
@app.get("/api/admin")
async def get_admin_data():
    return {"admin": "This is sensitive admin data"}

# Another service running on an unauthorized port
@app.get("/api/internal")
async def get_internal_data():
    return {"internal": "This is internal data not meant for external access"}
from fastapi import FastAPI
from pydantic import BaseModel
from study_agent.agent import study_coordinator

app = FastAPI()

class ChatRequest(BaseModel):
    message: str
    history: list = []

@app.post("/chat")
async def chat(request: ChatRequest):
    result = study_coordinator.invoke({"messages": request.history + [("user", request.message)]})
    return {"response": result["messages"][-1].content}


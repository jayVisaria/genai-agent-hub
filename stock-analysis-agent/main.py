from fastapi import FastAPI
from pydantic import BaseModel
from stock_analysis.agent import stock_analysis_coordinator

app = FastAPI()

class StockRequest(BaseModel):
    ticker: str

@app.post("/analyze")
async def analyze(request: StockRequest):
    result = stock_analysis_coordinator.invoke({"ticker": request.ticker})
    return {"analysis": result}

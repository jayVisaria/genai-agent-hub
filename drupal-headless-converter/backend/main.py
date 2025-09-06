from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import json

from agents.supervisor import app

class ConvertRequest(BaseModel):
    url: str

fastapi_app = FastAPI()

@fastapi_app.post("/convert")
async def convert(request: ConvertRequest):
    async def event_stream():
        async for event in app.astream_events({"messages": [("user", request.url)]}, version="v1"):
            if event["event"] == "on_chat_model_stream":
                content = event["data"]["chunk"]["content"]
                if content:
                    yield f"data: {json.dumps({'content': content})}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")

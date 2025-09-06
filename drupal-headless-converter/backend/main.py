from fastapi import FastAPI
from fastapi.responses import StreamingResponse, FileResponse
from pydantic import BaseModel
import json
import shutil

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

@fastapi_app.get("/download")
async def download():
    shutil.make_archive("website", "zip", "generated_code")
    return FileResponse("website.zip", media_type="application/zip", filename="website.zip")


import logging
import json
import shutil
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse, FileResponse
from pydantic import BaseModel

from agents.supervisor import app

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ConvertRequest(BaseModel):
    url: str

fastapi_app = FastAPI()

@fastapi_app.post("/convert")
async def convert(request: ConvertRequest):
    logger.info(f"Received conversion request for URL: {request.url}")
    
    async def event_stream():
        try:
            async for event in app.astream_events({"messages": [("user", request.url)]}, version="v1"):
                if event["event"] == "on_chat_model_stream":
                    content = event["data"]["chunk"]["content"]
                    if content:
                        yield f"data: {json.dumps({'content': content})}\n\n"
                elif event["event"] == "on_tool_end":
                    tool_name = event["name"]
                    output = event["data"].get("output", "No output available.")
                    log_message = f"Tool '{tool_name}' finished with output: {output}"
                    logger.info(log_message)
                    yield f"data: {json.dumps({'content': f'\\n*Tool finished: {tool_name}*\\n'})}\\n\\n"

            logger.info(f"Successfully finished conversion for URL: {request.url}")
            yield f"data: {json.dumps({'content': '\\n**Conversion complete!** You can now download the generated code.'})}\\n\\n"

        except Exception as e:
            error_message = f"An error occurred during the conversion process: {str(e)}"
            logger.error(error_message)
            yield f"data: {json.dumps({'content': f'\\n**Error**: {error_message}'})}\\n\\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")

@fastapi_app.get("/download")
async def download():
    try:
        shutil.make_archive("website", "zip", "generated_code")
        return FileResponse("website.zip", media_type="application/zip", filename="website.zip")
    except Exception as e:
        logger.error(f"Failed to create or send the zip archive: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create or send the zip archive.")

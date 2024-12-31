from fastapi import FastAPI
from fastapi.responses import RedirectResponse, JSONResponse
from agents.web_agent import web_agent
from sse_starlette.sse import EventSourceResponse
import asyncio
from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str

# from api.routes import router
app = FastAPI(
    title="Phidata API",
    version="1.0",
    description="A simple api server for phidata",
    docs_url="/docs")

@app.get("/")
async def redirect_to_doc():
    return RedirectResponse(url="/docs")

@app.post("/invoke")
async def invoke_agent(request: ChatRequest):
    response = web_agent.run(request.message, stream=False)
    return JSONResponse({
        "response": response.content,
        "status": "success"
    })
async def stream_generator(agent, message):
    # response = web_agent.arun(message,stream=True)
    
    # レスポンスを小さなチャンクに分割して送信
    for chunk in agent.run(message, stream=True):
        yield {
            "event": "message",
            "data": chunk.content
        }
        # await asyncio.sleep(0.1) # 適度な間隔を開ける
async def stream_msg_generator(agent, message):
    # response = web_agent.arun(message,stream=True)
    # response = agent.run(message, stream=True,stream_intermediate_steps=True)
    for chunk in agent.run(message, stream=True,stream_intermediate_steps=True):
        
        # if "Completed" in chunk.model_dump()["event"]:
        #     yield {
        #         "event": chunk.model_dump()["event"],
        #         "data": chunk.model_dump()["content"]
        #     }
        if chunk.model_dump()["event"]=="RunResponse":
            yield {
                "event": chunk.model_dump()["event"],
                "data": chunk.model_dump()["content"]
            }
        else:
            yield {
                "event": chunk.model_dump()["event"],
                "data": "=================\n\n"
            }
    yield {
        "event": "messages",
        "data": chunk.model_dump()["messages"]
        }
    # messagesの配列から、contentがあるメッセージのみを順番に送信


@app.post("/stream")
async def stream_agent(request: ChatRequest) -> EventSourceResponse:
    return EventSourceResponse(stream_generator(web_agent, request.message))

@app.post("/stream-messages")
async def stream_messages(request: ChatRequest):
    return EventSourceResponse(stream_msg_generator(web_agent, request.message))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
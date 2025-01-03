from fastapi import FastAPI
from fastapi.responses import RedirectResponse, JSONResponse
from agents.search_agent import agent as web_agent
from sse_starlette.sse import EventSourceResponse
import asyncio
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

class ChatRequest(BaseModel):
    message: str

# from api.routes import router
app = FastAPI(
    title="PydanticAI API",
    version="1.0",
    description="A simple api server for pydanticai",
    docs_url="/docs")

# CORSミドルウェアの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # フロントエンドのオリジンを指定
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def redirect_to_doc():
    return RedirectResponse(url="/docs")

@app.post("/webagent/invoke")
async def invoke_agent(request: ChatRequest):
    response = await invoke_generator(web_agent, request.message)
    return JSONResponse({
        "response": response,
        "status": "success"
    })

@app.post("/webagent/stream")
async def stream_agent(request: ChatRequest) -> EventSourceResponse:
    return EventSourceResponse(stream_generator(web_agent, request.message))

@app.post("/baseagent/invoke")
async def invoke_agent(request: ChatRequest):
    response = await invoke_generator(web_agent, request.message)
    return JSONResponse({
        "response": response,
        "status": "success"
    })

@app.post("/baseagent/stream")
async def stream_agent(request: ChatRequest) -> EventSourceResponse:
    return EventSourceResponse(stream_generator(web_agent, request.message))

async def invoke_generator(agent, message):
    response = await agent.run(message)
    return response.data

async def stream_generator(agent, message):
    # response = web_agent.arun(message,stream=True)
    
    # レスポンスを小さなチャンクに分割して送信
        async with agent.run_stream(message) as result:
            async for text in result.stream(debounce_by=0.01):
                # text here is a `str` and the frontend wants
                # JSON encoded ModelResponse, so we create one
                yield {
                    "event": "message",
                    "data": text
                }




# @app.post("/stream-messages")
# async def stream_messages(request: ChatRequest):
#     return EventSourceResponse(stream_msg_generator(web_agent, request.message))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

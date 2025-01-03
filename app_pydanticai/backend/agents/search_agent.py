# %%
from pydantic_ai import Agent, RunContext
from pydantic import BaseModel
from typing import List
import aiohttp
import json
import logfire
import os
from duckduckgo_search import DDGS
from dotenv import load_dotenv
from pydantic_ai.tools import ToolDefinition
from tavily import AsyncTavilyClient
load_dotenv("/home/ubuntu/workspace/python_development_baseline/.env")
logfire.configure(send_to_logfire='if-token-present')
# %%
# DuckDuckGoの検索APIを使用するエージェント
agent = Agent(
    "openai:gpt-4o-mini",
    deps_type=bool,
)

async def check_authorization(ctx: RunContext[bool], tool_def: ToolDefinition):
    if ctx.deps:
        return tool_def

@agent.tool(prepare=check_authorization)
async def tavily_websearch(ctx: RunContext, question) -> str:
    """Search the web for the answer to the question about technology topic."""
    api_key = os.getenv("Tavily_API_KEY")
    tavily_client = AsyncTavilyClient(api_key)
    answer = await tavily_client.qna_search(query=question)
    return answer

@agent.tool()
def ddg_websearch(ctx: RunContext, question) -> str:
    """Search the web for the answer to the question about cultural topic."""
    ddg_client = DDGS()
    answer = ddg_client.text(
        keywords=question)
    return answer

# %%
if __name__ == "__main__":
    import nest_asyncio
    nest_asyncio.apply()
    result = agent.run_sync("AIエージェントフレームワークのはやりを教えて", deps=True)
    print(result.data)
# %%
if __name__ == "__main__":
    import nest_asyncio
    nest_asyncio.apply()
    result = agent.run_sync("最近注目されている健康的な文化的な習慣がある国について教えて", deps=True)
    print(result.data)
# %%

# %%
if __name__ == "__main__":
    import nest_asyncio
    import asyncio
    nest_asyncio.apply()
    async def main():
        async with agent.run_stream('AIエージェントフレームワークのはやりを教えて') as response:
            print(await response.get_data())
    # asyncio.run(main())
# %%

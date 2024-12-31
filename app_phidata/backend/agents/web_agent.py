# -*- coding: utf-8 -*-
# %%
from phi.agent import Agent
from phi.model.openai import OpenAIChat
from phi.storage.agent.sqlite import SqlAgentStorage
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.yfinance import YFinanceTools
from dotenv import load_dotenv

# from phi.playground import Playground, serve_playground_app

load_dotenv("/home/ubuntu/workspace/python_development_baseline/.env")
web_agent = Agent(
    name="Web Agent",
    model=OpenAIChat(id="gpt-4o-mini",temperature=0),
    telemetry=False,
    add_references=True,
    
    tools=[DuckDuckGo()],
    instructions=["常にソースを含める", "見つからない場合クエリを変えて再検索する"],
    show_tool_calls=True,
    markdown=True,
)

# finance_agent = Agent(
#     name="Finance Agent",
#     model=OpenAIChat(id="gpt-4o-mini"),
#     tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, company_info=True, company_news=True)],
#     instructions=["Use tables to display data"],
#     storage=SqlAgentStorage(table_name="finance_agent", db_file="agents.db"),
#     add_history_to_messages=True,
#     markdown=True,
# )


# %%
if __name__ == "__main__":
    from phi.agent import Agent, RunResponse
    from typing import Iterator
    from rich.pretty import pprint
    run_stream: Iterator[RunResponse] = web_agent.run("AIの最新動向をおしえて",stream=True, stream_intermediate_steps=True)
    count = 0
    for chunk in run_stream:
        count += 1
        if chunk.model_dump()["event"] == "RunResponse":
        # if "Completed" in chunk.model_dump()["event"]:
            pprint(chunk.model_dump(exclude={"messages"}))
            # pprint(chunk.model_dump()["event"])
            print("---" * 20)
        


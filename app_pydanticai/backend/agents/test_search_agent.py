import asyncio
from pprint import pprint
from search_agent import tavily_websearch, ddg_websearch

async def main():
    print("\n=== Testing tavily_websearch (technology topic) ===")
    tech_result = await tavily_websearch(None, "最新のAI技術トレンド")
    print("\nSearch Results:")
    pprint(tech_result)
    
    print("\n=== Testing ddg_websearch (cultural topic) ===")
    culture_result = ddg_websearch(None, "日本の伝統文化")
    print("\nSearch Results:")
    pprint(culture_result)

if __name__ == "__main__":
    asyncio.run(main())

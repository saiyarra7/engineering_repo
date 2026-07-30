"""
Raw MCP client - connects to ci_obesity_mcp_server.py over stdio and calls tools directly.
No LLM involved here; this just proves the server works and shows the wire protocol in action.

Run:
  uv add mcp
  uv run ci_obesity_client_raw.py
"""

import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "ci_obesity_mcp_server.py"],  # path to the server script
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # 1. Discover what tools the server exposes
            tools_result = await session.list_tools()
            print("Available tools:")
            for t in tools_result.tools:
                print(f"  - {t.name}: {t.description}")
            print()

            # 2. Call a tool directly (you decide, no LLM in the loop)
            result = await session.call_tool(
                "get_competitor_pipeline", {"company": "Eli Lilly"}
            )
            print("get_competitor_pipeline result:")
            print(result.content[0].text)
            print()

            result = await session.call_tool(
                "search_clinical_trials",
                {"condition": "obesity", "sponsor": "Novo Nordisk", "max_results": 3},
            )
            print("search_clinical_trials result:")
            print(result.content[0].text)


if __name__ == "__main__":
    asyncio.run(main())

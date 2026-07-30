"""
LLM-orchestrated MCP client - Claude decides which server tools to call based on a
natural-language query, then synthesizes the final answer.

This is the actual point of MCP: you don't write "if user asks about pipeline, call X".
The model reads the tool schemas and chooses.

Run:
  uv add mcp anthropic
  export ANTHROPIC_API_KEY=...
  uv run ci_obesity_client_llm.py
"""

import asyncio
import os
from anthropic import Anthropic
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])


def mcp_tools_to_anthropic_schema(mcp_tools) -> list[dict]:
    """Convert MCP tool definitions to Anthropic API tool schema."""
    return [
        {
            "name": t.name,
            "description": t.description or "",
            "input_schema": t.inputSchema,
        }
        for t in mcp_tools
    ]


async def run_query(user_query: str):
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "ci_obesity_mcp_server.py"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools_result = await session.list_tools()
            anthropic_tools = mcp_tools_to_anthropic_schema(tools_result.tools)

            messages = [{"role": "user", "content": user_query}]

            # Agentic loop: let Claude call tools until it's done
            while True:
                response = client.messages.create(
                    model="claude-sonnet-4-6",
                    max_tokens=1500,
                    tools=anthropic_tools,
                    messages=messages,
                )

                # Print any text Claude produced this turn
                for block in response.content:
                    if block.type == "text":
                        print("\n[Claude]:", block.text)

                if response.stop_reason != "tool_use":
                    break  # Claude is done, no more tool calls

                messages.append({"role": "assistant", "content": response.content})

                tool_results = []
                for block in response.content:
                    if block.type == "tool_use":
                        print(f"\n[Calling MCP tool] {block.name}({block.input})")
                        result = await session.call_tool(block.name, block.input)
                        tool_results.append(
                            {
                                "type": "tool_result",
                                "tool_use_id": block.id,
                                "content": result.content[0].text,
                            }
                        )

                messages.append({"role": "user", "content": tool_results})


if __name__ == "__main__":
    query = (
        "Compare Eli Lilly and Novo Nordisk's obesity drug pipelines, "
        "and check for any active Phase 3 obesity trials from Novo Nordisk."
    )
    asyncio.run(run_query(query))

# mcp_router.py
import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from openai import OpenAI

openai_client = OpenAI()

async def run_mcp_intent_router(user_query: str):
    # 1. Define Server process parameters
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "mcp_server.py"]
    )

    # 2. Establish connection to MCP Server
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # 3. Dynamic Tool Discovery via Protocol Handshake
            mcp_tools_response = await session.list_tools()
            
            # Map MCP schema definition to LLM Tool Call Format
            formatted_tools = [
                {
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": tool.inputSchema
                    }
                }
                for tool in mcp_tools_response.tools
            ]

            messages = [
                {
                    "role": "system",
                    "content": "You are an intent routing assistant. Analyze the user request and call the appropriate specialized tool."
                },
                {"role": "user", "content": user_query}
            ]

            # 4. LLM classifies intent and selects the tool probabilistically
            response = openai_client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                tools=formatted_tools,
                tool_choice="auto"
            )

            response_message = response.choices[0].message
            tool_calls = response_message.tool_calls

            if not tool_calls:
                print("Intent Classification: No tool required. direct answer:")
                print(response_message.content)
                return

            # 5. Route Execution back to the MCP Server
            for tool_call in tool_calls:
                intent_name = tool_call.function.name
                intent_args = json.loads(tool_call.function.arguments)

                print(f"\n[Detected Intent]: {intent_name}")
                print(f"[Extracted Arguments]: {intent_args}")

                # Protocol RPC execution call
                execution_result = await session.call_tool(intent_name, arguments=intent_args)
                raw_output = execution_result.content[0].text
                
                print(f"[MCP Server Execution Output]: {raw_output}\n")


if __name__ == "__main__":
    # Test cases demonstrating intent routing
    asyncio.run(run_mcp_intent_router("What was the total revenue for region East last quarter?"))
    asyncio.run(run_mcp_intent_router("What is our company remote work expense policy?"))
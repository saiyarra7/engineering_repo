import asyncio
from fastmcp import Client

async def run_ci_agent():
    # -------------------------------------------------------------------------
    # 1. PROCESS SPAWNING & HANDSHAKE
    # Spawns 'ci_server.py' as a subprocess.
    # Automatically initiates the MCP handshake (initialization, capability 
    # exchange, and protocol version negotiation) over standard I/O (stdio).
    # -------------------------------------------------------------------------
    async with Client("python ci_server.py") as client:
        
        # ---------------------------------------------------------------------
        # 2. DYNAMIC TOOL DISCOVERY
        # Client sends a `tools/list` request over stdio.
        # The server returns registered tools, docstrings, and JSON schemas.
        # ---------------------------------------------------------------------
        tools = await client.list_tools()
        print("=== MCP Handshake Complete ===")
        print(f"Discovered Tools: {[t.name for t in tools]}\n")
        
        target_compound = "ONCO-402"
        
        # ---------------------------------------------------------------------
        # 3. TOOL EXECUTION 1 (Trial Registry)
        # Client calls `tools/call` via JSON-RPC.
        # FastMCP handles payload serialization and deserialization.
        # ---------------------------------------------------------------------
        print(f"Executing: Querying clinical trial status for {target_compound}...")
        trial_data = await client.call_tool(
            "get_competitor_trial_status", 
            {"compound_id": target_compound}
        )
        print("Trial Data Received:", trial_data)
        
        # ---------------------------------------------------------------------
        # 4. TOOL EXECUTION 2 (Patent Expiry)
        # ---------------------------------------------------------------------
        print(f"\nExecuting: Querying patent expiry for {target_compound}...")
        patent_data = await client.call_tool(
            "get_patent_expiry", 
            {"compound_id": target_compound}
        )
        print("Patent Data Received:", patent_data)

        # ---------------------------------------------------------------------
        # 5. SYNTHESIS & REPORTING
        # ---------------------------------------------------------------------
        print("\n=== Competitive Threat Assessment ===")
        print(f"Asset: {target_compound} ({trial_data.get('sponsor')})")
        print(f"Trial State: {trial_data.get('phase')} ({trial_data.get('status')})")
        print(f"Patent Cliff Risk: {patent_data.get('patent_cliff_risk')} ({patent_data.get('years_remaining')} years left)")

if __name__ == "__main__":
    asyncio.run(run_ci_agent())
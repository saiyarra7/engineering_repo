from fastmcp import FastMCP

# -----------------------------------------------------------------------------
# 1. INITIALIZE SERVER
# FastMCP manages the underlying JSON-RPC 2.0 protocol and stdio/SSE transports.
# -----------------------------------------------------------------------------
mcp = FastMCP("Competitive Intelligence Server")

# Simulated internal databases (In production, replace with real DB/API queries)
COMPETITOR_TRIALS_DB = {
    "ONCO-402": {
        "sponsor": "OncoPharm Corp",
        "phase": "Phase 3",
        "indication": "Non-Small Cell Lung Cancer",
        "status": "Recruiting",
        "primary_completion_date": "2027-04-15",
        "status_last_updated": "2026-06-10"
    },
    "NEURO-88": {
        "sponsor": "NeuroGen Bio",
        "phase": "Phase 2",
        "indication": "Alzheimer's Disease",
        "status": "Terminated (Efficacy Not Met)",
        "primary_completion_date": "N/A",
        "status_last_updated": "2026-07-01"
    }
}

PATENT_REGISTRY_DB = {
    "ONCO-402": {"patent_number": "US-982104-B2", "expiry_year": 2029, "exclusivity_type": "NCE"},
    "NEURO-88": {"patent_number": "US-871024-B1", "expiry_year": 2033, "exclusivity_type": "Biologic"}
}


# -----------------------------------------------------------------------------
# 2. DEFINE MCP TOOLS
# The @mcp.tool decorator registers functions as exposed tools.
# - Function docstrings become the tool description sent to the LLM context.
# - Python type hints (e.g. compound_id: str) automatically generate JSON Schemas.
# -----------------------------------------------------------------------------

@mcp.tool
def get_competitor_trial_status(compound_id: str) -> dict:
    """Fetch real-time trial phase, status, and completion timeline for a competitor asset."""
    asset = COMPETITOR_TRIALS_DB.get(compound_id.upper())
    if not asset:
        return {"error": f"Compound '{compound_id}' not found in trial registry."}
    return asset


@mcp.tool
def get_patent_expiry(compound_id: str) -> dict:
    """Retrieve patent expiration dates and exclusivity status for a competitor asset."""
    patent = PATENT_REGISTRY_DB.get(compound_id.upper())
    if not patent:
        return {"error": f"Compound '{compound_id}' not found in patent registry."}
    
    current_year = 2026
    years_remaining = patent["expiry_year"] - current_year
    
    return {
        **patent,
        "years_remaining": max(0, years_remaining),
        "patent_cliff_risk": "HIGH" if years_remaining <= 3 else "LOW"
    }


# -----------------------------------------------------------------------------
# 3. START TRANSPORT LISTENER
# Starts the stdio listener process. Listens on stdin for JSON-RPC messages 
# from clients and responds over stdout.
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    mcp.run()
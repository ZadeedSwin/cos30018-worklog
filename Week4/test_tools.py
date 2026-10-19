"""Section 4.5 - test the MCP tools with no agent (uses no API key)."""
from smolagents import MCPClient

SERVER = {"url": "http://127.0.0.1:8765/mcp", "transport": "streamable-http"}

with MCPClient(SERVER, structured_output=True) as tools:
    for t in tools:
        print(t.name, "|", t.inputs)
    d = {t.name: t for t in tools}
    print(d["list_products"]())
    print(d["get_revenue"](product_id="P-200", year=2025))
    print(d["get_returns"](product_id="P-200", year=2025))

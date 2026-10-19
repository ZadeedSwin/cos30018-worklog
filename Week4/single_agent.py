"""
COS30018 Week 4, Part 2 - the Week 2 single agent, now using MCP tools.
This is the baseline you compare the multi-agent system against.
Start sales_mcp_server.py in another terminal first.
"""
from smolagents import CodeAgent, MCPClient
from model_config import get_model

MCP_SERVER = {"url": "http://127.0.0.1:8765/mcp", "transport": "streamable-http"}

TASK = ("For each product, get total revenue for 2024 and 2025, rank the products by "
        "percentage growth, and save the ranking as growth_2025.md.")


def build_single_agent(tools):
    """One agent, all four MCP tools. Same shape as Week 2."""
    return CodeAgent(
        tools=list(tools),
        model=get_model("manager"),
        additional_authorized_imports=["statistics", "math", "json"],
        max_steps=15,
        return_full_result=True,
    )


if __name__ == "__main__":
    with MCPClient(MCP_SERVER, structured_output=True) as tools:
        print("Tools from MCP:", [t.name for t in tools])
        agent = build_single_agent(tools)
        result = agent.run(TASK)
        print("\n=== ANSWER ===")
        print(result.output)
        print("steps:", len(result.steps))
        print("tokens:", result.token_usage)
        print("seconds:", round(result.timing.duration, 1))

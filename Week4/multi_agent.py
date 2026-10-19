"""
COS30018 Week 4, Part 3 - a manager agent with three sub-agents.
Each sub-agent can do one thing and cannot do the others:
  data_agent    gets data, cannot compute
  analyst_agent computes, cannot get data
  report_agent  writes files, does no analysis
The manager can do none of them. It can only plan and delegate.
Start sales_mcp_server.py in another terminal first.
"""
from smolagents import CodeAgent, MCPClient, ToolCallingAgent
from model_config import get_model

MCP_SERVER = {"url": "http://127.0.0.1:8765/mcp", "transport": "streamable-http"}


def names_a_product(final_answer, memory, agent=None) -> bool:
    """Reject an answer that does not mention a product id."""
    if "P-" not in str(final_answer):
        raise ValueError("Your answer names no product id. Ask data_agent again.")
    return True


def build_multi_agent(tools):
    t = {tool.name: tool for tool in tools}
    data_agent = ToolCallingAgent(
        tools=[t["list_products"], t["get_revenue"], t["get_returns"]],
        model=get_model("worker"),
        max_steps=8,
        name="data_agent",
        description=("Gets raw records from the shop's MCP server: the product list, "
                     "revenue for a product and year, and returns. Ask it for numbers, "
                     "not for analysis. If a record is missing it says so."),
    )
    analyst_agent = CodeAgent(
        tools=[],
        model=get_model("worker"),
        additional_authorized_imports=["statistics", "math", "json"],
        max_steps=8,
        name="analyst_agent",
        description=("Does arithmetic and statistics on numbers you put in the task text: "
                     "totals, growth rates, rankings. It cannot reach the data, so you "
                     "must paste the numbers into the task."),
    )
    report_agent = ToolCallingAgent(
        tools=[t["save_report"]],
        model=get_model("worker"),
        max_steps=6,
        name="report_agent",
        description=("Writes a finished markdown report to disk. Give it a file name and "
                     "the findings. It does no analysis."),
    )
    manager = CodeAgent(
        tools=[],  # no tools, so it has to delegate
        model=get_model("manager"),
        managed_agents=[data_agent, analyst_agent, report_agent],
        additional_authorized_imports=["json"],
        max_steps=12,
        planning_interval=4,
        final_answer_checks=[names_a_product],
        return_full_result=True,
    )
    return manager, [data_agent, analyst_agent, report_agent]


def total_tokens(manager, subs):
    """RunResult.token_usage counts the manager only. Add the sub-agents yourself."""
    agents = [manager, *subs]
    return (sum(a.monitor.get_total_token_counts().input_tokens for a in agents),
            sum(a.monitor.get_total_token_counts().output_tokens for a in agents))


TASK = ("For each product, get total revenue for 2024 and 2025, rank the products by "
        "percentage growth, and save the ranking as growth_2025.md.")

if __name__ == "__main__":
    with MCPClient(MCP_SERVER, structured_output=True) as tools:
        manager, subs = build_multi_agent(tools)
        result = manager.run(TASK)
        print("\n=== ANSWER ===")
        print(result.output)
        print("manager steps:", len(result.steps))
        for a in subs:
            print(f"  {a.name}: {len(a.memory.steps)} steps")
        tin, tout = total_tokens(manager, subs)
        print(f"whole system tokens: in={tin} out={tout}")
        print("seconds:", round(result.timing.duration, 1))

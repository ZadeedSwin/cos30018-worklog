"""
COS30018 Week 4, Part 4 - the comparison harness.
Runs three tasks through the single agent and through the manager + sub-agents.
Records steps, seconds and tokens for each, and writes results.csv.
Start sales_mcp_server.py in another terminal first.
"""
import csv
import time
from smolagents import MCPClient
from multi_agent import MCP_SERVER, build_multi_agent, total_tokens
from single_agent import build_single_agent

TASKS = [
    ("T1", "Which product had the highest total revenue in 2025, and what was the total?"),
    ("T2", "For 2025, give total returns for every product where returns are tracked, "
           "and say clearly which products have no returns data."),
    ("T3", "For each product, get total revenue for 2024 and 2025, rank the products by "
           "percentage growth, and save the ranking as growth_2025.md."),
]

ANSWER_KEY = {
    "T1": "P-200 Riverbend Kayak, 688",
    "T2": "P-100 = 29, P-300 = 26. No data for P-200.",
    "T3": "P-300 +15.1%, P-100 +10.7%, P-200 +6.8%",
}


def run_one(agent_pair, task):
    """agent_pair is (main_agent, sub_agents). sub_agents is [] for the single agent."""
    main, subs = agent_pair
    start = time.time()
    result = main.run(task)
    if subs:
        tin, tout = total_tokens(main, subs)
        steps = len(main.memory.steps) + sum(len(a.memory.steps) for a in subs)
    else:
        usage = main.monitor.get_total_token_counts()
        tin, tout = usage.input_tokens, usage.output_tokens
        steps = len(main.memory.steps)
    return {"output": str(result.output), "steps": steps,
            "seconds": round(time.time() - start, 1),
            "in_tokens": tin, "out_tokens": tout}


def main():
    rows = []
    with MCPClient(MCP_SERVER, structured_output=True) as tools:
        for task_id, task in TASKS:
            for system in ("single", "multi"):
                print(f"\n##### {task_id} / {system} #####")
                pair = ((build_single_agent(tools), [])
                        if system == "single" else build_multi_agent(tools))
                try:
                    record = run_one(pair, task)
                    record["error"] = ""
                except Exception as exc:
                    record = {"output": "", "steps": "", "seconds": "", "in_tokens": "",
                              "out_tokens": "", "error": f"{type(exc).__name__}: {exc}"}
                record.update(task_id=task_id, system=system,
                              expected=ANSWER_KEY[task_id], correct="")
                rows.append(record)
                print(record["output"][:250] or record["error"])
    fields = ["task_id", "system", "correct", "steps", "seconds", "in_tokens",
              "out_tokens", "expected", "output", "error"]
    with open("results.csv", "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    print("\nWrote results.csv. Fill in the 'correct' column yourself: y or n.")


if __name__ == "__main__":
    main()

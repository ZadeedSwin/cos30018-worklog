# COS30018 Week 4 - MCP + Multi-Agent Systems

Yarra Outdoors MCP server, a single baseline agent, and a manager with three sub-agents (data / analyst / report).

## Run
```
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
cp .env.example .env    # add your GEMINI_API_KEY (never commit .env)
python sales_mcp_server.py        # terminal 2, leave running
python single_agent.py            # Part 2 baseline, run 3 times
python multi_agent.py             # Part 3
python compare.py                 # Part 4 -> results.csv
python make_table.py              # prints the comparison table
```

## Status (19 Oct 2026)
- [x] Part 1: MCP server written and tested (Section 4.5: all 4 tools discovered)
- [x] Parts 2-4: code written (`single_agent.py`, `multi_agent.py`, `compare.py`)
- [ ] Agent runs: blocked, because the model API returns 401 (Gemini `AQ.` key unsupported; HF token invalid)
- [ ] `results.csv`, `reports/growth_2025.md`, manager-run screenshot, final `comparison.md`

## Dependency fixes vs the lab sheet
- `mcp<2`: mcp 2.x renamed `FastMCP` to `MCPServer`
- `websockets`: needed by smolagents' MCP adapter after the downgrade
- `openai`: needed by `OpenAIModel` (Gemini's OpenAI-compatible endpoint)

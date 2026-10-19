# COS30018 Week 4 - Checkpoint answers

> Answers marked **[ADD FROM YOUR RUN]** need a line from your own transcript or numbers. Everything else is conceptual and ready to submit.

**1. Which sub-agent handled which part of the task, and how did the manager decide? Point at the line in the transcript.**
`data_agent` fetched the product list and the six revenue arrays. `analyst_agent` did the totals, growth rates and ranking. `report_agent` saved `growth_2025.md`. The manager decided from each sub-agent's `description`, which smolagents shows to it as if it were a tool: "Gets raw records..." routes to data, "Does arithmetic..." routes to analyst, "Writes a finished markdown report..." routes to report. **[ADD FROM YOUR RUN]** quote the manager line such as `rows = data_agent(task='...')` from your transcript.

**2. How is this different from the single agent with multiple tools you built in Week 2? One difference in structure, one in your numbers.**
Structure: in Week 2 one agent held every tool and the whole context. Here the manager has no tools and each sub-agent has a different capability, so work is delegated and each context stays small. Numbers: **[ADD FROM YOUR RUN]** for example the multi-agent system used TBD times the tokens and TBD more steps than the single agent on T3.

**3. What changed in your agent code when tools moved from local functions to MCP? What does that tell you about what MCP is for?**
Only where the tools come from changed: `tools=list(tools)` from an `MCPClient` instead of `@tool` functions in the same file. The agent loop, model and prompts stayed the same. MCP is plumbing: it lets a tool live in its own process, in any language, be discovered at run time and be shared by URL instead of by copying code. It does not make the agent smarter.

**4. `analyst_agent` has no tools. Why is it still an agent?**
It is a `CodeAgent`, so it still runs a loop of reasoning, writing Python and observing the result, and it decides when to stop and return. Its "tool" is the sandboxed Python executor, which runs the arithmetic for real instead of predicting it. It is an agent because of the loop and autonomy, not because it has external tools.

**5. When the returns data was missing, what did your system do, and which mechanism caused that?**
The server returned a readable error ("P-200 is not sold online, so returns are not tracked.") instead of raising, so the agent could read it and report it instead of inventing a number. `max_steps` stops any looping, the manager (a `CodeAgent`) can wrap a sub-agent call in `try/except`, and `final_answer_checks` can reject a bad answer. **[ADD FROM YOUR RUN]** state what your system actually answered for P-200 on T2.

**6. From your numbers: would you use the manager design for T1? Justify it with a number.**
Expected answer: no. T1 is a single lookup, so delegation is pure overhead. **[ADD FROM YOUR RUN]** justify with your T1 rows, for example multi used TBD tokens and TBD seconds versus TBD and TBD for single, with the same correct answer.

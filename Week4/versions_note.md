# Versions and models used

- Python: 3.12.10
- smolagents: 1.26.0 (lab tested with 1.26.0)
- mcp: 1.30.0 (lab tested with 1.27.0). pip first installed mcp 2.3.0, which renamed FastMCP to MCPServer, so it is pinned to mcp<2 in requirements.txt.
- Manager model id: `gemini-3.7-flash`
- Worker model id (main runs): `gemini-3.5-flash-lite`
- Worker model id (Section 7.4 experiment): `gemini-3.7-flash`
- Backend: Gemini via the OpenAI-compatible endpoint (`MODEL_BACKEND=gemini`)

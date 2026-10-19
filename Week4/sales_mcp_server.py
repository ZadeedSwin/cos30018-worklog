"""
COS30018 Week 4 - a minimal MCP server.
Serves four tools over MCP for a fictional shop, "Yarra Outdoors".
The data is fake and lives in this file. No database, no internet, no API key.

Run it in its own terminal:
    python sales_mcp_server.py

It listens on http://127.0.0.1:8765/mcp
"""
from pathlib import Path
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("yarra-outdoors", host="127.0.0.1", port=8765)

# Revenue is in AUD thousands. One number per month, Jan to Dec.
PRODUCTS = {
    "P-100": {"name": "Alpine 2P Tent", "category": "shelter"},
    "P-200": {"name": "Riverbend Kayak", "category": "watercraft"},
    "P-300": {"name": "Trailhead Backpack 45L", "category": "packs"},
}

REVENUE = {
    2025: {
        "P-100": [62, 58, 51, 44, 39, 35, 33, 38, 49, 61, 74, 88],
        "P-200": [95, 88, 70, 52, 33, 21, 18, 24, 41, 63, 82, 101],
        "P-300": [40, 42, 45, 44, 46, 45, 47, 52, 58, 61, 66, 70],
    },
    2024: {
        "P-100": [55, 52, 47, 41, 36, 32, 30, 34, 44, 55, 66, 79],
        "P-200": [90, 84, 66, 49, 31, 20, 17, 22, 38, 58, 76, 93],
        "P-300": [36, 37, 39, 38, 40, 39, 41, 45, 50, 53, 57, 60],
    },
}

# Returns are only tracked for products sold online. P-200 is not.
RETURNS = {
    2025: {"P-100": [3, 3, 2, 2, 1, 1, 1, 2, 2, 3, 4, 5],
           "P-300": [1, 1, 2, 1, 2, 2, 2, 2, 3, 3, 3, 4]},
    2024: {"P-100": [3, 2, 2, 2, 1, 1, 1, 1, 2, 3, 3, 4],
           "P-300": [1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3]},
}


@mcp.tool()
def list_products() -> list[dict]:
    """List every product the shop sells, with its id, name and category."""
    return [{"product_id": pid, **info} for pid, info in PRODUCTS.items()]


@mcp.tool()
def get_revenue(product_id: str, year: int) -> dict:
    """Monthly revenue in AUD thousands for one product in one year.

    Args:
        product_id: a product id such as 'P-100'. Call list_products to get valid ids.
        year: 2024 or 2025.
    """
    if year not in REVENUE:
        return {"error": f"No data for {year}. Available years: {sorted(REVENUE)}"}
    if product_id not in PRODUCTS:
        return {"error": f"Unknown product_id '{product_id}'. Call list_products first."}
    return {"product_id": product_id, "name": PRODUCTS[product_id]["name"],
            "year": year, "revenue": REVENUE[year][product_id]}


@mcp.tool()
def get_returns(product_id: str, year: int) -> dict:
    """Monthly unit returns for one product in one year.

    Returns are only tracked for products sold online, so some valid product ids
    have no data. This tool reports an error instead of guessing.

    Args:
        product_id: a product id such as 'P-100'.
        year: 2024 or 2025.
    """
    if year not in RETURNS:
        return {"error": f"No returns data for {year}."}
    if product_id not in PRODUCTS:
        return {"error": f"Unknown product_id '{product_id}'. Call list_products first."}
    if product_id not in RETURNS[year]:
        return {"error": f"{product_id} is not sold online, so returns are not tracked."}
    return {"product_id": product_id, "year": year, "returns": RETURNS[year][product_id]}


@mcp.tool()
def save_report(filename: str, content: str) -> str:
    """Save a markdown report into the reports/ folder. Returns the path written.

    Args:
        filename: a plain file name ending in .md, for example 'summary.md'.
        content: the full markdown text.
    """
    if not filename.endswith(".md"):
        return "error: filename must end in .md"
    if "/" in filename or "\\" in filename or ".." in filename:
        return "error: filename must be a plain file name, not a path"
    Path("reports").mkdir(exist_ok=True)
    path = Path("reports") / filename
    path.write_text(content, encoding="utf-8")
    return f"Saved {path} ({len(content)} characters)"


if __name__ == "__main__":
    import sys
    # Pass 'stdio' to let the agent launch this file itself. See Troubleshooting.
    mcp.run(transport=sys.argv[1] if len(sys.argv) > 1 else "streamable-http")

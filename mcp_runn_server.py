"""
MCP server exposing Runn billable hours, projects, and people.

Transport: streamable HTTP (default) on port 8000.

Usage:
  # install deps (in existing .venv):
  pip install "mcp[cli]"
  # run server
  RUNN_API_KEY=LIVE_... python3 mcp_runn_server.py

Tools:
  - list_projects() -> list of {id, name}
  - list_people() -> list of {id, name, email}
  - billable_hours(start=None, end=None, project_id=None, person_id=None)
      returns aggregated billable hours grouped by project/person/month

Notes:
  - Requires env RUNN_API_KEY.
  - Uses existing RunnClient from runn_reports.py.
"""

from __future__ import annotations

import datetime as dt
import os
from typing import Dict, List, Optional

from mcp.server.fastmcp import FastMCP

from runn_reports import RunnClient, build_billable_hours_report, parse_date


def get_client(api_key: Optional[str] = None) -> RunnClient:
    key = api_key or os.getenv("RUNN_API_KEY")
    if not key:
        raise RuntimeError("RUNN_API_KEY not set")
    return RunnClient(api_key=key)


mcp = FastMCP("Runn MCP Server", json_response=True)


@mcp.tool()
def list_projects(api_key: Optional[str] = None) -> List[Dict[str, object]]:
    """List all projects (id, name)."""
    client = get_client(api_key)
    return [{"id": pid, "name": name} for pid, name in sorted(client.projects_lookup().items())]


@mcp.tool()
def list_people(api_key: Optional[str] = None) -> List[Dict[str, object]]:
    """List all people (id, name, email)."""
    client = get_client(api_key)
    people_raw = client.iter_people()
    return [
        {"id": p["id"], "name": f"{p.get('firstName', '')} {p.get('lastName', '')}".strip(), "email": p.get("email")}
        for p in people_raw
    ]


@mcp.tool()
def billable_hours(
    start: Optional[str] = None,
    end: Optional[str] = None,
    project_id: Optional[int] = None,
    person_id: Optional[int] = None,
    api_key: Optional[str] = None,
) -> List[Dict[str, object]]:
    """Aggregate billable hours grouped by project/person/month."""
    client = get_client(api_key)
    rows = build_billable_hours_report(client, start=parse_date(start), end=parse_date(end))

    def matches(row: Dict[str, object]) -> bool:
        if project_id and row["project_id"] != project_id:
            return False
        if person_id and row["person_id"] != person_id:
            return False
        return True

    return [row for row in rows if matches(row)]


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run Runn MCP server.")
    parser.add_argument(
        "--transport",
        choices=["streamable-http", "stdio"],
        default="streamable-http",
        help="Transport for MCP (default: streamable-http).",
    )
    args = parser.parse_args()

    # FastMCP.run only accepts transport + optional mount_path
    mcp.run(transport=args.transport)

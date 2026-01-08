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
  - list_people(full=False, params=None, paginate=True, limit=200) -> list of {id, name, email} by default
  - billable_hours(start=None, end=None, project_id=None, person_id=None)
      returns aggregated billable hours grouped by project/person/month
  - list_clients(params=None, paginate=True, limit=200)
  - list_assignments(params=None, paginate=True, limit=200)
  - list_actuals(params=None, paginate=True, limit=200)
  - list_roles(params=None, paginate=True, limit=200)
  - list_skills(params=None, paginate=True, limit=200)
  - list_teams(params=None, paginate=True, limit=200)
  - list_rate_cards(params=None, paginate=True, limit=200)
  - runn_request(method, path, params=None, json_body=None, paginate=False, limit=200)
      calls any Runn API endpoint (optionally paginated for list endpoints)

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
def list_people(
    full: bool = False,
    params: Optional[Dict[str, object]] = None,
    paginate: bool = True,
    limit: int = 200,
    api_key: Optional[str] = None,
) -> object:
    """List people. Default returns {id, name, email}; set full=True for raw API objects."""
    client = get_client(api_key)
    if full:
        if paginate:
            return list(client.paginate("/people", params=params, limit=limit))
        return client.request("GET", "/people", params=params)

    if paginate:
        people_raw = client.paginate("/people", params=params, limit=limit)
    else:
        resp = client.request("GET", "/people", params=params)
        people_raw = resp.get("values", []) if isinstance(resp, dict) else resp

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


@mcp.tool()
def list_clients(
    params: Optional[Dict[str, object]] = None,
    paginate: bool = True,
    limit: int = 200,
    api_key: Optional[str] = None,
) -> object:
    """List clients (raw API objects)."""
    client = get_client(api_key)
    if paginate:
        return list(client.paginate("/clients", params=params, limit=limit))
    return client.request("GET", "/clients", params=params)


@mcp.tool()
def list_assignments(
    params: Optional[Dict[str, object]] = None,
    paginate: bool = True,
    limit: int = 200,
    api_key: Optional[str] = None,
) -> object:
    """List assignments (raw API objects)."""
    client = get_client(api_key)
    if paginate:
        return list(client.paginate("/assignments", params=params, limit=limit))
    return client.request("GET", "/assignments", params=params)


@mcp.tool()
def list_actuals(
    params: Optional[Dict[str, object]] = None,
    paginate: bool = True,
    limit: int = 200,
    api_key: Optional[str] = None,
) -> object:
    """List actuals (raw API objects)."""
    client = get_client(api_key)
    if paginate:
        return list(client.paginate("/actuals", params=params, limit=limit))
    return client.request("GET", "/actuals", params=params)


@mcp.tool()
def list_roles(
    params: Optional[Dict[str, object]] = None,
    paginate: bool = True,
    limit: int = 200,
    api_key: Optional[str] = None,
) -> object:
    """List roles (raw API objects)."""
    client = get_client(api_key)
    if paginate:
        return list(client.paginate("/roles", params=params, limit=limit))
    return client.request("GET", "/roles", params=params)


@mcp.tool()
def list_skills(
    params: Optional[Dict[str, object]] = None,
    paginate: bool = True,
    limit: int = 200,
    api_key: Optional[str] = None,
) -> object:
    """List skills (raw API objects)."""
    client = get_client(api_key)
    if paginate:
        return list(client.paginate("/skills", params=params, limit=limit))
    return client.request("GET", "/skills", params=params)


@mcp.tool()
def list_teams(
    params: Optional[Dict[str, object]] = None,
    paginate: bool = True,
    limit: int = 200,
    api_key: Optional[str] = None,
) -> object:
    """List teams (raw API objects)."""
    client = get_client(api_key)
    if paginate:
        return list(client.paginate("/teams", params=params, limit=limit))
    return client.request("GET", "/teams", params=params)


@mcp.tool()
def list_rate_cards(
    params: Optional[Dict[str, object]] = None,
    paginate: bool = True,
    limit: int = 200,
    api_key: Optional[str] = None,
) -> object:
    """List rate cards (raw API objects)."""
    client = get_client(api_key)
    if paginate:
        return list(client.paginate("/rate-cards", params=params, limit=limit))
    return client.request("GET", "/rate-cards", params=params)


@mcp.tool()
def runn_request(
    method: str,
    path: str,
    params: Optional[Dict[str, object]] = None,
    json_body: Optional[Dict[str, object]] = None,
    paginate: bool = False,
    limit: int = 200,
    api_key: Optional[str] = None,
) -> object:
    """Call any Runn API endpoint and return the JSON response."""
    client = get_client(api_key)
    if paginate:
        if method.upper() != "GET":
            raise ValueError("paginate=True only supports GET requests.")
        return list(client.paginate(path, params=params, limit=limit))
    return client.request(method, path, params=params, json_body=json_body)


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

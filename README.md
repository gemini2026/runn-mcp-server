# runn.io MCP Server

Standalone MCP server for the Runn API with simple reporting helpers.

## Requirements

- Python 3.10+
- Runn API key (`RUNN_API_KEY`)

## Install

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Run (MCP server)

### stdio (Claude Desktop)

```bash
RUNN_API_KEY=LIVE_... python3 mcp_runn_server.py --transport stdio
```

### streamable-http (default)

```bash
RUNN_API_KEY=LIVE_... python3 mcp_runn_server.py --transport streamable-http
```

## Run with Docker

Build the image:

```bash
docker build -t runn-mcp-server .
```

Run the container (HTTP transport):

```bash
docker run --rm -e RUNN_API_KEY=LIVE_... -p 8000:8000 runn-mcp-server
```

## GHCR image

The GitHub Actions workflow publishes to:

```
ghcr.io/gemini2026/runn-mcp-server
```

Pull and run:

```bash
docker pull ghcr.io/gemini2026/runn-mcp-server:main
docker run --rm -e RUNN_API_KEY=LIVE_... -p 8000:8000 ghcr.io/gemini2026/runn-mcp-server:main
```

## Claude Desktop config snippet

```json
{
  "mcpServers": {
    "runn": {
      "command": "/path/to/python3",
      "args": [
        "/path/to/mcp_runn_server.py",
        "--transport",
        "stdio"
      ],
      "env": {
        "RUNN_API_KEY": "<YOUR_API_KEY>"
      }
    }
  }
}
```

## MCP tools

- `list_projects` — returns `{id, name}` pairs.
- `list_people` — returns `{id, name, email}` by default (set `full=true` for raw objects).
- `billable_hours` — aggregates billable hours grouped by project/person/month.
- `list_clients` — list clients (raw API objects).
- `list_assignments` — list assignments (raw API objects).
- `list_assignments_by_person` — assignments for a person, optional date range.
- `list_assignments_by_project` — assignments for a project, optional date range.
- `list_actuals` — list actuals (raw API objects).
- `list_actuals_by_date_range` — actuals in a date range, optional person/project filters.
- `list_actuals_by_person` — actuals for a person, optional date range.
- `list_actuals_by_project` — actuals for a project, optional date range.
- `list_roles` — list roles (raw API objects).
- `list_roles_by_person` — roles that include a person.
- `list_skills` — list skills (raw API objects).
- `list_teams` — list teams (raw API objects).
- `list_people_by_team` — people in a team (optionally include archived).
- `list_rate_cards` — list rate cards (raw API objects).
- `list_rate_cards_by_project` — rate cards that include a project.
- `runn_request` — call any Runn API endpoint (GET/POST/PATCH/PUT/DELETE).

Pagination for list endpoints:

```json
{
  "method": "GET",
  "path": "/projects",
  "paginate": true
}
```

Filter-specific tools (e.g., `list_assignments_by_person`) fetch list endpoints and apply filters client-side.

## Reports (optional)

`runn_reports.py` can export billable hours grouped by project/person/month.

```bash
RUNN_API_KEY=LIVE_... python3 runn_reports.py --start 2025-01-01 --end 2025-12-31 --output billable.csv
```

PDF output requires ReportLab:

```bash
python -m pip install reportlab
```

## CI/CD

- CI runs on every push and pull request to `main`.
- CD publishes a GitHub Release when you push a tag like `v0.1.0`.

Example release:

```bash
git tag v0.1.0
git push origin v0.1.0
```

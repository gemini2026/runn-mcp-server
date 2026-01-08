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

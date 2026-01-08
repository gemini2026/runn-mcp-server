# runn.io MCP Server

Minimal standalone repository for the runn.io MCP server.

## Run

```bash
python3 mcp_runn_server.py --transport stdio
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

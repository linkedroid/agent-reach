# Exa Search setup guide

## Features
Exa is an AI semantic search engine. Its MCP integration is **free and requires no API key**. Once configured, it enables:
- Semantic search across the web
- Reddit search (using site:reddit.com)
- Twitter search (using site:x.com)

## Steps the agent can complete automatically

After explicit user authorization, `agent-reach install --env=auto --system` performs
the following steps. The default command without `--system` only runs read-only checks.

### 1. Install mcporter
```bash
npm install -g mcporter
```

### 2. Register Exa MCP
```bash
mcporter config add exa https://mcp.exa.ai/mcp --scope home
```

### 3. Verify
```bash
agent-reach doctor | grep "Search"
mcporter call exa.web_search_exa query="test" numResults=1
```

## Steps the user must complete manually

**None.** Exa connects through MCP, with no charge, registration, or API key required.

If `agent-reach install --system` could not configure Exa because of a network issue,
manually run the two installation/configuration commands above.

## FAQ

**Q: Is there a search limit?**
A: The MCP endpoint is provided by Exa (mcp.exa.ai) and is currently free and unlimited.
If this changes, Agent Reach updates will adapt accordingly.

**Q: What is mcporter?**
A: A command-line bridge for calling MCP servers. Agent Reach uses it to connect to
Exa and XiaoHongShu.

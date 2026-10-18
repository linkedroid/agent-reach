# Reddit setup guide

## Features

Reddit blocks almost all direct non-browser access, including data-center and ISP
proxy IPs; its JSON API returns 403.

Agent Reach uses **rdt-cli** to search and read Reddit:
- **Search**: `rdt search "keywords"`
- **Read a full post and comments**: `rdt read POST_ID`

Free, with no proxy or API key required. Login authentication is required
(`rdt login`, which automatically extracts cookies from the browser).

## Steps the agent can complete automatically

1. Check whether rdt-cli is available:
```bash
which rdt && echo "installed" || echo "not installed"
```

2. If it is not installed, install it automatically (the PyPI release currently lags
   behind, so install the latest version from GitHub):
```bash
pipx install 'git+https://github.com/public-clis/rdt-cli.git'
```

Or use the one-command installer:
```bash
agent-reach install --env=auto --system --channels=reddit
```

## Usage examples

Search Reddit:
```bash
rdt search "python best practices" -n 5
```

Read a full post and comments:
```bash
rdt read POST_ID
```

## Steps the user must complete manually

None. After explicit user authorization, install rdt-cli with
`agent-reach install --env=auto --system --channels=reddit`.

## Fallback: Exa search

If Exa is already configured through mcporter, it can also search Reddit content:

```bash
mcporter call exa.web_search_exa query="site:reddit.com python best practices" numResults=5
```

rdt-cli is the currently recommended option and requires no additional configuration.

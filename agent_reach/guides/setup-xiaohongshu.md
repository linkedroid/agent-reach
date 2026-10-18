# XiaoHongShu setup guide

## Features
Read and search XiaoHongShu posts. Prefer OpenCLI on desktops and
[xiaohongshu-mcp](https://github.com/xpzouying/xiaohongshu-mcp) on servers.
xhs-cli is only a legacy fallback for users who already have it installed.

## Prerequisites
- OpenCLI: an existing XiaoHongShu Chrome session explicitly controlled by the user
- xiaohongshu-mcp / legacy tools: the Cookie-Editor browser extension

## Authentication boundaries

Agent Reach does not log in to XiaoHongShu on the user's behalf or read browser cookies.

OpenCLI only uses an existing Chrome session explicitly controlled by the user.
`agent-reach configure xhs-cookies` does not inject cookies into OpenCLI or Chrome.
If no session exists, do not automate login. Instead, manually export cookies with
Cookie-Editor and configure xiaohongshu-mcp or a legacy tool:

1. Install the [Cookie-Editor](https://chromewebstore.google.com/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm) extension in Chrome
2. The user prepares the session they want to export on xiaohongshu.com
3. Click the Cookie-Editor icon → Export → Header String
4. Send the exported string to the agent, then run:

```bash
agent-reach configure xhs-cookies
agent-reach doctor
```

This explicit command saves/imports the user-provided cookie set for the
xiaohongshu.com domain. Confirm the cookie names and scope before running it.
Cookies from other domains are ignored.

If the xiaohongshu-mcp container is running, the configuration command imports the
cookies into it. Otherwise, it writes an owner-only local file and prints the path
for a later manual import.

## Usage examples

First select the command using `active_backend` from `agent-reach doctor --json`.
The following examples are for a legacy xhs-cli installation:

Search posts:
```bash
xhs search "keywords"
```

Read post details:
```bash
xhs read NOTE_ID
```

View comments:
```bash
xhs comments NOTE_ID
```

## FAQ

**Q: Have the cookies expired?**
A: Export them manually with Cookie-Editor again, then run
`agent-reach configure xhs-cookies` and paste them into the hidden-input prompt.

**Q: Does XiaoHongShu report an IP risk?**
A: A residential proxy is recommended: `export HTTP_PROXY="http://user:pass@ip:port"`.

**Q: Does xhs-cli not support my system?**
A: Make sure Python 3.10+ and pipx are installed. Run `pipx install xiaohongshu-cli`.

## Server option: Docker MCP

An existing [xiaohongshu-mcp](https://github.com/xpzouying/xiaohongshu-mcp) Docker
setup also works:

```bash
docker run -d \
  --name xiaohongshu-mcp \
  -p 18060:18060 \
  xpzouying/xiaohongshu-mcp

mcporter config add xiaohongshu http://localhost:18060/mcp --scope home
```

This server backend uses the manual Cookie-Editor export workflow described above.

<h1 align="center">👁️ Agent Reach</h1>

<p align="center">
  <strong>Give your AI Agent one-click access to the entire internet</strong>
</p>

<p align="center">
  The most reliable access path for each platform — chosen, installed, and health-checked for you. Backends come and go; you won't notice.
</p>

<p align="center">
  <a href="https://trendshift.io/repositories/24387"><img src="https://trendshift.io/api/badge/repositories/24387" alt="Trendshift GitHub Trending #1 Repository of the Day"></a>
  <a href="https://star-history.com/#Panniantong/Agent-Reach&Date"><img src="https://api.star-history.com/badge?repo=Panniantong/Agent-Reach" alt="Star History Rank" width="196" height="55"></a>
</p>

<p align="center">
  <a href="../LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge" alt="MIT License"></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.10+-green.svg?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.10+"></a>
  <a href="https://github.com/Panniantong/agent-reach/stargazers"><img src="https://img.shields.io/github/stars/Panniantong/agent-reach?style=for-the-badge" alt="GitHub Stars"></a>
</p>

<p align="center">
  <a href="#quick-start">Quick Start</a> · <a href="../README.md">English edition</a> · <a href="#supported-platforms">Platforms</a> · <a href="#design-philosophy">Philosophy</a>
</p>

> **English-localized edition:** This working copy translates the project documentation, setup guides, agent instructions, and user-facing diagnostics into English. See [ENGLISH_EDITION.md](../ENGLISH_EDITION.md) for provenance, installation, and validation details. To keep these translations, install this extracted checkout with `python -m pip install .`; upstream download/update commands below install the original upstream version instead.

> **No token or crypto affiliation:** Agent Reach has no official token, coin, investment product, fee-claim program, wallet connection, or Solana/Pump.fun project. Any crypto project using the Agent Reach name, GitHub URL, or author identity is not affiliated with this repository. Do not connect a wallet or claim fees based on messages, posts, or links that say otherwise.

---

## Why Agent Reach?

AI Agents can already access the internet — but "can go online" is barely the start.

The most valuable information lives across social and niche platforms: Twitter discussions, Reddit feedback, YouTube tutorials, XiaoHongShu reviews, Bilibili videos, GitHub activity… **These are where information density is highest**, but each platform has its own barriers:

| Pain Point | Reality |
|------------|---------|
| Twitter API | Pay-per-use, moderate usage ~$215/month |
| Reddit | Server IPs get 403'd |
| XiaoHongShu | Login required to browse |
| Bilibili | Blocks overseas/server IPs |

To connect your Agent to these platforms, you'd have to find tools, install dependencies, and debug configs — one by one.

**Agent Reach turns this into one command:**

```
Install Agent Reach: https://raw.githubusercontent.com/Panniantong/agent-reach/main/docs/install.md
```

Copy that to your Agent. A few minutes later, it can read tweets, search Reddit, and watch Bilibili.

**Already installed? Update in one command:**

```
Update Agent Reach: https://raw.githubusercontent.com/Panniantong/agent-reach/main/docs/update.md
```

### ✅ Before you start, you might want to know

| | |
|---|---|
| 💰 **Completely free** | All tools are open source, all APIs are free. The only possible cost is a server proxy ($1/month) — local computers don't need one |
| 🔒 **Privacy safe** | Cookies stay local. Never uploaded. Fully open source — audit anytime |
| 🔄 **Kept up to date** | Every platform routes through a primary + fallback backend list. When an access path dies, we switch to the next — you won't notice (June 2026: Bilibili 412-blocked yt-dlp → switched to bili-cli, zero action on your side) |
| 🤖 **Works with any Agent** | Claude Code, OpenClaw, Cursor, Windsurf… any Agent that can run commands |
| 🩺 **Built-in diagnostics** | `agent-reach doctor` — one command shows what works, what doesn't, and how to fix it |

---

## Supported Platforms

| Platform | Capabilities | Setup | Notes |
|----------|-------------|:-----:|-------|
| 🌐 **Web** | Read | Zero config | Any URL → clean Markdown ([Jina Reader](https://github.com/jina-ai/reader) ⭐9.8K) |
| 🐦 **Twitter/X** | Read · Search | Cookie | Cookie unlocks search, timeline, tweet reading, articles ([twitter-cli](https://github.com/public-clis/twitter-cli)) |
| 📕 **XiaoHongShu** | Read · Search · Comments | OpenCLI / MCP | OpenCLI uses only an existing user-controlled Chrome session; MCP/legacy tools use a manual Cookie-Editor export |
| 📘 **Facebook** | Search · Profiles · Feed · Groups list | OpenCLI | Desktop only: [OpenCLI](https://github.com/jackwener/opencli) reuses your logged-in Chrome session |
| 📷 **Instagram** | User search · Profiles · Recent posts · Explore | OpenCLI | Desktop only: [OpenCLI](https://github.com/jackwener/opencli) reuses your logged-in Chrome session |
| 💼 **LinkedIn** | Public pages; richer profiles, company details, people and job search after setup | MCP + login for richer access | Jina Reader for public pages; tell your Agent "help me set up LinkedIn" for MCP setup |
| 🎯 **BOSS Zhipin** | CDP connection diagnostics; job search and full job descriptions after setup | Dedicated real Chrome session | Tell your Agent "help me set up BOSS Zhipin"; the Agent opens dedicated Chrome and you log in manually |
| 💻 **V2EX** | Hot topics · Node topics · Topic detail + replies · User profile | Zero config | Public JSON API, no auth required. Great for tech community content |
| 📈 **Xueqiu** | Stock quotes · Search · Hot posts · Hot stocks | Browser cookie | Tell your Agent "help me set up Xueqiu" |
| 🎙️ **Xiaoyuzhou Podcast** | Transcription | Free API key | Podcast audio → full text transcript via Groq Whisper (free) |
| 🔍 **Web Search** | Search | MCP configuration | Configured during explicitly authorized setup, free, no API key ([Exa](https://exa.ai) via [mcporter](https://github.com/nicepkg/mcporter)) |
| 📦 **GitHub** | Read · Search | Zero config | [gh CLI](https://cli.github.com) powered. Public repos work immediately. `gh auth login` unlocks Fork, Issue, PR |
| 📺 **YouTube** | Read · **Search** | Zero config | Subtitles + search across 1800+ video sites ([yt-dlp](https://github.com/yt-dlp/yt-dlp) ⭐148K) |
| 📺 **Bilibili** | Read · **Search** | Zero config | Search + video detail via [bili-cli](https://github.com/public-clis/bilibili-cli) (no login needed); subtitles via [OpenCLI](https://github.com/jackwener/opencli). yt-dlp is 412-blocked by Bilibili and no longer used here |
| 📡 **RSS** | Read | Zero config | Any RSS/Atom feed ([feedparser](https://github.com/kurtmckee/feedparser) ⭐2.3K) |
| 📖 **Reddit** | Search · Read | OpenCLI / Cookie | No zero-config path (anonymous endpoints blocked). Desktop: [OpenCLI](https://github.com/jackwener/opencli) via browser session; or [rdt-cli](https://github.com/public-clis/rdt-cli) + cookie |

> **Setup levels:** Zero config = install and go · MCP configuration = handled during explicitly authorized setup · mcporter = needs MCP service · Cookie = export from browser · Proxy = $1/month

---

## Quick Start

> ⚠️ **OpenClaw users: enable `exec` permission first**
>
> Agent Reach relies on the Agent running shell commands (`pip install`, `mcporter`, `twitter`, etc.). If your OpenClaw uses the default `messaging` tool profile, the Agent won't be able to run them. **Enable `exec` before installing:**
>
> ```bash
> openclaw config set tools.profile "coding"
> ```
> Or set `"tools": { "profile": "coding" }` in `~/.openclaw/openclaw.json`. After changing it, restart the Gateway (`openclaw gateway restart`) and start a new conversation. Other platforms (Claude Code, Cursor, Windsurf, etc.) are not affected.

Copy this to your AI Agent (Claude Code, OpenClaw, Cursor, etc.):

```
Install Agent Reach: https://raw.githubusercontent.com/Panniantong/agent-reach/main/docs/install.md
```

The Agent installs the Python package, checks your environment, and tells you what's ready. System-level changes require an explicit `--system` flag.

> 🔄 **Already installed?** Update in one command:
> ```
> Update Agent Reach: https://raw.githubusercontent.com/Panniantong/agent-reach/main/docs/update.md
> ```

> 🛡️ **Safe by default:** `agent-reach install` checks the machine without installing system packages or writing configuration:
> ```
> Safely check and install Agent Reach: https://raw.githubusercontent.com/Panniantong/agent-reach/main/docs/install.md
> ```
> Use `agent-reach install --system` only after explicitly approving system changes.

<details>
<summary>Manual install</summary>

```bash
pip install https://github.com/Panniantong/agent-reach/archive/main.zip
agent-reach install --env=auto
```
</details>

<details>
<summary>Install as a Skill (Claude Code / OpenClaw / any agent with Skills support)</summary>

```bash
npx skills add Panniantong/Agent-Reach@agent-reach
```

After the Skill is installed, the Agent will auto-detect whether `agent-reach` CLI is available and install it if needed.

> If you explicitly install external tools with `agent-reach install --system`, the skill is registered automatically. The default read-only check leaves existing files unchanged.
>
> Both skill variants in this localized edition are English. The existing locale-selection
> mechanism is preserved, and the installed file is always named `SKILL.md`.
> Run `agent-reach skill --install` to install the skill from this checkout.
</details>

---

## Works Out of the Box

For public channels, no account configuration is needed once the required tools are installed. Login-backed examples, including Twitter, still require the credentials noted below:

- "Read this link" → `curl https://r.jina.ai/URL` for any web page
- "What's this GitHub repo about?" → `gh repo view owner/repo`
- "What does this video cover?" → `yt-dlp --dump-json URL` for subtitles
- "Read this tweet" → set `TWITTER_AUTH_TOKEN` / `TWITTER_CT0`, then run `twitter tweet URL`
- "Subscribe to this RSS" → `feedparser` to parse feeds
- "Search GitHub for LLM frameworks" → `gh search repos "LLM framework"`

**No commands to remember.** The Agent reads SKILL.md and knows what to call.

---

## Unlock on Demand

Don't use it? Don't configure it. Every step is optional.

### 🍪 Cookies — Free, 2 minutes

Tell your Agent "help me configure Twitter cookies" — it'll guide you through a
manual Cookie-Editor export. Agent Reach saves the values for `doctor` to check
whether credentials are present; `doctor` does not run `twitter status`.
Direct `twitter` commands still require `TWITTER_AUTH_TOKEN` and `TWITTER_CT0`
in their process environment.

For XiaoHongShu, Agent Reach never logs the user in or reads browser cookies.
OpenCLI may use only an existing Chrome session explicitly controlled by the
user. If none exists, do not automate login; use a manual Cookie-Editor export
with xiaohongshu-mcp or a legacy tool. `agent-reach configure xhs-cookies`
does not inject cookies into OpenCLI or Chrome.

### 🌐 Proxy — $1/month, restricted networks only

Most users need no proxy. If your network blocks Reddit/Twitter (e.g. mainland China) get one ([Webshare](https://webshare.io) recommended, $1/month) and send the address to your Agent — it saves it and exports HTTP(S)_PROXY when calling those tools.

> Reddit needs a logged-in session either way — OpenCLI rides your browser session, or rdt-cli after `rdt login`. Bilibili works via bili-cli without a proxy.

---

## Status at a Glance

Illustrative output; actual channels, messages, and availability depend on your setup.

```
$ agent-reach doctor

👁️  Agent Reach Status
========================================

✅ Ready to use:
  ✅ GitHub repos and code — public repos readable and searchable
  ✅ YouTube video subtitles — yt-dlp
  ✅ Bilibili search & video detail — bili-cli (subtitles via OpenCLI)
  ✅ RSS/Atom feeds — feedparser
  ✅ Web pages (any URL) — Jina Reader API

🔍 Search (free Exa MCP setup):
  ⬜ Web semantic search — configure mcporter with the Exa MCP endpoint; no API key required

🔧 Configurable:
  ⚠️  Twitter/X — doctor checks only that explicit credentials exist; direct CLI still needs its environment variables
  ⬜ Reddit posts and comments — needs login: rdt-cli after `rdt login`, or OpenCLI browser session
  ⬜ XiaoHongShu notes — OpenCLI needs an existing user-controlled session; otherwise use Cookie-Editor with MCP/legacy tools
  ⬜ Facebook / Instagram — desktop: OpenCLI browser session

Status: <available>/<total> channels available
```

---

## Design Philosophy

**Agent Reach is a capability layer, not yet another tool.**

It sits one level above any specific implementation — it handles **selection, installation, health checks, and routing**, not the reading itself. Reading is done by your Agent calling upstream tools directly; there is no wrapper layer.

Every time you spin up a new Agent, you spend time finding tools, installing deps, and debugging configs — what reads Twitter? How do you log into Reddit? What replaces a discontinued XiaoHongShu CLI? Every time, you re-do the same work. Agent Reach does one simple thing: **the most reliable access path for each platform, chosen, installed, and health-checked for you. Access paths come and go (in March 2026 a batch of single-platform CLIs went unmaintained — we re-routed), so you don't have to care.**

### 🔌 Every platform = an ordered backend list (primary + fallbacks)

Switching access paths means reordering the list, not rewriting code. `agent-reach doctor` tells you **which backend each platform is currently using**.

```
channels/
├── web.py          → Jina Reader
├── twitter.py      → twitter-cli ▸ OpenCLI ▸ bird
├── youtube.py      → yt-dlp
├── github.py       → gh CLI
├── bilibili.py     → bili-cli ▸ OpenCLI ▸ search API (yt-dlp retired, 412-blocked)
├── reddit.py       → OpenCLI ▸ rdt-cli (no zero-config path, login required)
├── facebook.py     → OpenCLI (desktop browser session)
├── instagram.py    → OpenCLI (desktop browser session)
├── xiaohongshu.py  → OpenCLI ▸ xiaohongshu-mcp ▸ xhs-cli
├── linkedin.py     → linkedin-mcp ▸ Jina Reader
├── rss.py          → feedparser
├── exa_search.py   → Exa via mcporter
└── __init__.py     → Channel registry (for doctor checks)
```

Each channel checks the candidates it can safely inspect and reports setup or repair guidance. Some checks are deliberately configuration-only: for example, saved Twitter credentials or an Exa MCP entry do not prove that a live request will work. An `active_backend` of `null` means live readiness has not been established. The Agent performs actual reading and searching by calling upstream tools for the user's requested task.

### Current Tool Choices

| Scenario | Primary | Fallback | Why |
|----------|---------|----------|-----|
| Read web pages | [Jina Reader](https://github.com/jina-ai/reader) | — | Free, no API key needed |
| Read tweets | [twitter-cli](https://github.com/public-clis/twitter-cli) | [OpenCLI](https://github.com/jackwener/opencli) | Reliable search in real-world tests; OpenCLI falls back on your browser session |
| Reddit | [OpenCLI](https://github.com/jackwener/opencli) (desktop) | [rdt-cli](https://github.com/public-clis/rdt-cli) | Anonymous endpoints blocked, official API gated — logged-in sessions are the only route left |
| Facebook | [OpenCLI](https://github.com/jackwener/opencli) (desktop) | — | Graph/Groups API access is heavily restricted; browser sessions are the practical route |
| Instagram | [OpenCLI](https://github.com/jackwener/opencli) (desktop) | Official Graph API (Business/Creator + review) | Instaloader-style paths are unstable; OpenCLI reuses the real browser session |
| YouTube subtitles + search | [yt-dlp](https://github.com/yt-dlp/yt-dlp) | — | 154K stars, still the best for YouTube (no longer used for Bilibili) |
| Bilibili | [bili-cli](https://github.com/public-clis/bilibili-cli) | OpenCLI ▸ search API | yt-dlp is 412-blocked by Bilibili (verified June 2026); bili-cli searches and reads without login |
| Search the web | [Exa](https://exa.ai) via [mcporter](https://github.com/nicobailon/mcporter) | — | AI semantic search, MCP integration, no API key |
| GitHub | [gh CLI](https://cli.github.com) | — | Official tool, full API after auth |
| Read RSS | [feedparser](https://github.com/kurtmckee/feedparser) | — | Python ecosystem standard |
| XiaoHongShu | [OpenCLI](https://github.com/jackwener/opencli) (desktop) | [xiaohongshu-mcp](https://github.com/xpzouying/xiaohongshu-mcp) (server) ▸ xhs-cli | OpenCLI uses only an existing user-controlled session; other backends use a manual Cookie-Editor export |
| LinkedIn | [mcp-server-linkedin](https://github.com/stickerdaniel/linkedin-mcp-server) | Jina Reader | MCP server, browser automation |
| Xiaoyuzhou Podcast | `transcribe.sh` | — | `bash ~/.agent-reach/tools/xiaoyuzhou/transcribe.sh <URL>` |

> 📌 These are the *current* choices, re-verified regularly on real machines. When a path dies we switch to the next — `agent-reach doctor` always tells you which one is active.

---

## Security

Agent Reach includes the following safeguards:

| Measure | Description |
|---------|-------------|
| 🔒 **Local credentials** | Cookies and tokens are stored on your machine in `~/.agent-reach/config.yaml`, with file mode 600 (owner read/write only). Agent Reach does not upload them to its own service. |
| 🛡️ **Safe by default** | `agent-reach install` does not modify the system by default. Installing external tools or writing configuration requires an explicit `--system` flag. |
| 👀 **Open source** | The code and its open-source tool dependencies can be reviewed. |
| 🔍 **Dry run** | `agent-reach install --dry-run` previews actions without changing anything. |
| 🧩 **Pluggable architecture** | Replace a channel implementation without affecting the others. |

### Cookie safety

> ⚠️ **Account restriction risk:** Calling platform scripts or APIs with login cookies can trigger account restrictions or bans. Use a dedicated secondary account instead of your primary account.

For platforms requiring cookies or a logged-in browser session (including Twitter, Xiaohongshu, Reddit, Facebook, and Instagram), a dedicated account limits both the impact of platform restrictions and the damage from credential exposure. Cookies can grant full account access.

### Installation modes

| Mode | Command | When to use |
|------|---------|-------------|
| Default safe check | `agent-reach install --env=auto` | Read-only environment check and a list of missing tools |
| Explicit system setup | `agent-reach install --env=auto --system` | Only after you authorize changes to the current machine |
| Compatibility safe flag | `agent-reach install --env=auto --safe` | Same behavior as the default |
| Preview only | `agent-reach install --env=auto --dry-run` | Preview the actions first |

### Uninstall

```bash
agent-reach uninstall
```

This removes `~/.agent-reach/` (including saved tokens and cookies), installed Agent Reach skill files, and its MCP entries in mcporter.

```bash
# Preview only; do not delete anything.
agent-reach uninstall --dry-run

# Remove installed skill files while keeping credentials for reinstallation.
agent-reach uninstall --keep-config
```

Remove the Python package itself with `pip uninstall agent-reach`.

---

## Why Star This Project?

The upstream author uses this project every day and plans to keep maintaining it: adding requested channels, keeping them usable and free where possible, and adapting when platforms change their APIs or anti-scraping systems. Star the original repository to find it again and follow its updates.

---

## Credits

[OpenCLI](https://github.com/jackwener/opencli) · [xiaohongshu-mcp](https://github.com/xpzouying/xiaohongshu-mcp) · [twitter-cli](https://github.com/public-clis/twitter-cli) · [rdt-cli](https://github.com/public-clis/rdt-cli) · [xhs-cli](https://github.com/jackwener/xiaohongshu-cli) · [bili-cli](https://github.com/public-clis/bilibili-cli) · [yt-dlp](https://github.com/yt-dlp/yt-dlp) · [Jina Reader](https://github.com/jina-ai/reader) · [Exa](https://exa.ai) · [mcporter](https://github.com/nicobailon/mcporter) · [feedparser](https://github.com/kurtmckee/feedparser) · [mcp-server-linkedin](https://github.com/stickerdaniel/linkedin-mcp-server)

## License

[MIT](../LICENSE)


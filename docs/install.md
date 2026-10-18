# Agent Reach — Installation Guide

> **English edition:** The upstream URLs and install/update commands below fetch the original upstream project and may overwrite this localization. To install or update this translated checkout, follow [ENGLISH_EDITION.md](../ENGLISH_EDITION.md).

## For Humans

Copy this to your AI Agent:

```
Install Agent Reach: https://raw.githubusercontent.com/Panniantong/agent-reach/main/docs/install.md
```

> 🛡️ **Safe by default:** `agent-reach install` only checks the machine and lists missing dependencies:
> ```
> Safely check and install Agent Reach: https://raw.githubusercontent.com/Panniantong/agent-reach/main/docs/install.md
> ```
> Only use `--system` after the user explicitly approves system-level installs and configuration writes.

---

## For AI Agents

### Goal

Install Agent Reach and all upstream tools so your user's agent has full internet access. After installation, you'll use the upstream tools directly (OpenCLI, twitter-cli, bili-cli, rdt-cli, yt-dlp, mcporter, gh CLI, etc.) — Agent Reach is the selector, installer, health checker and router, never a wrapper.

### ⚠️ Boundaries

When fixing issues, stay within these limits:

- **DO NOT** run commands with `sudo` unless the user explicitly approved
- **DO NOT** modify system files outside `~/.agent-reach/`
- **DO NOT** install packages not listed in this guide
- **DO NOT** disable firewalls, security settings, or system protections
- **DO NOT** clone repos, create files, or run commands inside the agent workspace / working directory
- If something requires elevated permissions, **tell the user** what's needed and let them decide

### 📁 Directory Rules

All Agent Reach files go in dedicated directories — **never in the agent workspace**:

| Purpose | Directory | Example |
|---------|-----------|---------|
| Config & tokens | `~/.agent-reach/` | `~/.agent-reach/config.yaml` |
| Upstream tool repos | `~/.agent-reach/tools/` | `~/.agent-reach/tools/xiaoyuzhou/` |
| Temporary files | `/tmp/` | `/tmp/yt-dlp-output/` |
| Skills | `~/.openclaw/skills/agent-reach/` | SKILL.md |

**Why?** If you clone repos or create files in the workspace, it pollutes the user's project directory and can break their agent over time. Keep the workspace clean.

### Step 1: Install the basics

```bash
# Recommended: pipx (the simplest option)
pipx install https://github.com/Panniantong/agent-reach/archive/main.zip
agent-reach install --env=auto               # Read-only check (default)
# After the user explicitly approves system changes:
agent-reach install --env=auto --system

# If Python comes from Homebrew / you encounter PEP 668 (externally-managed-environment),
# install in a virtual environment:
python3 -m venv ~/.agent-reach-venv
source ~/.agent-reach-venv/bin/activate
pip install https://github.com/Panniantong/agent-reach/archive/main.zip
agent-reach install --env=auto               # Read-only check (default)
# After the user explicitly approves system changes:
agent-reach install --env=auto --system
```

> 💡 **Windows / Microsoft Store Python alias?**
> If `python3 --version` opens Microsoft Store, or `where python3` points to
> `...\AppData\Local\Microsoft\WindowsApps\python3.exe`, `python3` is a Windows
> Store alias rather than a usable Python installation. Use the Python Launcher `py -3`, or `python.exe` from the actual installation directory instead.
>
> PowerShell example:
> ```powershell
> py -3 -m venv $env:USERPROFILE\.agent-reach-venv
> $env:USERPROFILE\.agent-reach-venv\Scripts\Activate.ps1
> python -m pip install https://github.com/Panniantong/agent-reach/archive/main.zip
> agent-reach install --env=auto
> ```

The default command checks core infrastructure (gh CLI, Node.js, mcporter, Exa search, yt-dlp config) without changing the host. With explicit `--system` approval it installs/configures the missing pieces and activates these zero-config channels:

- Web (Jina Reader), YouTube, GitHub, RSS, Exa Search, V2EX, Bilibili (basic)

> 💡 **Does macOS / Homebrew Python report `externally-managed-environment`?**
> This is PEP 668 protection, not an Agent Reach issue. Prefer `pipx install ...`, or create a `venv` before installing.

**Install modes:**

```bash
agent-reach install --env=auto             # Check only; safe default
agent-reach install --env=auto --safe      # Same check-only behavior (compatibility)
agent-reach install --env=auto --system    # Explicitly allow external/system installs
agent-reach install --env=auto --dry-run   # Preview what --system would do
```

### Step 2: Ask the user which optional channels they want

After installing the basics, **ask the user** which additional channels they need. Present this list:

> The basic channels are installed! You can now ask me to search the web, watch YouTube, read GitHub, and more.
>
> Which of these optional channels would you like?
>
> - 🌟 **OpenCLI** (recommended on desktop) — One installation provides Reddit/Facebook/Instagram/Bilibili subtitles/a Twitter fallback, and serves as the desktop backend for XiaoHongShu; XiaoHongShu only uses an existing Chrome session explicitly controlled by the user
> - 🐦 **Twitter/X** — Search tweets and read timelines (requires login cookies)
> - 📈 **Xueqiu** — Stock quotes and popular posts (requires login cookies)
> - 🎙️ **Xiaoyuzhou Podcast** — Transcribe audio (requires a free Groq key)
> - 📕 **XiaoHongShu** — Search, read, and comment (OpenCLI uses an existing session; MCP/existing tools use Cookie-Editor)
> - 📖 **Reddit** — Search and read posts (login required: desktop OpenCLI or rdt-cli + cookies)
> - 📘 **Facebook** — Search, profiles, feed, and group lists (desktop OpenCLI reuses the Chrome login session)
> - 📷 **Instagram** — User search, profiles, recent user posts, and Explore (desktop OpenCLI reuses the Chrome login session)
> - 📺 **Full Bilibili support** — Trending videos, rankings, search, and video details (bili-cli, no login required)
> - 💼 **LinkedIn** — Profiles and job search
> - 🎯 **BOSS Zhipin** — Job search + full job descriptions (dedicated local Chrome; the user logs in manually)
>
> Tell me which you want, for example "Install XiaoHongShu and Twitter" or "Install Facebook and Instagram". Or say "Install everything".

Based on the user's choice, run:

```bash
agent-reach install --env=auto --system --channels=opencli,xiaohongshu   # Desktop user chose XHS
agent-reach install --env=auto --system --channels=facebook,instagram    # Desktop Meta channels
agent-reach install --env=local --system --channels=boss                # Desktop BOSS Zhipin
agent-reach install --env=auto --system --channels=all                   # User approved everything
```

Supported channel names: `opencli`, `twitter`, `xiaoyuzhou`, `xueqiu`, `xiaohongshu`, `reddit`, `facebook`, `instagram`, `bilibili`, `linkedin`, `boss`, `all`

### Step 3: Fix what's broken

Run `agent-reach doctor` and check the output.

Try to get as many channels to ✅ as possible. If something failed during install or shows as ❌/⚠️ in doctor, diagnose the problem and try to fix it — but stay within the boundaries above. If a fix requires elevated permissions or system changes, ask the user first.

Only ask the user when you genuinely need their input (credentials, permissions, etc.).

### Step 3: Configure things that need user input

Some channels need credentials only the user can provide. Based on the doctor output, ask for what's missing:

> 🔒 **Security tip:** For platforms that need cookies or browser sessions (Twitter, XiaoHongShu, Reddit, Facebook, Instagram, BOSS Zhipin), we recommend using a **dedicated/secondary account** rather than your main account. Cookie/browser-session auth carries two risks:
> 1. **Account ban** — platforms may detect non-browser API calls and restrict or ban the account
> 2. **Credential exposure** — cookies grant full account access; using a secondary account limits the blast radius if credentials are ever compromised

> 🍪 **Cookies / login sessions:**
>
> For platforms whose traditional CLIs require cookies (Twitter, Xueqiu, etc.), **prefer importing with Cookie-Editor**. This is the simplest and most reliable method:
> 1. The user logs in to the platform in their own browser
> 2. Install the [Cookie-Editor](https://chromewebstore.google.com/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm) Chrome extension
> 3. Click the extension → Export → Header String
> 4. Send the exported string to the agent
>
> Twitter only accepts content explicitly exported by the user through Cookie-Editor. Agent Reach does not log in to XiaoHongShu for the user or read XiaoHongShu browser cookies; XiaoHongShu's OpenCLI backend only uses an existing Chrome session explicitly controlled by the user. If no session exists, export through Cookie-Editor and configure xiaohongshu-mcp or an existing tool instead. Xueqiu and Bilibili support explicit platform-specific imports, for example `agent-reach configure --from-browser chrome --platform xueqiu`; this command does not scan or save other platforms.

**Twitter search & posting:**
> "To unlock Twitter search, I need your Twitter cookies. Install the Cookie-Editor Chrome extension, go to x.com/twitter.com, click the extension → Export → Header String, and paste it to me."

```bash
agent-reach configure twitter-cookies
```

This saves `twitter_auth_token` and `twitter_ct0` for Agent Reach's own
`doctor` configuration checks. `doctor` does not run the upstream `twitter status`
command live or modify the current shell. Before running `twitter search/read/...` directly, explicitly set these variables in that process's environment:

```bash
export TWITTER_AUTH_TOKEN="..."
export TWITTER_CT0="..."
twitter search "query" -n 10
```

> **Proxy notes (mainland China and other networks that require a proxy):**
>
> twitter-cli and rdt-cli use Python. Configure a proxy through environment variables when the network requires one.
>
> **What you (the agent) need to do:**
> 1. Confirm that the user has configured a proxy: `agent-reach configure proxy` (hidden input)
> 2. Set the environment variables: `export HTTP_PROXY="..." HTTPS_PROXY="..."`
> 3. Agent Reach handles the rest automatically; the user needs no further steps
>
> If the user reports "fetch failed", see [troubleshooting.md](troubleshooting.md)

**Reddit (login is mandatory — no zero-config path):**
> Reddit has blocked anonymous endpoints, and its official API requires manual approval. Desktop users should prefer OpenCLI (available once logged in to reddit.com in the browser); server users or existing installations can use rdt-cli:

```bash
# PyPI lags upstream; install from GitHub (same pinned revision as _RDT_GIT_SOURCE in the code)
pipx install 'git+https://github.com/public-clis/rdt-cli.git@5e4fb3720d5c174e976cd425ccc3b879d52cac66'
rdt login   # Extract browser cookies automatically; on a server without a browser, follow doctor to enter cookies manually
```

> Accessing Reddit from mainland China requires a proxy. If the server IP is flagged, configure a residential proxy (for example https://webshare.io, about $1/month):
> ```bash
> agent-reach configure proxy
> ```

**XiaoHongShu (multiple backends; choose for your environment):**

> **Authentication boundaries:** Agent Reach does not log in to XiaoHongShu for the user
> or read browser cookies. OpenCLI only uses an existing Chrome session explicitly controlled by the user;
> `agent-reach configure xhs-cookies` does not inject cookies into OpenCLI or Chrome.
> If there is no existing session, do not log in automatically. Instead, manually export through Cookie-Editor
> and configure xiaohongshu-mcp or an existing tool:
>
> ```bash
> agent-reach configure xhs-cookies
> ```
>
> This explicit command saves/imports the user-provided cookie set for the xiaohongshu.com domain;
> confirm the cookie names and scope first. Cookies outside xiaohongshu.com are ignored.
>
> **Desktop (OpenCLI recommended):**

```bash
agent-reach install --system --channels opencli
```

> After installation, guide the user through the one manual step (Chrome security restrictions prevent doing it for them):
> 1. Open https://chromewebstore.google.com/detail/opencli/ildkmabpimmkaediidaifkhjpohdnifk
> 2. Click "Add to Chrome"
> 3. Run `opencli doctor` to verify (`Extension: connected` means success)
>
> If AUTH_REQUIRED appears and the user has no existing session, do not log in automatically for them.
> Use the Cookie-Editor route below for xiaohongshu-mcp or an existing tool instead.
>
> **Server / headless environment (xiaohongshu-mcp):**
> 1. Download the binary for the platform from https://github.com/xpzouying/xiaohongshu-mcp/releases to `~/.agent-reach/tools/`
> 2. Start the service (the first run automatically downloads a roughly 150MB headless browser; wait for it to finish)
> 3. Import cookies manually using the Cookie-Editor procedure above
> 4. Connect it: `mcporter config add xiaohongshu http://localhost:18060/mcp --scope home`
> 5. Always include `--timeout 120000` when making calls
>
> **Existing users (xhs-cli):** An already-installed xhs-cli continues to work as a fallback backend
> (upstream maintenance stopped in March 2026; new installations are not recommended).
> Authentication still uses the manual Cookie-Editor export procedure above.

**Facebook / Instagram (desktop OpenCLI):**
> Both platforms use OpenCLI: it reuses the user's own Chrome login session, does not save account passwords, and avoids the Meta Graph API approval process. Server/headless environments are not recommended or supported.

```bash
agent-reach install --system --channels facebook,instagram
```

> After installation:
> 1. Confirm that Chrome has the OpenCLI extension and passes `opencli doctor`
> 2. Log in to facebook.com / instagram.com in Chrome
> 3. The agent calls the tools directly:
>    ```bash
>    opencli facebook search "query" -f yaml
>    opencli facebook profile zuck -f yaml
>    opencli facebook groups -f yaml
>    opencli instagram search "query" -f yaml     # User search
>    opencli instagram profile nasa -f yaml
>    opencli instagram user nasa -f yaml          # Recent posts by the specified user
>    ```
>
> Facebook Groups currently only guarantees access to group lists/recent activity visible to the logged-in user, not arbitrary group-post or comment APIs. Instagram search finds users, not site-wide posts by keyword. If a 429/login error appears, first ask the user to log in again in Chrome and reduce request frequency.

**Xueqiu (stock quotes + popular posts):**
> "Xueqiu requires cookies from a logged-in session. First log in to xueqiu.com in Chrome, then run:"

```bash
agent-reach configure --from-browser chrome --platform xueqiu
```

> Only the minimum cookies needed by Xueqiu are read and saved; other platforms are not read.

**Xiaoyuzhou Podcast (Groq Whisper):**
> "Xiaoyuzhou podcast transcription is installed by default. All you need is a free Groq API key."

The script is automatically installed with Agent Reach; the user only needs to provide a key:

```bash
agent-reach configure groq-key
```

> **Get a Groq API key (free, no credit card, about 30 seconds):**
> 1. Open https://console.groq.com
> 2. Log in (or sign up) with a Google/GitHub account
> 3. Left menu → API Keys → Create API Key
> 4. Copy the key (starts with `gsk_`) and send it to the agent
>
> **Usage:**
> The user sends a Xiaoyuzhou link, and the agent automatically calls:
> ```bash
> bash ~/.agent-reach/tools/xiaoyuzhou/transcribe.sh https://www.xiaoyuzhoufm.com/episode/xxxxx
> ```
>
> Automatically download audio → transcode and split → transcribe with Groq Whisper → output a complete Chinese transcript.
>
> **Free quota and limitations:**
> - Approximately 2 hours of audio (7200 seconds) per hour; after exceeding the quota, wait 15 minutes for it to reset automatically
> - Enough for a few podcasts in daily use
> - High-quality transcription (Whisper large-v3), but no speaker identification
> - Process podcasts longer than 2 hours in batches

**LinkedIn (optional — mcp-server-linkedin):**
> "Basic LinkedIn content is readable through Jina Reader. Full functionality (profile details, people search, and job search) requires mcp-server-linkedin."

> **Configuration (stdio recommended):**
> First install `uv` using the official instructions (this also provides `uvx`):
> https://docs.astral.sh/uv/getting-started/installation/
>
> ```bash
> mcporter config add linkedin --command uvx --arg mcp-server-linkedin@latest --env UV_HTTP_TIMEOUT=300 --scope home
> ```
>
> `uvx` fetches and starts the latest server on demand; there is no need to install a separate Python package or keep an HTTP service running.
>
> **First login (requires a visible browser):**
> ```bash
> uvx mcp-server-linkedin@latest --login
> ```
> When the browser opens, log in to LinkedIn manually; the login session is saved in `~/.linkedin-mcp/profile/`. On a headless server, run the same login command in a visible desktop such as VNC.
>
> See https://github.com/stickerdaniel/linkedin-mcp-server for details.

**BOSS Zhipin (desktop only — boss-agent-cli + CDP):**

When the user says "help me set up BOSS Zhipin", the agent handles the automatable steps and leaves only website login to the user:

1. Explain that an upstream CLI will be installed and Chrome will be launched with a separate profile directory, then request approval for system installation.
2. After the user agrees, run:
   ```bash
   agent-reach install --env=local --system --channels=boss
   ```
3. Launch a dedicated Chrome instance for the operating system, bound only to the local loopback address:
   ```bash
   # macOS
   open -na "Google Chrome" --args --remote-debugging-address=127.0.0.1 \
     --remote-debugging-port=9222 --user-data-dir="$HOME/.boss-chrome-profile" \
     "https://www.zhipin.com/web/geek/job"

   # Linux
   google-chrome --remote-debugging-address=127.0.0.1 \
     --remote-debugging-port=9222 --user-data-dir="$HOME/.boss-chrome-profile" \
     "https://www.zhipin.com/web/geek/job"
   ```
   Windows PowerShell:
   ```powershell
   Start-Process chrome.exe -ArgumentList '--remote-debugging-address=127.0.0.1','--remote-debugging-port=9222',"--user-data-dir=$env:USERPROFILE\.boss-chrome-profile",'https://www.zhipin.com/web/geek/job'
   ```
4. Pause and ask the **user to visually confirm** the login state in the window (an avatar appears at the top right).
   If not logged in, ask the **user to log in manually**, scan the QR code, or handle the slider challenge.
   The agent does not request account passwords or log in for the user. Do not substitute `boss status`
   for this step: it only validates local `session.enc`, which does not prove that this Chrome instance is logged in.
5. After the user confirms login, run:
   ```bash
   boss --cdp-url http://localhost:9222 login --cdp
   agent-reach doctor    # Check the browser wt2 cookie probe result in the boss row message
   ```

> Security boundary: any local process that can access debugging port 9222 can fully control this Chrome instance.
> Always use `--remote-debugging-address=127.0.0.1`; never expose it to the LAN or public internet.
> Use a separate profile and reuse it long-term rather than deleting or recreating it each time. Do not switch
> to the user's everyday Chrome profile by default. Close the dedicated Chrome window when unused.
> Boss does not support server/headless environments. Search commands must include
> `--browser-source existing-browser --cdp-url http://localhost:9222`.
>
> Dependency: the follow-up split PRs #403–#407 for boss-agent-cli have been merged into upstream master.
> The installer pins upstream commit
> `4c991b77086a203173bf08a4cb64a23af6514fe6` instead of tracking a moving branch. This commit includes
> `browser_source="existing-browser"` (strict CDP), `JobItem.lid`, and `job_card_browser()`.
> Once upstream publishes an official release, Agent Reach should switch to a version constraint.

### Step 4: Final check

Run `agent-reach doctor` one final time and report the results to your user.

### Step 5: Set up daily monitoring (OpenClaw only)

If you are running inside **OpenClaw**, ask your user:

> "Agent Reach is installed. Would you like a daily automatic check? It will monitor channel health and new versions, and notify you only when something needs attention."

If the user agrees, create a **cron job** (daily, `sessionTarget: "isolated"`, `delivery: "announce"`) with this task:

```
Run agent-reach watch.
If the output contains "All healthy", finish silently without notifying the user.
If the output reports problems (❌ ⚠️) or a new version (🆕), send the full report to the user and suggest fixes.
If a new version is available, ask whether the user wants to upgrade (send this to the user's agent for the full update procedure: Update Agent Reach: https://raw.githubusercontent.com/Panniantong/agent-reach/main/docs/update.md).
```

If the user wants a different agent to handle it, let them choose.

---

## Quick Reference

| Command | What it does |
|---------|-------------|
| `agent-reach install --env=auto` | Read-only dependency and channel check (default) |
| `agent-reach install --env=auto --system` | Explicitly install/configure core external tools |
| `agent-reach install --env=auto --system --channels=twitter,xiaohongshu` | Install approved optional channels |
| `agent-reach install --env=local --system --channels=boss` | Install the desktop BOSS Zhipin strict-CDP backend |
| `agent-reach install --env=auto --system --channels=all` | Install everything after explicit approval |
| `agent-reach install --env=auto --safe` | Compatibility alias for the safe default |
| `agent-reach install --env=auto --dry-run` | Preview what would be done |
| `agent-reach doctor` | Show channel status |
| `agent-reach watch` | Quick health + update check (for scheduled tasks) |
| `agent-reach check-update` | Check for new versions |
| `agent-reach configure twitter-cookies` | Save Twitter cookies through hidden input; direct calls still require explicit environment variables |
| `agent-reach configure proxy` | Save a proxy URL through hidden input; does not automatically bypass access restrictions |
| `agent-reach configure groq-key` | Configure the Xiaoyuzhou transcription key through hidden input |

After installation, use upstream tools directly. See SKILL.md for the full command reference:

| Platform | Upstream Tool | Example |
|----------|--------------|---------|
| Twitter/X | `twitter` (`opencli` fallback) | Set `TWITTER_AUTH_TOKEN` / `TWITTER_CT0`, then run `twitter search "query" -n 10` |
| YouTube | `yt-dlp` | `yt-dlp --dump-json URL` |
| Bilibili | `bili` (`opencli` for subtitles) | `bili search "query" --type video` / `opencli bilibili subtitle BVxxx` |
| Reddit | `opencli` (`rdt` fallback) | `opencli reddit search "query" -f yaml` / `rdt read POST_ID` |
| Facebook | `opencli` | `opencli facebook search "query" -f yaml` |
| Instagram | `opencli` | `opencli instagram user nasa -f yaml` |
| GitHub | `gh` | `gh search repos "query"` |
| Web | `curl` + Jina | `curl -s "https://r.jina.ai/URL"` |
| Exa Search | `mcporter` | `mcporter call exa.web_search_exa query="..." numResults=5` |
| XiaoHongShu | `opencli` (`mcporter` on servers) | `opencli xiaohongshu search "query" -f yaml` |
| Xiaoyuzhou Podcast | `transcribe.sh` | `bash ~/.agent-reach/tools/xiaoyuzhou/transcribe.sh <URL>` |
| LinkedIn | `mcporter` | `mcporter call linkedin.get_person_profile linkedin_username="..."` |
| BOSS Zhipin | `boss` / Python public API | `agent-reach doctor` (browser wt2 probe; `boss status` only reflects local session.enc); see `references/career.md` for search and job descriptions |
| RSS | `feedparser` | `python3 -c "import feedparser; ..."` |

> For multi-backend platforms, use the `active_backend` value from `agent-reach doctor --json` as the source of truth.

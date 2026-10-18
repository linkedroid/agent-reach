# Changelog

All notable changes to this project will be documented in this file.

---

## [Unreleased]

### 🐛 Bug Fixes

#### 🔐 BOSS Zhipin — Incorrect login-state detection (two credential stores)

- **Root cause:** Boss has two independent login-state stores: local `~/.boss-agent/auth/session.enc`
  and browser cookies in the dedicated Chrome profile. `boss status` / `status --live` **only validates the former**
  (a legacy credential store from the Bridge/httpx era), while searches in strict `existing-browser` CDP mode use browser cookies.
  When local credentials are stale and the browser is not logged in, `boss status` reports `logged_in: true`, misleading the agent
  into skipping login and searching immediately, which results in `AUTH_EXPIRED`. The old runbook also prohibited interpreting
  `_security_check` as a missing login. Together, these rules pushed the agent down the incorrect "anti-bot slider" path.
- **Fix:** Added a fourth read-only check, `_cdp_zhipin_login_cookie()`, to `check()`. A minimal WebSocket client implemented
  entirely with the standard library asks the CDP browser directly (`Storage.getCookies`) whether it contains a zhipin
  `wt2` cookie. **The browser is the source of truth.** This adds no dependencies, launches no browser, and performs no searches.
  No wt2 → explicitly report that the browser is not logged in and searches will return AUTH_EXPIRED, directing the user to
  log in and run `login --cdp`. Probe failure → report an unknown login state. Security-check page messages also include browser cookie status.
- **Runbook correction:** Removed the misleading rule to trust only `boss status` when determining login state; use doctor's
  browser-cookie probe instead. After launching dedicated Chrome, **always pause for the user to visually confirm** the login state.
  Treat `AUTH_EXPIRED` as ground truth: go directly to the login procedure and never interpret it as a security check.
  Handle `_security_check` as a slider challenge only when `AUTH_EXPIRED` is absent.

### ✨ Features

#### 🎯 BOSS Zhipin channel

- Added the `boss` channel: search jobs and retrieve full job descriptions through boss-agent-cli + CDP with real Chrome.
- `check()` performs four read-only checks: boss-agent-cli installed → port 9222 reachable → zhipin tab present
  → `wt2` login cookie present in the browser.
- Retrieval uses the public API (`search_jobs` + `job_card_browser` + `browser_source="existing-browser"`).
- `agent-reach install --system --channels=boss` installs the backend pinned to an upstream boss-agent-cli commit
  (#403–#407 have merged into master). Switch back to a version constraint once upstream publishes an official release.
- The skill and installation guide support "Set up BOSS Zhipin for me": the agent launches dedicated Chrome listening only
  on the loopback address, the user logs in manually, and the agent then verifies login state and the CDP connection.
- Changed the pinned dependency from fork snapshot `8ff6bd3` to upstream commit `4c991b7` (#403–#407 merged into master).
  Already-authenticated CDP sessions can be reused directly, and searches can use `--browser-source existing-browser`
  to prevent a headless fallback.
- Classify code 37 using the original message: environment anomalies become `ENVIRONMENT_RISK` and stop immediately;
  allow a single refresh only when token/stoken expiration is explicit. Reuse the dedicated Chrome profile long-term and reduce request frequency.

## [1.3.1] - 2026-03-27

### 🐛 Bug Fixes

#### 📈 Xueqiu — Comprehensive fixes

- **Fixed the root cause of 400 errors:** `_ensure_cookies()` only visited the homepage, which yielded `acw_tc` (an anti-DDoS token). Xueqiu's frontend JavaScript dynamically generates `xq_a_token`, which cannot be obtained with plain HTTP requests. Added a three-level cookie-loading strategy: ① read the config file (saved by `--from-browser`) → ② automatically extract from local Chrome (requires browser-cookie3) → ③ homepage fallback.
- **Fixed User-Agent:** Xueqiu's anti-scraping system rejected `"agent-reach/1.0"`; replaced it with a real Chrome UA.
- **Fixed the missing `Referer` header:** Added `Referer: https://xueqiu.com/` to every API request.
- **Fixed the `get_hot_posts()` endpoint:** The old `/statuses/hot/listV3.json` endpoint was retired (returned an empty body). Replaced it with `/v4/statuses/public_timeline_by_category.json` and correctly parse the `item.data` JSON string for author/likes/text.
- **Fixed `urllib.request.quote` → `urllib.parse.quote`:** Explicitly use the correct module.
- **Fixed `configure --from-browser` not extracting Xueqiu cookies:** Added Xueqiu to `PLATFORM_SPECS`; only save cookies when `xq_a_token` is present.
- **Corrected misleading documentation:** Replaced "no configuration required" / "public API, no login required" in README/SKILL.md with accurate browser-cookie requirements.
- **Improved error messages:** When `check()` fails, recommend `configure --from-browser chrome` instead of suggesting that a proxy may be needed.

---

## [1.3.0] - 2026-03-12

### 🆕 New Channels

#### 💻 V2EX
- Hot topics, node topics, topic detail + replies, user profile via public JSON API
- Zero config — no auth, no proxy, no API key required
- `get_hot_topics(limit)`, `get_node_topics(node_name, limit)`, `get_topic(id)`, `get_user(username)`

### 📈 Improvements

- Channel count: 14 → 15

---

## [1.1.0] - 2025-02-25

### 🆕 New Channels

#### ~~📷 Instagram~~ (removed — upstream blocked)
- ~~Read public posts and profiles via [instaloader](https://github.com/instaloader/instaloader)~~
- **Removed:** Instagram's aggressive anti-scraping measures broke all available open-source tools (instaloader, etc.). See [instaloader#2585](https://github.com/instaloader/instaloader/issues/2585). Will re-add when upstream recovers.

#### 💼 LinkedIn
- Read person profiles, company pages, and job details via [linkedin-scraper-mcp](https://github.com/stickerdaniel/linkedin-mcp-server)
- Search people and jobs via MCP, with Exa fallback
- Fallback to Jina Reader when MCP is not configured

#### 🏢 BOSS Zhipin
- QR code login via [mcp-bosszp](https://github.com/mucsbr/mcp-bosszp)
- Job search and recruiter greeting via MCP
- Fallback to Jina Reader for reading job pages

### 📈 Improvements

- Channel count: 9 → 12
- `agent-reach doctor` now detects all 12 channels
- CLI: added `search-linkedin`, `search-bosszhipin` subcommands
- Updated install guide with setup instructions for new channels
- Historical discrepancy: the original Chinese notes listed the channel count as 9 → 11 and doctor as detecting all 11 channels, while the original English notes listed 12.

---

## [1.0.0] - 2025-02-24

### 🎉 Initial Release

- 9 channels: Web, Twitter/X, YouTube, Bilibili, GitHub, Reddit, XiaoHongShu, RSS, Exa Search
- CLI with `read`, `search`, `doctor`, `install` commands
- Unified channel interface — each platform is a single pluggable Python file
- Auto-detection of local vs server environments
- Built-in diagnostics via `agent-reach doctor`
- Skill registration for Claude Code / OpenClaw / Cursor

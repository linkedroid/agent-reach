# Troubleshooting

## Xueqiu: API returns 400

**Symptom:** `agent-reach doctor` shows a warning for Xueqiu with `HTTP Error 400`.

**Cause:** The Xueqiu API requires login cookies, which cannot be obtained through anonymous access.

**Solution:** Log in to xueqiu.com in Chrome, then run:

```bash
agent-reach configure --from-browser chrome --platform xueqiu
```

Run `agent-reach doctor` again to confirm that the channel is back to ✅. Repeat this command when the cookies expire.

---

## BOSS Zhipin: `boss status` reports a login, but search returns `AUTH_EXPIRED`

**Symptom:** `boss status` / `status --live` returns `logged_in: true` (possibly even with a username),
but `boss ... search` immediately returns `{"code": "AUTH_EXPIRED", "message": "用户未登录"}`
(the message means "User is not logged in").
The dedicated Chrome window may also be on a URL containing `_security_check`, which looks like an anti-bot slider challenge.

**Cause:** Boss has two login-state stores that authenticate different channels:

| Store | Consumers |
|---|---|
| `~/.boss-agent/auth/session.enc` | `boss status` / `status --live`; low-risk operations on the httpx channel (`detail` / `cities` / `job_card_httpx`). CDP search also reads it (and immediately reports "not logged in" if it cannot), but its cookies never actually take effect when reusing a real Chrome context |
| Browser cookies in `~/.boss-chrome-profile` | The credentials actually used by high-risk operations such as search / greet in strict `existing-browser` CDP mode |

`boss status` only validates the local session.enc file. If that file contains credentials from several days ago while the dedicated Chrome
profile itself is not logged in, it still reports `logged_in: true`. This does not prove that the login session is valid.
The `_security_check` page is an anti-bot challenge that **can also appear when logged in**, so it cannot establish login state.
Together, these signals can easily lead to mistaking "browser not logged in" for "stuck at a slider challenge".

> Do not delete either store. Without session.enc, CDP search fails before connecting to the browser.
> Run `login --cdp` when you need to refresh it; do not delete the file manually.

**Order of precedence:**

1. `AUTH_EXPIRED` is ground truth: if it appears, the browser is not logged in, regardless of what `boss status` says.
2. The boss row in `agent-reach doctor` directly checks whether the browser has a `wt2` cookie. Use that result.
3. Treat `boss status` as a reference only; never use the page URL as a login-state indicator.

**Solution:** Visually confirm the login state in the dedicated Chrome window and manually log in to zhipin.com, then synchronize the login state:

```bash
boss --cdp-url http://localhost:9222 login --cdp
agent-reach doctor    # The boss row should report that the browser contains a login cookie (wt2)
```

> After launching the dedicated Chrome window, always ask the user to visually confirm the login state first. Do not substitute `boss status` for this step.

---

## Twitter/X: twitter-cli connection failure

**Symptom:** `twitter search` or another command returns an error.

**Cause:** twitter-cli requires the `TWITTER_AUTH_TOKEN` and `TWITTER_CT0`
environment variables to access the Twitter API. The values saved by
`agent-reach configure twitter-cookies` are only used by doctor to check whether configuration is complete;
doctor does not perform upstream authentication or set variables in the current shell.
If your network requires a proxy to reach x.com, you also need to configure one.

**Solutions:**

### Option 1: Set credentials and proxy environment variables

```bash
export TWITTER_AUTH_TOKEN="..."
export TWITTER_CT0="..."
export HTTP_PROXY="http://user:pass@host:port"
export HTTPS_PROXY="http://user:pass@host:port"
twitter search "test" -n 1
```

### Option 2: Use a system-wide proxy tool

Route all network traffic through a proxy tool so that twitter-cli requests also use the proxy:

```bash
# macOS — enable "Enhanced Mode" in ClashX / Surge
# Linux — proxychains or tun2socks
proxychains twitter search "test" -n 1
```

### Option 3: Use Exa search instead of twitter-cli

If twitter-cli is unavailable, use Exa to search Twitter content directly:

```bash
mcporter call exa.web_search_exa query="site:x.com search terms" numResults=5
```

### Option 4: Check authentication

```bash
twitter check
```

> If it returns "Missing credentials", set `TWITTER_AUTH_TOKEN` and `TWITTER_CT0`
> in the environment of the process running that command.
>
> **Fallback:** If you already have bird CLI installed (`npm install -g @steipete/bird`), it can still work. Agent Reach automatically detects installed tools.

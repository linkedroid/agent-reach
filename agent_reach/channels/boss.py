# -*- coding: utf-8 -*-
"""BOSS Zhipin: search jobs and retrieve job descriptions with boss-agent-cli + real Chrome over CDP.

The backend is boss-agent-cli (reusing a signed-in Chrome instance via its CDP debugging port).
Headless mode is prohibited (it triggers code 36 risk controls), so check() performs only four read-only probe layers, without creating BossClient or launching a browser.

Retrieval uses the public boss-agent-cli API (search_jobs + job_card_browser + browser_source="existing-browser").
See skill/references/career.md for usage; check() only checks installation, CDP connectivity,
and the presence of browser login cookies. It does not search.

There are two login stores (past issues show that health checks must distinguish them). Both are required, but they authenticate different channels:

- `~/.boss-agent/auth/session.enc` (`boss status` / `status --live` only validate this store)
  1. This is a hard prerequisite: `_get_browser()` always calls `get_token()`, raising `AuthRequired` if unavailable.
     Do not delete it: CDP searches would fail before connecting to the browser.
  2. However, it is **not the search credential**: CDP reuses `contexts[0]` after connecting to real Chrome. These cookies
     are injected only when no context exists, so they never take effect in practice.
  3. The httpx channel (lower-risk operations: status/detail/cities/`job_card_httpx`) does use its
     cookies + stoken; code 37's `force_refresh()` also writes back to it.
- Browser cookies in the dedicated Chrome profile: these are the credentials actually sent by higher-risk
  operations such as search/greet in CDP mode.

Thus, a valid session.enc with a signed-out browser makes `boss status` report signed in while searches return
`AUTH_EXPIRED`. Layer 4 queries the CDP browser directly (Storage.getCookies), treating the browser as authoritative.
"""

import base64
import hashlib
import json
import os
import platform
import socket
import struct
import urllib.request
from urllib.parse import urlparse

from agent_reach.probe import probe_command
from agent_reach.utils.url import host_matches

from .base import Channel

_CDP_URL = "http://localhost:9222"
_CDP_TIMEOUT = 5


def _chrome_launch_command(system: str | None = None) -> str:
    """Return a dedicated-profile Chrome command for the current OS."""
    system = system or platform.system()
    common = (
        "--remote-debugging-address=127.0.0.1 "
        "--remote-debugging-port=9222 "
    )
    url = '"https://www.zhipin.com/web/geek/job"'
    if system == "Darwin":
        return (
            'open -na "Google Chrome" --args '
            + common
            + '--user-data-dir="$HOME/.boss-chrome-profile" '
            + url
        )
    if system == "Windows":
        return (
            "Start-Process chrome.exe -ArgumentList "
            "'--remote-debugging-address=127.0.0.1',"
            "'--remote-debugging-port=9222',"
            '"--user-data-dir=$env:USERPROFILE\\.boss-chrome-profile",'
            "'https://www.zhipin.com/web/geek/job'"
        )
    return (
        "google-chrome "
        + common
        + '--user-data-dir="$HOME/.boss-chrome-profile" '
        + url
    )


def _cdp_json(path: str):
    """GET a local CDP endpoint without system proxies; return parsed JSON or None on failure.

    CDP binds only to loopback (127.0.0.1), so a direct connection is sufficient. An empty ProxyHandler explicitly bypasses
    configured system/global proxies: proxying localhost probes is unnecessary and may block them. This deliberate
    localhost-only assumption must not be overridden by the proxy configuration.
    """
    req = urllib.request.Request(f"{_CDP_URL}{path}", method="GET")
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    try:
        with opener.open(req, timeout=_CDP_TIMEOUT) as resp:
            return json.loads(resp.read())
    except Exception:
        return None


def _has_zhipin_page(pages) -> bool:
    """Whether the CDP /json tab list contains a reusable zhipin.com tab (exact hostname validation)."""
    for page in pages or []:
        if page.get("type") == "page" and host_matches(page.get("url", ""), "zhipin.com"):
            return True
    return False


_SECURITY_CHECK_MARKERS = ("security-check", "zhipin-security", "_security_check")


def _security_check_blocks_all(pages) -> bool:
    """Whether all existing zhipin tabs are on anti-bot security verification pages (not login pages)."""
    zhipin_urls = [
        page.get("url", "")
        for page in (pages or [])
        if page.get("type") == "page" and host_matches(page.get("url", ""), "zhipin.com")
    ]
    if not zhipin_urls:
        return False
    return all(
        any(marker in url.lower() for marker in _SECURITY_CHECK_MARKERS)
        for url in zhipin_urls
    )


_WS_ACCEPT_GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"


def _read_ws_text_frame(sock: socket.socket, initial: bytes = b""):
    """Read the next text frame and return (payload, leftover).

    leftover contains excess bytes from recv belonging to later frames; callers must pass it back as initial
    for the next frame (one recv may contain multiple frames). Return (None, leftover) on a close frame or disconnection.
    Ignore ping/pong.
    """
    buf = initial
    while True:
        while len(buf) < 2:
            chunk = sock.recv(4096)
            if not chunk:
                return None, buf
            buf += chunk
        opcode = buf[0] & 0x0F
        length = buf[1] & 0x7F
        header_len = 2
        if length == 126:
            while len(buf) < header_len + 2:
                chunk = sock.recv(4096)
                if not chunk:
                    return None, buf
                buf += chunk
            length = struct.unpack(">H", buf[header_len:header_len + 2])[0]
            header_len += 2
        elif length == 127:
            while len(buf) < header_len + 8:
                chunk = sock.recv(4096)
                if not chunk:
                    return None, buf
                buf += chunk
            length = struct.unpack(">Q", buf[header_len:header_len + 8])[0]
            header_len += 8
        while len(buf) < header_len + length:
            chunk = sock.recv(4096)
            if not chunk:
                return None, buf
            buf += chunk
        payload = buf[header_len:header_len + length]
        buf = buf[header_len + length:]
        if opcode == 0x8:  # close
            return None, buf
        if opcode in (0x1, 0x2, 0x0):  # text / binary / continuation
            return payload, buf
        # Ignore ping(0x9)/pong(0xA), etc., and continue reading the next frame.


def _send_ws_text(sock: socket.socket, text: str) -> None:
    payload = text.encode("utf-8")
    mask = os.urandom(4)
    masked = bytes(b ^ mask[i % 4] for i, b in enumerate(payload))
    header = bytes([0x81])  # FIN + text
    n = len(payload)
    if n < 126:
        header += bytes([0x80 | n])
    elif n < 65536:
        header += bytes([0x80 | 126]) + struct.pack(">H", n)
    else:
        header += bytes([0x80 | 127]) + struct.pack(">Q", n)
    sock.sendall(header + mask + masked)


def _cdp_zhipin_login_cookie() -> bool | None:
    """Read-only probe for a zhipin.com login cookie (wt2) in the dedicated Chrome browser.

    True=present; False=absent (browser is signed out and CDP searches will return AUTH_EXPIRED);
    None=probe failed (for example, CDP WebSocket is unreachable), so login state is unknown.
    Only proves that the browser profile has signed in before; does not verify server-side cookie validity.
    """
    version = _cdp_json("/json/version")
    ws_url = (version or {}).get("webSocketDebuggerUrl")
    if not ws_url:
        return None
    parsed = urlparse(ws_url)
    host = parsed.hostname or "127.0.0.1"
    port = parsed.port or 80
    path = parsed.path or "/"
    try:
        with socket.create_connection((host, port), timeout=_CDP_TIMEOUT) as sock:
            sock.settimeout(_CDP_TIMEOUT)
            key = base64.b64encode(os.urandom(16)).decode()
            # Bracket IPv6 literals in the Host header (urlparse().hostname strips the brackets).
            host_header = f"[{host}]:{port}" if ":" in host else f"{host}:{port}"
            handshake = (
                f"GET {path} HTTP/1.1\r\n"
                f"Host: {host_header}\r\n"
                "Upgrade: websocket\r\n"
                "Connection: Upgrade\r\n"
                f"Sec-WebSocket-Key: {key}\r\n"
                "Sec-WebSocket-Version: 13\r\n"
                "\r\n"
            )
            sock.sendall(handshake.encode())
            response = b""
            while b"\r\n\r\n" not in response:
                chunk = sock.recv(4096)
                if not chunk:
                    return None
                response += chunk
            head, _, rest = response.partition(b"\r\n\r\n")
            status_line = head.split(b"\r\n", 1)[0]
            # Parse the exact status-code token: accept "HTTP/1.1 101" (optional reason phrase), reject fake codes such as 1019.
            if status_line.split()[1:2] != [b"101"]:
                return None
            accept = base64.b64encode(
                hashlib.sha1((key + _WS_ACCEPT_GUID).encode()).digest()
            ).decode()
            if accept not in head.decode("latin-1"):
                return None
            _send_ws_text(sock, json.dumps({"id": 1, "method": "Storage.getCookies"}))
            # Chrome may send event frames first (no id); read until the id==1 response arrives, with a limit to prevent infinite loops.
            # leftover preserves excess bytes from the previous recv so multiple frames in one recv do not lose data.
            buf = rest
            for _ in range(16):
                payload, buf = _read_ws_text_frame(sock, initial=buf)
                if payload is None:
                    return None
                data = json.loads(payload.decode("utf-8"))
                if data.get("id") != 1:
                    continue  # Skip event frames, etc., and read the next frame.
                if "result" not in data:
                    return None
                for cookie in data["result"].get("cookies", []):
                    if cookie.get("name") == "wt2" and "zhipin" in cookie.get("domain", ""):
                        return True
                return False
            return None
    except Exception:
        return None


class BossChannel(Channel):
    name = "boss"
    description = "BOSS Zhipin job search and descriptions"
    backends = ["boss-agent-cli (CDP)"]
    tier = 2

    def can_handle(self, url: str) -> bool:
        return host_matches(url, "zhipin.com")

    def check(self, config=None):
        self.active_backend = None

        # Layer 1: Is boss-agent-cli installed?
        probe = probe_command("boss", ["--version"], timeout=10)
        if probe.status == "missing":
            return "off", (
                "boss-agent-cli is not installed. Obtain user authorization first, then run:\n"
                "  agent-reach install --system --channels=boss\n"
                "After installation, the user must manually sign in to zhipin.com in the dedicated Chrome browser."
            )
        if probe.status == "broken":
            return "error", (
                "The boss command exists but cannot run; the installation is broken. Reinstall:\n"
                "  agent-reach install --system --channels=boss"
            )
        if not probe.ok:
            return "warn", f"boss command probe failed ({probe.status}); check the installation"

        # Layer 2: Is the CDP port reachable?
        if _cdp_json("/json/version") is None:
            return "off", (
                "The CDP debugging port is unreachable. Start Chrome with debugging enabled first:\n"
                f"  {_chrome_launch_command()}\n"
                "  Then have the user manually sign in to zhipin.com in that window.\n"
                "Bind only to 127.0.0.1; any process that can access port 9222 can fully control this Chrome instance."
            )

        # Layer 3: Is there a reusable BOSS Zhipin tab?
        pages = _cdp_json("/json")
        if pages is None:
            return "warn", "The CDP port is reachable, but /json tab enumeration failed"
        if not _has_zhipin_page(pages):
            return "warn", (
                "CDP is reachable, but no existing zhipin.com tab was found (this does not mean you are signed out: cookies may still exist, and "
                "boss-agent-cli will create a tab itself). Sign in to zhipin.com in Chrome first."
            )

        # Layer 4: Browser login cookie (wt2). The browser is authoritative; `boss status` only validates
        # local session.enc, which does not reflect the browser login state or vice versa.
        browser_cookie = _cdp_zhipin_login_cookie()
        if browser_cookie is False:
            return "warn", (
                "The CDP connection is ready, but the dedicated Chrome browser has no zhipin.com login cookie (wt2); "
                "the browser is signed out, and searches will return AUTH_EXPIRED. The logged_in reported by `boss status` "
                "only describes local session.enc credentials, not browser login. Have the user visually check and sign in to zhipin.com in that Chrome window "
                "(do this first after launching CDP Chrome), then run "
                "`boss --cdp-url http://localhost:9222 login --cdp` to synchronize the login state."
            )

        cookie_note = (
            "login cookie (wt2) is present in the browser" if browser_cookie else "browser login-cookie probe failed; login state is unknown"
        )

        if _security_check_blocks_all(pages):
            return "warn", (
                f"The CDP connection is ready, but all existing zhipin tabs are on security verification pages "
                "(security-check / zhipin-security). This is a BOSS Zhipin anti-bot challenge, unrelated to login; "
                "it can appear while signed in and does not mean you are signed out. Do not ask the user to sign in again because of this; "
                "have them manually complete the slider challenge. "
                f"Browser login-state reference: {cookie_note}. "
                "Do not use `boss status` to determine CDP browser login state (it only validates local session.enc)."
            )

        # All four probe layers passed: CDP is ready; mark the backend actually serving the channel (base contract).
        self.active_backend = self.backends[0]
        return "warn", (
            f"The CDP connection is ready (port 9222 is reachable and a reusable zhipin tab exists; {cookie_note}). "
            "Doctor does not run searches or verify server-side cookie validity or upstream boss-agent-cli #403-#407 APIs; "
            "first run `boss --cdp-url http://localhost:9222 login --cdp` to synchronize the existing login state; "
            "use `boss --browser-source existing-browser --cdp-url http://localhost:9222 search ...` for searches, "
            "ensuring execution stops immediately if CDP is unavailable instead of falling back to headless mode. "
            "If a search returns AUTH_EXPIRED, follow the login runbook (the user signs in in the dedicated window, then run login --cdp); "
            "do not interpret it as a security verification challenge."
        )

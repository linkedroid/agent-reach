# -*- coding: utf-8 -*-
"""Reddit — multi-backend: OpenCLI / rdt-cli. Login is mandatory.

Honest tiering (live-verified 2026-06): there is NO zero-config path.
Anonymous .json endpoints are blocked (403 anti-bot, all variants), and
the official API closed self-service registration in 2025-11 (manual
approval, individual scripts rarely granted — PRAW is only an option for
users who already hold credentials). Every working backend rides a
logged-in session: OpenCLI reuses the browser's, rdt-cli imports cookies.
"""

import json
import shutil
import time
from pathlib import Path

from agent_reach.utils.paths import (
    PrivatePathError,
    read_small_text_no_follow,
)

from .base import Channel

_CREDENTIAL_FILE = "~/.config/rdt-cli/credential.json"
_CREDENTIAL_TTL_SECONDS = 7 * 86400
_MAX_CREDENTIAL_BYTES = 1024 * 1024
# Pinned to the 0.4.2 state — PyPI still only has 0.4.1 (upstream issue #10).
_RDT_GIT_SOURCE = "git+https://github.com/public-clis/rdt-cli.git@5e4fb3720d5c174e976cd425ccc3b879d52cac66"

class RedditChannel(Channel):
    name = "reddit"
    description = "Reddit posts and comments"
    backends = ["OpenCLI", "rdt-cli"]
    tier = 1  # no zero-config path exists — see module docstring

    def can_handle(self, url: str) -> bool:
        from agent_reach.utils.url import host_matches

        return host_matches(url, "reddit.com", "redd.it")

    def check(self, config=None):
        """Probe candidates in order; first fully-usable backend wins."""
        self.active_backend = None
        findings = []

        for backend in self.ordered_backends(config):
            if backend == "OpenCLI":
                result = self._check_opencli()
            else:
                result = self._check_rdt()
            if result is None:
                continue
            findings.append((backend, *result))

        for wanted in ("ok", "warn"):
            for backend, status, message in findings:
                if status == wanted:
                    self.active_backend = backend if status == "ok" else None
                    return status, message

        if findings:
            return "error", "\n".join(m for _, _, m in findings)

        return "off", (
            "No Reddit backend is installed. Note: Reddit has no zero-configuration option "
            "(anonymous .json access is blocked and the official API requires manual approval); a login session is required. Recommended:\n"
            "  Desktop: agent-reach install --system --channels opencli\n"
            "       (reuses your Chrome session; available after signing in to reddit.com)\n"
            f"  Server/existing setups: pipx install '{_RDT_GIT_SOURCE}'\n"
            "       Then run `rdt login` or manually save cookies (see doctor guidance)\n"
            "A proxy is required to access Reddit from mainland China"
        )

    def _check_opencli(self):
        """OpenCLI candidate. None = not installed."""
        from agent_reach.backends import opencli_status

        st = opencli_status()
        if not st.installed:
            return None
        if st.broken:
            return "error", st.hint
        if st.ready:
            return "warn", (
                "The OpenCLI bridge is connected, but the Reddit login state and actual commands have not been verified live; "
                "Doctor does not run platform commands, so this is not currently marked as available."
            )
        return "warn", st.hint

    def _check_rdt(self):
        """Inspect rdt's saved credential without invoking its auto-refresh."""
        if not shutil.which("rdt"):
            return None

        credential_path = Path.home() / ".config" / "rdt-cli" / "credential.json"
        try:
            payload = read_small_text_no_follow(
                credential_path,
                max_bytes=_MAX_CREDENTIAL_BYTES,
            )
        except PrivatePathError as exc:
            return "warn", (
                f"rdt-cli is installed, but credential.json cannot be read safely: {exc}."
            )
        except OSError:
            return "warn", (
                "rdt-cli is installed, but credential.json cannot be read safely; "
                "Doctor did not run `rdt status`, which automatically refreshes cookies."
            )
        if payload is None:
            return "warn", self._rdt_login_hint()
        try:
            data = json.loads(payload)
        except (UnicodeError, json.JSONDecodeError, ValueError):
            return "warn", (
                "rdt-cli is installed, but the saved credential.json cannot be parsed safely; "
                "Doctor did not run `rdt status`, which automatically refreshes cookies."
            )
        if not isinstance(data, dict):
            return "warn", self._rdt_login_hint()
        cookies = data.get("cookies")
        if not isinstance(cookies, dict) or not cookies.get("reddit_session"):
            return "warn", self._rdt_login_hint()

        saved_at = data.get("saved_at")
        if isinstance(saved_at, (int, float)) and (
            time.time() - saved_at > _CREDENTIAL_TTL_SECONDS
        ):
            return "warn", (
                "rdt-cli is installed, but the saved cookies are over 7 days old; Doctor will not let "
                "upstream automatically read the browser or refresh files. Update them explicitly with Cookie-Editor."
            )
        return "warn", (
            "rdt-cli is installed and explicitly saved Reddit cookies were detected; to avoid "
            "upstream automatically refreshing browser cookies, Doctor does not run `rdt status`, so live verification has not been performed."
        )

    @staticmethod
    def _rdt_login_hint():
        return (
            "rdt-cli is installed but no usable explicit cookies were found. Use Cookie-Editor:\n"
            "  1. Install the Cookie-Editor extension from the Chrome Web Store:\n"
            "     https://chromewebstore.google.com/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm\n"
            "  2. Open reddit.com in your browser (make sure you are signed in)\n"
            "  3. Click the Cookie-Editor icon, find `reddit_session`, and copy its Value\n"
            f"  4. Write the following to {_CREDENTIAL_FILE}:\n"
            '     {"cookies": {"reddit_session": "<paste Value>"}, '
            '"source": "manual", "username": "<your username>", '
            '"modhash": null, "saved_at": 0, "last_verified_at": null}\n\n'
            "Doctor does not run `rdt status`, which automatically reads the browser and writes files."
        )

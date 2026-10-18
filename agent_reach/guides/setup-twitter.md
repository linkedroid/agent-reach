# Twitter advanced features setup guide (twitter-cli)

Basic Twitter reading is available free through Jina Reader, with no setup required.

Advanced features require twitter-cli (@public-clis/twitter-cli):

- Tweet search (`twitter search`)
- Full tweets and conversation threads (`twitter tweet`, `twitter thread`)
- User timelines (`twitter timeline`)
- Long-form articles (`twitter article`)

twitter-cli is a free, open-source tool installed with pipx, but it requires cookies
from your Twitter account.

## Quick setup

1. Check whether twitter-cli is installed:

```bash
which twitter && echo "installed" || echo "not installed"
```

2. Install twitter-cli:

```bash
pipx install twitter-cli
```

3. Confirm the command is installed (do not make an authentication request yet):

```bash
twitter --help
```

## Get cookies with Cookie-Editor (recommended)

1. Install the [Cookie-Editor](https://cookie-editor.com/) browser extension
2. Log in to x.com
3. Click the Cookie-Editor icon → Export → Header String
4. Run the configuration command:

```bash
agent-reach configure twitter-cookies
```

This extracts `auth_token` and `ct0` and securely saves them to
`~/.agent-reach/config.yaml`, where `agent-reach doctor` checks that explicit
credentials are complete. `doctor` does not run `twitter status` or verify the account
live, and does not modify the current shell.

By default, only `~/.agent-reach/config.yaml` is written. The following extra files
are written only if the user explicitly approves copying credentials and you
explicitly add `--sync-legacy-twitter`:

- `~/.config/xfetch/session.json`
- `~/.config/bird/credentials.env`

```bash
agent-reach configure twitter-cookies --sync-legacy-twitter
```

`agent-reach uninstall` only warns about these legacy copies; it does not delete
them automatically. To clean them up, obtain user confirmation first, then manually
delete the two files above.

`twitter` is a separate upstream command and does not read Agent Reach's configuration.
When running `twitter status/search/read/...` directly, explicitly set
`TWITTER_AUTH_TOKEN` and `TWITTER_CT0` in the current shell or child-process environment
as shown below. Do not rely on automatic browser-cookie extraction.

## Set cookies manually

If you already know your `auth_token` and `ct0`:

1. Install twitter-cli if needed: `pipx install twitter-cli`

2. Set the environment variables:

```bash
export TWITTER_AUTH_TOKEN="YOUR_AUTH_TOKEN"
export TWITTER_CT0="YOUR_CT0"
```

3. Test:

```bash
twitter search "test" -n 1
```

## Proxy configuration

> twitter-cli supports proxy configuration through environment variables:

```bash
export HTTP_PROXY="http://user:pass@host:port"
export HTTPS_PROXY="http://user:pass@host:port"
twitter search "test" -n 1
```

You can also use a system-wide proxy tool:

```bash
proxychains twitter search "test" -n 1
```

## Fallback: bird CLI

If [bird CLI](https://www.npmjs.com/package/@steipete/bird)
(`npm install -g @steipete/bird`) is already installed, it still works. Agent Reach
automatically detects and uses an existing bird installation. The two tools offer
similar features; twitter-cli is the currently recommended option.

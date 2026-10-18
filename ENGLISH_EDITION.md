# Agent Reach: English-localized source edition

This is a local English translation of [Panniantong/Agent-Reach](https://github.com/Panniantong/Agent-Reach), based on upstream commit `94f06c1969dfc1834001269d79d3ad0972d9dee6` (retrieved October 18, 2026). It is not an official upstream release or a new platform integration.

## Start here

- [English README](README.md): features, supported platforms, and security guidance
- [Installation guide](docs/install.md): upstream setup instructions, translated
- [Troubleshooting](docs/troubleshooting.md)
- [Agent skill](agent_reach/skill/SKILL.md)

The upstream repository URL in commands and documentation still points to the original project. Running its remote install, skill-download, or update commands can replace this copy with untranslated upstream files.

## Install this English copy

Nothing has been installed or configured for you. Review the source and the installation guide before running it. From the extracted `Agent-Reach-English` directory, use Python 3.10 or newer:

```bash
python -m venv .venv
```

Activate the environment:

```bash
# macOS / Linux
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\Activate.ps1
```

Then install this local source tree:

```bash
python -m pip install .
agent-reach version
agent-reach install --env=auto
```

The final command is the project's default read-only setup check. External tools, browser sessions, API keys, and cookies remain separate setup steps. System changes require the project's explicit `--system` option; authorize them only after reviewing what will change.

To register the localized skill with an agent that supports it:

```bash
agent-reach skill --install
```

Both packaged skill variants are English in this edition. The existing locale-selection mechanism is unchanged.

## Translation scope

The default README, installation/update/troubleshooting documentation, contributor guide, changelog, agent skills and references, channel setup guides, CLI diagnostics, shell-script help, and developer comments have been localized. English documentation that already existed was retained and reconciled with newer guidance. Tests that assert localized output were updated to the corresponding English wording.

Commands, public APIs, configuration keys, platform names, source URLs, dependencies, and program control flow are preserved. This translation does not add platform support or guarantee that a platform's upstream service is reachable.

### Intentionally retained original-language material

- The upstream Japanese and Korean README editions remain available as separate translations.
- Branding, sponsor artwork, and the author's original QR image are preserved.
- Chinese platform response strings, search/filter values, upstream error examples, and multilingual test data remain where changing them would alter compatibility or test coverage.
- Some backend identifiers remain in their original spelling for compatibility with saved backend ordering/configuration.
- The Xiaoyuzhou transcription script retains its Mandarin transcription/punctuation prompts and `language=zh` behavior. Translating the interface does not translate podcast content into English.

Original license, copyright, author attribution, and upstream links are retained. No fork, pull request, publication, or remote push was created.

## Validation

See [LOCALIZATION_VALIDATION.md](LOCALIZATION_VALIDATION.md) for the checks performed and their limits. The delivered ZIP contains the working tree, not the `.git` directory, installed dependencies, or local credentials.

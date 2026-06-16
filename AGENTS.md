# ovos-tts-plugin-azure

OpenVoiceOS TTS plugin backed by the Azure Cognitive Services Speech REST API.

## Setup

```bash
pip install -e .
```

Runtime deps: `ovos-plugin-manager>=1.0.0,<3.0.0`, `requests` (see `requirements.txt`).

Configuration is read from the OVOS `tts` config block. Only `api_key` is mandatory; `voice` defaults to `en-US-JennyNeural` and `region` defaults to `westus`.

## Test

No test suite exists. There is no test runner configured.

## Lint/Typecheck

None configured.

## Layout

- `ovos_tts_plugin_azure/__init__.py` — the entire implementation: `AzureTTSPlugin` (subclass of `ovos_plugin_manager.templates.tts.TTS`) plus `AzureTTSValidator`.
- `setup.py` — packaging. Entry-point group is `mycroft.plugin.tts`: `ovos-tts-plugin-azure = ovos_tts_plugin_azure:AzureTTSPlugin`.

Plugin flow: `renew_token()` posts to the Azure `issueToken` STS endpoint (token cached ~9 min), `get_tts()` builds an SSML `<speak>` document and POSTs to the `cognitiveservices/v1` endpoint, writing the returned `riff-24khz-16bit-mono-pcm` bytes to a wav file. Returns `(wav_file, None)` (no phonemes).

## Conventions

Org hard rules:
- Branches: work on `dev`, stable on `master`. NEVER use `main`.
- Never edit a `version.py`; gh-automations bumps semver from conventional-commit prefixes (`feat:` / `fix:` / `feat!:`).
- New repos private by default.
- Commit identity: JarbasAi <jarbasai@mailfence.com>.
- Reference `OpenVoiceOS/gh-automations` reusable workflows at `@dev`.
- No Neon / `neon-*` references.
- No meta-commentary (no history, no dates) in code, docs, commits, or PRs.
- CI is provided by `OpenVoiceOS/gh-automations`.

## Gotchas

- Packaging is stale: uses legacy `setup.py` (no `pyproject.toml`), version pinned inline at `0.1.1`, `url` points at `github.com/dalgwen/...` (not the OpenVoiceOS org), and the entry-point group is the legacy `mycroft.plugin.tts` rather than `opm.tts`. The author email is a placeholder.
- The committed `ovos_tts_plugin_azure.egg-info/` directory is a build artifact that should not be tracked.
- `get_tts()` does not raise on a non-200 response; it only logs and implicitly returns `None`, which will break callers expecting a `(path, phonemes)` tuple.
- `renew_token()` does not check the HTTP status of the token request before storing `response.text` as the bearer token.
- `available_languages` returns an empty set — the plugin advertises no supported languages.

# TODO

## Open issues

- [ ] #1 add automations

## Gaps

- [ ] No test suite and no test runner configured.
- [ ] No CI: missing gh-automations workflows (build-tests, coverage, license-check, release_workflow, publish_stable) and `opm-check` for the TTS plugin entry point.
- [ ] No `pyproject.toml`; packaging still uses legacy `setup.py` with an inline pinned `version='0.1.1'`.
- [ ] Stale packaging metadata: `url` points at `github.com/dalgwen/ovos-tts-plugin-azure` instead of the OpenVoiceOS org; placeholder `author_email='private@private.org'`.
- [ ] Legacy entry-point group `mycroft.plugin.tts` rather than `opm.tts`.
- [ ] Committed build artifact: `ovos_tts_plugin_azure.egg-info/` is tracked in the repo.
- [ ] `get_tts()` does not return or raise on non-200 responses (only logs).
- [ ] `renew_token()` stores `response.text` as the token without verifying the HTTP status.
- [ ] `available_languages` returns an empty set.

## Code TODOs

None found.

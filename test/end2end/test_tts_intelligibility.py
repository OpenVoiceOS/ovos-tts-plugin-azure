"""End-to-end TTS intelligibility test for ovos-tts-plugin-azure.

Synthesises a small set of phrases with the real plugin, transcribes the
rendered audio back with a reference STT and scores the round-trip with
WER/CER via ovoscope. Report-only by default (TTS_MAX_WER=1.0).

Azure is a cloud engine: this test is skipped when no Azure Speech
credentials are configured (runtime credential, not a packaging skip).
"""
import os
import json

import pytest

from ovoscope.tts_intelligibility import score_tts_intelligibility

from ovos_tts_plugin_azure import AzureTTSPlugin

LANG = "en-US"
PHRASES = [
    "hello world",
    "what time is it",
    "the weather is nice today",
    "thank you very much",
    "see you later",
]


def test_tts_intelligibility():
    api_key = os.environ.get("AZURE_SPEECH_KEY") or os.environ.get("AZURE_KEY")
    if not api_key:
        pytest.skip("requires Azure credentials")
    region = os.environ.get("AZURE_REGION", "westus")
    tts = AzureTTSPlugin({"lang": LANG, "api_key": api_key, "region": region})
    report = score_tts_intelligibility(tts, PHRASES, lang=LANG, mode="direct")
    print("::TTS-INTELLIGIBILITY:: " + json.dumps(report.to_dict()))
    assert report.mean_wer <= float(os.environ.get("TTS_MAX_WER", "1.0"))

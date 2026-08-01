### ovos-tts-plugin-azure

`ovos-tts-plugin-azure` is a text-to-speech plugin for OpenVoiceOS. It sends text to the [Azure Cognitive Services Speech API](https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/overview#create-the-azure-resource) and returns synthesized audio.

To use this plugin, you need a Microsoft Azure subscription and a Speech resource. The free plan handles domestic usage: 5 million characters a month, or 0.5 million characters a month with neural voices. Pick a voice from the "Voice name" column in the [language support table](https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/language-support#text-to-speech).

##### Installation

```bash
pip install ovos-tts-plugin-azure
```

##### Configuration

The `api_key` field is mandatory. Other fields default as shown below.

```json
"tts": {
    "module": "ovos-tts-plugin-azure",
    "ovos-tts-plugin-azure": {
        "api_key": "insert_your_key_here",
        "voice": "en-US-JennyNeural",
        "region": "westus"
    }
}
```

##### Related projects

- [OpenVoiceOS](https://github.com/OpenVoiceOS) — the voice assistant platform this plugin serves.

##### License

Apache-2.0

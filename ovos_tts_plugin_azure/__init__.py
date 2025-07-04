# Copyright 2017 Mycroft AI Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from xml.etree import ElementTree

import requests
from datetime import datetime, timedelta
from ovos_plugin_manager.templates.tts import TTS, TTSValidator
from ovos_utils import classproperty
from ovos_utils.log import LOG


class AzureTTSPlugin(TTS):

    def __init__(self, config=None):
        super().__init__(config=config,
                         validator=AzureTTSValidator(self),
                         audio_ext='wav')
        self.api_key = self.config.get("api_key")
        self.voice = self.config.get("voice", "en-US-JennyNeural")
        self.region = self.config.get("region", "westus")
        self.access_token = None
        self.last_renew = None

    @classproperty
    def available_languages(cls) -> set:
        """Return languages supported by this TTS implementation in this state
        This property should be overridden by the derived class to advertise
        what languages that engine supports.
        Returns:
            set: supported languages
        """
        return set()

    def renew_token(self):
        now = datetime.now()
        if self.last_renew and \
                now - timedelta(minutes=9) <= self.last_renew <= now:
            return

        constructed_url = "https://" + self.region + \
                          ".api.cognitive.microsoft.com/sts/v1.0/issueToken"
        headers = {
            'Ocp-Apim-Subscription-Key': self.api_key
        }
        response = requests.post(constructed_url, headers=headers)
        self.access_token = str(response.text)
        self.last_renew = now

    def get_tts(self, sentence, wav_file):
        self.renew_token()
        constructed_url = "https://" + self.region + \
                          ".tts.speech.microsoft.com/cognitiveservices/v1"
        headers = {
            'Authorization': 'Bearer ' + self.access_token,
            'Content-Type': 'application/ssml+xml',
            'X-Microsoft-OutputFormat': 'riff-24khz-16bit-mono-pcm',
            'User-Agent': 'ovos-plugin-manager'
        }
        xml_body = ElementTree.Element('speak', version='1.0')
        xml_body.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-us')
        voice = ElementTree.SubElement(xml_body, 'voice')
        voice.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-US')
        voice.set('name', self.voice)
        voice.text = sentence
        body = ElementTree.tostring(xml_body)
        response = requests.post(constructed_url, headers=headers, data=body)
        if response.status_code == 200:
            with open(wav_file, "wb") as f:
                f.write(response.content)
                return wav_file, None  # No phonemes
        else:
            LOG.error("Status code: " + str(response.status_code) +
                      " Error. Reason: " + str(response.reason))


class AzureTTSValidator(TTSValidator):
    def __init__(self, tts):
        super(AzureTTSValidator, self).__init__(tts)

    def validate_lang(self):
        pass

    def validate_connection(self):
        self.tts.renew_token()

    def get_tts_class(self):
        return AzureTTSPlugin

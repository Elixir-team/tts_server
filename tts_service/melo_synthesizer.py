import os
import io
from tts_service.base_synthesizer import BaseSynthesizer
from typing import Dict
from melo.api import TTS
from scipy.io.wavfile import write
import nltk

from utils import get_model_and_config, abs_path

nltk.download('averaged_perceptron_tagger_eng')

MODELS_DIR = abs_path("melo_models")

speakers_ids = {
    "en": "EN-US",
    "es": "ES",
    "fr": "FR",
    "jp": "JP",
    "ko": "KR",
    "zh": "ZH"
}

model_ids = {
    "en": "EN",
    "es": "ES",
    "fr": "FR",
    "ja": "JP",
    "ko": "KR",
    "zh": "ZH"
}

class MeloSynthesizer(BaseSynthesizer):
    def __init__(self, models: Dict[str, TTS]):
        self.models = models

    def supported_languages(self):
        return self.models.keys()

    def has_lan(self, language: str):
        return language in self.models

    def synthesize(self, language: str, text: str):
        if language not in self.models:
            raise ValueError(f"Model for language '{language}' not found.")

        model = self.models[language]
        speaker_id = speakers_ids[language]
        speaker = model.hps.data.spk2id[speaker_id]
        audio_numpy = model.tts_to_file(text, speaker, speed=1.0, quiet=True)

        audio_buffer = io.BytesIO()
        write(audio_buffer, model.hps.data.sampling_rate, audio_numpy)
        audio_buffer.seek(0)

        return audio_buffer


def init_melo_synthesizer(exclude: list = None):
    device = 'auto'

    print("Initialize melo models:")
    models = {}
    for lang in os.listdir(MODELS_DIR):
        if exclude is not None and lang in exclude:
            continue

        lang_path = os.path.join(MODELS_DIR, lang)

        (model_path, config_path) = get_model_and_config(lang_path, ".pth", ".json")

        model_language = model_ids[lang]
        models[lang] = TTS(language=model_language, device=device, config_path=config_path, ckpt_path=model_path)
        print(f"{lang} model initialized")

    return MeloSynthesizer(models)

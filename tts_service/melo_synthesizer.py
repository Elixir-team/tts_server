import io
import os
from typing import Dict

from melo.api import TTS
from scipy.io.wavfile import write

from config import get_melo_device, get_melo_models_dir
from tts_service.base_synthesizer import BaseSynthesizer
from utils import get_model_and_config

speakers_ids = {
    "en": "EN-US",
    "es": "ES",
    "fr": "FR",
    "ja": "JP",
    "ko": "KR",
    "zh": "ZH",
}

model_ids = {
    "en": "EN",
    "es": "ES",
    "fr": "FR",
    "ja": "JP",
    "ko": "KR",
    "zh": "ZH",
}


class MeloSynthesizer(BaseSynthesizer):
    def __init__(self, models: Dict[str, TTS]):
        self.models = models

    def supported_languages(self):
        return sorted(self.models.keys())

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

        return self._normalize_audio(audio_buffer)


def init_melo_synthesizer(exclude: list = None):
    models_dir = get_melo_models_dir()
    device = get_melo_device()

    if not os.path.isdir(models_dir):
        raise FileNotFoundError(f"Melo models directory '{models_dir}' does not exist")

    print("Initialize melo models:")
    models = {}
    for lang in sorted(os.listdir(models_dir)):
        if exclude is not None and lang in exclude:
            continue

        lang_path = os.path.join(models_dir, lang)
        if not os.path.isdir(lang_path) or lang not in model_ids:
            continue

        model_path, config_path = get_model_and_config(lang_path, ".pth", ".json")
        model_language = model_ids[lang]
        models[lang] = TTS(
            language=model_language,
            device=device,
            config_path=config_path,
            ckpt_path=model_path,
        )
        print(f"{lang} model initialized")

    return MeloSynthesizer(models)

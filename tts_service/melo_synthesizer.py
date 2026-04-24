import io
import os
from typing import Dict

import nltk
from melo.api import TTS
from scipy.io.wavfile import write

from tts_service.base_synthesizer import BaseSynthesizer
from utils import abs_path, get_model_and_config

MODELS_DIR = abs_path(os.getenv("MELO_MODELS_DIR", "melo_models"))

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


def ensure_nltk_resource():
    try:
        nltk.data.find("taggers/averaged_perceptron_tagger_eng")
    except LookupError as exc:
        raise RuntimeError(
            "NLTK resource 'averaged_perceptron_tagger_eng' is missing. "
            "Download it during image build."
        ) from exc


def init_melo_synthesizer(exclude: list = None):
    ensure_nltk_resource()

    if not os.path.isdir(MODELS_DIR):
        raise FileNotFoundError(f"Melo models directory '{MODELS_DIR}' does not exist")

    device = os.getenv("MELO_DEVICE", "auto")

    print("Initialize melo models:")
    models = {}
    for lang in sorted(os.listdir(MODELS_DIR)):
        if exclude is not None and lang in exclude:
            continue

        lang_path = os.path.join(MODELS_DIR, lang)
        if not os.path.isdir(lang_path) or lang not in model_ids:
            continue

        model_path, config_path = get_model_and_config(lang_path, ".pth", ".json")
        model_language = model_ids[lang]
        models[lang] = TTS(language=model_language, device=device, config_path=config_path, ckpt_path=model_path)
        print(f"{lang} model initialized")

    return MeloSynthesizer(models)

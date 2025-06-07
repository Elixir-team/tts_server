import os
import io
import wave
from piper import PiperVoice
from tts_service.base_synthesizer import BaseSynthesizer
from typing import Dict

from utils import get_model_and_config, abs_path

MODELS_DIR = abs_path("piper_models")

speakers_ids = {
    "sr": 1  # hsb
}


class PiperSynthesizer(BaseSynthesizer):
    def __init__(self, models: Dict[str, PiperVoice]):
        self.models = models

    def supported_languages(self):
        return self.models.keys()

    def has_lan(self, language: str):
        return language in self.models

    def synthesize(self, language: str, text: str):
        if language not in self.models:
            raise ValueError(f"Model for language '{language}' not found.")

        speaker_id = speakers_ids.get(language)

        audio_buffer = io.BytesIO()
        with wave.open(audio_buffer, "wb") as wav_file:
            self.models[language].synthesize(text, wav_file=wav_file, speaker_id=speaker_id)
        audio_buffer.seek(0)
        
        return self._normalize_audio(audio_buffer)


def init_piper_synthesizer(exclude: list = None):
    print("Initialize piper models:")
    models = {}
    for lang in os.listdir(MODELS_DIR):
        if exclude is not None and lang in exclude:
            continue

        lang_path = os.path.join(MODELS_DIR, lang)

        (model_path, config_path) = get_model_and_config(lang_path, ".onnx", ".json")

        models[lang] = PiperVoice.load(model_path, config_path)
        print(f"{lang} model initialized")

    return PiperSynthesizer(models)

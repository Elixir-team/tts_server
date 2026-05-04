import io
import os
import wave
from typing import Dict

from piper import PiperVoice

from config import get_piper_models_dir, get_piper_use_cuda
from tts_service.base_synthesizer import BaseSynthesizer
from utils import get_model_and_config

speakers_ids = {
    "sr": 1,
}


class PiperSynthesizer(BaseSynthesizer):
    def __init__(self, models: Dict[str, PiperVoice]):
        self.models = models

    def supported_languages(self):
        return sorted(self.models.keys())

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
    models_dir = get_piper_models_dir()
    use_cuda = get_piper_use_cuda()

    if not os.path.isdir(models_dir):
        raise FileNotFoundError(f"Piper models directory '{models_dir}' does not exist")

    print("Initialize piper models:")
    models = {}
    for lang in sorted(os.listdir(models_dir)):
        if exclude is not None and lang in exclude:
            continue

        lang_path = os.path.join(models_dir, lang)
        if not os.path.isdir(lang_path):
            continue

        model_path, config_path = get_model_and_config(lang_path, ".onnx", ".json")

        models[lang] = PiperVoice.load(model_path, config_path, use_cuda=use_cuda)
        print(f"{lang} model initialized")

    return PiperSynthesizer(models)

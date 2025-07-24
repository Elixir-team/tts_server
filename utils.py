import os
from io import BytesIO

from pydub import AudioSegment


def abs_path(path: str):
    current_file_path = os.path.dirname(__file__)
    return os.path.join(current_file_path, path)


def get_model_and_config(path: str, model_type, config_type):
    lang_files = os.listdir(path)
    model_file = next((file for file in lang_files if file.endswith(model_type)), None)
    config_file = next((file for file in lang_files if file.endswith(config_type)), None)
    model_path = os.path.join(path, model_file)
    config_path = os.path.join(path, config_file)

    return model_path, config_path


def is_raw_format(t: str):
    return t == "audio/raw"


def get_default_mime_type():
    return "audio/raw"


def get_supported_mimeTypes():
    return {
        "audio/raw": "raw",
        "audio/wav": "wav",
        "audio/mpeg": "mp3",
        "audio/ogg": "ogg",
        "audio/flac": "flac",
        "audio/opus": "opus"
    }


def audio_type_supported(t: str):
    return t in get_supported_mimeTypes()


def get_audio_format_from_type(t: str):
    return get_supported_mimeTypes()[t]


def convert_audio(audio_buffer: BytesIO, mime_type: str) -> BytesIO:
    if is_raw_format(mime_type):
        return audio_buffer

    audio = AudioSegment.from_file(audio_buffer, format="wav")
    out_buffer = BytesIO()

    audio.export(out_buffer, format=get_audio_format_from_type(mime_type))
    out_buffer.seek(0)
    return out_buffer

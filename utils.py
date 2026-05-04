import os
from io import BytesIO

from pydub import AudioSegment

from config import DEFAULT_MEDIA_TYPE

SUPPORTED_MIME_TYPES = {
    "raw": "audio/raw",
    "audio/raw": "audio/raw",
    "wav": "audio/wav",
    "audio/wav": "audio/wav",
    "mp3": "audio/mpeg",
    "mpeg": "audio/mpeg",
    "audio/mpeg": "audio/mpeg",
    "ogg": "audio/ogg",
    "audio/ogg": "audio/ogg",
    "flac": "audio/flac",
    "audio/flac": "audio/flac",
    "opus": "audio/opus",
    "audio/opus": "audio/opus",
}
SUPPORTED_AUDIO_FORMATS = {
    "audio/raw": "raw",
    "audio/wav": "wav",
    "audio/mpeg": "mp3",
    "audio/ogg": "ogg",
    "audio/flac": "flac",
    "audio/opus": "opus",
}


def abs_path(path: str):
    current_file_path = os.path.dirname(__file__)
    return os.path.join(current_file_path, path)


def get_model_and_config(path: str, model_type, config_type):
    lang_files = os.listdir(path)
    model_file = next((file for file in lang_files if file.endswith(model_type)), None)
    config_file = next((file for file in lang_files if file.endswith(config_type)), None)

    if model_file is None or config_file is None:
        raise FileNotFoundError(f"Model or config not found in '{path}'")

    model_path = os.path.join(path, model_file)
    config_path = os.path.join(path, config_file)

    return model_path, config_path


def is_raw_format(media_type: str):
    return media_type == "audio/raw"


def normalize_audio_type(media_type: str | None):
    if media_type is None:
        return None

    return SUPPORTED_MIME_TYPES.get(media_type.strip().lower())


def get_default_mime_type():
    return normalize_audio_type(DEFAULT_MEDIA_TYPE) or DEFAULT_MEDIA_TYPE


def get_public_media_type(media_type: str):
    normalized_media_type = normalize_audio_type(media_type)
    if normalized_media_type is None:
        raise ValueError(f"Unsupported format '{media_type}'")
    return normalized_media_type


def audio_type_supported(media_type: str):
    return normalize_audio_type(media_type) in SUPPORTED_AUDIO_FORMATS


def get_audio_format_from_type(media_type: str):
    normalized_media_type = get_public_media_type(media_type)
    return SUPPORTED_AUDIO_FORMATS[normalized_media_type]


def convert_audio(audio_buffer: BytesIO, mime_type: str) -> BytesIO:
    normalized_media_type = get_public_media_type(mime_type)

    if is_raw_format(normalized_media_type):
        return audio_buffer

    audio = AudioSegment.from_file(audio_buffer, format="wav")
    out_buffer = BytesIO()

    audio.export(out_buffer, format=get_audio_format_from_type(normalized_media_type))
    out_buffer.seek(0)
    return out_buffer

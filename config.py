import os


DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 8000
DEFAULT_MEDIA_TYPE = "audio/mpeg"
DEFAULT_MELO_MODELS_DIR = "melo_models"
DEFAULT_PIPER_MODELS_DIR = "piper_models"
DEFAULT_MELO_DEVICE = "auto"
DEFAULT_PIPER_USE_CUDA = False

_ROOT_DIR = os.path.dirname(__file__)
_TRUTHY_VALUES = {"1", "true", "yes", "on"}


def resolve_path(path: str) -> str:
    return path if os.path.isabs(path) else os.path.join(_ROOT_DIR, path)


def get_host() -> str:
    return os.getenv("HOST", DEFAULT_HOST)


def get_port() -> int:
    return int(os.getenv("PORT", str(DEFAULT_PORT)))


def get_default_media_type() -> str:
    return DEFAULT_MEDIA_TYPE


def get_melo_models_dir() -> str:
    return resolve_path(os.getenv("MELO_MODELS_DIR", DEFAULT_MELO_MODELS_DIR))


def get_piper_models_dir() -> str:
    return resolve_path(os.getenv("PIPER_MODELS_DIR", DEFAULT_PIPER_MODELS_DIR))


def get_melo_device() -> str:
    return os.getenv("MELO_DEVICE", DEFAULT_MELO_DEVICE)


def get_piper_use_cuda() -> bool:
    return os.getenv("PIPER_USE_CUDA", str(DEFAULT_PIPER_USE_CUDA)).strip().lower() in _TRUTHY_VALUES

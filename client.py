import requests
import uuid
import os

from utils import get_audio_format_from_type

API_URL = "http://localhost:8000/tts/synthesize/"
# API_URL = "https://72mp1d893c4wo6-8000.proxy.runpod.net/tts/synthesize/"
SAVE_PATH = "tts_audio"

# Поддерживаемые форматы
MIME_TYPES = [None, "audio/raw", "audio/wav", "audio/mpeg", "audio/ogg", "audio/flac", "audio/opus"]

os.makedirs(SAVE_PATH, exist_ok=True)


def text_to_speech_all_formats(language: str, text: str):
    for mime_type in MIME_TYPES:
        response = requests.post(API_URL, json={
            "language": language,
            "text": text,
            "mediaType": mime_type
        })

        if response.status_code == 200:
            request_id = str(uuid.uuid4())[:8]
            media_type = response.headers.get("Content-Type")
            file_path = os.path.join(SAVE_PATH, f"{request_id}.{get_audio_format_from_type(media_type)}")
            with open(file_path, "wb") as f:
                f.write(response.content)
            print(f"✅ [{mime_type}] Аудио сохранено: {file_path}")
        else:
            print(f"❌ [{mime_type}] Ошибка: {response.status_code}, {response.text}")


if __name__ == "__main__":
    while True:
        lanPrompt = input("Введите язык (или 'exit' для выхода): ").strip()
        if lanPrompt.lower() == "exit":
            break

        textPrompt = input("Введите текст: ").strip()

        text_to_speech_all_formats(lanPrompt, textPrompt)

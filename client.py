import requests
import uuid
import os

#API_URL = "http://localhost:8080/tts/synthesize/"
API_URL = "https://72mp1d893c4wo6-8000.proxy.runpod.net/tts/synthesize/"
SAVE_PATH = "tts_audio"

# Поддерживаемые форматы
SUPPORTED_FORMATS = ["wav", "mp3", "ogg", "flac", "m4a", "aac", "opus"]

os.makedirs(SAVE_PATH, exist_ok=True)


def text_to_speech_all_formats(language: str, text: str):
    for fmt in SUPPORTED_FORMATS:
        response = requests.post(API_URL, json={
            "language": language,
            "text": text,
            "format": fmt
        })

        if response.status_code == 200:
            request_id = str(uuid.uuid4())[:8]
            file_path = os.path.join(SAVE_PATH, f"{request_id}.{fmt}")
            with open(file_path, "wb") as f:
                f.write(response.content)
            print(f"✅ [{fmt}] Аудио сохранено: {file_path}")
        else:
            print(f"❌ [{fmt}] Ошибка: {response.status_code}, {response.text}")


if __name__ == "__main__":
    while True:
        lanPrompt = input("Введите язык (или 'exit' для выхода): ").strip()
        if lanPrompt.lower() == "exit":
            break

        textPrompt = input("Введите текст: ").strip()

        text_to_speech_all_formats(lanPrompt, textPrompt)

import requests
import uuid
import os

#API_URL = "http://localhost:8000/tts/synthesize/"
API_URL = "https://72mp1d893c4wo6-8000.proxy.runpod.net/tts/synthesize/"
SAVE_PATH = "tts_audio"  # Папка для сохранения аудиофайлов

os.makedirs(SAVE_PATH, exist_ok=True)  # Создаём папку, если её нет


def text_to_speech(language, text):
    response = requests.post(API_URL, json={"language": language, "text": text})

    if response.status_code == 200:
        request_id = response.headers.get("X-Request-ID", str(uuid.uuid4())[:8])  # Получаем request_id или генерируем
        file_path = os.path.join(SAVE_PATH, f"{request_id}.wav")

        # Сохраняем аудиофайл
        with open(file_path, "wb") as f:
            f.write(response.content)

        print(f"✅ Аудио сохранено: {file_path}")

    else:
        print(f"❌ Ошибка: {response.status_code}, {response.text}")


if __name__ == "__main__":
    while True:
        lanPrompt = input("Введите язык (или 'exit' для выхода): ").strip()
        textPrompt = input("Введите текст: ").strip()
        if lanPrompt.lower() == "exit":
            break
        text_to_speech(lanPrompt, textPrompt)

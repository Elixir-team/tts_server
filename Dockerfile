FROM python:3.10-slim

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PORT=8000 \
    DEFAULT_MEDIA_TYPE=audio/mpeg \
    NLTK_DATA=/usr/local/share/nltk_data \
    MELO_MODELS_DIR=/app/melo_models \
    PIPER_MODELS_DIR=/app/piper_models

WORKDIR /app

RUN apt-get update -y \
    && apt-get install -y --no-install-recommends \
        build-essential \
        ffmpeg \
        libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

RUN python -m pip install --upgrade pip setuptools wheel \
    && python -m pip install torch==2.7.0 torchaudio==2.7.0 --index-url https://download.pytorch.org/whl/cpu

COPY requirements.txt ./
COPY MeloTTS ./MeloTTS

RUN python -m pip install -r requirements.txt \
    && python -m pip install piper-tts==1.2.0 piper-phonemize==1.1.0 \
    && python -m pip install ./MeloTTS \
    && python -m unidic download \
    && python -c "import nltk; nltk.download('averaged_perceptron_tagger_eng', download_dir='/usr/local/share/nltk_data')"

COPY server.py utils.py start.sh ./
COPY tts_service ./tts_service
COPY melo_models ./melo_models
COPY piper_models ./piper_models

RUN chmod +x /app/start.sh

EXPOSE 8000

CMD ["./start.sh"]

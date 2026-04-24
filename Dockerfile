FROM python:3.10-slim

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PORT=8000 \
    DEFAULT_MEDIA_TYPE=audio/mpeg \
    NLTK_DATA=/usr/local/share/nltk_data \
    MELO_MODELS_DIR=/runpod-volume/tts-models/melo_models \
    PIPER_MODELS_DIR=/runpod-volume/tts-models/piper_models

WORKDIR /app

RUN set -eux; \
    if [ -f /etc/apt/sources.list.d/debian.sources ]; then \
        cp /etc/apt/sources.list.d/debian.sources /etc/apt/sources.list.d/debian.sources.bak; \
        sed -E 's/\btrixie-updates\b//g; s/  +/ /g; s/^Suites: $//g; s/^Suites: /Suites: /g' /etc/apt/sources.list.d/debian.sources.bak | sed '/^Suites: $/d' > /etc/apt/sources.list.d/debian.sources; \
    fi; \
    apt-get update -o Acquire::Retries=10 -y; \
    installed=0; \
    for i in 1 2 3; do \
        apt-get install -o Acquire::Retries=10 --fix-missing -y --no-install-recommends \
            build-essential \
            ffmpeg \
            libsndfile1 && installed=1 && break; \
        sleep 15; \
    done; \
    test "$installed" = "1"; \
    command -v ffmpeg; \
    command -v ffprobe; \
    rm -rf /var/lib/apt/lists/*

RUN python -m pip install --upgrade pip \
    && python -m pip install "setuptools<81" wheel \
    && python -m pip install torch==2.7.0 torchaudio==2.7.0 --index-url https://download.pytorch.org/whl/cpu

COPY requirements.txt ./
COPY MeloTTS ./MeloTTS

RUN python -m pip install -r requirements.txt \
    && python -m pip install piper-tts==1.2.0 piper-phonemize==1.1.0 \
    && python -m pip install ./MeloTTS \
    && python -c "import pkg_resources" \
    && python -m unidic download \
    && python -c "import nltk; nltk.download('averaged_perceptron_tagger_eng', download_dir='/usr/local/share/nltk_data'); nltk.download('cmudict', download_dir='/usr/local/share/nltk_data')" \
    && apt-get purge -y --auto-remove build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY server.py utils.py start.sh ./
COPY tts_service ./tts_service

RUN chmod +x /app/start.sh

EXPOSE 8000

CMD ["./start.sh"]

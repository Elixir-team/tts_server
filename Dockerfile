FROM nvidia/cuda:12.4.1-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PORT=8000 \
    NLTK_DATA=/usr/local/share/nltk_data \
    MELO_DEVICE=cuda \
    PIPER_USE_CUDA=true

WORKDIR /app

RUN set -eux; \
    if [ -f /etc/apt/sources.list ]; then \
        sed -i '/jammy-backports/d' /etc/apt/sources.list; \
        sed -i 's|http://archive.ubuntu.com/ubuntu|http://mirrors.edge.kernel.org/ubuntu|g' /etc/apt/sources.list; \
    fi; \
    if [ -f /etc/apt/sources.list.d/ubuntu.sources ]; then \
        sed -i '/jammy-backports/d' /etc/apt/sources.list.d/ubuntu.sources; \
        sed -i 's|http://archive.ubuntu.com/ubuntu|http://mirrors.edge.kernel.org/ubuntu|g' /etc/apt/sources.list.d/ubuntu.sources; \
    fi; \
    apt-get update -o Acquire::Retries=10 -y; \
    for i in 1 2 3; do \
        apt-get install -o Acquire::Retries=10 --fix-missing -y --no-install-recommends \
            build-essential \
            ffmpeg \
            libsndfile1 \
            python3 \
            python3-pip && break; \
        sleep 15; \
    done; \
    rm -rf /var/lib/apt/lists/*

RUN ln -sf /usr/bin/python3 /usr/bin/python

RUN python -m pip install --upgrade pip \
    && python -m pip install "setuptools<81" wheel \
    && python -m pip install torch==2.6.0+cu124 torchaudio==2.6.0+cu124 --index-url https://download.pytorch.org/whl/cu124

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
COPY melo_models ./melo_models
COPY piper_models ./piper_models

RUN chmod +x /app/start.sh

EXPOSE 8000

CMD ["./start.sh"]

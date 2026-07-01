FROM pytorch/pytorch:2.5.1-cuda12.4-cudnn9-devel

LABEL org.opencontainers.image.title="Mirivoice VITS Training"
LABEL org.opencontainers.image.description="An environment for training VITS model"
LABEL org.opencontainers.image.authors="crlotwhite@gmail.com"
LABEL org.opencontainers.image.version="0.0.1"
LABEL org.opencontainers.image.licenses="MIT"

WORKDIR /workspace

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

RUN apt-get update -y && apt-get install -y --no-install-recommends \
    espeak \
    aria2 \
    unzip \
    && rm -rf /var/lib/apt/lists/*

ENTRYPOINT [ "/bin/bash" ]
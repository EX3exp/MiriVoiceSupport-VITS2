FROM pytorch/pytorch:2.5.1-cuda12.4-cudnn9-devel

WORKDIR /workspace

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

RUN apt-get update -y && apt-get install -y --no-install-recommends \
    espeak \
    aria2 \
    unzip \
    && rm -rf /var/lib/apt/lists/*

ENTRYPOINT [ "/bin/bash" ]
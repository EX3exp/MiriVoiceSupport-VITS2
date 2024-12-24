FROM pytorch/pytorch:2.5.1-cuda12.4-cudnn9-devel

WORKDIR /workspace

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

RUN apt-get update -y && apt-get install -y \
    espeak \
    aria2 \
    unzip

RUN echo "Creating directories..." && \
    mkdir -p "/workspace/train/dataset" && \
    mkdir -p "/workspace/voicer" && \
    mkdir -p "/workspace/checkpoints" && \
    mkdir -p "/workspace/train"

COPY monotonic_align /workspace/monotonic_align
RUN echo "Installing monotonic_align..." && \
    cd /workspace/monotonic_align && \
    python setup.py build_ext --inplace

ENTRYPOINT [ "/bin/bash" ]
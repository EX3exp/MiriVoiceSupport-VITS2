FROM pytorch/pytorch:2.5.1-cuda12.4-cudnn9-devel

WORKDIR /workspace

COPY requirements.txt .

RUN pip install -r requirements.txt

ENTRYPOINT [ "/bin/bash" ]

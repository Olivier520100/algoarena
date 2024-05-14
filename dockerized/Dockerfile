FROM python:3.12-slim

WORKDIR /workspace

COPY . /workspace

RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

ENV NAME AlgoArena

CMD ["python", "./run.py"]
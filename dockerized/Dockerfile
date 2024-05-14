FROM python:3.12-slim

WORKDIR /workspace

COPY . /workspace

RUN apt-get -y update && apt-get -y upgrade && apt-get install -y --no-install-recommends ffmpeg
RUN pip install --no-cache-dir -r requirements.txt

ENV NAME AlgoArena

CMD ["python", "./run.py"]
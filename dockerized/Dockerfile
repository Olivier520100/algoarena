FROM python:3.12

WORKDIR /workspace

COPY . /workspace

RUN pip install --no-cache-dir -r requirements.txt

ENV NAME AlgoArena

CMD ["python", "./run.py"]
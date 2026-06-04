FROM python:3.11-slim

WORKDIR /app

COPY worker/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY shared /app/shared

COPY worker/worker.py /app/

CMD ["python","worker.py"]

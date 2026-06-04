FROM python:3.11-slim

WORKDIR /app

COPY api/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY shared /app/shared

COPY api/app.py /app/

EXPOSE 5000

CMD ["python","app.py"]

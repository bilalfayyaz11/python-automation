FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir flask requests

COPY retail_app.py .

ENV APP_VERSION=1.0.0

EXPOSE 5000

CMD ["python", "retail_app.py"]

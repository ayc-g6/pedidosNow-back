FROM python:3.8-slim

WORKDIR /app
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY ./app .
CMD gunicorn -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT app:app